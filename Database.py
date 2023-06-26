import sys
import sqlalchemy
import os

conn_addy = os.getenv('DB_URL')

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