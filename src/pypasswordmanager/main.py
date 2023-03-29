"""Script that runs the pypasswordmanager application.

Imports
-------
:mod:`login`: import login functions.

:mod:`ops`: import manager operations.

Global variables
----------------
.. data:: user
   :type: string

   Stores username for the session.

.. data:: master_password
   :type: string

   Stores master password for the session.

.. data:: user_salt
   :type: bytes

   Stores the user's salt for the session's cryptographic operations.

.. data:: decrypted_passwords
   :type: list of bytes

   Stores the user's decrypted passwords for the session's display.

.. data:: service_password
   :type: string

   Stores new password to be encrypted.
"""
import pypasswordmanager.login as login
import pypasswordmanager.ops as ops


def run():
    print("Welcome to the encrypted password manager written in python!")

    user = login.user_input()
    if login.is_new_user(user):
        login.write_new_user(user)
        master_password = login.create_master_password()
    else:
        user_salt = login.get_user_salt(user)
        while True:
            master_password = input(
                "Please enter your super secret master password. "
            )
            try:
                decrypted_passwords = ops.read_passwords(
                    user, master_password, user_salt
                )
            except:
                print("Wrong master password, please try again!")
            else:
                break
        print("Success! You're in!")

    while True:
        decrypted_passwords = ops.read_passwords(
            user, master_password, user_salt
        )
        ops.display_passwords(decrypted_passwords)
        decision = input(
            "Now input A to add a new password, D to "
            "delete a password or E to exit. "
        )

        if decision == "A":
            service_password = ops.new_password_input()
            ops.write_new_password(
                user, service_password, master_password, user_salt
            )

        if decision == "D":
            service = input(
                "Enter the name of the service you want to delete "
                "the password from. "
            )
            remaster_password = input("Now confirm your master password. ")
            if remaster_password == master_password:
                ops.delete_password(user, service, decrypted_passwords)
            else:
                print("Incorrect master password.")

        if decision == "E":
            break

    return
