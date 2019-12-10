from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def download_from_drive(materials_df, materials_selection):

    id_file = materials_df.iloc[materials_selection]['id']
    file_name = materials_df.iloc[materials_selection]['title']

    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    file_down = drive.CreateFile({'id': id_file})
    if os.path.exists('output') == False:
        os.mkdir('output')
    file_down.GetContentFile('output/{}'.format(file_name))
