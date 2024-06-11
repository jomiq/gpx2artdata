import gpx2artdata
from typing import Annotated
import fastapi
from fastapi import UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

STATIC = "static"

app = fastapi.FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


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
    accuracy: Annotated[float, Form()] = 10,
):
    try:
        ctx = gpx2artdata.do_convert(
            file=file.file, title=file.filename, locale=locale, accuracy=accuracy
        )
    except Exception as e:
        ctx = {"error": str(e)}

    ctx["gpx_version"] = gpx2artdata.__version__
    return templates.TemplateResponse(request=request, name="index.html", context=ctx)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
