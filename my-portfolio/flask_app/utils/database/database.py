import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path='flask_app/database/'):
        # Establish connection to MySQL database
        cnx = mysql.connector.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    port=self.port,
                                    database=self.database,
                                    charset='latin1')

        # Create a cursor object to execute queries
        cur = cnx.cursor()

        # Purge existing tables if specified
        if purge:
            tables_to_purge = ['skills', 'experiences', 'positions', 'institutions']
            for table in tables_to_purge:
                cur.execute(f"DROP TABLE IF EXISTS {table}")
            # Commit changes to the database
            cnx.commit()

        # Read SQL files and execute create table queries
        create_files = ['institutions.sql', 'positions.sql', 'experiences.sql', 'skills.sql', 'feedback.sql', 'users.sql']
        for file in create_files:
            with open(f'{data_path}create_tables/{file}', 'r') as f:
                query = f.read()
                cur.execute(query)

        # Define data to be inserted into tables
        data = [
            ('institutions', ['inst_id', 'name', 'department', 'type', 'address', 'city', 'state', 'zip'], f'{data_path}initial_data/institutions.csv'),
            ('positions', ['position_id', 'inst_id', 'title', 'start_date', 'end_date', 'responsibilities'], f'{data_path}initial_data/positions.csv'),
            ('experiences', ['experience_id', 'position_id', 'name', 'description', 'hyperlink', 'start_date', 'end_date'], f'{data_path}initial_data/experiences.csv'),
            ('skills', ['skill_id', 'experience_id', 'name', 'skill_level'], f'{data_path}initial_data/skills.csv')
        ]

        # Insert rows into tables from CSV files
        for table, columns, data_file in data:
            rows = []
            with open(data_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    values = []
                    for col in columns:
                        value = row[col]
                        if value == 'None':
                            values.append(None)
                        else:
                            values.append(value)
                    rows.append(values)
            # Call insertRows method to insert data into table
            self.insertRows(table, columns, rows)
        
        # Commit changes to the database
        cnx.commit()
        # Close cursor and database connection
        cur.close()
        cnx.close()


    def insertRows(self, table='table', columns=['x', 'y'], parameters=[['v11', 'v12'], ['v21', 'v22']]):
        # Establish connection to MySQL database
        cnx = mysql.connector.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    port=self.port,
                                    database=self.database,
                                    charset='latin1')

        # Create a cursor object to execute queries
        cur = cnx.cursor()

        # Create placeholders for parameterized query
        placeholders = ', '.join(['%s'] * len(columns))

        # Construct SQL query with placeholders
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"

        # Execute the insert query with multiple rows of data
        cur.executemany(query, parameters)

        # Commit changes to the database
        cnx.commit()

        # Close cursor and database connection
        cur.close()
        cnx.close()
    
    def getResumeData(self):
        # Initialize an empty dictionary to store resume data
        resume_data = {}

        # Establish connection to MySQL database
        cnx = mysql.connector.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    port=self.port,
                                    database=self.database,
                                    charset='latin1')

        # Create a cursor object to execute queries
        cur = cnx.cursor()

        # Fetch all institutions from the 'institutions' table
        cur.execute("SELECT * FROM institutions")
        institutions = cur.fetchall()

        # Iterate through each institution
        for institution in institutions:
            inst_id = institution[0]  # Extract institution ID
            # Create a dictionary for the institution and its details
            resume_data[inst_id] = {
                'type': institution[1],
                'name': institution[2],
                'department': institution[3],
                'address': institution[4],
                'city': institution[5],
                'state': institution[6],
                'zip': institution[7],
                'positions': {}  # Initialize positions dictionary
            }

            # Fetch all positions associated with the current institution
            cur.execute("SELECT * FROM positions WHERE inst_id = %s", (inst_id,))
            positions = cur.fetchall()

            # Iterate through each position
            for position in positions:
                position_id = position[0]  # Extract position ID
                # Create a dictionary for the position and its details
                resume_data[inst_id]['positions'][position_id] = {
                    'title': position[2],
                    'responsibilities': position[3],
                    'start_date': position[4],
                    'end_date': position[5],
                    'experiences': {}  # Initialize experiences dictionary
                }

                # Fetch all experiences associated with the current position
                cur.execute("SELECT * FROM experiences WHERE position_id = %s", (position_id,))
                experiences = cur.fetchall()

                # Iterate through each experience
                for experience in experiences:
                    experience_id = experience[0]  # Extract experience ID
                    # Create a dictionary for the experience and its details
                    resume_data[inst_id]['positions'][position_id]['experiences'][experience_id] = {
                        'name': experience[2],
                        'description': experience[3],
                        'hyperlink': experience[4],
                        'start_date': experience[5],
                        'end_date': experience[6],
                        'skills': {}  # Initialize skills dictionary
                    }

                    # Fetch all skills associated with the current experience
                    cur.execute("SELECT * FROM skills WHERE experience_id = %s", (experience_id,))
                    skills = cur.fetchall()

                    # Iterate through each skill
                    for skill in skills:
                        skill_id = skill[0]  # Extract skill ID
                        # Create a dictionary for the skill and its details
                        resume_data[inst_id]['positions'][position_id]['experiences'][experience_id]['skills'][skill_id] = {
                            'name': skill[2],
                            'skill_level': skill[3]
                        }

        # Close cursor and database connection
        cur.close()
        cnx.close()

        # Return the populated resume data dictionary
        return resume_data

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='user'):
        # Establish connection to MySQL database
        cnx = mysql.connector.connect(host=self.host,
                                       user=self.user,
                                       password=self.password,
                                       port=self.port,
                                       database=self.database,
                                       charset='latin1')

        # Create a cursor object to execute queries
        cur = cnx.cursor()

        # Define a SQL query to select columns from the "users" table where the email matches a specific value
        query = "SELECT * FROM users WHERE email = %s"

        # Execute the query to check if the user already exists
        cur.execute(query, (email,))

        # Fetch a match from the result set returned by the query if there is one
        result = cur.fetchone()

        # User email already exists
        if result:
            cur.close()
            cnx.close()
            return {'success': 0, 'message': 'User already exists.'}
        # User doesn't exist
        # Encrypt password with Scrypt
        encrypted_password = self.onewayEncrypt(password)

        # Insert user into the database
        query_insert = "INSERT INTO users (email, password, role) VALUES (%s, %s, %s)"
        cur.execute(query_insert, (email, encrypted_password, role))

        # Commit changes to the database
        cnx.commit()
        
        cur.close()
        cnx.close()

        return {'success': 1, 'message': 'User created successfully.'}

    def authenticate(self, email='me@email.com', encrypted_password='example_password'):
        # Query to check for a match
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        parameters = (email, encrypted_password)

        # If there is a user that matches provided info
        result = self.query(query, parameters)
        if result:
            role = result[0]['role']
            return {'success': 1, 'message': 'Authentication successful.', 'role': role}
        else:
            return {'success': 0, 'message': 'Invalid email or password.'}


    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message


