import pickle, sys
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/classroom.courses',
          'https://www.googleapis.com/auth/classroom.announcements']

def parse_courses():
    results = service.courses().list(courseStates='ACTIVE').execute()
    courses = results['courses']
    ids = []
    for n,i in enumerate(courses):
        ids.append({'name':courses[n]['name'],'id':courses[n]['id']})
    ids_df = pd.DataFrame(ids)

    print('Here is a list of your google classrooms:','\n')
    print('#',' ','Classroom Name')
    print('----------')
    for n,i in enumerate(ids_df['name']):
        print(n,' ',i)

    selection = int(input('Which classroom do you want to get files from? Enter the corresponding number with the name of the classroom: '))
    return ids_df, selection



def get_id(ids_df, selection):
    """Basic usage of the Classroom API."""
    courseid = ids_df.iloc[selection]['id']

    results = service.courses().announcements().list(courseId=courseid).execute()
    announcements = results.get('announcements', [])

    for i in range(2): #announcements[0] and [1]
        if "materials" in announcements[i].keys():
            # print(announcements[i]["materials"])
            drive_direct = announcements[i]['materials']
            file_id = drive_direct[0]['driveFile']['driveFile']['id']
            print('Aha! The id is: ',file_id)
        else:
            print('no pdf yet... searching on next recent post')
            file_id = 0
    
    return file_id


def download_from_drive(id_file):
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    file_down = drive.CreateFile({'id':id_file})
    file_down.GetContentFile('output.pdf')


if __name__ == '__main__':
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
    
    ###---------------------------------
    ids_df, selection = parse_courses()

    fileID = get_id(ids_df, selection)
    if fileID == 0:
        sys.exit('There are currently no recent files to parse')
    
    download_from_drive(fileID)
