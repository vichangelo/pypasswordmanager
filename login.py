import os
import crypto


def input_user():
    while True:
        user = input("Insert your username, or a new one to create it.\n")
        if len(user) < 4:
            print("User too short, please input at least 4 characters!\n")
        else:
            break
    return user


def is_new_user(user):
    with open("users.txt", "rb") as users_file:
        users_content = str(users_file.read())
        if user in users_content:
            return False
        else:
            return True


def write_new_user(user):
    salt = os.urandom(32)
    with open("users.txt", "ab") as users_file:
        user_string = (user + ":").encode("utf-8")
        users_file.write(user_string + salt + "\n".encode("utf-8"))
    return


def create_master_password():
    while True:
        master_password = input("Now, please input your master password. "
                                + "Don't worry, it won't be stored. Just "
                                + "pick one you will remember with at "
                                + "least 8 characters!\n")
        if len(master_password) < 8:
            print("Master password too short, try again!")
        else:
            break
    remaster_password = input("Please confirm the password.\n")
    
    while master_password != remaster_password:
        master_password = input("Sadly, you got it wrong. Please "
                                + "input a master password again.\n")
        remaster_password = input("Please confirm the password.\n")
    return master_password


def get_user_salt(user):
    with open("users.txt", "rb") as users_file:
        for line in users_file.readlines():
            if user.encode("utf-8") in line:
                user_salt = line[len(user)+1:-1]
    return user_salt
