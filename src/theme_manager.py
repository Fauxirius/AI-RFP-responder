import streamlit as st

class ThemeManager:
    def __init__(self):
        pass

    def initialize_theme(self):
        if 'theme' not in st.session_state:
            st.session_state['theme'] = 'light'

    def set_theme(self, theme):
        if theme in ['light', 'dark']:
            st.session_state['theme'] = theme

    def toggle_theme(self):
        if 'theme' in st.session_state:
            if st.session_state['theme'] == 'light':
                st.session_state['theme'] = 'dark'
            else:
                st.session_state['theme'] = 'light'
