# -*- coding: utf-8 -*-
"""MTG_Scraping.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sKfJZSw1C05wswxeaGKIqP-SNRtmmVBz
"""

# @title Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# @title Import Required Libraries
import json
import pandas as pd
import numpy as np
import sqlite3

# @title Load and Explore JSON Data
json_file_path = '/content/drive/MyDrive/Database Systems/MTG/COMMANDER.json'

# Load the JSON data and print the keys
with open(json_file_path, 'r') as file:
    data = json.load(file)
    print("Loaded JSON data keys:", data.keys())  # Print the top-level keys of the JSON

# Explore deeper into the structure of the 'data' key, if present
if 'data' in data:
    print("Keys in 'data':", data['data'].keys())

# @title Load a Sample of the CSV File (First 100 rows)
csv_file_path = '/content/drive/MyDrive/Database Systems/MTG/draft_data_public.BLB.PremierDraft.csv'

# Load a small sample to avoid memory issues
df_sample = pd.read_csv(csv_file_path, nrows=100)

# Display the first few rows of the sample and column names
print("Sample of the CSV (first 100 rows):")
print(df_sample.head())

print("\nColumn Names:")
print(df_sample.columns)

# @title Load Larger CSV File in Chunks for Processing
csv_file_path = '/content/drive/MyDrive/Database Systems/MTG/card-ratings-2024-10-13 (1).csv'
chunk_size = 10000
card_stats = {}  # Dictionary to store all card stats

# Example to show how you could process large CSV file in chunks
for chunk in pd.read_csv(csv_file_path, chunksize=chunk_size):
    print(chunk.head())  # For testing purposes, print the first few rows of each chunk

# @title Define Functions to Insert Data into Database
# Connect to SQLite database
db_path = '/content/drive/MyDrive/Database Systems/MTG/MTG_cards.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Insert data into CARD_INFO table
def insert_card_info(card_name, card_data):
    sql = '''
    INSERT OR IGNORE INTO CARD_INFO (card_name, type, rarity)
    VALUES (?, ?, ?)
    '''
    cursor.execute(sql, (card_name, card_data.get('type'), card_data.get('rarity')))

# Insert data into CARD_PRINT table
def insert_card_print(card_name, print_data):
    sql = '''
    INSERT OR IGNORE INTO CARD_PRINT (card_name, set_code, collector_number)
    VALUES (?, ?, ?)
    '''
    cursor.execute(sql, (card_name, print_data.get('set_code'), print_data.get('collector_number')))

# Insert data into CARD_PRICE table
def insert_card_price(card_name, price_data):
    sql = '''
    INSERT OR IGNORE INTO CARD_PRICE (card_name, eur_price, tix_price, usd_price)
    VALUES (?, ?, ?, ?)
    '''
    cursor.execute(sql, (
        card_name,
        price_data.get('eur'),
        price_data.get('tix'),
        price_data.get('usd')
    ))

# Insert data into LIMITED_ANALYTICS table
def insert_limited_analytics(card_name, limited_data):
    sql = '''
    INSERT OR IGNORE INTO LIMITED_ANALYTICS (card_name, format, win_rate_in_main_deck, play_rate, win_rate_opening_hand, win_rate_drawn)
    VALUES (?, 'Limited', ?, ?, ?, ?)
    '''
    cursor.execute(sql, (
        card_name,
        limited_data.get('win_rate_in_main_deck'),
        limited_data.get('play_rate'),
        limited_data.get('win_rate_opening_hand'),
        limited_data.get('win_rate_drawn')
    ))

# Insert data into COMMANDER_ANALYTICS table
def insert_commander_analytics(card_name, commander_data):
    sql = '''
    INSERT OR IGNORE INTO COMMANDER_ANALYTICS (card_name, format, edhrec_rank, salt_score)
    VALUES (?, 'Commander', ?, ?)
    '''
    cursor.execute(sql, (
        card_name,
        commander_data.get('edhrec_rank'),
        commander_data.get('salt_score')
    ))

# @title Populate Database with Data
# Iterate through the master JSON and generate SQL statements for each table
for card_name, card_data in data.items():
    # Insert into CARD_INFO
    if 'CARD_INFO' in card_data:
        insert_card_info(card_name, card_data['CARD_INFO'])

    # Insert into CARD_PRINT
    if 'CARD_PRINT' in card_data:
        insert_card_print(card_name, card_data['CARD_PRINT'])

    # Insert into CARD_PRICE
    if 'CARD_PRICE' in card_data:
        insert_card_price(card_name, card_data['CARD_PRICE'])

    # Insert into LIMITED_ANALYTICS
    if 'LIMITED_ANALYTICS' in card_data:
        insert_limited_analytics(card_name, card_data['LIMITED_ANALYTICS'])

    # Insert into COMMANDER_ANALYTICS
    if 'COMMANDER_ANALYTICS' in card_data:
        insert_commander_analytics(card_name, card_data['COMMANDER_ANALYTICS'])

# Commit the transactions and close
conn.commit()
conn.close()

print("Database populated successfully!")