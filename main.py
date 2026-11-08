from fastapi import FastAPI
from Scraping.scraping import main
from AIAnalysis.langchainapplication import analyzer

app = FastAPI()


@app.get("/")
async def getRoute():
    pass

@app.post("/analyze")
async def foo(linkedinUser: str):
    await main(linkedinUser)
    await analyzer()