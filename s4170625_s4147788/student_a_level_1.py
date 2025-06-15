def get_page_html(form_data):

    fact1 = "Fact 1"
    fact2 = "Fact 2"
    fact3 = "Fact 3"
    fact4 = "Fact 4"

    page_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Weather & Climate Data Portal</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }}
            header {{
                background: #fff;
                padding: 10px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #ccc;
            }}
            header .logo {{
                font-weight: bold;
                font-size: 1.2em;
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
            nav a:hover {{
                background: #003366;
                color: #fff;
            }}
            .container {{
                padding: 20px;
                text-align: center;
            }}
            .facts-section {{
                max-width: 600px;
                margin: 32px auto 30px auto;
                padding: 18px 32px;
                background: #fafafa;
                border-radius: 10px;
                border: 1px solid #ddd;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            }}
            .facts-section h2 {{
                margin-bottom: 16px;
                font-size: 1.4em;
                text-decoration: underline;
            }}
            .facts-section ul {{
                text-align: left;
                font-size: 1.13em;
                padding-left: 1.3em;
                margin: 0;
            }}
            .facts-section li {{
                margin-bottom: 10px;
            }}
            .facts-section li::marker {{
                color: #003366;
            }}
            .topics-section {{
                margin-top: 38px;
                margin-bottom: 18px;
            }}
            .topics-section h3 {{
                font-size: 1.15em;
                margin-bottom: 8px;
            }}
            .topics-list {{
                display: flex;
                justify-content: center;
                gap: 30px;
                margin-bottom: 24px;
                flex-wrap: wrap;
            }}
            .topics-list .topic {{
                padding: 10px 20px;
                background: #e6eefc;
                border-radius: 6px;
                font-weight: bold;
                border: 1px solid #aac3e6;
            }}
            footer {{
                background: #f8f8f8;
                padding: 30px 20px;
                display: flex;
                justify-content: space-between;
                flex-wrap: wrap;
                font-size: 0.95em;
            }}
            footer .column {{
                flex: 1;
                min-width: 180px;
                margin: 10px;
            }}
            footer .column h4 {{
                margin-bottom: 10px;
            }}
            footer .column ul {{
                list-style: none;
                padding: 0;
            }}
            footer .column ul li {{
                margin-bottom: 5px;
            }}
            footer .social-icons img {{
                width: 20px;
                margin-right: 10px;
                vertical-align: middle;
            }}
        </style>
    </head>
    <body>
    <header>
        <div class="logo">Logo</div>
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
        <div class="topics-section">
            <h3>Topics covered by this website:</h3>
            <div class="topics-list">
                <div class="topic">Weather Data</div>
                <div class="topic">Climate Trends</div>
                <div class="topic">Weather Stations</div>
                <div class="topic">Australian Regions</div>
            </div>
            <div style="font-size:1.09em;color:#444;margin-top:12px;">
                Explore Australia’s weather and climate history with easy-to-understand facts and interactive tools for all users.
            </div>
        </div>

        <div class="facts-section">
            <h2>Key Facts</h2>
            <ul>
                <li>{fact1}</li>
                <li>{fact2}</li>
                <li>{fact3}</li>
                <li>{fact4}</li>
            </ul>
        </div>
    </div>

    <footer>
        <div class="column">
            <h4>Logo</h4>
            <p><strong>Address:</strong><br>123 Main Street, City<br>State Province, Country</p>
            <div class="social-icons">
                <img src="https://cdn-icons-png.flaticon.com/512/1384/1384063.png">
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
    return page_html
