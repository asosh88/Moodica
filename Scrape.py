#Scrape azlyrics.com
import requests
from time import sleep
import os
import random
import re
from string import ascii_lowercase as alphabet
from bs4 import BeautifulSoup as bs
import concurrent.futures
from concurrent.futures import as_completed
from concurrent.futures import TimeoutError
import pandas
from datetime import datetime
from time import sleep
from fp.fp import FreeProxy
from latest_user_agents import get_latest_user_agents, get_random_user_agent

#Scrape A-Z pages with artist/band names/links:
os.chdir('/TDI Capstone Project/Retrieved Data/AZLyrics/')

for l in alphabet:
    url = f"https://www.azlyrics.com/{l}.html"
    file_name = f"azlyrics-{l}.html"
    
    try:
        page = requests.get(url, allow_redirects=True)
        sleep(random.uniform(6, 10))
        open(file_name, 'wb').write(page.content)
        print(f"https://www.azlyrics.com/{l}.html downloaded.")
        
    except:
        pass


#Extract artist URLs from pages stored right above:
os.chdir('/TDI Capstone Project/Retrieved Data/AZLyrics/')

artists_table = {'artists_names':[], 'artists_urls':[]}

string = ""

for l in alphabet:
    string = string + f"{l} "
    
string = string + "19"

c = 0 # counter

for l in string.split(" "):    

    file_name = f"azlyrics-{l}.html"
    page = open(file_name, 'r').read()

    artists = re.findall(r'<a href=".*</a><br>', page)
        
    for artist in artists:
        
        c += 1

        artist_name = re.findall(r'>.*</a>', artist)[0]
        artist_name = artist_name[1:-4]
        artists_table['artists_names'].append(artist_name)

        artist_url = re.findall(r'".*"', artist)[0]
        artist_url = artist_url.replace('"', '')
        artists_table['artists_urls'].append(artist_url)
        
        if c % 100 == 0:
            print(f"{c} Artists Exctracted.")


# Create Pandas Dataframe
df = pandas.DataFrame(artists_table)

# Write Dataframe to File
df.to_csv("AZLyrics-Artists.csv", index=False)


#Find and store each artist/band's page containing links their songs:
def shortener(row):
    
    shortname = row["artists_urls"]
    shortname = shortname[shortname.find("/") + 1:]
    return shortname

os.chdir('/TDI Capstone Project/Retrieved Data/AZLyrics/')
df = pandas.read_csv("AZLyrics-Artists.csv")
df["shortname"] = df.apply(lambda row: shortener(row), axis=1)

os.chdir('/TDI Capstone Project/Retrieved Data/AZLyrics/Artists Pages/')
for c in range(14000, 19434):
    
    url = f"https://www.azlyrics.com/" + df["artists_urls"][c]
    file_name = df["shortname"][c]
    
    try:

        page = requests.get(url, allow_redirects=True)
        sleep(random.uniform(3, 7))
        open(file_name, 'wb').write(page.content)
                            
        if c % 150 == 0:
            print(f"Pages of {c} Artists Downloaded.")
            sleep(random.uniform(30, 60))
        
    except:
        pass

    
#Extract and store all song lyric links for all available artists:
songs_table = {'songs_names':[], 'songs_urls':[], 'save_as':[]}

os.chdir('/TDI Capstone Project/Retrieved Data/AZLyrics/')
df_artists = pandas.read_csv("AZLyrics-Artists.csv")

os.chdir('/TDI Capstone Project/Retrieved Data/AZLyrics/Artists Pages/')

for i in range(len(df_artists)):
    
    try:
        file_name = df_artists["artists_urls"][i]
        file_name = file_name = file_name[file_name.find("/")+1:]
        page = open(file_name, 'r').read()

        bs_obj = bs(page, 'html.parser')
        albums = bs_obj.find_all(class_="album")

        songs = bs_obj.find_all(class_="listalbum-item")

        for song in songs:
            if song.a:        
                url = song.a["href"]
                url = url.replace("https://www.azlyrics.com", "")
                save_as = url.replace("/lyrics/", "")
                save_as = save_as.replace("/", "_")
                song_name = song.a.text

                songs_table['songs_names'].append(song_name)
                songs_table['songs_urls'].append(url)
                songs_table['save_as'].append(save_as)
    except:
        pass
            
    if i % 150 == 0:
        print(f"{i} Artists Processed...")
        
df_songs = pandas.DataFrame(songs_table)

df = df_songs

print(f"Number of All Extracted Song Links from AZ Artist Pages: {len(df)}")

df = df.drop_duplicates(subset=['songs_urls'])

df = df.reset_index(drop=True)

print(f"Number of Song Links After Dropping Duplicate Songs: {len(df)}")

path = '/TDI Capstone Project/Retrieved Data/AZLyrics/Songs Pages/'
os.chdir(path)

for c in range(len(df)):
    
    save_as = df["save_as"][c]
    file_name = path + save_as
    
    if os.path.exists(file_name):
        df = df.drop([c])
        
        
df = df.reset_index(drop=True)

print("Number of Pages Still to Be Downloaded:", len(df))


#Extract and store artists_urls:
songs_table = {'songs_names':[], 'songs_urls':[], 'save_as':[]}

os.chdir('/TDI Capstone Project/Retrieved Data/AZLyrics/')
df_artists = pandas.read_csv("AZLyrics-Artists.csv")

