from langchain.tools import tool
from ddgs import DDGS

@tool(description="Use this to search and find the related content for the query")
def search_web(query:str):
    
    """Search the web and return the resu;t"""
    try:
        searches = DDGS().text(query,max_results =3)
    except Exception as e:
        return f"Search Failed: {e}"
    result = []
    
    for search in searches:
        result.append(f"Title: {search.get('title', '')}\nReference: {search.get('href', '')}\nBody: {search.get('body', '')}")
        
    return result