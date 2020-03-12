import os
import pickle
import sys
import io
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.announcements.readonly',
          'https://www.googleapis.com/auth/drive.readonly']


def main():
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
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)

    class_selection_id = select_class(service)
    file_selection_id = select_file(service, class_selection_id)
    down_file(file_selection_id, creds)


def select_class(service):
    results = service.courses().list(courseStates='ACTIVE').execute()
    courses = results.get('courses', [])

    if not courses:
        print('No courses found.')
    else:
        print('Courses:\n====')
        for n, course in enumerate(courses):
            print(n, ' | ', course['name'])

    class_selection = ask_input('Select which classroom to parse file by inputting its corresponding number')

    return courses[class_selection]['id']


def select_file(service, class_selection_id):
    results = service.courses().announcements().list(courseId=class_selection_id, pageSize=20).execute()
    results = results['announcements']
    items = [result for result in results if 'materials' in result]
    items = [item['materials'][0]['driveFile']['driveFile'] for item in items]

    for n, file in enumerate(items):
        print(n, ' | ', file['title'])

    file_selection = ask_input('Select which file to parse')

    return items[file_selection]['id']


def down_file(file_selection_id, creds):
    drive_service = build('drive', 'v3', credentials=creds)

    meta = drive_service.files().get(fileId=file_selection_id).execute()
    name = meta['name']

    request = drive_service.files().get_media(fileId=file_selection_id)

    if not os.path.exists('output'): os.mkdir('output')
    os.chdir('output')

    fh = io.FileIO(name, mode='w')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    print('Done!!!')


def ask_input(string):
    ask = input(f'{string}, or quit with \'q\':')

    if ask == 'q' or ask == 'Q':
        halt(0)
    else:
        ask = int(ask)

    if not isinstance(ask, int):
        halt(1)

    return ask


def halt(exit_code):
    sys.exit('Quitting...') if exit_code == 0 else sys.exit('Invalid argument. Quitting...')


if __name__ == '__main__':
    main()