os.chdir('/TDI Capstone Project/Retrieved Data/AZLyrics/Artists Pages/')
    
def songs_extraction(row):
    os.chdir('/TDI Capstone Project/Retrieved Data/AZLyrics/Artists Pages/')
    try:
        file_name = row["artists_urls"]
        file_name = file_name[file_name.find("/")+1:]
        page = open(file_name, 'r').read()

        bs_obj = bs(page, 'html.parser')
        albums = bs_obj.find_all(class_="album")

        songs = bs_obj.find_all(class_="listalbum-item")

        for song in songs:
            if song.a:        
                url = song.a["href"]
                url = url.replace("https://www.azlyrics.com", "")
                save_as = url.replace("/lyrics/", "")
                save_as = save_as.replace("/", "_")
                song_name = song.a.text

                songs_table['songs_names'].append(song_name)
                songs_table['songs_urls'].append(url)
                songs_table['save_as'].append(save_as)

    except:
        pass


df_artists.apply(lambda row: songs_extraction(row), axis=1)

df_songs = pandas.DataFrame(songs_table)

df = df_songs

print(f"Number of All Extracted Song Links from AZ Artist Pages: {len(df)}")

df = df.drop_duplicates(subset=['songs_urls'])

df = df.reset_index(drop=True)

print(f"Number of Song Links After Dropping Duplicate Songs: {len(df)}")


#Final AZLyrics Scraping Code:
def file_exists(row):
    
    path = '/TDI Capstone Project/Retrieved Data/AZLyrics/Songs Pages/'
    save_as = row["save_as"]
    file_name = path + save_as
    if os.path.exists(file_name):
        return 1
    else:
        return 0

    
def scraper(rows, proxy):
    
    proxy = proxy.replace("http://", "")
    proxy = proxy.replace("https://", "")

    proxies = {
       'http': f'{proxy}',
       'https': f'{proxy}',
    }

    bad_ip = "Our systems have detected unusual activity from your IP address"

    access_denied = "Access denied."

    proxy_fail = 0

    headers = {'User-Agent': get_random_user_agent()}
    
    for i in rows:

        page = ""
        
        try:
            c = i[0]
            url = "https://www.azlyrics.com" + str(df["songs_urls"][c])
            save_as = df["save_as"][c]
            file_name = path + save_as
            page = requests.get(url, allow_redirects=True, proxies=proxies, headers=headers, timeout=14)
            sleep(random.uniform(3, 6))

            if bad_ip not in str(page.content) and access_denied not in str(page.content) and page != "":
                with open(save_as, 'wb') as f:
                    f.write(page.content)
            else:
                proxy_fail += 1

            if proxy_fail >= 3:
                print("|", end="")
                break 
            
        except:
            pass

df = pandas.read_csv("/TDI Capstone Project/Retrieved Data/AZLyrics/AZLyrics-Songs.csv")

print(f"Number of Files on The List At Present: {len(df)}")

df = df.drop_duplicates(subset=['songs_urls'])

df = df.reset_index(drop=True)

print(f"Number of Song Links After Dropping Duplicates: {len(df)}")

path = '/TDI Capstone Project/Retrieved Data/AZLyrics/Songs Pages/'
os.chdir(path)

counter = 0

while True:
    
    counter += 1
    
    #Delete songs already processed from the list of songs to download:
    df["Exists"] = df.apply(lambda row: file_exists(row), axis=1)

    df = df[df["Exists"] == 0]

    df = df.drop(['Exists'], axis=1)
    
    df = df.reset_index(drop=True)
    
    print(f"Total Number of Pages Still Required to Download: {len(df)}")

    path = '/TDI Capstone Project/Retrieved Data/AZLyrics/Songs Pages/'
    os.chdir(path)

    series = [[i] for i in range(int(len(df) / 18))]
    random.shuffle(series)
    
    dl_chunk = 52000
    
    if len(series) > dl_chunk:
        series = series[:dl_chunk - 1]


    print(f"{counter} ({datetime.today().strftime('%H:%M:%S')}) - Number of Pages to Download This Round:", dl_chunk)
    
    proxy_list = FreeProxy(rand=True).get_proxy_list(repeat=True)
    
    proxy_num = len(proxy_list)

    print(f"Number of Proxies Available: {len(proxy_list)}")

    slice_ = 180
    
    print(f"Load per Thread: {slice_} Pages")

    rows = []

    for j in range(len(proxy_list)):
        rows.append(series[:slice_])
        series = series[slice_+1:]

    threads_num = len(proxy_list)
    
    futures = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads_num) as executor:
        for i, proxy in enumerate(proxy_list):
            futures.append(executor.submit(scraper, rows[i], proxy))
            
    sleepy = random.randint(120, 480)
    
    minutes = int(sleepy / 60)
    
    if minutes <= 1:
        min_str = f"{minutes} minute"
    else:
        min_str = f"{minutes} minutes"
        
    seconds = sleepy % 60
    
    if seconds <= 1:
        sec_str = f"{seconds} second"
    else:
        sec_str = f"{seconds} seconds"
        
    print(" ")
    
    print(f"{counter} ({datetime.today().strftime('%H:%M:%S')})- Finished all download tasks. Pausing for {min_str} and {sec_str}.")
    
    sleep(sleepy)

