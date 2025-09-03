from django.conf import settings
from django.urls import reverse

__all__ = [
    "credentials_to_dict",
    "get_redirect_uri",
    "final_redirect_uri"
]

absolute_url_for = lambda request, value : request.url_root.strip("/") + "/" + reverse(value).strip("/")

def get_redirect_uri(request) -> str:
    """
    *   Since Oauth consent screen is set for `localhost`, hence
        we must access the endpoints on browser using `http://localhost:<port>/...`
        for local environment
    *   But for production environments , we must use the hosted domain .

    Formulates the google callback `redirect_uri` based on above considerations

    NOTE : It's better you run the server on localhost itself ( i.e same as what you have mentioned on consent screen )
    """
    if settings.DEBUG:
        port: int = 5000 # make it dynamic
        return f"http://localhost:{port}" + reverse("gauth:callback")
    
    return absolute_url_for(request, "gauth:callback")

def final_redirect_uri(request) -> str:
    """
    *   Since Oauth consent screen is set for `localhost`, hence
        we must access the endpoints on browser using `http://localhost:<port>/...`
        for local environment
    *   But for production environments , we must use the hosted domain .

    Formulates the application post login `redirect_uri` based on above considerations

    NOTE : It's better you run the server on localhost itself ( i.e same as what you have mentioned on consent screen )
    """
    if settings.DEBUG:
        port: int = 5000
        return f"http://localhost:{port}" + reverse("gsheets:index")
    
    return absolute_url_for(request, "gauth:logged_in")

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}