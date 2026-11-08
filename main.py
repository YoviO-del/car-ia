from auth_dependencies import get_profile
from fastapi import FastAPI, Depends
from Scraping.scraping import main
from AIAnalysis.langchainapplication import analyzer

app = FastAPI()


@app.get("/")
async def getRoute(profile = Depends(get_profile)):
    pass

@app.post("/analyze")
async def foo(linkedinUser: str):
    await main(linkedinUser)
    await analyzer()