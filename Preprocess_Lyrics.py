import pandas as pd
import re
import os


df = pd.read_csv("/TDI Capstone Project/Retrieved Data/AZLyrics/AZLyrics-Songs-OG.csv")
df = df[["songs_names", "songs_urls", "save_as"]]

def extract_lyrics(page_body):
    
    start = r"<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->"

    end = r"<!-- MxM banner -->"

    pattern = f'{start}.+{end}'

    
    lyrics = re.findall(str(pattern), page_body, re.DOTALL)
    
    lyrics = lyrics[0]
    
    lyrics = lyrics.replace(start, "")
    lyrics = lyrics.replace(end, "")
    
    lyrics = re.sub(r'<.+?>', '', lyrics)
    
    lyrics = re.sub(r'^\s+|\s+$', '', lyrics)
    
    #lyrics = lyrics.strip()
    
    return lyrics



def extract_artist_genre(page_body):
    
    block = re.findall(r'"genre".+?];', page_body, re.DOTALL)
    
    genre = block[0]
    
    genre = re.findall(r'"genre".+?]', genre)
    
    genre = genre[0]
    
    genre = re.sub(r'^.+?, ', '', genre)
    
    genre = genre.replace('"', "")
    genre = genre.replace(']', "")
    
    artist = block[0]
    
    artist = re.findall(r'"artist".+?]', artist)
    
    artist = artist[0]
    
    artist = re.sub(r'^.+?, ', '', artist)

    artist = artist.replace('"', "")
    artist = artist.replace(']', "")
        
    return tuple([artist, genre])



def extract_album_year(page_body):
    
    start = r'<!-- album songlists -->'
    
    end = r'<!-- album songlists end -->'
    
    pattern = f"{start}.+?{end}"
    
    block = re.findall(pattern, page_body, re.DOTALL)
    
    try:
        
        block = block[0]
        
        block = block.replace(start, "")
        block = block.replace(end, "")
        
        if len(block) <= 10:
            return tuple([None, None])
            
        block = re.findall(r'<div class="songinalbum_title">album:.+?<div>', block, re.DOTALL)
                
        try:
            
            block = block[0]
            
            album = re.findall(r'<b>.+?</b>', block)
            
            album = album[0]
            
            album = re.sub(r'<.+?>', '', album)
            album = album.replace('"', "")
            
            album_year = re.findall(r'</b>.+?<div>', block)
                        
            album_year = re.findall(r'\d{4}', album_year[0])
            
            album_year = album_year[0]
            
            
            return tuple([album, int(album_year)])
        
        except:
            return tuple([None, None])
        
           
    except:
        return tuple([None, None])

    

def extract_songname(page_body):
    
    songname = re.findall(r'SongName = .+?";', page_body, re.DOTALL)    
    
    songname = re.findall(r'".+"', songname[0])
    
    songname = songname[0].replace('"', "")

    return songname



def extract_similar_songs(page_body):
    
    if "<b>You May Also Like</b>" in page_body:
        
        start = r'<b>You May Also Like</b>.+?'
        end = r'<form class="search noprint" method="get"'
        pattern = f"{start}.+?{end}"
        
        songs = re.findall(pattern, page_body, re.DOTALL)
        
        songs = re.findall(r'http.+?\.html', songs[0])
        
        songs2 = list()
        
        for song in songs:
            
            songs2.append(re.sub(r'^.+?lyrics/', '', song).replace('/', '_'))
            
        songs = songs2
        
        return songs
    
    else:
        
        return None
    
    
def extract_credits(page_body):
        
    start = r'<!-- credits -->'
    
    end = r'</div>'
    
    pattern = f"{start}.+?{end}"
    
    block = re.findall(pattern, page_body, re.DOTALL)
    
    block = block[0]
        
    if "Writer(s):" in block:
        
        credits = re.findall(r'<small>.+?</small>', block)
                
        credits = re.sub(r'<.+?>', '', credits[0])
        
        credits = credits.replace('Writer(s): ', "")
        
        credits = credits.split(', ')
    
        return credits
    
    else:
        
        return None

    

