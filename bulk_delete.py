import base64
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_service():
    """Get a service that communicates to a Google API."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0, authorization_prompt_message="Please go to this URL: {url}", open_browser=True)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def delete_emails(service, query):
    """Delete emails matching the query."""
    try:
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        for message in messages:
            service.users().messages().trash(userId='me', id=message['id']).execute()
        print(f"Deleted {len(messages)} emails.")
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == '__main__':
    service = get_service()
    query = "from:*@yemeksepeti.com"
# Example: delete all unread emails. Modify the query as per your needs.
    delete_emails(service, query)
