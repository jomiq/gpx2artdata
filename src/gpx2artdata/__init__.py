# SPDX-FileCopyrightText: 2024-present Jon Mihkkal Inga <jon.mihkkal.inga@gmail.com>
#
# SPDX-License-Identifier: MIT

from typing import IO
import gpxpy
from openpyxl import Workbook
from datetime import datetime as dt

COLMAP = [
    "Artnamn",
    "Lokalnamn",
    "Noggrannhet",
    "Ost",
    "Nord",
    "Startdatum",
    "Publik kommentar",
]


def to_xlsx(file: IO, locale="",  accuracy=10, title="result") -> str:
    gpx = gpxpy.parse(file)
    wb = Workbook()
    ws = wb.active
    ws.append(COLMAP)
    res = {"title": title, "headings": COLMAP, "rows": []}
    for wp in gpx.waypoints:
        data = [
            wp.name,
            locale,
            f"{accuracy} m",
            wp.longitude,
            wp.latitude,
            wp.time.date().isoformat(),
            "",
        ]
        res["rows"].append(data)
        ws.append(data)
        
    basename = title.split(".")[0]
    output_name = f"static/converted/{basename}-{dt.now().isoformat()}.xlsx"
    wb.save(output_name)
    res["xlsx_url"] = output_name

    return res


def to_context(file: IO, title="result", locale="", accuracy=10):
    gpx = gpxpy.parse(file)
    res = {"title": title, "headings": COLMAP, "rows": []}
    for wp in gpx.waypoints:
        res["rows"].append(
            [
                wp.name,
                locale,
                f"{accuracy} m",
                wp.longitude,
                wp.latitude,
                wp.time.date().isoformat(),
                "",
            ]
        )

    return res
