import mysql.connector

# Create connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Hari_4127@",
    database="dummy"
)

# Create cursor
cur = con.cursor()

# Execute query (example: select all records from a table named 'students')
cur.execute("SELECT * FROM students")

# Fetch all results
all_data = cur.fetchall()
print("All Data:", all_data)

# OR Fetch one result
# one_data = cur.fetchone()
# print("One Record:", one_data)

# OR Fetch limited results
# many_data = cur.fetchmany(3)
# print("Many Records:", many_data)

# Close connection
con.close()