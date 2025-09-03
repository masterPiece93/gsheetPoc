from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
from gauth.utilities import credentials_to_dict, final_redirect_uri, get_redirect_uri
from typing import Final


STATE_KEY_NAME: Final[str] = "oauth_state"

# Create your views here.

def index(request):
    return render(request, 'gauth/index.html')


def login(request):
    flow = Flow.from_client_config(
        client_config={
            "web":
            {
                    "client_id": settings.GOOGLE_CLIENT_ID
                ,   "client_secret": settings.GOOGLE_CLIENT_SECRET
                ,   "auth_uri":"https://accounts.google.com/o/oauth2/v2/auth"
                ,   "token_uri":"https://oauth2.googleapis.com/token"
            }
        }
        #if you need additional scopes, add them here
        ,scopes=[
            "https://www.googleapis.com/auth/userinfo.email"
            ,"https://www.googleapis.com/auth/userinfo.profile"
            ,"openid"
            ,"https://www.googleapis.com/auth/drive"
        ]      
    )

    # flow.redirect_uri = get_redirect_uri(request) # use this when 
    flow.redirect_uri = request.build_absolute_uri(reverse("gauth:callback"))

    authorization_url, state = (
        flow.authorization_url(
            access_type="offline"
            ,prompt="select_account"
            ,include_granted_scopes="true"
        )
    )
    request.session[STATE_KEY_NAME] = state
    if "final_redirect" not in request.session or not request.session["final_redirect"]:
        # request.session['final_redirect'] = final_redirect_uri(request) # directs where to land after login is successful.
        print("final redirect : ", request.build_absolute_uri(reverse("gsheets:index")))
        request.session['final_redirect'] = request.build_absolute_uri(reverse("gsheets:index")) # directs where to land after login is successful.

    return redirect(authorization_url)


def callback(request):
    #pull the state from the session
    session_state = request.session.get(STATE_KEY_NAME)
    
    # redirect_uri = request.base_url # --- Flask
    # redirect_uri = get_redirect_uri(request) # --- Django # use this when 
    redirect_uri = request.build_absolute_uri(reverse("gauth:callback"))

    #pull the authorization response
    # authorization_response = request.url # --- Flask
    authorization_response = request.build_absolute_uri() # --- Django
    #create our flow object similar to our initial login with the added "state" information
    flow = Flow.from_client_config(
        client_config={
            "web":
            {
                "client_id": settings.GOOGLE_CLIENT_ID
                ,"client_secret": settings.GOOGLE_CLIENT_SECRET
                ,"auth_uri":"https://accounts.google.com/o/oauth2/v2/auth"
                ,"token_uri":"https://oauth2.googleapis.com/token"
            }
        }
        ,scopes=[
            "https://www.googleapis.com/auth/userinfo.email"
            ,"https://www.googleapis.com/auth/userinfo.profile"
            ,"openid"
            ,"https://www.googleapis.com/auth/drive"
        ]  
        ,state=session_state    
    )  

    flow.redirect_uri = redirect_uri  
    #fetch token
    flow.fetch_token(authorization_response=authorization_response)
    #get credentials
    credentials = flow.credentials
    #verify token, while also retrieving information about the user
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token
        ,request= requests.Request()
        ,audience= settings.GOOGLE_CLIENT_ID
        ,clock_skew_in_seconds=5
    )
    #setting the user information to an element of the session
    #you'll generally want to do something else with this (login, store in JWT, etc)
    request.session["id_info"] = id_info
    request.session[settings.CREDENTIALS_SESSION_KEY_NAME] = credentials_to_dict(credentials)
    #redirecting to the final redirect (i.e., logged in page)
    redirect_response = redirect(request.session['final_redirect'])   

    return redirect_response
