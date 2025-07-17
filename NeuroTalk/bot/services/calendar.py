from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

import os

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build('calendar', 'v3', credentials=credentials)


def list_free_slots(start_iso: str, end_iso: str, duration_minutes: int):
    events_result = service.freebusy().query(
        body={
            "timeMin": start_iso,
            "timeMax": end_iso,
            "items": [{"id": CALENDAR_ID}],
        }
    ).execute()

    busy_times = events_result['calendars'][CALENDAR_ID].get('busy', [])
    free_slots = []

    start_time = datetime.fromisoformat(start_iso)
    end_time = datetime.fromisoformat(end_iso)

    current = start_time
    while current + timedelta(minutes=duration_minutes) <= end_time:
        slot_start = current.isoformat()
        slot_end = (current + timedelta(minutes=duration_minutes)).isoformat()
        conflict = any(
            busy['start'] < slot_end and busy['end'] > slot_start
            for busy in busy_times
        )
        if not conflict:
            free_slots.append((slot_start, slot_end))
        current += timedelta(minutes=15)

    return free_slots


def create_appointment(start_iso: str, end_iso: str, summary: str, description: str, attendee_email: str = None):
    event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start_iso, 'timeZone': 'Europe/Kyiv'},
        'end': {'dateTime': end_iso, 'timeZone': 'Europe/Kyiv'},
        'status': 'confirmed',
    }

    if attendee_email:
        event['attendees'] = [{'email': attendee_email}]

    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return created_event.get('htmlLink')
