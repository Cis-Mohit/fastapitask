import sqlite3
from fastapi import FastAPI
import datetime
from typing import Optional
from pydantic import BaseModel

app = FastAPI()
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


class User(BaseModel):
    name: str
    username: str
    email: str
    password: str
    createdAt: Optional[str] = None
    bitcoinAmount:Optional[float] = 0.0
    usdBalance:Optional[float] = 0.0
    updatedAt: Optional[str] = None


@app.get('/')
async def test():
    return {'msg': 'hello'}

@app.post("/users")
async def signup(user: User):
    # {
    # “name”: “Jon A”,
    # “username”: “jonjon”,
    # “email”: “jon@jmail.com”
    # }
    # conn = sqlite3.connect(':memory:') 
    global cur
    if user.name:

        name = user.name
    else:
        return {'status':False, 'code':404, 'msg': 'Name field required.'}
    if user.username:

        username = user.username
    else:
        return {'status':False, 'code':404, 'msg': 'Username field required.'}

    if user.email:

        email = user.email
    else:
        return {'status':False, 'code':404, 'msg': 'EMAIL field required.'}
    if user.password:

        password = user.password
    else:
        return {'status':False, 'code':404, 'msg': 'Password field required.'}
    cur = conn.cursor()
    current_time = datetime.datetime.now().timestamp()
    # Insert a row of data

    tables = list(cur.execute("select name from sqlite_master where type is 'table'"))
    print(tables)


    cur.execute("""INSERT INTO users (name, username, email, password, bitcoinAmount, usdBalance, createdAt)
        VALUES ('{name}', '{username}' ,'{username}' ,'{password}' ,0 ,0 ,'{current_time}');""")

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

    response = {
    'id':1,
    'bitcoinAmount':0,
    'usdBalance':0,
    'createdAt':'',
    'updatedAt':'',
    'name': 'Jon A',
    'username': 'jonjon',
    'email': 'jon@jmail.com'
        }

    return response


@app.get("/users/{id}")
async def fetch_user():

    # SELECT * FROM USERS WHERE id=id;
    response = {
    'id':1,
    'bitcoinAmount':0,
    'usdBalance':0,
    'createdAt':'',
    'updatedAt':'',
    'name': 'Jon A',
    'username': 'jonjon',
    'email': 'jon@jmail.com'
    }
    return response

@app.put("/users/{id}")
async def update_user():
    # {
    # “name”: “Jon A”,
    # “email”: “jon@jmail.com”
    # }
    response = {
    'id':1,
    'bitcoinAmount':0,
    'usdBalance':0,
    'createdAt':'',
    'updatedAt':'',
    'name': 'Jon A',
    'username': 'jonjon',
    'email': 'jon@jmail.com'
    }
    return response




@app.post("/users/{id}/usd")
async def user_usd_balance_update():
    # {
    # “action”: “withdraw” or “deposit”,
    # “amount”: 40.05
    # }
    response = {
    'id':1,
    'bitcoinAmount':0,
    'usdBalance':0,
    'createdAt':'',
    'updatedAt':'',
    'name': 'Jon A',
    'username': 'jonjon',
    'email': 'jon@jmail.com'
    }
    return response

@app.post("/users/{id}/bitcoins")
async def user_bitcoins_balance_update():
    # {
    # “action”: "buy" or “sell”,
    # “amount”: 40.05
    # }
    response = {
    'id':1,
    'bitcoinAmount':0,
    'usdBalance':0,
    'createdAt':'',
    'updatedAt':'',
    'name': 'Jon A',
    'username': 'jonjon',
    'email': 'jon@jmail.com'
    }
    return response


@app.get("/users/{id}/balance")
async def get_user_balance():
    # {
    # “action”: "bubalr “sell”,
    # “amount”: 40.05
    # }
    balance = usd + bitcoin * 32100
    response = {
    'balance': balance,
    
    }
    return response

@app.get("/bitcoin")
async def fetch_bitcoin():
    # {
    # “price”: 100.00,
    # }
    response = {
    'price': 100.00,
    'updatedAt' :'2021-01-04T00:12:01.000Z'
    }
    return response

@app.put("/bitcoin")
async def update_bitcoin():
    # {
    # “price”: 100.00,
    # }
    response = {
    'price': 100.00,
    'updatedAt': '2021-01-04T00:12:01.000Z'
    }
    return response




