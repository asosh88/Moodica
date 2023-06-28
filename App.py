import streamlit as st
import Database
import Display
import pandas as pd
from urllib.parse import unquote, quote

def app():
    
    st.title('Welcome to Moodica!')
    st.markdown('*Music Search & Recommendation*')
    
    service_type = st.sidebar.radio(
    'Service Type:',
    ('Search', 'Recommendation')
    )
    
    sort_by = st.sidebar.radio(
    'Sort by:',
    ('Artist', 'Album', 'Year'),
    index=2
    )
    
    sort_asc = st.sidebar.radio(
    'Sort:',
    ('Ascending', 'Descending'),
    index=1
    )
    
    if service_type == 'Search':
        search_type = st.radio(
        'Search for:',
        ('Artists', 'Albums', 'Songs', 'Lyrics', 'Credits'),
        horizontal=True,
        index=3
        )
    
        keyword = st.text_input('Keywords:')        

        field = {'Artists': 'Artist Name', 'Albums': 'Album Name', 'Songs': 'Song Name', 'Lyrics': 'Song Lyrics', 'Credits': 'Song Credits'}
        sort_asc_dict = {'Ascending': True, 'Descending': False}
        
        if keyword != '':
            results = pd.DataFrame(Database.kw_search(keyword, search_type))
            if len(results) > 0:
                results = results.sort_values(by=[sort_by], ascending=sort_asc_dict[sort_asc], axis=0)            
                results = results.reset_index(drop=True)                        
                results_num = len(results['SongName'])

                st.write('\n\n')
                st.write(f'Showing {results_num} Results with "{keyword}" in {field[search_type]}:')
                st.title('\n\n')

                for i in range(len(results['SongName'])):                
                    songname = results['SongName'][i]
                    artist = results['Artist'][i]
                    st.markdown(f'**{i+1}. {songname}** | {artist}')

                    if results['Year'][i] != None:
                        yr = str(results['Year'][i])[:-2]
                        album = results['Album'][i]
                        st.markdown(f'Album: *{album} ({yr})*')
                        
                        
                    st.button('*Similar Songs*', key=i, help=f'Find Songs with Lyrics Similar to Those of "{songname}" by {artist}')
                    st.markdown('\n\n')
                        
            else:
                st.write(f'No Results Found with "{keyword}" in {field[search_type]}.')
                
    
    if service_type == 'Recommendation':
        recommendation_type = st.radio(
        'Search for Similar Songs Using:',
        ('Song', 'Playlist'),
        horizontal=True
        )
            
if __name__ == '__main__':
    app()