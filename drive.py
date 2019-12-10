from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def download_from_drive(materials_df, materials_selection):

    id_file = materials_df.iloc[materials_selection]['id']

    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    file_down = drive.CreateFile({'id': id_file})
    file_down.GetContentFile('output.pdf')
