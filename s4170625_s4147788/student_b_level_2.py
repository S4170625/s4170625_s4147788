import sqlite3
import os
import html

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "climate.db")

def get_first(val, default=""):
    return val[0] if isinstance(val, list) and val else (val or default)

def get_metrics():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(climate_data);")
        cols = cur.fetchall()
        return [{"id": col[1], "name": col[1].replace("_", " ").title()}
                for col in cols if col[1] not in ("station_id", "date")]

def get_all_stations():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT station_id, name FROM weather_station ORDER BY name;")
        return [{"id": str(row[0]), "name": row[1]} for row in cur.fetchall()]

def get_sort_link(form_data, table, col):
    sort_by = f"{table}_sort_by"
    sort_order = f"{table}_sort_order"
    cur_by = form_data.get(sort_by, "")
    cur_order = form_data.get(sort_order, "asc")
    new_order = "desc" if cur_by == col and cur_order == "asc" else "asc"
    params = []
    for k, v in form_data.items():
        if k not in [sort_by, sort_order]:
            params.append(f"{html.escape(k)}={html.escape(str(v))}")
    params += [f"{sort_by}={col}", f"{sort_order}={new_order}"]
    return f"?{'&'.join(params)}"

def get_metric_data(metric, station_id, start, end, sort_by, sort_order):
    allowed = ["station_id", "date", "value", "state", "region"]
    col = sort_by if sort_by in allowed else "date"
    order = "DESC" if sort_order == "desc" else "ASC"
    sql = f"""
        SELECT cd.station_id, cd.date, cd.[{metric}] AS value, ws.state, ws.region
        FROM climate_data cd
        JOIN weather_station ws ON cd.station_id = ws.station_id
        WHERE cd.station_id = ? AND cd.date BETWEEN ? AND ?
        ORDER BY {col} {order};
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(sql, (station_id, start, end))
        return [
            {"station_id": r[0], "date": r[1], "value": r[2], "state": r[3], "region": r[4]}
            for r in cur.fetchall()
        ]

def get_summary_data(metric, station_id, start, end, sort_by, sort_order):
    col = "state" if sort_by not in ["state", "total"] else sort_by
    order = "DESC" if sort_order == "desc" else "ASC"
    sql = f"""
        SELECT ws.state, AVG(cd.[{metric}]) AS total
        FROM weather_station ws
        JOIN climate_data cd ON ws.station_id = cd.station_id
        WHERE ws.station_id = ? AND cd.date BETWEEN ? AND ?
        GROUP BY ws.state
        ORDER BY {col} {order};
    """
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(sql, (station_id, start, end))
        return [
            {"state": r[0], "total": f"{r[1]:.1f}" if r[1] is not None else "N/A"}
            for r in cur.fetchall()
        ]

def get_page_html(form_data):
    metrics = get_metrics()
    stations = get_all_stations()

    metric = get_first(form_data.get("metric"))
    station_id = get_first(form_data.get("station_id"))
    dt_start = get_first(form_data.get("dt_start"))
    dt_end = get_first(form_data.get("dt_end"))
    t1_sort_by = get_first(form_data.get("t1_sort_by", "date"))
    t1_sort_order = get_first(form_data.get("t1_sort_order", "asc"))
    t2_sort_by = get_first(form_data.get("t2_sort_by", "state"))
    t2_sort_order = get_first(form_data.get("t2_sort_order", "asc"))

    metric_options = "".join(
        f'<option value="{m["id"]}" {"selected" if metric == m["id"] else ""}>{m["name"]}</option>'
        for m in metrics
    )
    station_options = "".join(
        f'<option value="{s["id"]}" {"selected" if station_id == s["id"] else ""}>{s["name"]}</option>'
        for s in stations
    )

    daily_rows = []
    summary_rows = []

    if metric and station_id and dt_start and dt_end:
        daily_rows = get_metric_data(metric, station_id, dt_start, dt_end, t1_sort_by, t1_sort_order)
        summary_rows = get_summary_data(metric, station_id, dt_start, dt_end, t2_sort_by, t2_sort_order)

    metric_name = next((m["name"] for m in metrics if m["id"] == metric), "Metric")

    def arrow(active, order):
        return " ▲" if active and order == "asc" else (" ▼" if active and order == "desc" else "")

    t1_rows = "\n".join(
        f"<tr><td>{r['station_id']}</td><td>{r['date']}</td><td>{r['value']}</td><td>{r['state']}</td><td>{r['region']}</td></tr>"
        for r in daily_rows
    ) if daily_rows else '<tr><td colspan="5" style="text-align:center">No data available.</td></tr>'

    t2_rows = "\n".join(
        f"<tr><td>{r['state']}</td><td>{r['total']}</td></tr>"
        for r in summary_rows
    ) if summary_rows else '<tr><td colspan="2" style="text-align:center">No summary available.</td></tr>'

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Climate By Metric | Weather Portal</title>
    <style>
        body {{ font-family: Arial, sans-serif; background:#f4f4f8; margin:0; padding:0; }}
        header {{
            background:#fff; padding:10px 20px;
            display:flex; justify-content:space-between; align-items:center;
            border-bottom:1px solid #ccc;
        }}
        nav {{ display:flex; gap:12px; }}
        nav a {{
            padding:6px 14px; border:1px solid #000;
            background:#fff; color:#222;
            text-decoration:none; border-radius:3px;
        }}
        nav a.active, nav a:hover {{
            background:#003366; color:#fff;
        }}
        .container {{
            max-width:1000px; margin:0 auto;
            padding:34px 8vw 60px;
        }}
        .form-section {{
            background:#fff; padding:28px 34px;
            border-radius:12px; box-shadow:0 2px 12px rgba(0,0,0,0.08);
            margin-bottom:36px;
        }}
        .form-grid {{
            display:grid; grid-template-columns:1fr 1fr;
            gap:26px 38px; align-items:center;
        }}
        .form-grid label {{ font-weight:500; margin-bottom:4px; }}
        .form-grid select, .form-grid input[type="date"] {{
            padding:6px 12px; font-size:1em;
            border-radius:6px; border:1px solid #b2b6c0;
        }}
        .form-button-row {{
            grid-column: 1 / span 2;
            display:flex; justify-content:center;
            margin-top:10px;
        }}
        .form-button-row input[type="submit"] {{
            background:#003366; color:#fff;
            border:none; padding:9px 34px;
            font-size:1em; border-radius:6px;
            font-weight:600; cursor:pointer;
        }}
        table {{
            width:100%; border-collapse:collapse;
            background:#fff; margin-bottom:30px;
        }}
        th, td {{
            padding:10px 12px;
            border:1px solid #b8b8b8;
            text-align:left;
        }}
        th {{ background:#e3eaf3; font-weight:bold; }}
    </style>
</head>
<body>
<header>
    <a href="/"><img src="https://cdn-icons-png.flaticon.com/512/1163/1163661.png" style="height:40px;"></a>
    <nav>
        <a href="/">Home</a>
        <a href="/page1b">Mission</a>
        <a href="/page2a">Climate By Location</a>
        <a href="/page2b">Climate By Metric</a>
        <a href="/page3a">Similar Weather Station Sites</a>
        <a href="/page3b">Similar Weather Station Metrics</a>
    </nav>
</header>

<div class="container">
    <h2 style="text-align:center; color:#003366;">Focused View of Climate Change by Climate Metric</h2>
    <div class="form-section">
        <form class="form-grid" method="GET" action="/page2b">
            <div>
                <label>Climate Metric:</label>
                <select name="metric" required>
                    <option value="">-- Select Metric --</option>
                    {metric_options}
                </select>
            </div>
            <div>
                <label>Station:</label>
                <select name="station_id" required>
                    <option value="">-- Select Station --</option>
                    {station_options}
                </select>
            </div>
            <div>
                <label>Start Date:</label>
                <input type="date" name="dt_start" value="{dt_start}" required>
            </div>
            <div>
                <label>End Date:</label>
                <input type="date" name="dt_end" value="{dt_end}" required>
            </div>
            <!-- Hidden sort fields -->
            <input type="hidden" name="t1_sort_by" value="{t1_sort_by}">
            <input type="hidden" name="t1_sort_order" value="{t1_sort_order}">
            <input type="hidden" name="t2_sort_by" value="{t2_sort_by}">
            <input type="hidden" name="t2_sort_order" value="{t2_sort_order}">
            <div class="form-button-row">
                <input type="submit" value="View Data">
            </div>
        </form>
    </div>

    <h3>Table 1: Daily {metric_name} Values</h3>
    <table>
        <tr>
            <th><a href="{get_sort_link(form_data, 't1', 'station_id')}">Station ID{arrow(t1_sort_by=='station_id', t1_sort_order)}</a></th>
            <th><a href="{get_sort_link(form_data, 't1', 'date')}">Date{arrow(t1_sort_by=='date', t1_sort_order)}</a></th>
            <th><a href="{get_sort_link(form_data, 't1', 'value')}">{metric_name}{arrow(t1_sort_by=='value', t1_sort_order)}</a></th>
            <th><a href="{get_sort_link(form_data, 't1', 'state')}">State{arrow(t1_sort_by=='state', t1_sort_order)}</a></th>
            <th><a href="{get_sort_link(form_data, 't1', 'region')}">Region{arrow(t1_sort_by=='region', t1_sort_order)}</a></th>
        </tr>
        {t1_rows}
    </table>

    <h3>Table 2: State-Level Total {metric_name}</h3>
    <table>
        <tr>
            <th><a href="{get_sort_link(form_data, 't2', 'state')}">State{arrow(t2_sort_by=='state', t2_sort_order)}</a></th>
            <th><a href="{get_sort_link(form_data, 't2', 'total')}">Total {metric_name}{arrow(t2_sort_by=='total', t2_sort_order)}</a></th>
        </tr>
        {t2_rows}
    </table>
</div>
</body>
</html>
"""
