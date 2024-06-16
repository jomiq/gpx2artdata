import gpx2artdata
from typing import Annotated
import fastapi
from fastapi import UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os

PRODUCTION = os.environ.get("PRODUCTION", "True").lower() not in ["false"]
PROTOCOL = os.environ.get("PROTOCOL", "http")
WEBSITE_HOSTNAME = os.environ.get("WEBSITE_HOSTNAME", False)
STATIC_URL = os.environ.get("STATIC_URL", False)
BUILD_VERSION = (
    os.environ.get("BUILD_VERSION", "none") + f"{'' if PRODUCTION else '-dev'}"
)

if PRODUCTION:
    PROTOCOL = "https"
    app = fastapi.FastAPI(docs_url=None, redoc_url=None)
else:
    app = fastapi.FastAPI()

WEBSITE_URL = f"{PROTOCOL}://{WEBSITE_HOSTNAME}"

static_app = StaticFiles(directory="static")
app.mount("/static", static_app, name="static")

templates = Jinja2Templates(directory="templates")


def root_ctx(request: Request):
    return {
        "toast": WEBSITE_HOSTNAME
        and bool(WEBSITE_HOSTNAME not in str(request.base_url)),
        "env": {
            "STATIC_URL": STATIC_URL,
            "PROTOCOL": PROTOCOL,
            "WEBSITE_HOSTNAME": WEBSITE_HOSTNAME,
            "BUILD_VERSION": BUILD_VERSION,
        },
    }


def is_htmx(request: Request):
    return request.headers.get("hx-request", False)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context=root_ctx(request)
    )


@app.post("/", response_class=HTMLResponse)
async def post_convert(
    request: Request,
    file: UploadFile,
    locale: Annotated[str, Form()] = "",
    accuracy: Annotated[int, Form()] = 1,
):
    try:
        ctx = gpx2artdata.do_convert(file=file.file, locale=locale, accuracy=accuracy)
    except Exception as e:
        ctx = {"error": str(e)}

    ctx["result"] = True
    ctx["title"] = f"{file.filename} - {locale}"

    if is_htmx(request):
        res = templates.TemplateResponse(
            request=request, name="result.html", context=ctx
        )
        res.headers.append("hx-response", "")
        return res
    else:
        ctx.update(root_ctx(request))
        return templates.TemplateResponse(
            request=request, name="index.html", context=ctx
        )


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port, proxy_headers=True)
