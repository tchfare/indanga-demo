#!/usr/bin/env bash
# Start the INDANGA Streamlit demo. Works offline once Streamlit is installed.
cd "$(dirname "$0")"
if [ -x "$HOME/.venv/bin/streamlit" ]; then ST="$HOME/.venv/bin/streamlit"; else ST="streamlit"; fi
"$ST" run app.py --browser.gatherUsageStats false
