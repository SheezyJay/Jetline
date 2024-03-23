import logging
import tkinter as tk
from tkinter import filedialog
import pandas as pd

logging.basicConfig(level=logging.INFO)

def choose_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def load_file_to_dataframe(file_path, file_type='csv', delimiter=','):
    if file_path:
        try:
            if file_type.lower() == 'csv':
                df = pd.read_csv(file_path, delimiter=delimiter)
            elif file_type.lower() in ['xls', 'xlsx', 'xlsm']:
                df = pd.read_excel(file_path)
            elif file_type.lower() == 'json':
                df = pd.read_json(file_path)
            elif file_type.lower() == 'txt':
                df = pd.read_csv(file_path, delimiter=delimiter)
            elif file_type.lower() in ['h5', 'hdf5']:
                df = pd.read_hdf(file_path)
            elif file_type.lower() in ['pkl', 'pickle']:
                df = pd.read_pickle(file_path)
            elif file_type.lower() in ['html', 'htm']:
                df = pd.read_html(file_path)[0]
            else:
                logging.error("Unsupported file type.")
                return None
            
            logging.info(f"Successfully loaded {file_type} file: {file_path}")
            return df
        except Exception as e:
            logging.error(f"Error loading the file: {e}")
            return None
    else:
        logging.warning("No file selected.")
        return None



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
