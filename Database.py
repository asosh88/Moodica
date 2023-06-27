import sys
import sqlalchemy
import os



def kw_search(keyword, field):
    
    conn_addy = os.getenv('DB_URL')
    
    engine = sqlalchemy.create_engine(conn_addy)

    conn = engine.connect()
    
    match field:
        case 'Artists':
            query = sqlalchemy.text(f"""
            SELECT df."SongName", df."Artist", df."Album", df."Year"
            FROM df
            WHERE df."Artist" LIKE :keyword
            AND df."Year" IS NOT NULL
            ORDER BY df."Year" DESC;
            """)

            
        case 'Albums':
            query = sqlalchemy.text(f"""
            SELECT df."SongName", df."Artist", df."Album", df."Year"
            FROM df
            WHERE df."Album" LIKE :keyword
            AND df."Year" IS NOT NULL
            ORDER BY df."Year" DESC;
            """)
            
        case 'Songs':
            query = sqlalchemy.text(f"""
            SELECT df."SongName", df."Artist", df."Album", df."Year"
            FROM df
            WHERE df."SongName" LIKE :keyword
            AND df."Year" IS NOT NULL
            ORDER BY df."Year" DESC;
            """)
            
        case 'Lyrics':
            query = sqlalchemy.text(f"""
            SELECT df."SongName", df."Artist", df."Album", df."Year"
            FROM df
            WHERE df."Lyrics" LIKE :keyword
            AND df."Year" IS NOT NULL
            ORDER BY df."Year" DESC;
            """)
            
    
        case 'Credits':
            query = sqlalchemy.text(f"""
            SELECT df."SongName", df."Artist", df."Album", df."Year"
            FROM df
            WHERE df."Credits" LIKE :keyword
            AND df."Year" IS NOT NULL
            ORDER BY df."Year" DESC;
            """)

            
    results = conn.execute(query, {'field': f'"{field}"', 'keyword': f'%{keyword}%'})
    
    return results.fetchall()

if __name__ == '__main__':
    
    kw = str(input("Search Term:"))
    
    print(kw_search(kw))
    
