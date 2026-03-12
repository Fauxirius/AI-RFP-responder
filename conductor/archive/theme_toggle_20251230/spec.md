# Specification: Dark/Light Mode Theme Toggle

## Overview
This track involves implementing a theme toggle (Dark Mode / Light Mode) for the RFP Genie application to improve user experience and accessibility. The toggle will allow users to switch between light and dark themes, with their preference persisting across browser sessions.

## Functional Requirements
- **Theme Toggle UI:** Implement two distinct buttons (Sun and Moon icons) in the top-right corner of the main header area.
- **Theme Switching Logic:** 
    - Clicking the 'Moon' icon switches the application to Dark Mode.
    - Clicking the 'Sun' icon switches the application to Light Mode.
- **Visual Feedback:** The active theme should be visually distinct. The button corresponding to the inactive theme should be clickable.
- **Persistence:** 
    - Store the selected theme in the browser's local storage.
    - On application load, retrieve the theme from local storage. If no preference exists, default to a sensible default (e.g., Light Mode or System Preference).
    - Manage the current theme state within Streamlit's session state.
- **Styling Application:** Ensure the selected theme is applied globally across all UI components, including the custom "Crystal Teal" styles, sidebar, and main content area.

## Non-Functional Requirements
- **Performance:** Theme switching should be near-instantaneous and not require a full page reload if possible (within Streamlit limitations).
- **Accessibility:** Ensure the color contrast in both modes meets WCAG AA standards.

## Acceptance Criteria
- [ ] Sun and Moon icons are visible in the top-right header.
- [ ] Clicking the Moon icon changes the background to dark colors and text to light colors.
- [ ] Clicking the Sun icon changes the background to light colors and text to dark colors.
- [ ] Refreshing the page preserves the last selected theme.
- [ ] Closing and reopening the browser preserves the last selected theme.

## Out of Scope
- Automatic switching based on time of day.
- Custom user-defined color palettes beyond standard Light/Dark.
