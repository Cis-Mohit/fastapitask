import sqlite3


conn = sqlite3.connect(':memory:') 

cur = conn.cursor()

# Create User table
cur.execute('''CREATE TABLE users
	( user_id int AUTO_INCREMENT,
  username varchar(25)  NOT NULL UNIQUE,
  name varchar(25) NOT NULL,
  email varchar(25) NOT NULL,
  password varchar(30) NOT NULL,
  bitcoinAmount float(20) NOT NULL,
  usdBalance float(20) NOT NULL,
  createdAt timestamp NOT NULL,
  updatedAt timestamp NULL,
  PRIMARY KEY (user_id)
  );''')

# Create Crypto table.
cur.execute('''CREATE TABLE crypto
( name varchar(25) PRIMARY KEY,
  
  price float(20) NOT NULL,
  updatedAt timestamp NULL

  );''')

# Save (commit) the changes.
conn.commit()

# Closing Connection.
# conn.close()
tables = list(cur.execute("select name from sqlite_master where type is 'table'"))
print(tables)