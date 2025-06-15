def get_page_html(form_data):
    page_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Mission Statement</title>
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
            header nav a:hover {
                background: #003366;
                color: #fff;
            }
            .container {
                padding: 20px;
                text-align: center;
            }
            .personas-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                grid-template-rows: 1fr 1fr;
                gap: 24px;
                max-width: 900px;
                margin: 30px auto 0 auto;
            }
            .persona {
                background: #fafafa;
                padding: 18px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .persona img {
                width: 120px;
                height: 120px;
                object-fit: cover;
                border-radius: 50%;
                margin-bottom: 12px;
                background: #ccc;
            }
            .persona h3 {
                margin: 8px 0 6px 0;
            }
            .persona p {
                margin: 0;
                color: #444;
                font-size: 1em;
            }
            @media (max-width: 700px) {
                .personas-grid {
                    grid-template-columns: 1fr;
                    grid-template-rows: repeat(4, 1fr);
                }
            }
            footer {
                background: #f8f8f8;
                padding: 30px 20px;
                display: flex;
                justify-content: space-between;
                flex-wrap: wrap;
                font-size: 0.95em;
            }
            footer .column {
                flex: 1;
                min-width: 180px;
                margin: 10px;
            }
            footer .column h4 {
                margin-bottom: 10px;
            }
            footer .column ul {
                list-style: none;
                padding: 0;
            }
            footer .column ul li {
                margin-bottom: 5px;
            }
            footer .social-icons img {
                width: 20px;
                margin-right: 10px;
                vertical-align: middle;
            }
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
        <h2><strong>Mission Statement</strong></h2>
        <p>Our mission for the creation of this website, was to enable different groups of people to
        be able to easily access climate data that they may need, as weather is one of the factors that
        we as humans are unable to control, and can only log and predict patterns from previous trends, when 
        other peoples livelihood maybe at stake. From those unfamiliar with basic website controls to those more
        techonologically inclined, this website was built for the sole purpose of allowing as many people as possible
        to freely access this data, regardless of profession.</p>

        <div class="personas-grid">
            <div class="persona">
                <img src="images/persona1.jpg" alt="Persona 1">
                <h3>Persona 1</h3>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dictum, ipsum at eleifend tristique.</p>
            </div>
            <div class="persona">
                <img src="images/persona2.jpg" alt="Persona 2">
                <h3>Persona 2</h3>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dictum, ipsum at eleifend tristique.</p>
            </div>
            <div class="persona">
                <img src="images/persona3.jpg" alt="Persona 3">
                <h3>Persona 3</h3>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dictum, ipsum at eleifend tristique.</p>
            </div>
            <div class="persona">
                <img src="images/persona4.jpg" alt="Persona 4">
                <h3>Persona 4</h3>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dictum, ipsum at eleifend tristique.</p>
            </div>
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
