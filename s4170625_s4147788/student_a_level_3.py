def get_page_html(form_data):
    page_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Climate Statistics</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }
            header {
                background: #fff;
                padding: 10px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #ccc;
            }
            header .logo {
                font-weight: bold;
                font-size: 1.2em;
            }
            header nav a {
                margin-left: 10px;
                padding: 6px 14px;
                border: 1px solid #000;
                background: #fff;
                color: #222;
                text-decoration: none;
                border-radius: 3px;
                font-size: 1em;
                transition: background 0.2s;
            }
            header nav a:hover, header nav a.active {
                background: #003366;
                color: #fff;
            }
            .container {
                padding: 20px;
                max-width: 1200px;
                margin: 0 auto;
            }
            h2 {
                text-align: center;
                font-size: 2em;
                margin: 32px 0 18px 0;
                font-weight: bold;
                text-decoration: underline;
            }
            .stats-form-wrapper {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .stats-form {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 22px;
                background: #f5f5f5;
                border: 1px solid #bbb;
                border-radius: 10px;
                padding: 30px 36px;
                margin-bottom: 35px;
                max-width: 850px;
                width: 100%;
            }
            .left-section, .right-section {
                flex: 1 1 340px;
                min-width: 300px;
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            .optional-group, .dates-group {
                border: 1px solid #bbb;
                border-radius: 8px;
                padding: 12px 15px;
                background: #fff;
                margin-top: 10px;
            }
            .optional-title, .dates-title {
                font-weight: bold;
                margin-bottom: 6px;
                text-align: left;
            }
            label {
                display: block;
                margin-bottom: 3px;
                font-size: 1em;
            }
            input, select {
                width: 100%;
                padding: 6px;
                margin-bottom: 7px;
                border: 1px solid #aaa;
                border-radius: 4px;
                font-size: 1em;
            }
            .add-btn {
                display: inline-block;
                margin-top: 7px;
                background: #e0e0e0;
                border: none;
                border-radius: 4px;
                padding: 4px 10px;
                font-size: 1.2em;
                cursor: pointer;
                transition: background 0.2s;
            }
            .add-btn:hover {
                background: #003366;
                color: #fff;
            }
            .start-btn {
                align-self: flex-end;
                margin-top: 17px;
                padding: 10px 25px;
                border-radius: 4px;
                border: none;
                background: #003366;
                color: #fff;
                font-size: 1.1em;
                cursor: pointer;
                transition: background 0.2s;
            }
            .start-btn:hover {
                background: #3366cc;
            }
            .results-table {
                width: 95%;
                margin: 0 auto;
                border-collapse: collapse;
                background: #fff;
                border: 1px solid #bbb;
                margin-bottom: 35px;
            }
            .results-table th, .results-table td {
                border: 1px solid #bbb;
                padding: 11px 9px;
                text-align: center;
            }
            .results-table th {
                background: #003366;
                color: #fff;
                font-weight: bold;
            }
            @media (max-width: 900px) {
                .stats-form {
                    flex-direction: column;
                    align-items: stretch;
                }
            }
        </style>
    </head>
    <body>
    <header>
        <div class="logo">Logo</div>
        <nav>
            <a href="/">Mission Statement</a>
            <a href="/page2a">Weather</a>
            <a href="/page3a" class="active">Climate</a>
        </nav>
    </header>
    <div class="container">
        <h2>Climate Statistics</h2>
        <div class="stats-form-wrapper">
            <form class="stats-form" autocomplete="off">
                <div class="left-section">
                    <label for="metric_a">Select Metric (with unit)</label>
                    <select id="metric_a" name="metric_a">
                        <option>Rainfall (mm)</option>
                        <option>Temperature (°C)</option>
                        <option>Humidity (%)</option>
                    </select>
                    <label for="station_id">Station ID</label>
                    <input type="text" id="station_id" name="station_id" placeholder="e.g., 101">
                    
                    <div class="optional-group">
                        <div class="optional-title">Additional Settings (Optional)</div>
                        <label for="metric_optional">Select Metric (with unit)</label>
                        <select id="metric_optional" name="metric_optional">
                            <option>Rainfall (mm)</option>
                            <option>Temperature (°C)</option>
                            <option>Humidity (%)</option>
                        </select>
                        <button class="add-btn" type="button">+</button>
                        <div style="margin-top:10px">
                            <label for="metric_constant">Metric Constant</label>
                            <select id="metric_constant" name="metric_constant">
                                <option>Rainfall (mm)</option>
                                <option>Temperature (°C)</option>
                                <option>Humidity (%)</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="right-section">
                    <label for="start_date_a">Start Date A (DD/MM/YYYY)</label>
                    <input type="text" id="start_date_a" name="start_date_a" placeholder="DD/MM/YYYY">
                    <label for="end_date_a">End Date A (DD/MM/YYYY)</label>
                    <input type="text" id="end_date_a" name="end_date_a" placeholder="DD/MM/YYYY">
                    <div class="dates-group">
                        <div class="dates-title">Additional Dates (Optional)</div>
                        <label for="start_date_b">Start Date B (DD/MM/YYYY)</label>
                        <input type="text" id="start_date_b" name="start_date_b" placeholder="DD/MM/YYYY">
                        <label for="end_date_b">End Date B (DD/MM/YYYY)</label>
                        <input type="text" id="end_date_b" name="end_date_b" placeholder="DD/MM/YYYY">
                        <button class="add-btn" type="button">+</button>
                    </div>
                    <button class="start-btn" type="submit">Start Search</button>
                </div>
            </form>
        </div>
        <table class="results-table">
            <thead>
                <tr>
                    <th>Metric (Unit)</th>
                    <th>Total Metric<br>(Start A - End A)</th>
                    <th>Total Metric<br>(Start B - End B)</th>
                    <th>Percentage Difference</th>
                    <th>Difference from<br>selected metric (%)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td colspan="5" style="color: #666;">Results will appear here after search</td>
                </tr>
            </tbody>
        </table>
    </div>
    </body>
    </html>
    """
    return page_html
