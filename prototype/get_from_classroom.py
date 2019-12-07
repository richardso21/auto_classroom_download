from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses',
          'https://www.googleapis.com/auth/classroom.announcements']


def get_file_id(option):
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_classroom.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)

    # Call the Classroom API
    if option == 1:
        results = service.courses().list().execute()
        courses = results.get('courses', [])

        index_map = ["id", "name", "section", "descriptionHeading", "description", "room", "ownerId",
                     "creationTime", "updateTime", "enrollmentCode",
                     "courseState", "alternateLink", "teacherGroupEmail", "courseGroupEmail", "teacherFolder", "courseMaterialSets", "guardiansEnabled", "calendarId"]

        x = pd.DataFrame(courses, columns=index_map)
        # print(x)
        # x.to_csv('example.csv')

    elif option == 2:
        courseid = 23945367370 #APUSH classroom id

        results = service.courses().announcements().list(courseId=courseid).execute()
        announcements = results.get('announcements', [])

        # index_map = ["courseId", "id", "text", "materials", "state", "alternateLink", "creationTime",
        #              "updateTime", "scheduledTime", "assigneeMode", "individualStudentsOptions", "creatorUserId"]
        # x = pd.DataFrame(announcements, columns = index_map)
        # x.to_csv('announcements.csv')

        for i in range(2): #announcements[0] and [1]
            if "materials" in announcements[i].keys():
                # print(announcements[i]["materials"])
                drive_direct = announcements[i]['materials']
                file_id = drive_direct[0]['driveFile']['driveFile']['id']
                print('Aha! The id is: ',file_id)

            else:
                print('no pdf here... searching on next recent post')
    
    return file_id


# if __name__ == '__main__':
#     main(option)
