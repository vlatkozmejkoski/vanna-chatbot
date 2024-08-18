# Sample Vanna Chatbot querying against PostgreSQL Database
## Database
We use PostgreSQL driver, by default vanna uses psyocopg.
You can setup local postgre and execute the scripts in the repo to have some data to query against.

## Setup
1. Setup your venv
2. Run `pip install -r requirements.txt`
3. Copy the settings in `secrets.toml`, and create a file in your local `C:\Users\%user%\.streamlit` with the same name and insert the corresponding values  in the file
4. Run `streamlit run vanna-script.py`
