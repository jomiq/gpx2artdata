import gpx2artdata
from typing import Annotated
import fastapi
from fastapi import UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os

try:
    with open("hostname.txt") as f:
        HOSTNAME = f.read()
except FileNotFoundError as _:
    pass

STATIC = "static"
if os.environ.get("GPX2ARTDATA_PROD", False):
    app = fastapi.FastAPI(docs_url=None, redoc_url=None)
else:
    app = fastapi.FastAPI()

static_app = StaticFiles(directory="static")
app.mount("/static", static_app, name="static")
templates = Jinja2Templates(directory="templates")


def root_ctx(request: Request):
    return {
        "toast": HOSTNAME and bool(HOSTNAME not in str(request.base_url)),
        "gpx_version": gpx2artdata.__version__,
    }


def is_htmx(request: Request):
    return request.headers.get("hx-request", False)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "gpx2artdata",
            "toast": bool("gpx.skolbacken.com" not in str(request.base_url)),
            "gpx_version": gpx2artdata.__version__,
        },
    )


@app.post("/", response_class=HTMLResponse)
async def post_convert(
    request: Request,
    file: UploadFile,
    locale: Annotated[str, Form()] = "",
    accuracy: Annotated[int, Form()] = 1,
):
    ctx = root_ctx(request)
    try:
        ctx.update(
            gpx2artdata.do_convert(
                file=file.file, title=file.filename, locale=locale, accuracy=accuracy
            )
        )
    except Exception as e:
        ctx = {"error": str(e)}

    ctx["gpx_version"] = gpx2artdata.__version__
    ctx["result"] = True
    if is_htmx(request):
        res = templates.TemplateResponse(
            request=request, name="result.html", context=ctx
        )
        res.headers.append("hx-response", "")
        return res
    else:
        return templates.TemplateResponse(
            request=request, name="index.html", context=ctx
        )


if __name__ == "__main__":
    import uvicorn

    port = os.environ.get("PORT", "8080")
    uvicorn.run(app, host="0.0.0.0", port=port, proxy_headers=True)
