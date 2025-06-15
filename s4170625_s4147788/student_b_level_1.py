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
    </body>
    </html>
    """
    return page_html
