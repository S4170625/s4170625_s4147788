import sqlite3
import os
import html

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "climate.db")

#Sorting ;-;
STATION_COLS = {
    "site": "station_id",
    "name": "name",
    "region": "region",
    "latitude": "latitude"
}
SUMMARY_COLS = {
    "region": "region",
    "num_stations": "num_stations",
    "avg_max_temp": "avg_max_temp"
}

def get_states():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT UPPER(TRIM(state)) FROM weather_station ORDER BY UPPER(TRIM(state));")
        return [row[0] for row in cur.fetchall()]

def get_metrics():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(climate_data);")
        cols = cur.fetchall()
        metrics = []
        for col in cols:
            col_name = col[1]
            if col_name not in ("station_id", "date"):  # Exclude PK/FK cause we dont need it 
                #changes display name so it doesn't look like back end code/bad
                display = col_name.replace("_", " ").title()
                metrics.append({"id": col_name, "name": display})
        return metrics

def get_station_data(state, lat_start, lat_end, sort_by, sort_order):
    col = STATION_COLS.get(sort_by, "station_id")
    order = "DESC" if sort_order == "desc" else "ASC"
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT station_id, name, region, latitude
            FROM weather_station
            WHERE UPPER(TRIM(state))=? AND latitude BETWEEN ? AND ?
            ORDER BY {col} {order};
        """, (state, lat_start, lat_end))
        return [
            {"site": row[0], "name": row[1], "region": row[2], "latitude": row[3]}
            for row in cur.fetchall()
        ]

def get_summary_data(state, lat_start, lat_end, metric, sort_by, sort_order):
    #sorting by columns
    col_map = {
        "region": "region",
        "num_stations": "num_stations",
        "avg_max_temp": "avg_max_temp"
    }
    col = col_map.get(sort_by, "region")
    order = "DESC" if sort_order == "desc" else "ASC"
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT ws.region, COUNT(DISTINCT ws.station_id) AS num_stations, AVG(cd.[{metric}]) AS avg_max_temp
            FROM weather_station ws
            LEFT JOIN climate_data cd ON ws.station_id = cd.station_id
            WHERE UPPER(TRIM(ws.state))=? AND ws.latitude BETWEEN ? AND ?
            GROUP BY ws.region
            ORDER BY {col} {order};
        """, (state, lat_start, lat_end))
        return [
            {
                "region": row[0],
                "num_stations": row[1],
                "avg_max_temp": f"{row[2]:.1f}" if row[2] is not None else "N/A"
            }
            for row in cur.fetchall()
        ]

def get_first(val):
    if isinstance(val, list):
        return val[0] if val else ""
    return val

def get_page_html(form_data):
    try:
        states = get_states()
        metrics = get_metrics()

        state = get_first(form_data.get("state", "")).upper().strip()
        lat_start = get_first(form_data.get("lat_start", ""))
        lat_end = get_first(form_data.get("lat_end", ""))
        metric = get_first(form_data.get("metric", ""))

        # Default sorting for both tables
        station_sort_by = get_first(form_data.get("station_sort_by", "site"))
        station_sort_order = get_first(form_data.get("station_sort_order", "asc"))
        summary_sort_by = get_first(form_data.get("summary_sort_by", "region"))
        summary_sort_order = get_first(form_data.get("summary_sort_order", "asc"))

        stations_data = []
        summary_data = []

        if state and lat_start and lat_end and metric:
            try:
                stations_data = get_station_data(state, float(lat_start), float(lat_end), station_sort_by, station_sort_order)
                summary_data = get_summary_data(state, float(lat_start), float(lat_end), metric, summary_sort_by, summary_sort_order)
            except Exception as e:
                return f"<pre>Error: {e}</pre>"

        return get_level2_page_html(
            form_data={
                "state": state, "lat_start": lat_start, "lat_end": lat_end, "metric": metric,
                "station_sort_by": station_sort_by, "station_sort_order": station_sort_order,
                "summary_sort_by": summary_sort_by, "summary_sort_order": summary_sort_order
            },
            states=states,
            metrics=metrics,
            stations_data=stations_data,
            summary_data=summary_data
        )
    except Exception as e:
        return f"<pre>Fatal error: {e}</pre>"

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

