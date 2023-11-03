import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()

def df_to_sql(dataframe, table_name):
    try:
        # Buat koneksi ke MySQL menggunakan SQLAlchemy
        db_url = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        engine = create_engine(db_url)

        # Unggah dataframe ke tabel MySQL
        dataframe.to_sql(table_name, con=engine, if_exists='append', index=False)

    except Exception as error:
        print(f"Error: {error}")

    finally:
        if 'engine' in locals():
            engine.dispose()

