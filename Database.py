import sys
import sqlalchemy
import os

def get_all_songs():
    
    conn_addy = 'postgresql://edb_admin:6H4BqmoA26ge!byY1@p-r8xgmu1bk5.pg.biganimal.io:5432/edb_admin'
    
    engine = sqlalchemy.create_engine(conn_addy)

    conn = engine.connect()
    
    query = sqlalchemy.text(f"""
        SELECT
            df."SongName",
            df."Artist"
            FROM df;
    """)

    songs = conn.execute(query)
    
    return songs.fetchall()
    

def get_similar_songs(source_songs):
    
    conn_addy = 'postgresql://edb_admin:6H4BqmoA26ge!byY1@p-r8xgmu1bk5.pg.biganimal.io:5432/edb_admin'
    
    engine = sqlalchemy.create_engine(conn_addy)

    conn = engine.connect()
    
    song_list = ""
    
    for s in source_songs:
        song_list += f"{s}, "
        
    song_list = song_list[:-2]
    
    song_list = f"({song_list})"

    query = sqlalchemy.text(f"""
        SELECT *
            FROM similar_songs
            WHERE similar_songs."Row_Index" IN {song_list};
    """)

    similar_songs = conn.execute(query)
    
    results = list()
    table = list()
    
    for sim_son in similar_songs:
        
        #results = list()
        
        for so in sim_son:
        
            #results.append(so)
            
            #results = str(tuple(results))
            
            query = sqlalchemy.text(f"""
                SELECT
                    df."Row_Index",
                    df."SongName", 
                    df."Artist", 
                    df."Album", 
                    df."Year"
                    FROM df
                    WHERE df."Row_Index" = {so};
            """)
            
            #results.append(so)
        
            similar_songs_ = conn.execute(query)
            similar_songs_ = similar_songs_.fetchall()
            table.append(similar_songs_[0])
    
    
    return table
    

def get_songs(artist):
        
    conn_addy = 'postgresql://edb_admin:6H4BqmoA26ge!byY1@p-r8xgmu1bk5.pg.biganimal.io:5432/edb_admin'
    
    
    engine = sqlalchemy.create_engine(conn_addy)

    conn = engine.connect()
    
    artist_list = ""
    
    for a in artist:
        artist_list += f"'{a}', "
        
    artist_list = artist_list[:-2]
    
    artist_list = f"({artist_list})"
    
    
    query = sqlalchemy.text(f"""
        SELECT
            df."Row_Index",
            df."Artist",
            df."SongName"
            FROM df
            WHERE df."Artist" IN {artist_list};
    """)
        
    songs = conn.execute(query)
    
    return songs.fetchall()


def get_lyrics(artist):
        
    conn_addy = 'postgresql://edb_admin:6H4BqmoA26ge!byY1@p-r8xgmu1bk5.pg.biganimal.io:5432/edb_admin'
    
    
    engine = sqlalchemy.create_engine(conn_addy)

    conn = engine.connect()
        
    artist_list = ""
    
    for a in artist:
        artist_list += f"'{a}', "
        
    artist_list = artist_list[:-2]
    
    artist_list = f"({artist_list})"
    
    
    query = sqlalchemy.text(f"""
        SELECT
            STRING_AGG(df."Lyrics", ' ')
            FROM df
            WHERE df."Artist" IN {artist_list};
    """)
        
    lrc = conn.execute(query)
    
    return  (' '.join((lrc.fetchall()[0]))
                .replace('\n', ' '))



def get_artists():
    
    conn_addy = 'postgresql://edb_admin:6H4BqmoA26ge!byY1@p-r8xgmu1bk5.pg.biganimal.io:5432/edb_admin'
    
    
    engine = sqlalchemy.create_engine(conn_addy)

    conn = engine.connect()
    
    query = sqlalchemy.text(f"""
        SELECT
            DISTINCT(df."Artist")
            FROM df
            GROUP BY df."Artist";
    """)

    artists = conn.execute(query)
    
    return artists.fetchall()

def kw_search(keyword, field):
    
    #conn_addy = os.getenv('DB_URL')
    
    #conn_addy = 'postgresql://edb_admin:http%3A//hY5-C67%2A_frEs%40m0/%2323%21@p-r8xgmomuzb.pg.biganimal.io:5432/edb_admin'
    
    conn_addy = 'postgresql://edb_admin:6H4BqmoA26ge!byY1@p-r8xgmu1bk5.pg.biganimal.io:5432/edb_admin'
    
    
    engine = sqlalchemy.create_engine(conn_addy)

    conn = engine.connect()
    
    fields = {
        'Artists': 'Artist',
        'Albums': 'Album',
        'Songs': 'SongName',
        'Lyrics': 'Lyrics',
        'Credits': 'Credits'
    }

    query = sqlalchemy.text(f"""
        SELECT
            df."Row_Index",
            df."SongName", 
            df."Artist", 
            df."Album", 
            df."Year"
            FROM df
        WHERE LOWER(df."{fields[field]}") LIKE :keyword
        ORDER BY df."Year" DESC;
    """)

    results = conn.execute(query, {'keyword': f'%{keyword.lower()}%'})
    
    return results.fetchall()

if __name__ == '__main__':
    
    kw = str(input("Search Term:"))
    
    print(kw_search(kw))
    
