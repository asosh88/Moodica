import streamlit as st
import Database
import Display
import pandas as pd

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
        

        if keyword != '':
            
            #sort_asc_dict = {'Ascending': True, 'Descending': False}
            
            results = pd.DataFrame(Database.kw_search(keyword, search_type))
            
            if sort_by == 'Artist' and sort_asc == 'Ascending':
                results = results.sort_values(by=['Artist'], ascending=True)
            elif sort_by == 'Artist' and sort_asc == 'Descending' :
                results = results.sort_values(by=['Artist'], ascending=False)
            elif sort_by == 'Album' and sort_asc == 'Ascending':
                results = results.sort_values(by=['Album'], ascending=True)
            elif sort_by == 'Album' and sort_asc == 'Descending':
                results = results.sort_values(by=['Album'], ascending=False)
            elif sort_by == 'Year' and sort_asc == 'Ascending':
                results = results.sort_values(by=['Year'], ascending=True)
            elif sort_by == 'Year' and sort_asc == 'Descending':
                results = results.sort_values(by=['Year'], ascending=False)
            
            results = results.reset_index(drop=True)
            
            
            results_num = len(results['SongName'])
            
            field = {'Artists': 'Artist(s)', 'Albums': 'Album Names', 'Songs': 'Song Names', 'Lyrics': 'Song Lyrics', 'Credits': 'Song Credits'}
            
            st.write('\n\n')
            st.write(f'Showing {results_num} Results for "{keyword}" in {field[search_type]}:')
            st.title('\n\n')

            for i in range(len(results['SongName'])):
                
                songname = results['SongName'][i]
                artist = results['Artist'][i]
                
                st.markdown(f'**{i+1}. {songname}** | {artist}')
                
                if results['Year'][i] != None:
                    yr = str(results['Year'][i])[:-2]
                    album = results['Album'][i]
                    st.markdown(f'Album: *{album} ({yr})*')
                    st.markdown('\n\n')
    
    if service_type == 'Recommendation':
        recommendation_type = st.radio(
        'Search for A:',
        ('Song', 'Playlist'),
        horizontal=True
        )
            

        
if __name__ == '__main__':
    app()