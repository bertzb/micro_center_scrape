import sqlite3


con = sqlite3.connect('data.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE inventory
    (timestamp INT,
    sku INT,
    name TEXT,
    price REAL,
    store_id TEXT,
    stock INT,
    availability TEXT)''')

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
