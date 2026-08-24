from fastapi import FastAPI
from Scraping.scraping import main
from AIAnalysis.langchainapplication import analyzer
#import mysql.connector

app = FastAPI()



@app.post("/analyze")
async def foo(linkedinUser: str):
    await main(linkedinUser)
    await analyzer()