import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

SCOPES = ['https://www.googleapis.com/auth/classroom.courses',
          'https://www.googleapis.com/auth/classroom.announcements']

def get_file_id(courseid):
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_classroom.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds) 

    results = service.courses().announcements().list(courseId=courseid).execute()
    announcements = results.get('announcements', [])

    for i in range(2): #announcements[0] and [1]
        if "materials" in announcements[i].keys():
            # print(announcements[i]["materials"])
            drive_direct = announcements[i]['materials']
            file_id = drive_direct[0]['driveFile']['driveFile']['id']
            print('Aha! The id is: ',file_id)

        else:
            print('no pdf here... searching on next recent post')
    
    return file_id

def download_from_drive(id_file):
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    file_down = drive.CreateFile({'id':id_file})
    file_down.GetContentFile('test3.pdf')


if __name__ == '__main__':
    courseid = 23945367370 #APUSH classroom id
    fileID = get_file_id(courseid)
    download_from_drive(fileID)
