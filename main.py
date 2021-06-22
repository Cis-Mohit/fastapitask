"""Main file to create api's."""
import sqlite3
from fastapi import FastAPI
import datetime
from typing import Optional
from pydantic import BaseModel
import logging
import json

#Create and configure logger

#Creating an object

app = FastAPI()

logging.basicConfig(filename="/var/log/fastapi.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

conn = sqlite3.connect(':memory:')

cur = conn.cursor()


cur.execute('''CREATE TABLE users
    ( user_id int AUTO_INCREMENT,
  username varchar(25)  NOT NULL UNIQUE,
  name varchar(25) NOT NULL,
  email varchar(25) NOT NULL,
  password varchar(30) NOT NULL,
  bitcoinAmount float(20) NOT NULL,
  usdBalance float(20) NOT NULL,
  createdAt timestamp NULL,
  updatedAt timestamp NULL,
  PRIMARY KEY (user_id)
  );''')
# logger.info("Users table created in in-memory")


# Create Crypto table.
cur.execute('''CREATE TABLE crypto
( name varchar(25) PRIMARY KEY,

  price float(20) NOT NULL,
  updatedAt timestamp NULL

  );''')
# logger.info("Crypto table created in in-memory")

# Save (commit) the changes.
conn.commit()

# Closing Connection.
# conn.close()
# tables = list(cur.execute("select name from sqlite_master where type is 'table'"))
# print(tables)

# dummy data.
cur.execute("""INSERT INTO users (user_id, name, username, email, password, bitcoinAmount, usdBalance)
        VALUES (1,'joy', 'cooljoy', 'joy@gmail.com', 'joy123', 0, 0)""")

cur.execute("""INSERT INTO crypto (name, price, updatedAt)
        VALUES ('bitcoin', 100, '2021-01-04T00:12:01.000Z')""")

conn.commit


class User(BaseModel):
    """User model to get data to functon."""

    user_id:Optional[int]
    name: str
    username: str
    email: str
    password: str
    createdAt: Optional[str] = None
    bitcoinAmount: Optional[float] = 0.0
    usdBalance: Optional[float] = 0.0
    updatedAt: Optional[str] = None


class Crypto(BaseModel):
    """Crypto model to get data to functon."""

    price: Optional[float] = 100.0


class UpdateUsdBalance(BaseModel):
    """Model to update data to functon."""

    action_type: str
    balance: float


class UpdateBitcoinBalance(BaseModel):
    """Model to get data to functon."""

    action_type: str
    balance: float

class UpdateUserDetail(BaseModel):
    """Model to update user_detail"""
    user_id:Optional[int]
    name: str
    email: str


@app.post("/users")
async def signup(user: User):
    """Api to signup user."""
    
    logger.info("Request recieved for signup with data:: user_id:{}, name:{}, username:{}, email:{}, password:{}".format(user.user_id, user.name, user.username, user.email, user.password))
    if user.name:
        name = user.name
    else:
        return {'status': False, 'code': 404, 'msg': 'Name field required.'}
    if user.username:

        username = user.username
    else:
        return {'status': False, 'code': 404, 'msg': 'Username field required.'}

    if user.email:

        email = user.email
    else:
        return {'status': False, 'code': 404, 'msg': 'EMAIL field required.'}

    if user.password:
        password = user.password
    else:
        return {'status': False, 'code': 404, 'msg': 'Password field required.'}
    if user.user_id:
        user_id = user.user_id
    else:
        return {'status': False, 'code': 404, 'msg': 'user_id field required.'}
    global cur
    cur = conn.cursor()
    current_time = datetime.datetime.now().timestamp()
    # Insert a row of data

    # tables = list(cur.execute("select name from sqlite_master where type is 'table'"))
    # print(tables)

    cur.execute("""INSERT INTO users (user_id, name, username, email, password, bitcoinAmount, usdBalance, createdAt)
        VALUES (?,?, ?, ?, ?, 0, 0, ?)""", (user_id, name, username, username, password, current_time))
    logger.info("New user created with user_id: {} & username: {}".format(user.user_id, user.username))

    # Save (commit) the changes
    conn.commit()
    user_data = cur.execute("SELECT * FROM users WHERE username=?;", (username,)).fetchone()
    user_collumn = ('user_id', 'name', 'username', 'email', 'password', 'bitcoinAmount', 'usdBalance',
                    'createdAt', 'updatedAt')
    response = dict(zip(user_collumn, user_data))

    # conn.close()

    response = {'response': response}
    # logger.info("Response sent for signup request with data:: {}".format(json.dump(response)))
    return response


@app.get("/users/{id}")
async def fetch_user(id):

    global cur
    # logger.info("Request recieved for fetch user api details with data:: id:{}".format(id))
    user_data = cur.execute("SELECT * FROM users WHERE user_id=?;", (id,)).fetchone()
    user_collumn = ('user_id', 'name', 'username', 'email', 'password', 'bitcoinAmount', 'usdBalance',
                    'createdAt', 'updatedAt')
    response = dict(zip(user_collumn, user_data))

    response = {'response': response}
    # logger.info("Response sent for fetch user api request with data:: {}".format(json.dump(response)))
    return response


@app.put("/users/{id}")
async def update_user(id, user: UpdateUserDetail):
    """Fuction to update user details."""
    global cur
    # logger.info("Request recieved for update user api with data:: name:{}, email:{}".format(user.name, user.email))
    user_id = id
    if user.name:
        name = user.name
    else:
        return {'status': False, 'code': 404, 'msg': 'Name field required.'}

    if user.email:
        email = user.email
    else:
        return {'status': False, 'code': 404, 'msg': 'EMAIL field required.'}

    current_time = datetime.datetime.now().timestamp()

    cur.execute(""" UPDATE users SET name=?, email=?, updatedAt=? WHERE user_id=?;""", (
        name, email, current_time, user_id))
    # Save (commit) the changes.
    conn.commit()
    user_data = cur.execute("SELECT * FROM users WHERE user_id=?;", (id,)).fetchone()
    user_collumn = ('user_id', 'name', 'username', 'email', 'password', 'bitcoinAmount', 'usdBalance',
                    'createdAt', 'updatedAt')
    response = dict(zip(user_collumn, user_data))

    response = {'response': response}
    # logger.info("Response sent for update user api request with data:: {}".format(json.dump(response)))
    return response


@app.post("/users/{id}/usd")
async def user_usd_balance_update(id, usdbal: UpdateUsdBalance):
    """Fuction to sell and buy bitcoins."""
    global cur
    # logger.info("Request recieved for user usd balance update api with data:: action_type:{}, balance:{}".format(usdbal.action_type, usdbal.balance))
    user_bal = cur.execute("SELECT usdBalance  FROM users WHERE user_id=?;", (id,)).fetchone()
    usdbalance = user_bal[0]

    if usdbal.action_type:
        action_type = usdbal.action_type
    else:
        return {'status': False, 'code': 404, 'msg': 'Type field required.'}

    if usdbal.balance:
        balance = usdbal.balance
    else:
        return {'status': False, 'code': 404, 'msg': 'Balance field required.'}
    if action_type == 'deposit':
        updated_balance = usdbalance + balance

    elif action_type == 'withdraw':
        if usdbalance < balance:
            return {'status': False, 'code': 404, 'msg': 'Not Sufficient balance'}
        else:
            updated_balance = usdbalance - balance

    else:
        return {'status': False, 'code': 404, 'msg': 'Enter valid type field.'}

    current_time = datetime.datetime.now().timestamp()
    cur.execute(""" UPDATE users SET usdBalance=?, updatedAt=? WHERE user_id=?""", (
        updated_balance, current_time, id))
    # Save (commit) the changes.
    conn.commit()
    user_bal = cur.execute("SELECT usdBalance  FROM users WHERE user_id=?;", (id,)).fetchone()
    usdbalance = user_bal[0]

    response = {'usdbalance': usdbalance}
    # logger.info("Response sent for user usd balance update api request with data:: {}".format(json.dump(response)))
    return response

@app.post("/users/{id}/bitcoins")
async def user_bitcoins_balance_update(id, bitcoinbal: UpdateBitcoinBalance):
    """Fuction to sell and buy bitcoins."""
    global cur
    # logger.info("Request recieved for user bitcoin balance update api with data:: action_type:{}, balance:{}".format(bitcoinbal.action_type, bitcoinbal.balance))
    user_bal = cur.execute("SELECT bitcoinAmount  FROM users WHERE user_id=?;", (id,)).fetchone()
    bitcoinbalance = user_bal[0]

    if bitcoinbal.action_type:
        action_type = bitcoinbal.action_type
    else:
        return {'status': False, 'code': 404, 'msg': 'Type field required.'}

    if bitcoinbal.balance:
        balance = bitcoinbal.balance

    else:
        return {'status': False, 'code': 404, 'msg': 'Balance field required.'}
    if action_type == 'buy':
        updated_balance = bitcoinbalance + balance

    elif action_type == 'sell':
        if bitcoinbalance < balance:
            return {'status': False, 'code': 404, 'msg': 'Not Sufficient balance'}
        else:
            updated_balance = bitcoinbalance - balance

    else:
        return {'status': False, 'code': 404, 'msg': 'Enter valid type field.'}

    current_time = datetime.datetime.now().timestamp()
    cur.execute(""" UPDATE users SET bitcoinAmount=?, updatedAt=? WHERE user_id=?""", (
        updated_balance, current_time, id))

    # Save (commit) the changes.
    conn.commit()
    user_bal = cur.execute("SELECT bitcoinAmount  FROM users WHERE user_id=?;", (id,)).fetchone()
    bitcoinbalance = user_bal[0]

    response = {'bitcoinbalance': bitcoinbalance}
    # logger.info("Response sent for user bitcoin balance update api request with data:: {}".format(json.dump(response)))
    return response


@app.get("/users/{id}/balance")
async def get_user_balance(id):
    """Get User current balance."""
    global cur
    # logger.info("Request recieved for get use balance api with data:: id:{}".format(id))
    user_bal = cur.execute("SELECT usdBalance,bitcoinAmount  FROM users WHERE user_id=?;", (id,)).fetchone()
    crypto = cur.execute("SELECT price  FROM crypto WHERE name='bitcoin';").fetchone()
    bitcoin_price = crypto[0]
    usdbal = user_bal[0]
    bitcoinbal = user_bal[1]
    total_bal = usdbal + bitcoinbal * bitcoin_price

    response = {'balance': total_bal}
    # logger.info("Response sent for get use balance api request with data:: {}".format(json.dump(response)))
    return response


@app.get("/bitcoin")
async def fetch_bitcoin():
    """Get bitcoin current price."""
    global cur
    # logger.info("Request recieved for fetch bitcoin details api")
    bitcoin = cur.execute("SELECT price, updatedAt  FROM crypto WHERE name='bitcoin';").fetchone()
    response = {
        'price': bitcoin[0],
        'updatedAt': bitcoin[1]
    }
    # logger.info("Response sent for fetch bitcoin details api request with data:: {}".format(json.dump(response)))
    return response


@app.put("/bitcoin")
async def update_bitcoin(crypto: Crypto):
    """Api to update bitcoin price."""
    global cur
    # logger.info("Request recieved for update bitcoin details api with data:: price:{}".format(crypto.price))
    if crypto.price:
        price = crypto.price
    else:
        return {'status': False, 'code': 404, 'msg': 'Price field required.'}
    current_time = datetime.datetime.now().timestamp()
    cur.execute(""" UPDATE crypto SET price=?, updatedAt=? WHERE name='bitcoin';""", (
        price, current_time))

    # Save (commit) the changes.
    conn.commit()
    bitcoin = cur.execute("SELECT price, updatedAt  FROM crypto WHERE name='bitcoin';").fetchone()
    response = {
        'price': bitcoin[0],
        'updatedAt': bitcoin[1]
    }
    logger.info("Response sent for update bitcoin details api request with data:: {}".format(json.dump(response)))
    return response
    return response
