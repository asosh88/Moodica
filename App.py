import streamlit as st
import Database
import Display
import pandas as pd
from urllib.parse import unquote, quote
from streamlit_tags import st_tags, st_tags_sidebar
import re

def init():
    
    artists_list = Database.get_artists()

    artists = list()
    
    for artist in artists_list:
        artists.append(re.sub(r"\(|\)|'|,", '', str(artist)))
        
    st.session_state['artists_'] = artists
            

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
                        
                                            
                    
                    st.markdown('\n\n')
                        
            else:
                st.write(f'No Results Found with "{keyword}" in {field[search_type]}.')
                
    
    if st.session_state['service_type'] == 'Recommendation':
        
        st.write('**Search for Songs with Similar Lyrics**')
        st.write('\n\n')
        
        artists = st.session_state['artists_']
        
        artists_ = st_tags(
        label='Artist(s):',
        text='Enter Up to 5 Bands or Artists',
        suggestions=artists,
        maxtags = 5,
        key='1')
        
        #song_list = Database.get_songs(str(artist_))
        
        try:
            song_list = Database.get_songs(artists_)
            
            #st.write(artists_)
            
            song_list = pd.DataFrame(song_list)
                        
            artists_picked = len(artists_)
            
            if artists_picked >= 1:
                artist_names = ""
                for a in artists_:
                    artist_names += f'{a}, '
                    
                artist_names = artist_names[:-2]
                artist_names = " and ".join(artist_names.rsplit(', ', 1))
                
            if artists_picked > 0:
                
                st.write(f'{len(song_list)} Songs Available from {artist_names}')
                
                song_names = list(song_list['SongName'])
            
                songs_ = st_tags(
                label='Song(s):',
                text='Enter Up to 10 Songs',
                suggestions=song_names,
                maxtags = 5,
                key='2')
                                
                if len(songs_) > 0:
                    
                    selected_songs = song_list.loc[song_list['SongName'].isin(songs_)]
                    
                    picked_songs_desc = ""

                    for s in songs_:
                        picked_songs_desc += f'"{s}", '

                    picked_songs_desc = 'You Have Selected ' + picked_songs_desc[:-2]
                    picked_songs_desc = ' and '.join(picked_songs_desc.rsplit(', ', 1))

                    st.write(picked_songs_desc)

                    st.dataframe(selected_songs)
                    
                    st.write(list(selected_songs['Row_Index']))
                    
                    #st.write(songs_)                
                
                #st.dataframe(song_list)
                
                    
        except:
            pass
        
        try:
            if len(songs_) > 0:
                song_artist_list = st.session_state['selected_songs']
                st.write(f'You Have Selected {song_artist_list}')
            
        except:
            pass
        
        #for artist in artists:
        #    st.write(str(artist))

            
if __name__ == '__main__':
    init()
    app()