def extract_song_facts(page_body):
    
    start = r'<!-- song facts -->'
    
    end = r'<div class="abovebreadcrumb noprint">'
    
    pattern = f"{start}.+?{end}"
    
    block = re.findall(pattern, page_body, re.DOTALL)
    
    block = block[0]
    
    block = block.replace(start, '')
    block = block.replace(end, '')
    
    if len(block) <= 10:
        return None
    
    song_facts = block.split('</div>')
    
    facts = list()
    
    for fact in song_facts:
        
        fact = fact.replace('<div class="panel album-panel noprint">', '')
        fact = re.sub(r'<.+?>', '', fact)
        fact = fact.replace('\n', ' ')
        fact = fact.strip()
        
        if len(fact) > 5:
            
            facts.append(fact)
        
    
    
    return facts
    
    
#Extract all useful fields for all songs:

os.chdir("/TDI Capstone Project/Retrieved Data/AZLyrics/Lyrics Pages")

dataset = {
    "SongHandle": [],
    "SongName": [],
    "Credits": [],
    "Facts": [],
    "Album": [],
    "Year": [],
    "Artist": [],
    "Genre": [],
    "Lyrics": [],
    "SimilarSongs": []
}

for i in range(len(df)):

    file_name = df['save_as'][i]
    
    try:
        with open(file_name, 'r') as f:

            l = f.read()

            b = extract_artist_genre(str(l))

            artist = b[0]

            genre = b[1]

            lyrics = extract_lyrics(str(l))

            ay = extract_album_year(str(l))

            album = ay[0]

            album_year = ay[1]

            songname = extract_songname(str(l))

            similar_songs = extract_similar_songs(str(l))

            credits = extract_credits(str(l))

            song_facts = extract_song_facts(str(l))


            dataset["SongHandle"].append(file_name)
            dataset["SongName"].append(songname)
            dataset["Credits"].append(credits)
            dataset["Facts"].append(song_facts)
            dataset["Album"].append(album)
            dataset["Year"].append(album_year)
            dataset["Artist"].append(artist)
            dataset["Genre"].append(genre)
            dataset["Lyrics"].append(lyrics)
            dataset["SimilarSongs"].append(similar_songs)
            
    except:
        pass
    
    if i % 5000 == 0:
        print(i)
        
df2 = pd.DataFrame(dataset)
df2.to_csv("/TDI Capstone Project/Retrieved Data/AZLyrics/Extracted Lyrics.csv", index=False)

#Drop rows with missing value for lyrics:

df3 = pd.read_csv("/TDI Capstone Project/Retrieved Data/AZLyrics/Extracted Lyrics.csv")
df3 = df3.dropna(subset = ['Lyrics'])

#Remove bad unicode charachters from lyrics bodies:

RE_BAD_CHARS = re.compile('\x00|\x01|\x02|\x03|\x04|\x05|\x06|\x07|\x08|\x0b|\x0e|\x0f|\x10|\x11|\x12|\x13|\x14|\x15|\x16|\x17|\x18|\x19|\x1a|\x1b|\x1c|\x1d|\x1e|\x1f|\x7f|\x80|\x81|\x82|\x83|\x84|\x85|\x86|\x87|\x88|\x89|\x8a|\x8b|\x8c|\x8d|\x8e|\x8f|\x90|\x91|\x92|\x93|\x94|\x95|\x96|\x97|\x98|\x99|\x9a|\x9b|\x9c|\x9d|\x9e|\x9f+')


def remove_bad_chars(text):
    return RE_BAD_CHARS.sub("", text)


#Flag songs with all english lyrics:

def is_lyrics_english(row):
    
    text_content = remove_bad_chars(row['Lyrics'])

    detected_language = cld2.detect(text_content)

    if detected_language[2][0][0] == 'ENGLISH' and detected_language[2][1][0] == 'Unknown' and detected_language[2][2][0] == 'Unknown':
        return 1
    
    else:
        return 0
        

df3['IsEnglish'] = df3.apply(is_lyrics_english, axis=1)

df4 = df3.query('IsEnglish == 1')

df4 = df4.drop(['IsEnglish'], axis=1)

df4.to_csv("/TDI Capstone Project/Retrieved Data/AZLyrics/Extracted Lyrics-English Only-Bad Characters Removed-Quotations Extra Spaces Removed-Indexed.csv", index_label='Row_Index')


