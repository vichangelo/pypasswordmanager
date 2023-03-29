"""Module containing the login functions.

Imports
-------
:mod:`os`: for salt generation (``os.urandom``) and path functions.

Functions
---------
:func:`input_user`: receives which user the session is for.

:func:`is_new_user`: check for a new user.

:func:`write_new_user`: write new user and salt to disk.

:func:`get_user_salt`: get user's salt from disk.
"""
import os


def input_user():
    """Receive input for username.

    Receives input from user to determine username for the session.
    Contains a loop executed while the username is not at least 4
    characters long. Returns username.

    :return: the username for the session.
    :rtype: string
    """
    while True:
        user = input("Insert your username, or a new one to create it. ")
        if len(user) < 4:
            print("User too short, please input at least 4 characters!")
        else:
            break
    return user


def is_new_user(user):
    """Check if username belongs to existing user or not.

    Reads the users file and checks if the username is in it.

    :returns: if the username is new or not.
    :rtype: bool
    """
    with open("users.txt", "rb") as users_file:
        users_content = str(users_file.read())
        if user in users_content:
            return False
        else:
            return True


def write_new_user(user):
    """Write new user information to disk.

    Generates random salt using `os` library, opens users file in binary
    mode and writes salt and username as a pair. Then, creates file for
    user passwords in password folder.

    :param user: username.
    :type user: string
    :var salt: user's salt.
    :type salt: bytes
    """
    salt = os.urandom(32)
    with open("users.txt", "ab") as users_file:
        user_string = (user + ":").encode("utf-8")
        users_file.write(user_string + salt + "\n".encode("utf-8"))

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "passwords/" + user + ".txt")
    f = open(filename, "x")
    f.close()
    return


def create_master_password():
    """Receive input of a new master password for the session.

    Uses a while loop to ensure the user creates a password at least
    8 characters long, then returns the password for use in the
    session.

    :return: the new master password.
    :rtype: string
    """
    while True:
        master_password = input("Now, please input your master password. "
                                + "Don't worry, it won't be stored. Just "
                                + "pick one you will remember with at "
                                + "least 8 characters! ")
        if len(master_password) < 8:
            print("Master password too short, try again!")
        else:
            break
    remaster_password = input("Please confirm the password. ")

    while master_password != remaster_password:
        master_password = input("Sadly, you got it wrong. Please "
                                + "input a master password again. ")
        remaster_password = input("Please confirm the password. ")
    return master_password


def get_user_salt(user):
    """Retrieve user's salt from file in binary mode."""
    with open("users.txt", "rb") as users_file:
        for line in users_file.readlines():
            if user.encode("utf-8") in line:
                user_salt = line[len(user)+1:-1]
    return user_salt
