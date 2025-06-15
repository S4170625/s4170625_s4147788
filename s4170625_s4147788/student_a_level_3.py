import sqlite3
import os

# Point to the database location
DB_PATH = os.path.join(os.path.dirname(__file__), "database", "climate.db")

def get_metrics():
    # List of available weather data types the user can pick
    return [
        {"id": "max_temp", "name": "Max Temperature"},
        {"id": "min_temp", "name": "Min Temperature"},
        {"id": "precipitation", "name": "Precipitation"},
        {"id": "evaporation", "name": "Evaporation"},
        {"id": "sunshine", "name": "Sunshine"},
    ]

def get_all_stations():
    # Gets all weather station IDs and names, ordered alphabetically for the dropdown
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT station_id, name FROM weather_station ORDER BY name;")
        return [{"station_id": str(row[0]), "name": row[1]} for row in cur.fetchall()]

def get_station_name(station_id):
    # Gets the name of a station using its ID
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM weather_station WHERE station_id = ?", (station_id,))
        row = cur.fetchone()
        return row[0] if row else "Unknown"

def get_station_period_avg(station_id, metric, start_date, end_date):
    # Gets the average value of the metric for the station between the two dates
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT AVG({metric})
            FROM climate_data
            WHERE station_id=? AND date BETWEEN ? AND ?;
        """, (station_id, start_date, end_date))
        result = cur.fetchone()
        return result[0] if result and result[0] is not None else None

def get_first(val):
    # If the value is a list, return its first item; otherwise, return the value as-is
    if isinstance(val, list):
        return val[0] if val else ""
    return val

def get_similar_stations(period1_start, period1_end, period2_start, period2_end, metric, reference_station_id, num_similar):
    # Finds the weather stations with the most similar percentage change as the reference
    stations = get_all_stations()
    reference_station_id = str(reference_station_id)
    ref_avg1 = get_station_period_avg(reference_station_id, metric, period1_start, period1_end)
    ref_avg2 = get_station_period_avg(reference_station_id, metric, period2_start, period2_end)
    if ref_avg1 is None or ref_avg2 is None or ref_avg1 == 0:
        return []

    ref_pct_change = ((ref_avg2 - ref_avg1) / ref_avg1) * 100.0
    results = []

    # Add the reference station at the top
    ref_station_name = get_station_name(reference_station_id)
    results.append({
        "name": ref_station_name,
        "avg1": f"{ref_avg1:.2f}",
        "avg2": f"{ref_avg2:.2f}",
        "pct_change": f"{ref_pct_change:+.2f}",
        "diff_from_ref": "0.00",
        "selected": True
    })

    # Compare all other stations to the reference
    others = []
    for s in stations:
        sid = s["station_id"]
        if sid == reference_station_id:
            continue
        avg1 = get_station_period_avg(sid, metric, period1_start, period1_end)
        avg2 = get_station_period_avg(sid, metric, period2_start, period2_end)
        if avg1 is None or avg2 is None or avg1 == 0:
            continue
        pct_change = ((avg2 - avg1) / avg1) * 100.0
        diff_from_ref = pct_change - ref_pct_change
        others.append({
            "name": s["name"],
            "avg1": f"{avg1:.2f}",
            "avg2": f"{avg2:.2f}",
            "pct_change": f"{pct_change:+.2f}",
            "diff_from_ref": f"{diff_from_ref:+.2f}",
            "selected": False
        })

    # Sort by how close each station is to the reference
    others = sorted(others, key=lambda x: abs(float(x["diff_from_ref"])))
    # Only include as many as the user asked for (no duplicates)
    results += others[:int(num_similar)]
    return results

def get_page_html(form_data):
    # This sets up the form and the table
    metrics = get_metrics()
    stations = get_all_stations()

    # Keep the form values after the user submits (so their choices stick)
    period1_start = get_first(form_data.get("period1_start", ""))
    period1_end = get_first(form_data.get("period1_end", ""))
    period2_start = get_first(form_data.get("period2_start", ""))
    period2_end = get_first(form_data.get("period2_end", ""))
    metric = get_first(form_data.get("metric", ""))
    reference_station = get_first(form_data.get("reference_station", ""))
    num_similar = get_first(form_data.get("num_similar", "2"))

    # Build the dropdowns for the form
    metric_options = "".join(
        f'<option value="{m["id"]}" {"selected" if metric == m["id"] else ""}>{m["name"]}</option>'
        for m in metrics
    )
    station_options = "".join(
        f'<option value="{s["station_id"]}" {"selected" if reference_station == s["station_id"] else ""}>{s["name"]}</option>'
        for s in stations
    )

    # Only show the table if the form is filled out
    show_table = all([period1_start, period1_end, period2_start, period2_end, metric, reference_station, num_similar])
    table_rows = ""
    if show_table:
        try:
            results = get_similar_stations(period1_start, period1_end, period2_start, period2_end, metric, reference_station, num_similar)
            if not results:
                table_rows = '<tr><td colspan="5" style="text-align:center">No data for these dates or stations.</td></tr>'
            else:
                for row in results:
                    diff_from_ref = f'{float(row["diff_from_ref"]):+.2f}%'
                    if row["selected"]:
                        diff_from_ref = "0.00% (selected)"
                    table_rows += f"""
                    <tr>
                        <td>{row["name"]}</td>
                        <td>{row["avg1"]}</td>
                        <td>{row["avg2"]}</td>
                        <td>{row["pct_change"]}%</td>
                        <td>{diff_from_ref}</td>
                    </tr>
                    """
        except Exception as e:
            table_rows = f'<tr><td colspan="5" style="color:red">Error: {e}</td></tr>'
    else:
        table_rows = '<tr><td colspan="5" style="text-align:center">No data to display. Please fill the form and submit.</td></tr>'

    # Navigation bar HTML
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

    # Main HTML structure
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Simmilar Weather Stations over 2 periods</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f4f4f8; }}
            header {{
                background: #fff;
                padding: 10px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #ccc;
            }}
            header .logo {{ font-weight: bold; font-size: 1.2em; }}
            nav {{ display: flex; gap: 8px; }}
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
                padding: 24px 34px;
                border-radius: 10px;
                border: 1px solid #e0e2ea;
                margin-bottom: 34px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            }}
            .form-section label {{ margin-right: 8px; font-weight: 500; }}
            .form-section select, .form-section input[type="number"], .form-section input[type="date"] {{
                padding: 4px 12px;
                font-size: 1em;
                border-radius: 4px;
                border: 1px solid #b2b6c0;
                margin-right: 14px;
            }}
            .form-section input[type="submit"] {{
                background: #003366;
                color: #fff;
                border: none;
                border-radius: 4px;
                padding: 6px 20px;
                font-size: 1em;
                cursor: pointer;
            }}
            h2 {{
                margin-top: 18px;
                margin-bottom: 9px;
                color: #003366;
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
           
        </style>
    </head>
    <body>
        {nav_bar}
        <div class="container">
            <h2>Find Weather Stations with Similar Climate Metric Change</h2>
            <div class="form-section">
                <form method="GET" action="/page3a">
                    <div>
                        <label>Period 1:</label>
                        <input type="date" name="period1_start" value="{period1_start}" required>
                        <span>to</span>
                        <input type="date" name="period1_end" value="{period1_end}" required>
                    </div>
                    <div>
                        <label>Period 2:</label>
                        <input type="date" name="period2_start" value="{period2_start}" required>
                        <span>to</span>
                        <input type="date" name="period2_end" value="{period2_end}" required>
                    </div>
                    <div>
                        <label>Climate Metric:</label>
                        <select name="metric" required>
                            <option value="">-- Select --</option>
                            {metric_options}
                        </select>
                    </div>
                    <div>
                        <label>Reference Station:</label>
                        <select name="reference_station" required>
                            <option value="">-- Select Station --</option>
                            {station_options}
                        </select>
                    </div>
                    <div>
                        <label>Number of similar stations:</label>
                        <input type="number" name="num_similar" min="1" max="10" value="{num_similar}" required>
                    </div>
                    <input type="submit" value="View Data">
                </form>
            </div>
            <table>
                <tr>
                    <th>Weather Station</th>
                    <th>Average (Period 1)</th>
                    <th>Average (Period 2)</th>
                    <th>% Change</th>
                    <th>Difference from Reference</th>
                </tr>
                {table_rows}
            </table>
        </div>
    </body>
    </html>
    """
    return html
