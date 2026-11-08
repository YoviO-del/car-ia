from fastapi import Request, FastAPI, HTTPException, status


app = FastAPI()

@app.middleware("http")
# request represents the incoming HTTP request from the client.
async def get_profile(request: Request):
    id = request.state.get("linkedin_id")
    name = request.state.get("name")

    if id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        ) 
    return {"user_id":id,"name":name}
