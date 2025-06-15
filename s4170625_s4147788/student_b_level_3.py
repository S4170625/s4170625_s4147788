import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "climate.db")

def get_metrics():
    return [
        {"id": "precipitation", "name": "Precipitation"},
        {"id": "evaporation", "name": "Evaporation"},
        {"id": "max_temp", "name": "Max Temperature"},
        {"id": "min_temp", "name": "Min Temperature"},
        {"id": "sunshine", "name": "Sunshine"},
        {"id": "cloud_cover", "name": "Cloud Cover"},
        {"id": "avg_temp", "name": "Average Temp"},
    ]

def get_all_stations():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT station_id, name FROM weather_station ORDER BY name;")
        return [{"id": str(row[0]), "name": row[1]} for row in cur.fetchall()]

def get_metric_total(metric, station_id, start_date, end_date):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        query = f"""
            SELECT SUM({metric})
            FROM climate_data
            WHERE station_id = ? AND date BETWEEN ? AND ?
        """
        cur.execute(query, (station_id, start_date, end_date))
        result = cur.fetchone()
        return result[0] if result and result[0] is not None else None

def get_first(val):
    return val[0] if isinstance(val, list) and val else val

def get_metric_name(metric_id):
    for m in get_metrics():
        if m["id"] == metric_id:
            return m["name"]
    return "Unknown"

def get_similar_metrics(ref_metric, station_id, p1_start, p1_end, p2_start, p2_end, num_results):
    metrics = get_metrics()
    ref_total1 = get_metric_total(ref_metric, station_id, p1_start, p1_end)
    ref_total2 = get_metric_total(ref_metric, station_id, p2_start, p2_end)

    if not ref_total1 or not ref_total2 or ref_total1 == 0:
        return []

    ref_pct_change = ((ref_total2 - ref_total1) / ref_total1) * 100.0
    results = [{
        "name": get_metric_name(ref_metric),
        "total1": f"{ref_total1:.2f}",
        "total2": f"{ref_total2:.2f}",
        "pct_change": f"{ref_pct_change:+.2f}",
        "diff": "0.00 (selected)"
    }]

    others = []
    for m in metrics:
        mid = m["id"]
        if mid == ref_metric:
            continue
        t1 = get_metric_total(mid, station_id, p1_start, p1_end)
        t2 = get_metric_total(mid, station_id, p2_start, p2_end)
        if not t1 or not t2 or t1 == 0:
            continue
        pct = ((t2 - t1) / t1) * 100.0
        diff = pct - ref_pct_change
        others.append({
            "name": m["name"],
            "total1": f"{t1:.2f}",
            "total2": f"{t2:.2f}",
            "pct_change": f"{pct:+.2f}",
            "diff": f"{diff:+.2f}"
        })

    others = sorted(others, key=lambda x: abs(float(x["diff"])))
    results += others[:int(num_results)]
    return results

def get_page_html(form_data):
    metrics = get_metrics()
    stations = get_all_stations()

    p1_start = get_first(form_data.get("period1_start", ""))
    p1_end = get_first(form_data.get("period1_end", ""))
    p2_start = get_first(form_data.get("period2_start", ""))
    p2_end = get_first(form_data.get("period2_end", ""))
    ref_metric = get_first(form_data.get("ref_metric", ""))
    station_id = get_first(form_data.get("station_id", ""))
    num_results = get_first(form_data.get("num_results", "3"))

    metric_options = "".join(
        f'<option value="{m["id"]}" {"selected" if ref_metric == m["id"] else ""}>{m["name"]}</option>'
        for m in metrics
    )
    station_options = "".join(
        f'<option value="{s["id"]}" {"selected" if station_id == s["id"] else ""}>{s["name"]}</option>'
        for s in stations
    )

    show_table = all([p1_start, p1_end, p2_start, p2_end, ref_metric, station_id, num_results])
    table_rows = ""
    if show_table:
        try:
            results = get_similar_metrics(ref_metric, station_id, p1_start, p1_end, p2_start, p2_end, num_results)
            if not results:
                table_rows = '<tr><td colspan="5" style="text-align:center">No data found for this station and time period.</td></tr>'
            else:
                for row in results:
                    table_rows += f"""
                        <tr>
                            <td>{row["name"]}</td>
                            <td>{row["total1"]}</td>
                            <td>{row["total2"]}</td>
                            <td>{row["pct_change"]}%</td>
                            <td>{row["diff"]}%</td>
                        </tr>
                    """
        except Exception as e:
            table_rows = f'<tr><td colspan="5" style="color:red">Error: {e}</td></tr>'
    else:
        table_rows = '<tr><td colspan="5" style="text-align:center">No data to display. Please fill the form and submit.</td></tr>'

    nav_bar = """
    <header>
        <div class="logo">Logo</div>
        <nav>
            <a href="/">Home</a>
            <a href="/page1b">Mission</a>
            <a href="/page2a">Climate By Location</a>
            <a href="/page2b">Climate By Metric</a>
            <a href="/page3a">Similar Weather Station Sites</a>
            <a href="/page3b" class="active">Similar Weather Station Metrics</a>
        </nav>
    </header>
    """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Similar Climate Metrics</title>
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
            h2 {{ margin-top: 18px; margin-bottom: 9px; color: #003366; }}
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
            th {{ background: #e3eaf3; font-weight: bold; }}
        </style>
    </head>
    <body>
        {nav_bar}
        <div class="container">
            <h2>Find Metrics with Similar Climate Change</h2>
            <div class="form-section">
                <form method="GET" action="/page3b">
                    <div>
                        <label>Period 1:</label>
                        <input type="date" name="period1_start" value="{p1_start}" required>
                        <span>to</span>
                        <input type="date" name="period1_end" value="{p1_end}" required>
                    </div>
                    <div>
                        <label>Period 2:</label>
                        <input type="date" name="period2_start" value="{p2_start}" required>
                        <span>to</span>
                        <input type="date" name="period2_end" value="{p2_end}" required>
                    </div>
                    <div>
                        <label>Reference Station:</label>
                        <select name="station_id" required>
                            <option value="">-- Select Station --</option>
                            {station_options}
                        </select>
                    </div>
                    <div>
                        <label>Reference Metric:</label>
                        <select name="ref_metric" required>
                            <option value="">-- Select Metric --</option>
                            {metric_options}
                        </select>
                    </div>
                    <div>
                        <label>Number of similar metrics:</label>
                        <input type="number" name="num_results" value="{num_results}" min="1" max="6" required>
                    </div>
                    <input type="submit" value="View Data">
                </form>
            </div>
            <table>
                <tr>
                    <th>Metric Name</th>
                    <th>Total (Period 1)</th>
                    <th>Total (Period 2)</th>
                    <th>% Change</th>
                    <th>Difference from Reference (%)</th>
                </tr>
                {table_rows}
            </table>
        </div>
    </body>
    </html>
    """
