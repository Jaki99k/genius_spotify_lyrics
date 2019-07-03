import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.PhantomJS()
base_url = 'https://api.genius.com'
TOKEN = 'hiz5gVarH9_P-nDfty0JaCHpSV1khtMnABdWidLwFw0nj_KpIh3_Z6IPTkeO9kcm'

headers = {
    "Authorization" : "Bearer " + TOKEN,
}

class Genius:
    
    def __init__(self):
        self.token = TOKEN
    
    def search(self, song_name):
        return requests.get(base_url + '/search?q=' + song_name, headers=headers).json()
        
    def get_song_lyrics(self, track_name):
        #print(track_name)
        track_infos = self.search(track_name)
        #print(track_infos)
        song_path = track_infos['response']['hits'][0]['result']['api_path']
        new_url = 'https://genius.com{}'.format(song_path)
        driver.get(new_url)
        #print(new_url)
        elem = driver.find_element_by_class_name('lyrics')
        return elem.text
        
#s = Genius()
#s.get_song_lyrics('All me')