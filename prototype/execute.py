import drive_download
import get_from_classroom


id_for_down = get_from_classroom.get_file_id(2) #2 means to get file-id

print('passing id down to google drive...','\n')

drive_download.download_from_drive(id_for_down)

print()
print('done?')