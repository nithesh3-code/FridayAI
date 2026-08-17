import webbrowser

def search_google(query):

    url = "https://www.google.com/search?q=" + query.replace(" ", "+")

    webbrowser.open(url)

    return f"Searching Google for {query}"