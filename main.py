import MySQLdb
from Spotify import Spotify
from Genius import Genius
from flask import Flask, render_template, request

sp = Spotify('')
genius = Genius()
app = Flask("Real time spotify lyrics")
db = MySQLdb.connect("localhost", "root", "camillo", "spotify_player")
cursor = db.cursor()

sql = 'SELECT * FROM User WHERE username = "{}" and password = "{}"'
sql_insert = 'INSERT INTO User(first_name, last_name, email, username, password) VALUES ("{}","{}","{}","{}","{}")'        

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/auth', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    
    try:
        cursor.execute(sql.format(username, password))
        #print(sql.format(username, password))
        results = cursor.fetchall()
        
        if len(results) > 0:
            print('[/] Requesting current playing track')
            track_infos = sp.get_current_track()
            print('[+] Got current playing track')
            album_url = track_infos['item']['album']['images'][0]['url']
            name = track_infos['item']['album']['name'] #Not necessary
            artist_name = track_infos['item']['album']['artists'][0]['name'] #Not necessary
            track_name = track_infos['item']['name']
            print('[/] Requesting lyrics for {}'.format(track_name))
            lyrics = genius.get_song_lyrics(track_name)
            print('[+] Got lyrics for {}'.format(track_name))
            
            return render_template('home.html', link=album_url, lyrics=lyrics)
            # return render_template('home.html', link=album_url)
        
        else:
            return render_template('index.html')
    except:
        print('Unable to fetch data')
        
    return ''

@app.route('/new_user', methods=['POST'])
def new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']

    try:
        cursor.execute(sql_insert.format(first_name, last_name, email, username, password))
        db.commit()
        #print('User added succesfully!')
    except:
        print('AN error occurred while creating new user!')
        
    return ''

@app.route('/signup')
def signup():
    return render_template('signup.html')

app.run('0.0.0.0', 3000)