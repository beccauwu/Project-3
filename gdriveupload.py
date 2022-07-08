from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from run import start


def upload_to_folder(filename):
    """
    from: https://developers.google.com/drive/api/guides/folder#create
    Upload a file to the specified folder and prints file ID, folder ID
    Args: Id of the folder
    Returns: ID of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.load_credentials_from_file('creds.json')

    try:
        # create gmail api client
        service = build('drive', 'v3', credentials=creds)

        folder_id = '1_C-fAnZgSmfio28gpGks6ZPZRlW9G981'
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        media = MediaFileUpload(filename,
                                mimetype=None, resumable=True)
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        fileid = file.get('id')
        print(F'File with ID: "{fileid}" has been added to the folder with '
              F'ID "{folder_id}".')
        end(fileid)

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')


def end(fileid= None):
    """last function to be called. has an option to go to start menu or end

    Args:
        fileid (str, optional): id for a created invoice if an invoice was created. 
        Defaults to None.
    """
    print('-----Links-----')
    if fileid:
        print("Open created invoice:")
        print(f"https://drive.google.com/file/d/{fileid}/view?usp=sharing")
    print('Open invoices folder:')
    print('https://drive.google.com/drive/folders/1_C-fAnZgSmfio28gpGks6ZPZRlW9G981?usp=sharing')
    print('Open spreadsheets folder:')
    print('https://drive.google.com/drive/folders/1pOgtupYWIjwE0W5tDjbob2cMwOyht9K6?usp=sharing\n')
    print("""
          ---What would you like to do?---
          1. Go to start menu
          2. End
          """)
    while True:
        choise = input('Choose an option:')
        if choise == '1':
            start()
            break
        if choise == '2':
            print('Thank you for trying the app :)')
            quit()
        print('Value entered is not valid.')
        print('Please try again.')
