import getpass
import base64
import os
import hashlib
import sqlite3 as sql

con = sql.connect("pwdManager.db")
cur = con.cursor()

def is_valid_credentials(username, password):
    res = cur.execute("SELECT user, password_hash, salt FROM users WHERE user =? AND type=?", (username,0,))
    user = res.fetchone()
    password_hash = hashlib.sha256(password+bytes(user[2],'utf-8')).hexdigest()
    if password_hash == user[1]:
        return True
    else:
        return False

def prompt_login():
    username = input("Username: ")
    password = getpass.getpass("Password: ").encode()
    if not is_valid_credentials(username, password):
        prompt_login()

def add_user():
    salt = os.urandom(16).hex()

    user = input("What would you like your username to be? ")

    count = cur.execute("SELECT COUNT(username) FROM users WHERE user =? AND type =?", (user,0,)).fetchone()[0]
    table_count = cur.execute("SELECT COUNT(username) FROM users WHERE type=?", (0,)).fetchone()[0]
    if count>0 and table_count>0:
        print("This username is taken by another user. Please pick a new one.")
        add_user()
    password = getpass.getpass("What would you like your password to be? ").encode()
    password_hash = hashlib.sha256(password+bytes(salt,'utf-8')).hexdigest()
    cur.execute("INSERT INTO users (type, user, password_hash, salt) VALUES (?,?,?,?)", (0,user,password_hash,salt,))
    con.commit()
    print('User added!')

def create_table():

    cur.execute("DROP TABLE IF EXISTS users")
    
    table = """ CREATE TABLE users (
            type SMALLINT,
            user VARCHAR,
            password_hash VARCHAR,
            salt,
            username VARCHAR,
            password VARCHAR
        ); """
    
    cur.execute(table)

def pull_table(user):
    res = cur.execute("SELECT username, password FROM users WHERE type=? AND user=?", (1,user,))
    return res.fetchall()

    # for i in res.fetchall():
    #     print(i)

    # print(type(res.fetchall()))

def add_password(user, username, password):
    cur.execute("INSERT INTO users (type, user, username, password) VALUES (?, ?, ?, ?)", (1, user, username, password))
    con.commit()

def add_user_gui(username, password):
    salt = os.urandom(16).hex()

    count = cur.execute("SELECT COUNT(username) FROM users WHERE username =? AND type=?", (username,0,)).fetchone()[0]
    table_count = cur.execute("SELECT COUNT(username) FROM users WHERE type=?", (0,)).fetchone()[0]
    if count>0 and table_count>0:
        return False
    else:
        password_hash = hashlib.sha256(password+bytes(salt,'utf-8')).hexdigest()
        cur.execute("INSERT INTO users (type, user, password_hash, salt) VALUES (?,?,?,?)", (0, username, password_hash, salt,))
        con.commit()
        return True

def remove_user(username):
    password = getpass.getpass('Enter the password of the user you would like to remove: ').encode()
    if is_valid_credentials(username, password):
        cur.execute("DELETE FROM users WHERE username = ?", (username, ))
        con.commit()
        print('User deleted!')
    else:
        remove_user(username)

def see_table():
    res = cur.execute("SELECT * FROM users")
    print(res.fetchall())

def delete():
    cur.execute("DELETE FROM users WHERE type = 1")
    con.commit()

def main():
    prompt = input("What would you like to do? (login (l), add user(a), remove user(r), quit(q)) ")

    match prompt:
        case 'l':
            prompt_login()
            main()
        case 'a':
            add_user()
            main()
        case 'r':
            username = input('Enter the username of the user you would like to remove: ')
            remove_user(username)
            main()
        case 'q':
            quit()
        case _:
            print('Input not recognized. Please try again.')
            main()

see_table()
# main()