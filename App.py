import streamlit as st
import Database
import Display
import pandas as pd
from urllib.parse import unquote, quote
from streamlit_tags import st_tags, st_tags_sidebar
import re


def on_click():
    st.session_state['service_type'] = 'Recommendation'

def app(state=0):
    
    st.title('Welcome to Moodica!')
    st.markdown('*Music Search & Recommendation*')
    
    #service_type_options = 
    
    service_type =  st.sidebar.radio(
    'Service Type:',
    ('Search', 'Recommendation'),
    index=state,
    #key='service_type'
    )
    
    st.session_state['service_type'] = service_type
    
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
    
    
    if st.session_state['service_type'] == 'Search':
        search_type = st.radio(
        'Search for:',
        ('Artists', 'Albums', 'Songs', 'Lyrics', 'Credits'),
        horizontal=True,
        index=3
        )
    
        placeholder = st.empty()
        
        keyword = placeholder.text_input('Keywords:', placeholder='Type your keywords here.')        

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

                buttons = list()
                
                for i in range(len(results['SongName'])):                
                    songname = results['SongName'][i]
                    artist = results['Artist'][i]
                    row_index = results['Row_Index'][i]
                    st.markdown(f'**{i+1}. {songname}** | {artist}')

                    if results['Year'][i] != None:
                        yr = str(results['Year'][i])[:-2]
                        album = results['Album'][i]
                        st.markdown(f'Album: *{album} ({yr})*')
                        
                        
                    st.button('*Similar Songs*', key=i, help=f'Find Songs with Lyrics Similar to Those of "{songname}" by {artist}', on_click=on_click())
                    
                    
                    st.markdown('\n\n')
                        
            else:
                st.write(f'No Results Found with "{keyword}" in {field[search_type]}.')
                
    
    if st.session_state['service_type'] == 'Recommendation':
        
        st.write('**Search for Similar Songs**')
        st.write('\n\n')
        
        artists_list = Database.get_all_songs()
        
        artists = list()
        for artist in artists_list:
            artists.append(re.sub(r"\(|\)|'|,", '', str(artist[0] + ' BY ' + str(artist[1]))))
            
        artist_ = st_tags(
        label='Song(s):',
        text='Enter A Song Name...',
        suggestions=artists,
        maxtags = 10,
        key='1')
        
        #song_list = Database.get_songs(str(artist_))
        
        try:
            song_list = Database.get_songs(str(artist_[0]))
            
            
            songs = list()
            for song in song_list:
                songs.append(song)

                st.write(song[1])
        
        except:
            pass
        
        
        #for artist in artists:
        #    st.write(str(artist))

            
if __name__ == '__main__':
    app()