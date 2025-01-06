# views.py
from google.auth.transport.requests import Request
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings
import os
import datetime
import json

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(settings.GOOGLE_API_CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=8080)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def get_events(request):
    creds = get_credentials()
    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.now().isoformat() + "Z"
        events_result = service.events().list(calendarId="primary", timeMin=now, maxResults=10, singleEvents=True, orderBy="startTime").execute()
        events = events_result.get("items", [])
        if not events:
            return JsonResponse({"message": "No upcoming events found."})
        event_list = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            event_list.append({"start": start, "summary": event["summary"]})
        return JsonResponse(event_list, safe=False)
    except HttpError as error:
        return JsonResponse({"error": str(error)})

def create_event(request):
    if request.method == 'POST':
        creds = get_credentials()
        event_data = json.loads(request.body)
        try:
            service = build("calendar", "v3", credentials=creds)
            event = {
                "summary": event_data.get("summary"),
                "start": {
                    "dateTime": event_data.get("start"),
                    "timeZone": "Asia/Kolkata",
                },
                "end": {
                    "dateTime": event_data.get("end"),
                    "timeZone": "Asia/Kolkata",
                },
            }
            event = service.events().insert(calendarId="primary", body=event).execute()
            return JsonResponse({"message": "Event created", "event": event})
        except HttpError as error:
            return JsonResponse({"error": str(error)})

    return HttpResponse(status=405)
