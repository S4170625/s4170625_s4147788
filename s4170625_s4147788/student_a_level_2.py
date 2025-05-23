import pyhtml
def get_page_html(form_data):
    print("About to return page 2")
    
    page_html=f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Reading from a .db file</title>
    </head>
    <body>
        <h1>Page 2A - Example of retrieving data from a .db file...</h1>
    """
    sql_query = "select * from movie;"
    page_html+= f"<h2>Result from \"{sql_query}\"</h2>"
    
    #Run the query in sql_query and get the results
    results = pyhtml.get_results_from_query("database/movies.db",sql_query)
    
    #Adding results to the web page without any beautification. Try turning it into a nice table!
    for row in results:
        page_html+="<p>"+str(row)+"</p>\n"
    page_html+="""
        <p><a href="/">Go to Page 1A</a></p>
        <p><a href="/page2a">Go to Page 2A</a></p>
        <p><a href="/page3a">Go to Page 3A</a></p>
        <p><a href="/page1b">Go to Page 1B</a></p>
        <p><a href="/page2b">Go to Page 2B</a></p>
        <p><a href="/page3b">Go to Page 3B</a></p>
    </body>
    </html>
    """
    return page_html