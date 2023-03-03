#============================== IMPORT LIBRARIES ==============================

from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
from evernote.edam.notestore.ttypes import NoteFilter
from evernote.edam.notestore.ttypes import NotesMetadataResultSpec
from config import EVERNOTE_DEVELOPER_TOKEN as evernote_developer_token
import xml.etree.ElementTree as ET
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID as spotify_client_id
from config import SPOTIFY_CLIENT_SECRET as spotify_client_secret
from config import SPOTIFY_REDIRECT_URI as spotify_redirect_uri

#============================== METHOD DEFINITIONS ==============================

def setup_evernote_client():
    # Set up the Evernote client
    client = EvernoteClient(token=evernote_developer_token, sandbox=True)
    print("Client set up complete")
    return client

def create_list(note):
    # Create a list of strings from the Evernote note
    item_list = []
    print(f"Note Name: {note.title}")
    #print(f"Note Content: {note.content}")
    root = ET.fromstring(note.content)
    for child in root:
        item_list.append("".join(child.itertext()))
    return item_list

def find_note(note_list):
    # Check if a note was found 
    if len(note_list.notes) > 0:
        # Get the first note in the list (The newest note)
        note = NOTE_STORE.getNote(evernote_developer_token, note_list.notes[0].guid, True, True, False, False)
        return note
    
    else:
        return False

def get_notebook():
    notebooks = NOTE_STORE.listNotebooks()

    for notebook in notebooks:
        if(notebook.name == NOTEBOOK_NAME):
            print('Found Notebook: ')
            print("  * ", notebook.name)
            return notebook
        
    raise ValueError(f"Notebook '{NOTEBOOK_NAME}' not found.")
    
def get_list_from_evernote():
    # Returns  list_name(str), list()
    notebook = get_notebook()

    # Set up the NoteFilter to search for notes with the specified title
    note_filter = NoteFilter(order=Types.NoteSortOrder.CREATED, notebookGuid=notebook.guid)

    # Use the NoteStore to search for notes that match the filter
    note_list = NOTE_STORE.findNotesMetadata(evernote_developer_token, note_filter, 0, 1, NotesMetadataResultSpec(includeTitle=True))

    note = find_note(note_list)

    if (note):
        # Create list of strings if note is found
        item_list = create_list(note)
        return note.title, item_list
    else:
        print('Note not found')
        return

def setup_spotify_client():
    # Set up the Spotify API client
    client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= spotify_client_id,
                                                       client_secret=spotify_client_secret,
                                                       redirect_uri=spotify_redirect_uri,
                                                       scope='playlist-modify-public'
                                                       ))
    return client

def get_tracks(shopping_list: list):
    # Returns a list of track URIs
    track_list = []
    for item in shopping_list:
        track_name = item
        results = SPOTIFY_CLIENT.search(q=track_name, type='track', limit = 50)
        track_uri = results['tracks']['items'][0]['uri']
        print(results['tracks']['items'][0]['name'])
        track_list.append(track_uri)
    

    return track_list

def add_tracks(track_uris: list, playlist ):
    # Add tracks to the playlist
    SPOTIFY_CLIENT.playlist_add_items(playlist['id'], track_uris)
    print(f'Added {len(track_uris)} tracks to the playlist.')
    return
    
def create_playlist(list_name: str, shopping_list: list):
    
    track_uris = get_tracks(shopping_list)
    # Create the new playlist
    playlist_name = list_name
    playlist_description = (f'Playlist from note "{playlist_name}"')
    user_id = SPOTIFY_CLIENT.me()['id']
    playlist = SPOTIFY_CLIENT.user_playlist_create(user_id, playlist_name, public=True, description=playlist_description)

    add_tracks(track_uris, playlist)

    print(f"Playlist '{playlist_name}' created!")

#============================== SCRIPT ==============================

EVERNOTE_CLIENT = setup_evernote_client()
NOTE_STORE = EVERNOTE_CLIENT.get_note_store()
NOTEBOOK_NAME = input("Enter the name of your notebook: ")
list_name, shopping_list = get_list_from_evernote()
print(shopping_list)
SPOTIFY_CLIENT = setup_spotify_client()
create_playlist(list_name, shopping_list)


