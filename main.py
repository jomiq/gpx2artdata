import os
import gpx2artdata
from typing import Annotated
import fastapi
from fastapi import UploadFile, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime as dt, timedelta

STATIC = "static"
FILES = "converted"

FILE_DIR = f"{STATIC}/{FILES}"
ROWS_FILE = "rows.txt"
RESET_FILE = "reset.txt"

if not os.path.isdir(FILE_DIR):
    os.mkdir(FILE_DIR)


def file_count():
    try:
        return len([p for p in os.listdir(FILE_DIR) if p.endswith(".xlsx")])
    except Exception as e:  # noqa
        reset()
    return 0


def row_count():
    n = 0
    try:
        with open(ROWS_FILE, "r") as f:
            n = int(f.read())
    except Exception as e:  # noqa
        reset()
    return n


def add_rows(n: int) -> int:
    N = row_count() + n
    with open(ROWS_FILE, "w") as f:
        f.write(str(N))

    return N


def get_reset_time() -> dt:
    try:
        with open(RESET_FILE, "r") as f:
            t = dt.fromisoformat(f.read())
    except Exception as e:  # noqa
        t = dt.now()
        with open(RESET_FILE, "w") as f:
            f.write(t.isoformat())

    return t


def reset():
    with open(ROWS_FILE, "w") as f:
        f.write("0")
    for file in os.listdir(FILE_DIR):
        os.remove(f"{FILE_DIR}/{file}")

    t = dt.now()
    with open(RESET_FILE, "w") as f:
        f.write(t.isoformat())


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
        },
    )


@app.post("/", response_class=HTMLResponse)
async def post_convert(
    request: Request,
    file: UploadFile,
    locale: Annotated[str, Form()] = "",
    accuracy: Annotated[int, Form()] = 10,
):
    try:
        ctx = gpx2artdata.to_xlsx(
            file=file.file, title=file.filename, locale=locale, accuracy=accuracy
        )
        add_rows(ctx["n_rows"])
    except Exception as e:
        ctx = {"error": str(e)}

    return templates.TemplateResponse(request=request, name="index.html", context=ctx)


def days_hours_minutes(td: timedelta):
    return f"{td.days} dagar, {td.seconds//3600:02} timmar, {(td.seconds//60)%60:02} minuter"


@app.get("/info", response_class=HTMLResponse)
async def get_info(request: Request):
    t = get_reset_time()
    ut = dt.now() - t
    up_str = days_hours_minutes(ut)
    reset_t = f"{t.date().isoformat()} kl. {t.hour}:{t.minute:02}"

    return templates.TemplateResponse(
        request=request,
        name="info.html",
        context={
            "n_rows": row_count(),
            "n_files": file_count(),
            "reset_t": reset_t,
            "up_str": up_str,
        },
    )


@app.get("/reset", response_class=RedirectResponse)
async def get_reset():
    reset()
    return "/info"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
