from typing import IO
import gpxpy
from gpx2artdata.colmaps import DEFAULT_COLMAP, COLMAP


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


def advanced_convert(
    rows: list[str], colmap: dict[str, str] = {}
) -> list[dict[str, str]]:
    for row in rows:
        parts = [c.strip() for c in row["comment"].split(",")]
        headings = []
        for p in parts:
            head_key = p.split(":")[0].strip().lower()
            heading = colmap.get(head_key, COLMAP.get(head_key, None))
            if heading:
                row[heading] = p.split(":")[-1].strip()
                if heading not in headings:
                    headings += [heading]
