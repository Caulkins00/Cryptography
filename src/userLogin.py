import getpass
import base64
import os
import hashlib
import json
import sqlite3 as sql

con = sql.connect("pwdManager.db")
cur = con.cursor()

def is_valid_credentials(username, password):
    res = cur.execute("SELECT * FROM users WHERE username =?", (username,))
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

    username = input("What would you like your username to be? ")

    count = cur.execute("SELECT COUNT(username) FROM users WHERE username =?", (username,)).fetchone()[0]
    table_count = cur.execute("SELECT COUNT(username) FROM users").fetchone()[0]
    if count>0 and table_count>0:
        print("This username is taken by another user. Please pick a new one.")
        add_user()
    password = getpass.getpass("What would you like your password to be? ").encode()
    password_hash = hashlib.sha256(password+bytes(salt,'utf-8')).hexdigest()
    cur.execute("INSERT INTO users VALUES (?,?,?)", (username,password_hash,salt,))
    con.commit()
    print('User added!')

def add_user_gui(username, password):
    salt = os.urandom(16).hex()

    count = cur.execute("SELECT COUNT(username) FROM users WHERE username =?", (username,)).fetchone()[0]
    table_count = cur.execute("SELECT COUNT(username) FROM users").fetchone()[0]
    if count>0 and table_count>0:
        return False
    else:
        password_hash = hashlib.sha256(password+bytes(salt,'utf-8')).hexdigest()
        cur.execute("INSERT INTO users VALUES (?,?,?)", (username,password_hash,salt,))
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

# main()