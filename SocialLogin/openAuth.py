import logging
from fastapi import Request, FastAPI, HTTPException
from authlib.integrations.starlette_client import OAuth
from decouple import config
from starlette.middleware.sessions import SessionMiddleware



app = FastAPI()
logger = logging.getLogger(__name__)

oauth = OAuth()

# Required by Authlib for OAuth state validation
app.add_middleware(
    SessionMiddleware,
    secret_key=config("SESSION_SECRET_KEY"),
    https_only=config("SESSION_HTTPS_ONLY", default=True, cast=bool),
)

# LinkedIn OAuth configuration
linkedin = oauth.register(
    name="linkedin",
    client_id=config("LINKEDIN_CLIENT_ID"),
    client_secret=config("LINKEDIN_CLIENT_SECRET"),
    server_metadata_url="https://www.linkedin.com/oauth/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)


@app.get("/auth/login/linkedin")
async def linkedin_login(request: Request):
    redirect_uri = request.url_for("auth_callback", provider="linkedin")
    return await linkedin.authorize_redirect(request, redirect_uri)


@app.get("/auth/callback/{provider}")
async def auth_callback(request: Request, provider: str):
    if provider != "linkedin":
        raise HTTPException(status_code=400, detail="Unsupported provider")

    try:
        oauth_provider = oauth.create_client(provider)

        token = await oauth_provider.authorize_access_token(request)

        response = await oauth_provider.get(
            "https://api.linkedin.com/v2/userinfo",
            token=token
        )
        response.raise_for_status()

        user_info = response.json()

        email = user_info.get("email")
        linkedin_id = user_info.get("sub")

        if not email or not linkedin_id:
            raise HTTPException(
                status_code=400,
                detail="Required LinkedIn user information is missing"
            )

        existing_user = users_collection.find_one(
            {"linkedin_id": linkedin_id}
        )

        if not existing_user:
            new_user = {
                "linkedin_id": linkedin_id,
                "email": email,
                "name": user_info.get("name"),
                "profile_picture": user_info.get("picture"),
            }

            users_collection.insert_one(new_user)

        else:
            users_collection.update_one(
                {"_id": existing_user["_id"]},
                {
                    "$set": {
                        "email": email,
                        "name": user_info.get("name"),
                        "profile_picture": user_info.get("picture"),
                    }
                }
            )

        return {
            "message": "User authenticated successfully"
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("LinkedIn OAuth authentication failed")

        raise HTTPException(
            status_code=401,
            detail="Authentication failed. Please try again."
        )