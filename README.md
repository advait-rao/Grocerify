# Grocerify

Grocerify is a Python application that reads your shopping list from Evernote and creates a Spotify playlist comprising of the items on your shopping list.

## How it works

The app uses Evernote API to access the user's Evernote notes and extract the shopping list. It then uses Spotify API to search for songs with the same names as the items on the shopping list and creates a new Spotify playlist with those songs.

The user needs to have an Evernote account and a Spotify account with a valid Spotify developer token, Spotify client ID, client secret, and redirect URI.

## Installation

**1. Clone this repository:**

```bash
git clone https://github.com/username/grocerify.git
```

**2. Install the required libraries by running**

```bash
pip3 install -r requirements.txt
```

**3. Create a file called `config.py` and paste this text:**

```bash
EVERNOTE_CONSUMER_KEY = ''
EVERNOTE_CONSUMER_SECRET = ''
EVERNOTE_DEVELOPER_TOKEN = ''
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''
SPOTIFY_REDIRECT_URI = ''
```

Enter in your values. You need to create accounts for both [Evernote](https://dev.evernote.com/#apikey) and [Spoitfy](https://developer.spotify.com/dashboard/login).

## Usage

As of now, the app works with the developer verson of Evernote, so create a notebook on sandbox.evernote.com . Create your shopping list as a note inside the notebook you created.

Run the `grocerify.py` file using the command:

```bash
python3 grocerify.py
```

### Future improvements

The app could be improved by adding a user interface that allows the user to create and edit the shopping list within the app, without having to access Evernote separately. The app could also ask for the user's music taste and prioritize songs that fit that genre. I will be implementing a feature that stores a record of songs the user has added to playlists already and prioritise adding new songs.

### Contributing

Contributions to this project are welcome. If you find a bug or want to suggest an improvement, please open an issue or submit a pull request.

### License

This project is licensed under the MIT License - see the LICENSE.md file for details.
