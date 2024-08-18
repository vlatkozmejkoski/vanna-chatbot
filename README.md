# Sample Vanna Chatbot querying against PostgreSQL Database
## Database
We use PostgreSQL driver, by default vanna uses psyocopg.
You can setup local postgre and execute the scripts in the repo to have some data to query against.

## Setup
1. Setup your venv
2. Run `pip install -r requirements.txt`
3. Copy the settings in `secrets.toml`, and create a file in your local `C:\Users\%user%\.streamlit` with the same name and insert the corresponding values  in the file
4. Run `streamlit run vanna-script.py`
* The startup does train vanna model with data provided from the table schema information so it will take a while to boot up.

Sample query against current data:

> Report all customers that ordered in May 2024, and the status of their order is completed
