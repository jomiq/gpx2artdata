# SPDX-FileCopyrightText: 2024-present Jon Mihkkal Inga <jon.mihkkal.inga@gmail.com>
#
# SPDX-License-Identifier: MIT

from typing import IO
import gpxpy

COLMAP = [
    "Artnamn",
    "Lokalnamn",
    "Noggrannhet",
    "Ost",
    "Nord",
    "Startdatum",
    "Publik kommentar",
]


def do_convert(file: IO, locale="", accuracy=10, title="result") -> str:
    gpx = gpxpy.parse(file)
    res = {"title": title, "headings": COLMAP, "rows": [], "n_rows": len(gpx.waypoints)}
    for wp in gpx.waypoints:
        data = {
            "species": wp.name,
            "locale": locale,
            "accuracy": accuracy,
            "lon": wp.longitude,
            "lat": wp.latitude,
            "date": str(wp.time.date().isoformat()),
            "comment": "",
        }
        res["rows"].append(data)

    return res
