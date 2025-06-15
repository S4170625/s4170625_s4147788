import os
import csv

def get_page_html(form_data):
    # Get the path for FRICKEN DESCRIPTION.CSV ;-;
    desc_csv_path = os.path.join(os.path.dirname(__file__), "description.csv")
    
    attributes_list = []
    
    with open(desc_csv_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            
            attributes_list.append(f"{row['Field']}: {row['Description']}")

    # FACTS :3
    fact1 = "Available year range: 1910 to 2023"
    fact2 = "Lowest recorded temperature: -15.6°C at Charlotte Pass"
    fact3 = "Highest recorded rainfall: 894mm at Tully Sugar Mill"
    fact4 = "Region with most weather stations: Western District (21 stations)"
    
    # HTML mumbojumbo :P 
    page_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Weather & Climate Data</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; }}
            header {{ background: #fff; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #ccc; }}
            header .logo {{ font-weight: bold; font-size: 1.2em; }}
            nav {{ display: flex; gap: 8px; }}
            nav a {{ margin-left: 0; padding: 6px 14px; border: 1px solid #000; background: #fff; color: #222; text-decoration: none; border-radius: 3px; font-size: 1em; transition: background 0.2s; }}
            nav a:hover {{ background: #003366; color: #fff; }}
            .container {{ padding: 20px; text-align: center; }}
            .facts-section {{ max-width: 600px; margin: 32px auto 30px auto; padding: 18px 32px; background: #fafafa; border-radius: 10px; border: 1px solid #ddd; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }}
            .facts-section h2 {{ margin-bottom: 16px; font-size: 1.4em; text-decoration: underline; }}
            .facts-section ul {{ text-align: left; font-size: 1.13em; padding-left: 1.3em; margin: 0; }}
            .facts-section li {{ margin-bottom: 10px; }}
            .facts-section li::marker {{ color: #003366; }}
            .topics-section {{ margin-top: 38px; margin-bottom: 18px; }}
            .topics-section h3 {{ font-size: 1.15em; margin-bottom: 8px; }}
            .topics-list {{ display: flex; justify-content: center; gap: 30px; margin-bottom: 24px; flex-wrap: wrap; }}
            .topics-list .topic {{ padding: 10px 20px; background: #e6eefc; border-radius: 6px; font-weight: bold; border: 1px solid #aac3e6; }}
            .attributes-section {{ max-width: 650px; margin: 34px auto 40px auto; background: #f8faff; border: 1px solid #c7e0fc; border-radius: 10px; padding: 18px 32px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); text-align: left; }}
            .attributes-section h2 {{ font-size: 1.16em; text-decoration: underline; }}
            .attributes-section ul {{ font-size: 1.04em; padding-left: 1.4em; }}
        </style>
    </head>
    <body>
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
    <div class="container">
        <div class="topics-section">
            <h3>Topics covered by this website:</h3>
            <div class="topics-list">
                <div class="topic">Weather Data</div>
                <div class="topic">Climate Trends</div>
                <div class="topic">Weather Stations</div>
                <div class="topic">Weather Districts</div>
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
        <div class="attributes-section">
            <h2>Natural Language (Attributes and descriptions)</h2>
            <ul>
                {''.join(f'<li>{attr}</li>' for attr in attributes_list)}
            </ul>
        </div>
    </div>
    </body>
    </html>
    """
    return page_html
