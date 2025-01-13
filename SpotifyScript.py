import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Step 1: Set up Spotify API credentials
CLIENT_ID = 'd71a0e0d7d4046d48efba4600287a0c3'  # Replace with your Client ID
CLIENT_SECRET = '1b35115a5f8449a98426c32718817bfd'  # Replace with your Client Secret

# Spotify Authentication
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Step 2: Load your dataset
file_path = r"D:\Spotify Dashboard\Most Streamed Spotify Songs 2024.csv"  # Input file path
try:
    spotify_data = pd.read_csv(file_path, encoding='latin1')
    print("Dataset loaded successfully.")
    print(spotify_data.head())  # Show the first few rows to confirm
except FileNotFoundError:
    print(f"Error: File not found at {file_path}. Please check the path and try again.")
    exit()
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

# Step 3: Function to fetch cover URL
def get_cover_url(track_name, artist_name):
    try:
        query = f"track:{track_name} artist:{artist_name}"
        results = sp.search(q=query, type='track', limit=1)
        if results['tracks']['items']:
            return results['tracks']['items'][0]['album']['images'][0]['url']
        return None  # No match found
    except Exception as e:
        print(f"Error fetching cover URL for {track_name} by {artist_name}: {e}")
        return None

# Step 4: Add cover URLs
print("Fetching cover URLs. This might take a while...")
try:
    spotify_data['cover_url'] = spotify_data.apply(
        lambda row: get_cover_url(row['Track'], row['Artist']), axis=1
    )
    print("Cover URLs fetched successfully.")
except Exception as e:
    print(f"Error adding cover URLs: {e}")
    exit()

# Step 5: Save the updated dataset
output_file = r"D:\Spotify Dashboard\Updated_Most_Streamed_Spotify_Songs_2024.csv"  # Output file path
try:
    spotify_data.to_csv(output_file, index=False, encoding='latin1')
    print(f"Updated dataset saved to {output_file}")
except Exception as e:
    print(f"Error saving dataset: {e}")
