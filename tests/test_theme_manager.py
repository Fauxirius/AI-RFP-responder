import unittest
from unittest.mock import MagicMock, patch
import streamlit as st
from src.theme_manager import ThemeManager

class TestThemeManager(unittest.TestCase):
    def setUp(self):
        # Mock streamlit session state
        self.patcher = patch('streamlit.session_state', {})
        self.mock_session_state = self.patcher.start()
        
    def tearDown(self):
        self.patcher.stop()

    def test_default_theme_initialization(self):
        """Test that theme initializes to a default value if not set."""
        manager = ThemeManager()
        manager.initialize_theme()
        self.assertIn('theme', st.session_state)
        self.assertEqual(st.session_state['theme'], 'light')

    def test_set_theme(self):
        """Test setting the theme updates session state."""
        manager = ThemeManager()
        manager.set_theme('dark')
        self.assertEqual(st.session_state['theme'], 'dark')
        
        manager.set_theme('light')
        self.assertEqual(st.session_state['theme'], 'light')

    def test_toggle_theme(self):
        """Test toggling the theme switches between light and dark."""
        manager = ThemeManager()
        st.session_state['theme'] = 'light'
        manager.toggle_theme()
        self.assertEqual(st.session_state['theme'], 'dark')
        
        manager.toggle_theme()
        self.assertEqual(st.session_state['theme'], 'light')

if __name__ == '__main__':
    unittest.main()
