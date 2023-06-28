import sys
import sqlalchemy
import os



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
        AND df."Year" IS NOT NULL
        ORDER BY df."Year" DESC;
    """)

    results = conn.execute(query, {'keyword': f'%{keyword.lower()}%'})
    
    return results.fetchall()

if __name__ == '__main__':
    
    kw = str(input("Search Term:"))
    
    print(kw_search(kw))
    
