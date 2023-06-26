import sys
import sqlalchemy
from urllib.parse import quote

conn_addy = "postgresql://edb_admin:%s@p-r8xgmomuzb.pg.biganimal.io:5432/edb_admin" % quote('http://hY5-C67*_frEs@m0/#23!')

def kw_search(keyword):
    
    engine = sqlalchemy.create_engine(conn_addy)

    conn = engine.connect()

    query = sqlalchemy.text(f"""
    SELECT df."SongName", df."Artist", df."Album", df."Year"
    FROM df
    WHERE df."Lyrics" LIKE :keyword
    ORDER BY df."Year" DESC;
    """)

    results = conn.execute(query, {'keyword': f'%{keyword}%'})
    
    return results.fetchall()

if __name__ == '__main__':
    
    kw = str(input("Search Term:"))
    
    print(kw_search(kw))
    
#Woody Allen