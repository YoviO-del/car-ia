from fastapi import FastAPI
from Scraping.scraping import main
from starlette.config import Config
from AIAnalysis.langchainapplication import analyzer

# logging.basicConfig( level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
config = Config('.env')

# MYSQL DB CONNECTION HERE


linkedin = oauth.register(
    name='linkedin',
    client_id=config('LINKEDIN_CLIENT_ID'),
    client_secret=config('LINKEDIN_CLIENT_SECRET'),
    authorize_url=config('LINKEDIN_AUTHORIZE_URL'),
    access_token_url=config('LINKEDIN_ACCESS_TOKEN_URL'),
    userinfo_endpoint=config('LINKEDIN_USERINFO_ENDPOINT'),
    client_kwargs={"scope": "email"},
)


@app.get('/auth/callback/{provider}')
async def auth_callback(request: Request, provider: str):
    try:
        if provider not in ['google', 'linkedin', 'github']:
            return {"error": "Unsupported provider"}
        
        oauth_provider = oauth.create_client(provider)
        token = await oauth_provider.authorize_access_token(request)
        user_info = (await oauth_provider.get('userinfo')).json()

        # Save or update user in MongoDB
        existing_user = users_collection.find_one({"email": user_info("email")})
        if not existing_user:
            new_user = {
                "email": user_info("email"),
                "name": user_info.get("name"),
                "profile_picture": user_info.get("picture"),
            }
            users_collection.insert_one(new_user)
        else:
            users_collection.update_one(
                {"_id": existing_user["_id"]},
                {"$set": {
                    "name": user_info.get("name"),
                    "profile_picture": user_info.get("picture"),
                }}
            )

        return {"message": "User authenticated successfully", "user_info": user_info}

    except Exception as e:
        logger.error(f"Error in {provider} OAuth: {str(e)}")
        return {"error": "Authentication failed. Please try again."}

@app.get('/auth/callback/linkedin')
async def linkedin_auth_callback(request: Request):
    try:
        oauth_provider = oauth.create_client('linkedin')
        token = await oauth_provider.authorize_access_token(request)
        user_response = await oauth_provider.get('me', token=token)
        email_response = await oauth_provider.get(
            "emailAddress?q=members&projection=(elements*(handle~))", token=token
        )

        return {"message": "LinkedIn authentication successful"}

    except Exception as e:
        logger.error(f"Error in LinkedIn OAuth: {str(e)}")
        return {"error": str(e)}


@app.get("/")
async def getRoute():
    pass

@app.post("/analyze")
async def foo(linkedinUser: str):
    await main(linkedinUser)
    await analyzer()