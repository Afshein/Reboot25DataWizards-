
import pypyodbc as odbc
import pandas

username = 'team12.hacker02@lbgreboot2025outlook.onmicrosoft.com'
password = 'Team12team'
server = 'team12server.database.windows.net'
database = 'rankingdbsqlauth'

#connectionstring = 'Driver={ODBC Driver 18 for SQL Server};Server='+ server + ';Database=' + database + ';Uid=' + username + ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryIntegrated'
connectionstring = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:team12serversqlauth.database.windows.net,1433;Database=rankingdbsqlauth;Uid=datawiz;Pwd=' + password + ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
conn = odbc.connect(connectionstring)
cursor = conn.cursor()

#Schema for the table
"""
CREATE TABLE ratings (
    party_id VARCHAR(255)
    ,product VARCHAR(255)
    ,rating INT
PRIMARY KEY (party_id)
);
"""

#What tables exist in the db
"""
SELECT TABLE_NAME, TABLE_SCHEMA
FROM INFORMATION_SCHEMA.TABLES
--WHERE TABLE_NAME = 'ratings';
"""

def add_entry(cursor, party_id, product_name, rating):

    #Can only have one rating per product rating combination 
    sql_delete_entry = f"""
    DELETE FROM dbo.ratings
    WHERE party_id = \'{party_id}\'
    AND product = \'{product_name}\';
    """
    cursor.execute(sql_delete_entry)

    sql = f"""
    INSERT INTO dbo.ratings (party_id, product, rating)
    VALUES (\'{party_id}\', \'{product_name}\', {rating});
    """

    cursor.execute(sql)
    conn.commit()

def read_all_entries(cursor):
    
    sql = """
    select * from ratings;
    """
    all_entries = cursor.execute(sql)
    ratings_list = []
    for row in all_entries:
        ratings_list.append({
            'party_id': row[0]
            ,'product_name': row[1]
            ,'rating': row[2]
        })
    return ratings_list

def read_rating(cursor, party_id, product_name):
    sql = f"""
    SELECT rating
    FROM ratings
    WHERE product = \'{product_name}\'
    AND party_id = \'{party_id}\';
    """
    print(sql)
    cursor.execute(sql)
    
    row = cursor.fetchone()
    return row[0] if row else None

def get_average_product_ratings(cursor):
    sql = """
    SELECT product, AVG(rating) as average_rating, COUNT(*) as rating_count
    FROM ratings
    GROUP BY product;
    """
    cursor.execute(sql)
    return {row[0]: (row[1], row[2]) for row in cursor.fetchall()}

import random

# Function to add synthetic ratings
def add_synthetic_ratings(cursor, num_entries):
    products_list = ["club-lloyds", "ready-made-investments", "mortgage", "savings-plan"]
    for _ in range(num_entries):
        party_id = str(random.randint(1, 10000000))  # Example user IDs from 1 to 100
        product_name = random.choice(products_list)
        rating = random.choices([1, 2, 3, 4, 5], weights=[5, 5, 10, 25, 55])[0]  # Ratings between 1 and 5
        
        # Use an SQL query to insert values
        add_entry(cursor, party_id, product_name, rating)
    conn.commit()
