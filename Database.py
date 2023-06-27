import sys
import sqlalchemy
import os



def kw_search(keyword, field):
    
    #conn_addy = os.getenv('DB_URL')
    
    conn_addy = 'postgresql://edb_admin:http%3A//hY5-C67%2A_frEs%40m0/%2323%21@p-r8xgmomuzb.pg.biganimal.io:5432/edb_admin'
    
    engine = sqlalchemy.create_engine(conn_addy)

    conn = engine.connect()
    
    if field == 'Artists':
        query = sqlalchemy.text(f"""
        SELECT df."SongName", df."Artist", df."Album", df."Year"
        FROM df
        WHERE df."Artist" LIKE :keyword
        ORDER BY df."Year" DESC;
        """)


    if field == 'Albums':
        query = sqlalchemy.text(f"""
        SELECT df."SongName", df."Artist", df."Album", df."Year"
        FROM df
        WHERE df."Album" LIKE :keyword
        ORDER BY df."Year" DESC;
        """)

    if field == 'Songs':
        query = sqlalchemy.text(f"""
        SELECT df."SongName", df."Artist", df."Album", df."Year"
        FROM df
        WHERE df."SongName" LIKE :keyword
        ORDER BY df."Year" DESC;
        """)

    if field == 'Lyrics':
        query = sqlalchemy.text(f"""
        SELECT df."SongName", df."Artist", df."Album", df."Year"
        FROM df
        WHERE df."Lyrics" LIKE :keyword
        ORDER BY df."Year" DESC;
        """)


    if field == 'Credits':
        query = sqlalchemy.text(f"""
        SELECT df."SongName", df."Artist", df."Album", df."Year"
        FROM df
        WHERE df."Credits" LIKE :keyword
        ORDER BY df."Year" DESC;
        """)

            
    results = conn.execute(query, {'field': f'"{field}"', 'keyword': f'%{keyword}%'})
    
    return results.fetchall()

if __name__ == '__main__':
    
    kw = str(input("Search Term:"))
    
    print(kw_search(kw))
    
