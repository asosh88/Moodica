import os
import pandas as pd

os.environ['DB_URL'] = "postgresql://edb_admin:http%3A//hY5-C67%2A_frEs%40m0/%2323%21@p-r8xgmomuzb.pg.biganimal.io:5432/edb_admin"

import Database

def disp(kw):
    
    data = Database.kw_search(kw)

    return pd.DataFrame(data)
    
    