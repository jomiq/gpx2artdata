from typing import IO
import gpxpy
from gpx2artdata.colmaps import DEFAULT_COLMAP


def default_convert(file: IO, locale: str = "", accuracy: int = 1) -> dict:
    gpx = gpxpy.parse(file)
    res = {"headings": DEFAULT_COLMAP, "rows": [], "n_rows": len(gpx.waypoints)}
    for wp in gpx.waypoints:
        data = {
            "species": wp.name,
            "locale": locale,
            "accuracy": accuracy,
            "lon": wp.longitude,
            "lat": wp.latitude,
            "date": str(wp.time.date().isoformat()),
            "comment": str(wp.comment) if wp.comment else "",
        }
        res["rows"].append(data)

    return res