def get_level2_page_html(form_data, states, metrics, stations_data, summary_data):
    # Sort indicators
    station_sort_by = form_data.get("station_sort_by", "site")
    station_sort_order = form_data.get("station_sort_order", "asc")
    summary_sort_by = form_data.get("summary_sort_by", "region")
    summary_sort_order = form_data.get("summary_sort_order", "asc")

    # Arrow indicator
    def arrow(selected, order):
        return " ▲" if order == "asc" and selected else (" ▼" if order == "desc" and selected else "")

    state_options = "".join(
        f'<option value="{s}" {"selected" if form_data.get("state") == str(s) else ""}>{s}</option>'
        for s in states
    )
    metric_options = "".join(
        f'<option value="{m["id"]}" {"selected" if form_data.get("metric") == m["id"] else ""}>{m["name"]}</option>'
        for m in metrics
    )
    if stations_data:
        table1_rows = "\n".join(
            f"<tr><td>{s['site']}</td><td>{html.escape(s['name'])}</td><td>{html.escape(s['region'])}</td><td>{s['latitude']}</td></tr>"
            for s in stations_data
        )
    else:
        table1_rows = '<tr><td colspan="4" style="text-align:center">No stations in this range.</td></tr>'

    if summary_data:
        table2_rows = "\n".join(
            f"<tr><td>{html.escape(s['region'])}</td><td>{s['num_stations']}</td><td>{s['avg_max_temp']}</td></tr>"
            for s in summary_data
        )
    else:
        table2_rows = '<tr><td colspan="3" style="text-align:center">No summary data.</td></tr>'

    nav_bar = """
    <header style="display:flex; align-items:center; gap:20px; padding:10px;">
    <a href="/">
        <img src="https://cdn-icons-png.flaticon.com/512/1163/1163661.png"
             alt="Weather Logo"
             style="height:40px; width:auto; vertical-align:middle;">
    </a>
    <nav style="display:flex; gap:12px;">
        <a href="/">Home</a>
        <a href="/page1b">Mission</a>
        <a href="/page2a">Climate By Location</a>
        <a href="/page2b">Climate By Metric</a>
        <a href="/page3a">Similar Weather Station Sites</a>
        <a href="/page3b">Similar Weather Station Metrics</a>
    </nav>
    </header>
    """
    # Build table headers with links
    t1 = f"""
    <table>
        <tr>
            <th><a href="{get_sort_link(form_data, 'station', 'site')}">Station no.{arrow(station_sort_by=='site', station_sort_order)}</a></th>
            <th><a href="{get_sort_link(form_data, 'station', 'name')}">Station Name{arrow(station_sort_by=='name', station_sort_order)}</a></th>
            <th><a href="{get_sort_link(form_data, 'station', 'region')}">Region{arrow(station_sort_by=='region', station_sort_order)}</a></th>
            <th><a href="{get_sort_link(form_data, 'station', 'latitude')}">Latitude{arrow(station_sort_by=='latitude', station_sort_order)}</a></th>
        </tr>
        {table1_rows}
    </table>
    """
    t2 = f"""
    <table>
        <tr>
            <th><a href="{get_sort_link(form_data, 'summary', 'region')}">Region{arrow(summary_sort_by=='region', summary_sort_order)}</a></th>
            <th><a href="{get_sort_link(form_data, 'summary', 'num_stations')}">Number Weather Stations{arrow(summary_sort_by=='num_stations', summary_sort_order)}</a></th>
            <th><a href="{get_sort_link(form_data, 'summary', 'avg_max_temp')}">Average {next((m['name'] for m in metrics if m['id'] == form_data.get('metric')), 'Metric')}{arrow(summary_sort_by=='avg_max_temp', summary_sort_order)}</a></th>
        </tr>
        {table2_rows}
    </table>

    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Climate By Location | Weather & Climate Data</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: #f4f4f8;
            }}
            header {{
                background: #fff;
                padding: 10px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #ccc;
            }}
            nav {{
                display: flex;
                gap: 8px;
            }}
            nav a {{
                margin-left: 0;
                padding: 6px 14px;
                border: 1px solid #000;
                background: #fff;
                color: #222;
                text-decoration: none;
                border-radius: 3px;
                font-size: 1em;
                transition: background 0.2s;
            }}
            nav a.active, nav a:hover {{
                background: #003366;
                color: #fff;
            }}
            .container {{
                padding: 34px 8vw 60px 8vw;
                max-width: 950px;
                margin: 0 auto;
            }}
            .form-section {{
                background: #fff;
                padding: 32px 32px 22px 32px;
                border-radius: 22px;
                border: 1px solid #e0e2ea;
                margin-bottom: 34px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);
                display: flex;
                justify-content: center;
            }}
            .form-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 26px 38px;
                width: 100%;
                max-width: 780px;
                align-items: center;
            }}
            .form-grid > div {{
                display: flex;
                flex-direction: column;
            }}
            .form-grid label {{
                font-weight: 500;
                margin-bottom: 4px;
            }}
            .form-grid select,
            .form-grid input[type="number"] {{
                padding: 6px 14px;
                font-size: 1em;
                border-radius: 6px;
                border: 1px solid #b2b6c0;
                min-width: 145px;
            }}
            .form-button-row {{
                grid-column: 1 / span 2;
                display: flex;
                justify-content: center;
                margin-top: 10px;
            }}
            .form-button-row input[type="submit"] {{
                background: #003366;
                color: #fff;
                border: none;
                border-radius: 6px;
                padding: 9px 34px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
            }}
            .form-button-row input[type="submit"]:hover {{
                background: #205c97;
            }}
            h2 {{
                margin-top: 18px;
                margin-bottom: 16px;
                color: #003366;
                text-align: center;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 22px;
                background: #fff;
            }}
            th, td {{
                padding: 10px 9px;
                border: 1px solid #b8b8b8;
                text-align: left;
            }}
            th {{
                background: #e3eaf3;
                font-weight: bold;
            }}
            .summary-title {{
                margin-top: 36px;
                font-size: 1.17em;
            }}
        </style>
    </head>
    <body>
        {nav_bar}
        <div class="container">
            <h2>Focused View of Climate Change by Location</h2>
            <div class="form-section">
                <form class="form-grid" method="GET" action="/page2a">
                    <div>
                        <label for="state">State:</label>
                        <select name="state" id="state" required>
                            <option value="">-- Select State --</option>
                            {state_options}
                        </select>
                    </div>
                    <div>
                        <label for="lat_start">Start Latitude:</label>
                        <input type="number" step="0.01" name="lat_start" id="lat_start" value="{form_data.get('lat_start', '')}" required>
                    </div>
                    <div>
                        <label for="lat_end">End Latitude:</label>
                        <input type="number" step="0.01" name="lat_end" id="lat_end" value="{form_data.get('lat_end', '')}" required>
                    </div>
                    <div>
                        <label for="metric">Climate Metric:</label>
                        <select name="metric" id="metric" required>
                            <option value="">-- Select Metric --</option>
                            {metric_options}
                        </select>
                    </div>
                    <!-- Hidden sort fields to preserve on submit -->
                    <input type="hidden" name="station_sort_by" value="{form_data.get('station_sort_by', 'site')}">
                    <input type="hidden" name="station_sort_order" value="{form_data.get('station_sort_order', 'asc')}">
                    <input type="hidden" name="summary_sort_by" value="{form_data.get('summary_sort_by', 'region')}">
                    <input type="hidden" name="summary_sort_order" value="{form_data.get('summary_sort_order', 'asc')}">
                    <div class="form-button-row">
                        <input type="submit" value="View Data">
                    </div>
                </form>
            </div>
            <h3>Table 1: Weather Station Details</h3>
            {t1}
            <div class="summary-title"><b>Table 2: Regional Climate Summary</b></div>
            {t2}
        </div>
    </body>
    </html>
    """
#html has ruined my life :(