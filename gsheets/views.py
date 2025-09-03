from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from typing import Dict
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
import gsheets.utils as google_sheet_utils

def is_authenticated(session):

    credentials_session_key = settings.CREDENTIALS_SESSION_KEY_NAME

    if credentials_session_key not in session:
        # request.session['final_redirect'] = url_for('ssr_ui.google-sheets.all_sheets_data_api_request')
        # return redirect(url_for('auth.login'))
        return None
    
    # Load credentials from the session.
    credentials = Credentials(
        **session[credentials_session_key])

    if not credentials.valid:
        # session['final_redirect'] = url_for('ssr_ui.google-sheets.all_sheets_data_api_request')
        # return redirect(url_for('auth.login'))
        return None
    
    return credentials

# Create your views here.

def index(request):
    context: Dict = {
        "auth_url": request.build_absolute_uri(reverse("gauth:login")),
        "api": {
            "read_all_sheet": request.build_absolute_uri(reverse("gsheets:sheet")),
        }
    }
    return render(request, 'gsheets/index.html', {'context_data': context})

def read_sheet_data(request):

    response: dict = dict(message="successful", data=[])

    sheet_id = request.GET.get('sheetId', None)
    sheet_url = request.GET.get('sheetUrl', None) # given prefrence

    fetchByOptions = ['ALL', 'GID', 'INDEX', 'TITLE']
    fetchBy = request.GET.get('fetchBy', 'ALL')

    if fetchBy not in fetchByOptions:
        response["message"] = "error"
        response["errors"] = [f"fetchBy:{fetchBy} is not supported. supported `fetchBy` options are : {fetchByOptions}"]
        return JsonResponse(response, status=400)
    if fetchBy in ['INDEX', 'TITLE']:
        response["message"] = "error"
        response["errors"] = [f"as of now `fetchBy` only supports ['ALL', 'GID']"]
        return JsonResponse(response, status=400)
    
    if sheet_url:
        try:
            sheet_id, gid = google_sheet_utils.extract_id_gid(sheet_url)
        except:
            response["message"] = "error"
            response["errors"] = ["unable to parse google sheet url"]
            return JsonResponse(response, status=400)
    elif sheet_id:
        ...
    else:
        response["message"] = "error"
        response["errors"] = ["sheeId or sheetUrl is required"]
        return JsonResponse(response, status=400)
    
    credentials = is_authenticated(request.session)

    if not credentials:
        response["message"] = "unauthenticated"
        return JsonResponse(response, status=401)
    
    service = build("sheets", "v4", credentials=credentials)
    
    try:
        # Call the Sheets API
        sheet = service.spreadsheets()
        if fetchBy == 'ALL':
            data: list = google_sheet_utils.get_all_sheets_data(sheet, sheet_id, without_headers=False)
        if fetchBy == 'GID':
            data: list = google_sheet_utils.get_gid_sheets_data(sheet, sheet_id, gid, without_headers=False)
        response["data"] = data
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")
    except RefreshError:
        # session['final_redirect'] = url_for('ssr_ui.google-sheets.all_sheets_data_api_request')
        # return redirect(url_for('auth.login'))
        response["message"] = "unauthenticated"
        return JsonResponse(response, status=401)
    
    return JsonResponse(response, status=200)
    