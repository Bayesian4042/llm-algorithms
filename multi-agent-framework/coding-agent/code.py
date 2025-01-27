from fastapi import FastAPI, HTTPException, Query
import requests

app = FastAPI()

GITHUB_API_URL = "https://api.github.com/search/repositories"

@app.get("/search")
def search_repositories(query: str = Query(..., min_length=1)):
    try:
        response = requests.get(GITHUB_API_URL, params={"q": query})
        response.raise_for_status()
        data = response.json()
        return {"repositories": data.get("items", [])}
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            raise HTTPException(status_code=403, detail="API rate limit exceeded")
        elif response.status_code == 422:
            raise HTTPException(status_code=422, detail="Invalid query")
        else:
            raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail="Internal server error")