# SPDX-FileCopyrightText: 2024-present Jon Mihkkal Inga <jon.mihkkal.inga@gmail.com>
#
# SPDX-License-Identifier: MIT
from gpx2artdata.__about__ import __version__ as __version__
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


def do_convert(file: IO, locale: str = "", accuracy: int = 1) -> dict:
    gpx = gpxpy.parse(file)
    res = {"headings": COLMAP, "rows": [], "n_rows": len(gpx.waypoints)}

    if gpx.creator.startswith("Avenza Maps"):

        def get_comment(wp) -> str:
            return str(getattr(wp, "description", "")).split("Description:")[-1]

    else:

        def get_comment(wp) -> str:
            return str(getattr(wp, "comment", ""))

    for wp in gpx.waypoints:
        comment = get_comment(wp)
        data = {
            "species": wp.name,
            "locale": locale,
            "accuracy": accuracy,
            "lon": wp.longitude,
            "lat": wp.latitude,
            "date": str(wp.time.date().isoformat()),
            "comment": comment,
        }
        res["rows"].append(data)

    return res
