"""Module containing the login functions.

Imports
-------
:mod:`os`: for salt generation (:func:`os.urandom`).

:mod:`datahelper`: for getting data file paths.

Functions
---------
:func:`first_login`: create a users file.

:func:`user_input`: receive which user the session is for.

:func:`is_new_user`: check for a new user.

:func:`write_new_user`: write new user and salt to disk.

:func:`get_user_salt`: get user's salt from disk.
"""
import os
import pypasswordmanager.datahelper as datahelper


def first_login():
    """Create a users file if this is the first use of the app."""
    users_path = datahelper.get_file_path("users.txt")
    if os.path.exists(users_path):
        return
    else:
        users_file = open(users_path, "x")
        users_file.close()
        return


def user_input() -> str:
    """Receive input for username.

    Receives input from user to determine username for the session.
    Contains a loop executed while the username is not at least 4
    characters long. Returns username.

    :return: the username for the session.
    :rtype: str
    """
    while True:
        user = input("Insert your username, or a new one to create it. ")
        if len(user) < 4:
            print("User too short, please input at least 4 characters!")
        else:
            break
    return user


def is_new_user(user: str) -> bool:
    """Check if username belongs to existing user or not.

    Reads the users file and checks if the username is in it.

    :returns: if the username is new or not.
    :rtype: bool
    """
    users_path = datahelper.get_file_path("users.txt")
    with open(users_path, "rb") as users_file:
        users_content = str(users_file.read())
        if user in users_content:
            return False
        else:
            return True


def write_new_user(user: str):
    """Write new user information to disk.

    Generates random salt using `os` library, opens users file in binary
    mode and writes salt and username as a pair. Then, creates file for
    user passwords in password folder.

    :param user: username.
    :type user: str
    :var salt: user's salt.
    :type salt: bytes
    """
    salt = os.urandom(32)
    users_path = datahelper.get_file_path("users.txt")
    with open(users_path, "ab") as users_file:
        user_string = (user + ":").encode("utf-8")
        users_file.write(user_string + salt + "\n".encode("utf-8"))

    password_path = datahelper.get_file_path(user + ".txt")
    f = open(password_path, "x")
    f.close()
    return


def create_master_password() -> str:
    """Receive input of a new master password for the session.

    Uses a while loop to ensure the user creates a password at least
    8 characters long, then returns the password for use in the
    session.

    :return: the new master password.
    :rtype: str
    """
    while True:
        master_password = input(
            "Now, please input your master password. "
            + "Don't worry, it won't be stored. Just "
            + "pick one you will remember with at "
            + "least 8 characters! "
        )
        if len(master_password) < 8:
            print("Master password too short, try again!")
        else:
            break
    remaster_password = input("Please confirm the password. ")

    while master_password != remaster_password:
        master_password = input(
            "Sadly, you got it wrong. Please "
            + "input a master password again. "
        )
        remaster_password = input("Please confirm the password. ")
    return master_password


def get_user_salt(user: str) -> bytes:
    """Retrieve user's salt from file in binary mode."""
    users_path = datahelper.get_file_path("users.txt")
    with open(users_path, "rb") as users_file:
        for line in users_file.readlines():
            if user.encode("utf-8") in line:
                user_salt = line[len(user) + 1 : -1]
    return user_salt
