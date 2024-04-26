import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os


def choose_file():
    """
    This method opens a file dialog window to allow the user to choose a file on their system. It returns the path of the selected file.
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


def load_file_to_dataframe(file_path, delimiter=';'):
    """
    Loads a file from the given file_path and loads it into a pandas dataframe
    """
    if not file_path:
        raise ValueError('File path is empty. Please provide a valid path to the file.')

    # Obtain the file extension
    _, file_type = os.path.splitext(file_path)
    # remove the dot from the file_extension
    file_type = file_type[1:]

    # Create a dictionary where the keys are file types and the values are Pandas read functions
    read_funcs = {'csv': lambda x: pd.read_csv(x, delimiter=delimiter),
                  'xls': pd.read_excel,
                  'xlsx': pd.read_excel,
                  'xlsm': pd.read_excel,
                  'json': pd.read_json,
                  'txt': lambda x: pd.read_csv(x, delimiter=delimiter),
                  'h5': pd.read_hdf,
                  'hdf5': pd.read_hdf,
                  'pkl': pd.read_pickle,
                  'pickle': pd.read_pickle,
                  'html': pd.read_html,
                  'htm': pd.read_html}

    try:
        if file_type.lower() not in read_funcs:
            raise ValueError('Unsupported file type. Please try using a file with supported extension.')

        df = read_funcs[file_type.lower()](file_path)

        # If file is HTML, it returns a list of DataFrames. So it will be contacted
        if file_type.lower() in ['html', 'htm']:
            df = pd.concat(df)

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f'File not found at path: {file_path}')

    except Exception as e:
        raise LookupError(f"Error loading the file: {e}")




"""
import logging
import psycopg2
import pymysql
import pyodbc

logging.basicConfig(level=logging.INFO)

def connect_to_database(db_type, host, port, database, user, password):
    conn = None
    try:
        if db_type.lower() == 'postgresql':
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
        elif db_type.lower() == 'mysql':
            conn = pymysql.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
        elif db_type.lower() == 'sqlserver':
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=' + host + ';DATABASE=' + database + ';UID=' + user + ';PWD=' + password
            )
        else:
            logging.error("Unsupported database type.")
            return None
        
        logging.info(f"Successfully connected to {db_type} database.")
        return conn
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        return None
"""
