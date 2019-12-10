import pickle, sys, os, argparse
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
    for n, i in enumerate(courses):
        ids.append({'name': courses[n]['name'], 'id': courses[n]['id']})
    ids_df = pd.DataFrame(ids)

    print('Here is a list of your google classrooms:', '\n')
    print('#', ' ', 'Classroom Name')
    print('----------')
    for n, i in enumerate(ids_df['name']):
        print(n, ' ', i)

    selection = input(
        'Which classroom do you want to get files from? Enter the corresponding number with the name of the classroom or quit with \'q\': ')

    while selection == '':
        selection = input('Please select a classroom')

    if selection == 'q' or selection == 'Q':
        sys.exit('Quitting...')

    selection = int(selection)

    return ids_df, selection


def get_id(ids_df, selection):
    """Basic usage of the Classroom API."""
    courseid = ids_df.iloc[selection]['id']

    results = service.courses().announcements().list(
        courseId=courseid).execute()
    announcements = results.get('announcements', [])

    materials = [announcements[n]['materials'][0] for n, i in enumerate(
        announcements) if 'materials' in announcements[n].keys()]
    materials_drive = [materials[n]['driveFile']['driveFile']
                       for n, i in enumerate(materials) if 'driveFile' in materials[n].keys()]
    materials_drive_df = pd.DataFrame(materials_drive).head(10)

    try:
        materials_drive_df['title']
    except:
        sys.exit('No files to parse')

    print('Listing most recent posts...')
    print('#', ' ', 'Post name')
    print('----------')

    for n, i in enumerate(materials_drive_df['title']):
        print(n, ' ', i)

    selection = input(
        'Which pdf do you want to download? (Select by entering # or quit with \'q\'): ')
    if selection == '':
        selection = 0
    elif selection == 'q' or selection == 'Q':
        sys.exit('Quitting...')
    else:
        selection = int(selection)

    return materials_drive_df, selection


def download_from_drive(materials_df, materials_selection):

    id_file = materials_df.iloc[materials_selection]['id']

    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    file_down = drive.CreateFile({'id': id_file})
    file_down.GetContentFile('output.pdf')


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='only if you know what you\'re doing')
    # parser.add_argument('')

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

    # ---------------------------------
    ids_df, selection = parse_courses()

    materials_df, materials_selection = get_id(ids_df, selection)

    download_from_drive(materials_df, materials_selection)
