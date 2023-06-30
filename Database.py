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
    
