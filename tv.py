import requests
import codecs
import schedule
import time

# Function to perform handshake and fetch bearer token
def perform_handshake_and_get_token(base_url, mac):
    handshake_url = f"{base_url}/server/load.php?type=stb&action=handshake&token=&JsHttpRequest=1-xml"
    
    # Set headers and cookies
    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3",
        "X-User-Agent": "Model: MAG250; Link: WiFi",
        "Referer": f"{base_url}/c/",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=GMT",
        "Accept": "*/*",
        "Accept-Encoding": "gzip",
        "Connection": "keep-alive"
    }
    
    try:
        response = requests.get(handshake_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad responses
        
        # Attempt to decode gzip-encoded response
        decoded_response = response.content.decode('utf-8')
        
        # Parse JSON response to get token
        data = response.json()
        token = data['js']['token']
        
        return token
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to perform handshake: {e}")
        return None

# Function to fetch all channels and create playlist.txt
def fetch_and_create_playlist(base_url, mac, token):
    get_channels_url = f"{base_url}/server/load.php?type=itv&action=get_all_channels&JsHttpRequest=1-xml"
    
    # Set headers with bearer token
    headers = {
        "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3",
        "X-User-Agent": "Model: MAG250; Link: WiFi",
        "Referer": f"{base_url}/c/",
        "Cookie": f"mac={mac}; stb_lang=en; timezone=GMT",
        "Accept": "*/*",
        "Authorization": f"Bearer {token}",
        "Accept-Encoding": "gzip",
        "Connection": "keep-alive"
    }
    
    try:
        response = requests.get(get_channels_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad responses
        
        # Attempt to decode gzip-encoded response
        decoded_response = response.content.decode('utf-8')
        
        # Parse JSON response
        data = response.json()
        channels = data['js']['data']
        
        # Create playlist.txt containing all channels
        with codecs.open('playlist.txt', 'w', encoding='utf-8') as playlist_file:
            # Write #EXTtxt at the beginning of the file
            playlist_file.write('#EXTM3U\n')
            
            # Write each channel entry
            for channel in channels:
                name = channel['name']
                stream_url = channel['cmds'][0]['url'].replace('ffmpeg ', '')  # Remove 'ffmpeg ' prefix
                playlist_file.write(f"#EXTINF:0,{name}\n{stream_url}\n")
        
        print("playlist.txt file generated successfully.")
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch channels: {e}")

# Function to create main.txt by copying streams from playlist.txt based on stream IDs
def create_main_from_playlist(stream_ids):
    try:
        with codecs.open('playlist.txt', 'r', encoding='utf-8') as playlist_file:
            playlist_content = playlist_file.readlines()
        
        with codecs.open('main.txt', 'w', encoding='utf-8') as main_file:
            # Ensure the first line starts with #EXTtxt
            main_file.write('#EXTM3U\n')
            
            # Copy subsequent lines from playlist.txt
            for stream_id in stream_ids:
                for line in playlist_content:
                    if line.startswith('#EXTINF:0,'):
                        url_line = playlist_content[playlist_content.index(line) + 1].strip()
                        if f"stream={stream_id}" in url_line:
                            main_file.write(f"{line}{url_line}\n")
                            break
        
        print("main.txt file generated successfully.")
    
    except FileNotFoundError:
        print("Error: playlist.txt not found. Please generate playlist.txt first.")

# Function to update both playlists every hour
def update_playlists():
    base_url = 'http://185.243.7.154'
    mac = '00:1A:79:BD:60:0F'
    stream_ids = [
        546170, 155971, 156173, 280777, 156014, 156101, 156089, 156012, 156011, 
        155989, 156013, 280780, 155969, 1112132, 156033, 155970, 1116481, 156000, 1097624, 
        1097666, 1097664, 1569746, 1114582, 1114581, 1114583, 1114576, 1114577, 1283290
    ]
    
    # Perform handshake and get bearer token
    token = perform_handshake_and_get_token(base_url, mac)
    
    if token:
        # Fetch all channels and create playlist.txt
        fetch_and_create_playlist(base_url, mac, token)
        
        # Create main.txt by copying from playlist.txt in specified order
        create_main_from_playlist(stream_ids)

# Initial setup to generate both playlists
update_playlists()

# Schedule the update to run every hour
schedule.every().hour.do(update_playlists)

# Run the scheduler continuously
while True:
    schedule.run_pending()
    time.sleep(1)
