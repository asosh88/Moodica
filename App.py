import streamlit as st
import Database
import Display

def app():
    
    st.title('Welcome to Moodica!')
    st.markdown('*Music Search & Recommendation*')
    
    
    keyword = st.text_input('Keywords:')
    
    if keyword != '':
        st.write('\n\n')
        st.write(f'Showing Results for "{keyword}":')
    
        for i, r in enumerate(Database.kw_search(keyword)):
            st.markdown(f'**{i+1}. {r[0]}** | {r[1]}')
            yr = str(r[3])[:-2]
            st.markdown(f'Album: *{r[2]} ({yr})*')
            st.markdown('\n\n')
    
    
if __name__ == '__main__':
    app()