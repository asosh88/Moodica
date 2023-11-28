import streamlit as st
import Database
import Plotting
import matplotlib.pyplot as plt
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
            

def app(state=2):
    
    st.title('Welcome to Moodica!')
    st.markdown('*Music Search & Recommendation*')
    
    
    service_type =  st.sidebar.radio(
    'Service Type:',
    ('Search', 'Recommendation', 'Visualization'),
    index=state,
    )
    
    st.session_state['service_type'] = service_type
        
    if st.session_state['service_type'] == 'Search':
        
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
                
                for i in range(len(results['SongName'])):                
                    songname = results['SongName'][i]
                    artist = results['Artist'][i]
                    row_index = results['Row_Index'][i]
                    url = results['SongHandle'][i]
                    url = url.replace('_', '/')
                    url = 'https://www.azlyrics.com/lyrics/' + url
                    st.markdown(f'{i+1}. [{songname}](%s) | {artist}' % url )

                    if results['Album'][i] != None:
                        yr = str(results['Year'][i])[:-2]
                        album = results['Album'][i]
                        st.markdown(f'Album: *{album} ({yr})*')
                    
                    st.markdown('\n\n')
                        
            else:
                st.write(f'No Results Found with "{keyword}" in {field[search_type]}.')
                
    
    elif st.session_state['service_type'] == 'Recommendation':
        st.write('**Search for Songs with Similar Lyrics**')
        st.write('\n\n')
        
        artists = st.session_state['artists_']
        artists_ = st_tags(
        label='Artist(s):',
        text='Enter Up to 5 Bands or Artists',
        suggestions=artists,
        maxtags = 5,
        key='1')
                
        try:
            song_list = Database.get_songs(artists_)
                        
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

                    picked_songs_desc = 'Searching for Songs Similar to ' + picked_songs_desc[:-2] + '...'
                    picked_songs_desc = ' and '.join(picked_songs_desc.rsplit(', ', 1))

                    st.write(picked_songs_desc)
                    
                    st.markdown('\n\n')
                                                            
                    similar_songs_ = Database.get_similar_songs(list(selected_songs['Row_Index']))

                    similar_songs_ = pd.DataFrame(similar_songs_)

                    row_counter = 0
                    for k in range(len(similar_songs_['SongName'])):                
                        songname_rec = similar_songs_['SongName'][k]
                        artist_rec = similar_songs_['Artist'][k]
                        row_counter += 1
                        
                        if k % 51 == 0:
                            if k > 0:
                                st.divider()
                                
                            st.markdown(f'Songs with Lyrics Similar to **{songname_rec}** by {artist_rec}:')
                            st.markdown('\n\n')
                            
                            row_counter = 0
                                
                        else:
                            url = results['SongHandle'][k]
                            url = url.replace('_', '/')
                            url = 'https://www.azlyrics.com/lyrics/' + url
                            st.markdown(f'{row_counter}. [{songname_rec}](%s) | {artist_rec}' % url)

                            if similar_songs_['Album'][k] != None:
                                yr_rec = str(similar_songs_['Year'][k])[:-2]
                                album_rec = similar_songs_['Album'][k]
                                st.markdown(f'Album: *{album_rec} ({yr_rec})*')

                            st.markdown('\n\n')
                    
        except:
            pass
        
    elif st.session_state['service_type'] == 'Visualization':
        st.write("**Visualize WordCloud of Artist/Band's Discography**")
        st.write('\n\n')
        
        artists = st.session_state['artists_']
        artists_ = st_tags(
        label='Artist(s):',
        text="Enter A Band or Artist's Name",
        suggestions=artists,
        maxtags = 1,
        key='3')
                
        try:

            artists_picked = len(artists_)

            if artists_picked >= 1:
                song_list = Database.get_songs(artists_)
                song_list = pd.DataFrame(song_list)

                artist_names = ""

                for a in artists_:
                    artist_names += f'{a}, '

                artist_names = artist_names[:-2]
                artist_names = " and ".join(artist_names.rsplit(', ', 1))

            if artists_picked > 0:
                st.write(f'Showing Word-Cloud for {len(song_list)} Songs by {artist_names}')

                lc = str(Database.get_lyrics(list(artists_)))

                pl = Plotting.word_cloud(lc)

                fig, ax = plt.subplots()
                ax.imshow(pl, interpolation="bilinear")
                plt.axis('off')
                st.pyplot(fig)
                
                
        except:
            pass
        
if __name__ == '__main__':
    init()
    app()