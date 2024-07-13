#https://developers.google.com/drive/api/guides/api-specific-auth

from dotenv import load_dotenv #get the Data of the .env
import os.path
import webbrowser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


def auth_with_cred():
   """
   idk copyd this function from the api doc, just changed the path to the credentials.json on line 33
   """
   creds = None
   # The file token.json stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
   if os.path.exists("token.json"):
     creds = Credentials.from_authorized_user_file("token.json", SCOPES)
   # If there are no (valid) credentials available, let the user log in.
   if not creds or not creds.valid:
     if creds and creds.expired and creds.refresh_token:
       creds.refresh(Request())
     else:
       flow = InstalledAppFlow.from_client_secrets_file(
           "basic_py/pokesheet/credentials.json", SCOPES
       )
       creds = flow.run_local_server(port=0)
     # Save the credentials for the next run
     with open("token.json", "w") as token:
       token.write(creds.to_json())
   return creds

def get_folder_id_by_name(service, folder_name):
    try:
        results = (
            service.files()
            .list(q=f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'",
                  fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])
        for i in items:
           print(f'id: {i["id"]} name: {i["name"]}')

    except HttpError as error:
     print(f"An error occurred: {error}")

def get_Files_in_Folder(service, team_folder):
    try:
        results = (
            service.files()
            .list(q="'{}' in parents".format(team_folder),
                  fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])
        return items

    except HttpError as error:
        print(f"An error occurred: {error}")

#get the data of the credentials.json
service = build('drive', 'v3', credentials=auth_with_cred())
pokesheets = "https://pokesheets.app/pokemon/drive/"

#get the Constants of the Folder-IDs using the .env file
load_dotenv()

team=''
folder_to_search = input("Welcher Spieler soll verwaltet werden?\n1: AE\n2: JE\n3: HD\n")
if folder_to_search == "AE" or folder_to_search == "1":
    team = os.getenv('AE_Team')
    box = os.getenv('AE_Box')

elif folder_to_search == "JE" or folder_to_search == "2":
    team = os.getenv('JE_Team')
    box = os.getenv('JE_Box')

elif folder_to_search == "HD" or folder_to_search == "3":
    team = os.getenv('HD_Team')
    box = os.getenv('HD_Box')


if team:
    mode_folder = input("1: Team\n2: Box\n[Team]: ")
    if mode_folder == "Box":
       mode_folder = box
    else:
       mode_folder = team
    Team = get_Files_in_Folder(service, mode_folder)

    if Team:
        for mon in Team:
           webbrowser.open_new_tab(pokesheets+ mon['id'])

else:
   print("Invalid input")
