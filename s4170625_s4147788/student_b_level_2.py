import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "climate.db")

def get_metrics():
    return [
        {"id": "max_temp", "name": "Max Temperature"},
        {"id": "min_temp", "name": "Min Temperature"},
        {"id": "precipitation", "name": "Precipitation"},
        {"id": "evaporation", "name": "Evaporation"},
        {"id": "sunshine", "name": "Sunshine"},
    ]

def get_all_stations():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT station_id, name FROM weather_station ORDER BY name;")
        return [{"id": str(row[0]), "name": row[1]} for row in cur.fetchall()]

def get_metric_data(metric, station_id, dt_start, dt_end):
    sql = f"""
        SELECT cd.station_id, cd.date, cd.[{metric}], ws.state, ws.region
        FROM climate_data cd
        JOIN weather_station ws ON ws.station_id = cd.station_id
        WHERE cd.station_id = ?
          AND cd.date BETWEEN ? AND ?
        ORDER BY cd.date;
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(sql, (station_id, dt_start, dt_end))
        rows = cur.fetchall()
    return [
        {
            "station_id": r[0],
            "date": r[1],
            "value": r[2],
            "state": r[3],
            "region": r[4],
        }
        for r in rows
    ]

def get_summary_by_state(metric, station_id, dt_start, dt_end):
    sql = f"""
        SELECT ws.state, SUM(cd.[{metric}])
        FROM climate_data cd
        JOIN weather_station ws ON ws.station_id = cd.station_id
        WHERE cd.station_id = ?
          AND cd.date BETWEEN ? AND ?
        GROUP BY ws.state
        ORDER BY ws.state;
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(sql, (station_id, dt_start, dt_end))
        rows = cur.fetchall()
    return [
        {"state": r[0], "total": round(r[1], 1) if r[1] is not None else "N/A"} for r in rows
    ]

def get_first(val, default=""):
    if isinstance(val, list):
        return val[0] if val else default
    return val or default

def get_page_html(form_data):
    metrics = get_metrics()
    stations = get_all_stations()

    metric = get_first(form_data.get("metric"))
    station_id = get_first(form_data.get("station_id"))
    dt_start = get_first(form_data.get("dt_start"))
    dt_end = get_first(form_data.get("dt_end"))

    daily_rows = []
    summary_rows = []

    if metric and station_id and dt_start and dt_end:
        try:
            daily_rows = get_metric_data(metric, station_id, dt_start, dt_end)
            summary_rows = get_summary_by_state(metric, station_id, dt_start, dt_end)
        except Exception as exc:
            return f"<pre style='color:red'>DB ERROR: {exc}</pre>"

    return _render_page(
        metrics=metrics,
        stations=stations,
        selected={
            "metric": metric,
            "station_id": station_id,
            "dt_start": dt_start,
            "dt_end": dt_end,
        },
        daily_rows=daily_rows,
        summary_rows=summary_rows,
    )

def _render_page(metrics, stations, selected, daily_rows, summary_rows):
    metric_options = "\n".join(
        f'<option value="{m["id"]}" {"selected" if selected["metric"] == m["id"] else ""}>{m["name"]}</option>'
        for m in metrics
    )
    station_options = "\n".join(
        f'<option value="{s["id"]}" {"selected" if selected["station_id"] == s["id"] else ""}>{s["name"]}</option>'
        for s in stations
    )

    table1_rows = (
        "\n".join(
            f"<tr><td>{r['station_id']}</td><td>{r['date']}</td><td>{r['value']}</td><td>{r['state']}</td><td>{r['region']}</td></tr>"
            for r in daily_rows
        )
        if daily_rows
        else '<tr><td colspan="5" style="text-align:center">No data for your selection.</td></tr>'
    )

    table2_rows = (
        "\n".join(f"<tr><td>{r['state']}</td><td>{r['total']}</td></tr>" for r in summary_rows)
        if summary_rows
        else '<tr><td colspan="2" style="text-align:center">No summary available.</td></tr>'
    )

    metric_name = next((m["name"] for m in metrics if m["id"] == selected["metric"]), "Metric")

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Climate By Metric | Weather & Climate Data Portal</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin:0; padding:0; background:#f4f4f8; }}
        header {{ background:#fff; padding:10px 20px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #ccc; }}
        header .logo {{ font-weight:bold; font-size:1.2em; }}
        nav {{ display:flex; gap:8px; }}
        nav a {{ padding:6px 14px; border:1px solid #000; background:#fff; color:#222; text-decoration:none; border-radius:3px; }}
        nav a.active, nav a:hover {{ background:#003366; color:#fff; }}
        .container {{ max-width:950px; margin:0 auto; padding:34px 8vw 60px; }}
        .form-section {{ background:#fff; padding:24px 34px; border-radius:10px; border:1px solid #e0e2ea; margin-bottom:34px; box-shadow:0 2px 8px rgba(0,0,0,.06); }}
        .form-section label {{ margin-right:8px; font-weight:500; }}
        .form-section select, .form-section input[type=date] {{ padding:4px 12px; font-size:1em; border-radius:4px; border:1px solid #b2b6c0; margin-right:14px; }}
        .form-section input[type=submit] {{ background:#003366; color:#fff; border:none; border-radius:4px; padding:6px 20px; font-size:1em; cursor:pointer; }}
        h2 {{ color:#003366; margin:18px 0 9px; }}
        table {{ width:100%; border-collapse:collapse; margin-bottom:22px; background:#fff; }}
        th, td {{ padding:10px 9px; border:1px solid #b8b8b8; text-align:left; }}
        th {{ background:#e3eaf3; cursor:pointer; }}
    </style>
</head>
<body>
<header>
    <div class="logo">Logo</div>
    <nav>
        <a href="/">Home</a>
        <a href="/page1b">Mission</a>
        <a href="/page2a">Climate By Location</a>
        <a href="/page2b" class="active">Climate By Metric</a>
        <a href="/page3a">Similar Weather Station Sites</a>
        <a href="/page3b">Similar Weather Station Metrics</a>
    </nav>
</header>

<div class="container">
    <h2>Focused View of Climate Change by Climate Metric</h2>

    <div class="form-section">
        <form method="GET" action="/page2b">
            <label for="metric">Climate Metric:</label>
            <select name="metric" required>
                <option value="">-- Select Metric --</option>
                {metric_options}
            </select>

            <label for="station_id">Station:</label>
            <select name="station_id" required>
                <option value="">-- Select Station --</option>
                {station_options}
            </select>

            <label for="dt_start">Start Date:</label>
            <input type="date" name="dt_start" value="{selected['dt_start']}" required>

            <label for="dt_end">End Date:</label>
            <input type="date" name="dt_end" value="{selected['dt_end']}" required>

            <input type="submit" value="View Data">
        </form>
    </div>

    <h3>Table 1: Daily {metric_name} Values</h3>
    <table>
        <thead>
            <tr><th>Station ID</th><th>Date</th><th>{metric_name}</th><th>State</th><th>Region</th></tr>
        </thead>
        <tbody>
            {table1_rows}
        </tbody>
    </table>

    <h3>Table 2: State‑level Total {metric_name}</h3>
    <table>
        <tr><th>State</th><th>Total {metric_name}</th></tr>
        {table2_rows}
    </table>
</div>
</body>
</html>
"""
