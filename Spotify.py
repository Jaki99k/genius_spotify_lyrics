import requests

spotify_url = 'https://api.spotify.com/v1/me/player/currently-playing'

headers_refresh = {
        'client_id': '1f8bb2845ee9488d88f31a11ea0481f1',
        'client_secret': 'e96a525870c04b98ad5863b269da83f3',
        'refresh_token': 'AQA4pDS2dQRgGC0X2MfEMzHkrRTId6w1d6B5govjZdOMHa7wxN-zkm2D0kDo5QPu7awelkIP6N48TjWCfYFv49ZKiC74aFbXj_XrWcDMuEY7b39sUC1Ja9MQFre0ZSfvJJzL2w',
        'grant_type': 'refresh_token',
        'redirect_uri': 'http://localhost:3000/home'
}

class Spotify:
        
    def __init__(self, spotify_token):
        self.headers = {'Authorization': 'Bearer {}'.format(spotify_token),}

    def get_new_token(self):
        return requests.post('https://accounts.spotify.com/api/token', data=headers_refresh).json()
    
    def get_current_track(self):
        current_track_info = requests.get(spotify_url, headers=self.headers).json()
        
        if 'error' in current_track_info:
            print('[!] The token u provided is invalid or is expired!')
            self.headers = {'Authorization': 'Bearer {}'.format(self.get_new_token()['access_token'])}
            print('[+] Spotify token updated!')
            return self.get_current_track()
        else:
            return current_track_info
        #print(current_track_info)
