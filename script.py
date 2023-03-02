import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter
from evernote.edam.notestore.ttypes import NotesMetadataResultSpec
import xml.etree.ElementTree as ET
from config import DEVELOPER_TOKEN as developer_token

def get_list_from_evernote(notebook_name: str):

    # Set up the Evernote client
    client = EvernoteClient(token=developer_token, sandbox=True)
    note_store = client.get_note_store()
    print("Client set up complete")

    notebooks = note_store.listNotebooks()
    print("Found ", len(notebooks), " notebooks:")
    notebook_guid = 0
    for notebook in notebooks:
        if(notebook.name == notebook_name):
            notebook_guid = notebook.guid
            print('Found Shopping Notebook')
            print("  * ", notebook.name)

    if(notebook_guid == 0):
        print(f"Notebook {notebook_name} not found.")
        return


    # Set up the NoteFilter to search for notes with the specified title
    note_filter = NoteFilter(order=Types.NoteSortOrder.CREATED, notebookGuid=notebook_guid)

    # Use the NoteStore to search for notes that match the filter
    note_list = note_store.findNotesMetadata(developer_token, note_filter, 0, 1, NotesMetadataResultSpec(includeTitle=True))

    # Check if a note was found
    if len(note_list.notes) > 0:
        # Get the first note in the list (assuming there is only one note with the specified title)
        note = note_store.getNote(developer_token, note_list.notes[0].guid, True, True, False, False)
        item_list = []
        # Do something with the note
        print(f"Note Name: {note.title}")
        #print(f"Note Content: {note.content}")
        root = ET.fromstring(note.content)
        for child in root:
            item_list.append("".join(child.itertext()))
        return item_list
    else:
        print(f"No notes were found in notebook {notebook_name}.")
        return

def main():
    notebook_name = input("Enter the name of your notebook: ")
    shopping_list = get_list_from_evernote(notebook_name)
    #print(shopping_list)
    #create_playlist(shopping_list)

main()


