#!/usr/bin/env python3
# etl_pipeline.py

"""
A robust ETL (Extract, Transform, Load) pipeline for financial data.
This script extracts data from a CSV file, performs a transformation,
and loads the result into a SQLite database.
"""

import sys
import sqlite3
from typing import Optional

# Requirement 1 & 2: Robustly import pandas and handle its absence.
try:
    import pandas as pd
    from pandas import DataFrame
except ImportError:
    print("Error: The 'pandas' library is required to run this script.")
    print("Please install it using: pip install pandas")
    sys.exit(1)


class DataPipeline:
    """
    Encapsulates the ETL process for financial data.
    """

    def __init__(self, csv_path: str, db_path: str, table_name: str):
        """
        Initializes the DataPipeline with source and destination paths.

        Args:
            csv_path (str): The path to the source CSV file.
            db_path (str): The path to the destination SQLite database file.
            table_name (str): The name of the table to create/replace in the database.
        """
        self.csv_path = csv_path
        self.db_path = db_path
        self.table_name = table_name
        self.df: Optional[DataFrame] = None
        print(f"[INFO] DataPipeline initialized for source '{csv_path}' and destination '{db_path}'.")

    def extract(self) -> None:
        """
        Extracts data from the source CSV file.
        Raises:
            FileNotFoundError: If the CSV file does not exist.
        """
        print(f"[INFO] Stage 1/3: EXTRACING data from '{self.csv_path}'...")
        try:
            self.df = pd.read_csv(self.csv_path)
            print(f"[SUCCESS] Extracted {len(self.df)} rows successfully.")
        except FileNotFoundError:
            print(f"[ERROR] Source file not found at '{self.csv_path}'.")
            raise

    def transform(self) -> None:
        """
        Transforms the extracted data by adding a 'tax' column.
        The 'amount' column is assumed to exist.
        Raises:
            ValueError: If the dataframe has not been extracted yet.
            KeyError: If the 'amount' column is missing from the dataframe.
        """
        print("[INFO] Stage 2/3: TRANSFORMING data...")
        if self.df is None:
            raise ValueError("Dataframe is not loaded. Please run extract() first.")
        
        if 'amount' not in self.df.columns:
            raise KeyError("The required column 'amount' is missing from the source data.")

        # Ensure 'amount' is a numeric type, coercing errors to NaN
        self.df['amount'] = pd.to_numeric(self.df['amount'], errors='coerce')
        
        # Drop rows where 'amount' could not be converted to a number
        original_rows = len(self.df)
        self.df.dropna(subset=['amount'], inplace=True)
        if len(self.df) < original_rows:
            print(f"[WARNING] Dropped {original_rows - len(self.df)} rows with non-numeric 'amount'.")

        # Requirement 3: Add a 'tax' column
        self.df['tax'] = self.df['amount'] * 0.15
        print("[SUCCESS] Transformation complete. 'tax' column added.")

    def load(self) -> None:
        """
        Loads the transformed data into a SQLite database table.
        This will replace the table if it already exists.
        Raises:
            ValueError: If the dataframe has not been transformed yet.
            sqlite3.Error: If there is an issue with the database operation.
        """
        print(f"[INFO] Stage 3/3: LOADING data into '{self.db_path}' (table: '{self.table_name}')...")
        if self.df is None:
            raise ValueError("Dataframe is empty. Please run extract() and transform() first.")

        try:
            with sqlite3.connect(self.db_path) as conn:
                self.df.to_sql(
                    self.table_name,
                    conn,
                    if_exists='replace',
                    index=False
                )
                print(f"[SUCCESS] Data loaded into table '{self.table_name}'.")
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to load data into SQLite database: {e}")
            raise

    def run(self) -> None:
        """
        Executes the full ETL pipeline in sequence.
        """
        try:
            self.extract()
            self.transform()
            self.load()
        except (FileNotFoundError, ValueError, KeyError, sqlite3.Error):
            print("[FAILURE] ETL pipeline execution failed.")
            # Re-raise the exception to be caught by the main execution block
            raise


# Requirement 4: Main execution block
if __name__ == "__main__":
    # Configuration
    CSV_FILE = 'data.csv'
    DB_FILE = 'finance.db'
    TABLE_NAME = 'transactions'

    # To make this script runnable out-of-the-box, let's create a dummy data.csv
    try:
        with open(CSV_FILE, 'w') as f:
            f.write("transaction_id,date,amount,description\n")
            f.write("1,2023-01-15,150.75,Office Supplies\n")
            f.write("2,2023-01-16,99.99,Software Subscription\n")
            f.write("3,2023-01-18,500.00,Client Dinner\n")
            f.write("4,2023-01-19,invalid,Data Entry Error\n")
            f.write("5,2023-01-20,250.50,Travel Expense\n")
        print(f"[SETUP] Created dummy '{CSV_FILE}' for demonstration.")
    except IOError as e:
        print(f"[ERROR] Could not create dummy CSV file: {e}")
        sys.exit(1)

    # Execute the pipeline
    pipeline = DataPipeline(csv_path=CSV_FILE, db_path=DB_FILE, table_name=TABLE_NAME)
    try:
        pipeline.run()
        print("\n" + "="*50)
        print("Pipeline Finished. Data saved to finance.db")
        print("="*50)
    except Exception:
        print("\n[CRITICAL] The pipeline process was terminated due to a critical error.")
        sys.exit(1)