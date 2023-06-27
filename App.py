import streamlit as st
import Database
import Display

def app():
    
    st.title('Welcome to Moodica!')
    st.markdown('*Music Search & Recommendation*')
    
    service_type = st.radio(
    'Service Type:',
    ('Search', 'Recommendation')
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
            
            results = Database.kw_search(keyword, search_type)
            
            results_num = len(results)
            
            st.write('\n\n')
            st.write(f'Showing {results_num} Results for "{keyword}":')

            for i, r in enumerate(results):
                st.markdown(f'**{i+1}. {r[0]}** | {r[1]}')
                yr = str(r[3])[:-2]
                st.markdown(f'Album: *{r[2]} ({yr})*')
                st.markdown('\n\n')
    
    if service_type == 'Recommendation':
        recommendation_type = st.radio(
        'Search for A:',
        ('Song', 'Playlist'),
        horizontal=True
        )

        
if __name__ == '__main__':
    app()