from flask import Flask, jsonify, request
import sqlite3
import pandas as pd

app = Flask(__name__)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('SQLLite.db')
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn

@app.route('/newemps', methods=['GET'])
def get_newemps():
    conn = sqlite3.connect('SQLLite.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table named 'users'
    users=cursor.execute('''Select * from Employee_Details''').fetchall()
    #cursor.execute('''''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    return jsonify(users)
    #return ""

# Endpoint to get all users
@app.route('/nts', methods=['GET'])
def get_nts():
    excel_file = 'New Microsoft Excel Worksheet.xlsx'  # Path to your Excel file
    df = pd.read_excel(excel_file)

    # Step 2: Print the first few rows of the dataframe to verify the data
    print(df.head())

    # Step 3: Connect to your SQLite database (or create one if it doesn't exist)
    db_file = 'SQLLite.db'  # SQLite database file
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Step 4: Optionally, create a table (only if the table does not already exist)
    # You need to match this with the structure of your Excel data.
    table_creation_query = '''
    CREATE TABLE IF NOT EXISTS Demo_TBL (
        column1_name TEXT,
        column2_name TEXT,
        column3_name INTEGER
    );
    '''

    # Run the query to create the table
    cursor.execute(table_creation_query)
    conn.commit()

    # Step 5: Insert the data from the DataFrame into the SQLite database
    # Convert the DataFrame to a list of tuples (each row in the DataFrame becomes a tuple)
    data_to_insert = df.values.tolist()

    # You can write a parameterized query to insert the data
    insert_query = '''
    INSERT INTO Demo_TBL (column1_name, column2_name, column3_name)
    VALUES (?, ?, ?);
    '''

    # Execute the insert query for each row
    cursor.executemany(insert_query, data_to_insert)

    # Step 6: Commit the changes and close the connection
    conn.commit()

    users=cursor.execute('''Select * from Demo_TBL''').fetchall()


    # Close the connection to the database
    conn.close()

    print("Data inserted successfully.")
    return jsonify(users)
    
# Endpoint to get all users
@app.route('/emps', methods=['GET'])
def get_emps():
    conn = sqlite3.connect('SQLLite.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table named 'users'
    users=cursor.execute('''Select * from Employees''').fetchall()
    #cursor.execute('''''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    return jsonify(users)
    #return ""

@app.route('/accs', methods=['GET'])
def get_accs():
    conn = sqlite3.connect('SQLLite.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table named 'users'
    users=cursor.execute('''Select * from Accelerators''').fetchall()
    #cursor.execute('''''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    return jsonify(users)

# Endpoint to get a single user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user))
    else:
        return jsonify({"error": "User not found"}), 404

# Endpoint to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.get_json()
    name = new_user.get('name')
    email = new_user.get('email')
    
    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        conn.close()
        return jsonify({"message": "User created successfully"}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Email already exists"}), 400

# Endpoint to update a user by ID
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    updated_user = request.get_json()
    name = updated_user.get('name')
    email = updated_user.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    conn = get_db_connection()
    conn.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (name, email, id))
    conn.commit()
    conn.close()

    return jsonify({"message": "User updated successfully"})

# Endpoint to delete a user by ID
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "User deleted successfully"})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
