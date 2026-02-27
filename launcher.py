import sys
import os

# Explicitly add site-packages if needed, though diagnostics said it was there.
# We will just try to import.
try:
    from streamlit.web import cli as stcli
    print("Streamlit imported successfully.")
except ImportError as e:
    print(f"Failed to import streamlit: {e}")
    # Try adding the path found in diagnostics explicitly just in case
    sys.path.append(r"C:\Users\Teagan Holland\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages")
    try:
        from streamlit.web import cli as stcli
        print("Streamlit imported successfully after path fix.")
    except ImportError as e2:
        print(f"Failed to import streamlit again: {e2}")
        sys.exit(1)

if __name__ == '__main__':
    # Set up args for streamlit run
    sys.argv = ["streamlit", "run", "Monolith-Core/dashboard.py", "--server.headless", "true"]
    sys.exit(stcli.main())
