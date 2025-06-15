import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "climate.db")

def get_states():
    #Geting unique states from weather_station table :3
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT state FROM weather_station ORDER BY state;")
        return [row[0] for row in cur.fetchall()]

def get_metrics():
    #These are the column names for climate_data that users can select for metrics 
   
    return [
        {"id": "max_temp", "name": "Max Temperature"},
        {"id": "min_temp", "name": "Min Temperature"},
        {"id": "precipitation", "name": "Precipitation"},
        {"id": "evaporation", "name": "Evaporation"},
        {"id": "sunshine", "name": "Sunshine"},
    ]

def get_station_data(state, lat_start, lat_end):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT station_id, name, region, latitude
            FROM weather_station
            WHERE state=? AND latitude BETWEEN ? AND ?
            ORDER BY latitude;
        """, (state, lat_start, lat_end))
        return [
            {"site": row[0], "name": row[1], "region": row[2], "latitude": row[3]}
            for row in cur.fetchall()
        ]

def get_summary_data(state, lat_start, lat_end, metric):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        # Getting no. of stations in the selected region and getting tghe average for the selected metric 
        cur.execute(f"""
            SELECT ws.region, COUNT(ws.station_id), AVG(cd.[{metric}])
            FROM weather_station ws
            LEFT JOIN climate_data cd ON ws.station_id = cd.station_id
            WHERE ws.state=? AND ws.latitude BETWEEN ? AND ?
            GROUP BY ws.region;
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

        state = get_first(form_data.get("state", ""))
        lat_start = get_first(form_data.get("lat_start", ""))
        lat_end = get_first(form_data.get("lat_end", ""))
        metric = get_first(form_data.get("metric", ""))

        stations_data = []
        summary_data = []

        if state and lat_start and lat_end and metric:
            try:
                stations_data = get_station_data(state, float(lat_start), float(lat_end))
                summary_data = get_summary_data(state, float(lat_start), float(lat_end), metric)
            except Exception as e:
                return f"<pre>Error: {e}</pre>"

        return get_level2_page_html(
            form_data={"state": state, "lat_start": lat_start, "lat_end": lat_end, "metric": metric},
            states=states,
            metrics=metrics,
            stations_data=stations_data,
            summary_data=summary_data
        )
    except Exception as e:
        return f"<pre>Fatal error: {e}</pre>"

def get_level2_page_html(form_data, states, metrics, stations_data, summary_data):
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
            f"<tr><td>{s['site']}</td><td>{s['name']}</td><td>{s['region']}</td><td>{s['latitude']}</td></tr>"
            for s in stations_data
        )
    else:
        table1_rows = '<tr><td colspan="4" style="text-align:center">No stations in this range.</td></tr>'

    if summary_data:
        table2_rows = "\n".join(
            f"<tr><td>{s['region']}</td><td>{s['num_stations']}</td><td>{s['avg_max_temp']}</td></tr>"
            for s in summary_data
        )
    else:
        table2_rows = '<tr><td colspan="3" style="text-align:center">No summary data.</td></tr>'
#this is the nav bar hope this helps :P 
    nav_bar = """
    <header>
        <div class="logo">Logo</div>
        <nav>
            <a href="/">Home</a>
            <a href="/page1b">Mission</a>
            <a href="/page2a" class="active">Climate By Location</a>
            <a href="/page2b">Climate By Metric</a>
            <a href="/page3a">Similar Weather Station Sites</a>
            <a href="/page3b">Similar Weather Station Metrics</a>
        </nav>
    </header>
    """
    # The rest of my sprawling HTML mumbojumbo
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Climate By Weather Station | Weather & Climate Data Portal</title>
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
            .form-section label {{
                margin-right: 8px;
                font-weight: 500;
            }}
            .form-section select, .form-section input[type="number"] {{
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
            }}
            footer {{
                background: #f8f8f8;
                padding: 30px 20px;
                display: flex;
                justify-content: space-between;
                flex-wrap: wrap;
                font-size: 0.95em;
                border-top: 1px solid #e2e2e2;
            }}
            footer .column {{
                flex: 1;
                min-width: 180px;
                margin: 10px;
            }}
            footer .column h4 {{ margin-bottom: 10px; }}
            footer .column ul {{ list-style: none; padding: 0; }}
            footer .column ul li {{ margin-bottom: 5px; }}
            footer .social-icons img {{
                width: 20px;
                margin-right: 10px;
                vertical-align: middle;
            }}
        </style>
    </head>
    <body>
        {nav_bar}
        <div class="container">
            <h2>Focused View of Climate Change by Weather Station</h2>
            <div class="form-section">
                <form method="GET" action="/page2a">
                    <label for="state">State:</label>
                    <select name="state" id="state" required>
                        <option value="">-- Select State --</option>
                        {state_options}
                    </select>
                    <label for="lat_start">Start Latitude:</label>
                    <input type="number" step="0.01" name="lat_start" id="lat_start" value="{form_data.get('lat_start', '')}" required>
                    <label for="lat_end">End Latitude:</label>
                    <input type="number" step="0.01" name="lat_end" id="lat_end" value="{form_data.get('lat_end', '')}" required>
                    <label for="metric">Climate Metric:</label>
                    <select name="metric" id="metric" required>
                        <option value="">-- Select Metric --</option>
                        {metric_options}
                    </select>
                    <input type="submit" value="View Data">
                </form>
            </div>
            <h3>Table 1: Weather Station Details</h3>
            <table>
                <tr>
                    <th>Station no.</th>
                    <th>Station Name</th>
                    <th>Region</th>
                    <th>Latitude</th>
                </tr>
                {table1_rows}
            </table>
            <div class="summary-title"><b>Table 2: Regional Climate Summary</b></div>
            <table>
                <tr>
                    <th>Region</th>
                    <th>Number Weather Stations</th>
                    <th>Average {next((m['name'] for m in metrics if m['id'] == form_data.get('metric')), 'Metric')}</th>
                </tr>
                {table2_rows}
            </table>
        </div>
        <footer>
            <div class="column">
                <h4>Logo</h4>
                <p><strong>Address:</strong><br>123 Main Street, City<br>State Province, Country</p>
                <div class="social-icons">

                    <img src="https://cdn-icons-png.flaticon.com/512/1384/1384063.png"> #easier to call them from the web than it is to call them from the local machine also they wont link to anything cause I cant be bothered...
                    <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png">
                    <img src="https://cdn-icons-png.flaticon.com/512/733/733579.png">
                </div>
            </div>
            <div class="column">
                <ul>
                    <li>About us</li>
                    <li>Help</li>
                    <li>Contact us</li>
                    <li>Info</li>
                </ul>
            </div>
            <div class="column">
                <ul>
                    <li>Services</li>
                    <li>Station</li>
                    <li>Map</li>
                    <li>Data Download</li>
                </ul>
            </div>
        </footer>
    </body>
    </html>
    """
