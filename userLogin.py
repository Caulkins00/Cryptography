import getpass
import base64
import os
import hashlib
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

userDB = 'userDB.json'
file = open(userDB)
users = json.load(file)
print(type(users))
for entry in users:
    print(entry['username'])
file.close()

def is_valid_credentials(username, password):
    for entry in users:
        if entry['username']==username:
            password_hash = hashlib.sha256(password+bytes(entry['salt'],'ascii')).hexdigest()
            if password_hash == entry['password_hash']:
                print('Success!')
                return True
            else:
                print('Incorrect username of password... Try again!')
                return False
    print('Incorrect username or password... Try again!')
    return False

def prompt_login():
    username = input("Username: ")
    password = getpass.getpass("Password: ").encode()
    if not is_valid_credentials(username, password):
        prompt_login()

def add_user():
    salt = os.urandom(16).hex()

    username = input("What would you like your username to be? ")

    for entry in users:
        if entry['username']==username:
            print("This username is taken by another user. Please pick a new one.")
            add_user()
    password = getpass.getpass("What would you like your password to be? ").encode()
    password_hash = hashlib.sha256(password+bytes(salt,'ascii')).hexdigest()

    write_json(username, password_hash, salt)
    
    for entry in users:
        print(entry['username'])

def remove_user(username, password):
    for entry in users:
        if entry['username']==username:
            if entry['password_hash'] == hashlib.sha256(password + bytes(entry['salt'],'ascii')).hexdigest():
                users.remove(entry)
                print('User removed.\n')


def write_json(usrnm, pwd_hash, slt):
    file = open(userDB,'w')
    print(users)
    dic = dict(username = usrnm, password_hash = pwd_hash, salt = slt)
    print(dic)
    users.append(dic)
    outfile = json.dumps(users, indent=4)
    file.write(outfile)
    file.close()

def main():
    prompt = input("What would you like to do? (login (l), add user(a), remove user(r), quit(q)) ")

    match prompt:
        case 'l':
            prompt_login()
            main()
        case 'a':
            add_user()
            main()
        case 'q':
            quit()
        case 'r':
            username = input('Enter the username of the user you would like to remove: ')
            password = getpass.getpass('Enter the password of the user you would like to remove: ').encode()
            remove_user(username, password)
            main()
        case _:
            print('Input not recognized. Please try again.')
            main()

main()