"""Operations module for pypasswordmanager application.

Imports
-------
:mod:`os`: for path functions.

:mod:`crypto`: for custom cryptographic functions.

Functions
---------
:func:`input_new_password`: receives new password from the user.

:func:`write_new_password`: write new password to disk.

:func:`read_passwords`: get list of decrypted passwords.

:func:`display_passwords`: display the decrypted passwords.

:func:`delete_password`: delete password from disk.
"""
import os
import crypto


def input_new_password():
    """Receive input for a new service-password pair.

    Receives input of the new service, then uses a while loop to confirm
    the password of said service, then returns them as a pair with ":"
    in the middle.

    :return: new service-password pair.
    :rtype: string
    """
    new_service = input("Please write the name of the service of the new "
                        + "password. ")
    while True:
        new_password = input("Now write the new password. ")
        renew_password = input("Please confirm the password. ")
        if new_password == renew_password:
            break
        else:
            print("Inconsistency detected, try again.")
    return new_service + ":" + new_password


def write_new_password(user, service_password, master_password, salt):
    """Write new encrypted service-password pair to disk.

    Encodes the service-password pair to UTF-8 so it can be encrypted,
    then encrypts it using :func:`fernet_encrypt` from :mod:`crypto`
    and finally writes the encrypted password to the user's password
    file.

    :param user: username.
    :type user: string
    :param service_password: service-password pair to be encrypted.
    :type service_password: string
    :param master_password: master password to be used in encryption.
    :type master_password: string
    :param salt: user's salt.
    :type salt: bytes
    """
    service_password = service_password.encode("utf-8")
    encrypted_password = crypto.fernet_encrypt(service_password,
                                               master_password, salt)

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "passwords/" + user + ".txt")

    with open(filename, "ab") as passwords_file:
        passwords_file.write(encrypted_password + "\n".encode("utf-8"))
    return


def read_passwords(user, master_password, salt):
    """Read encrypted passwords from disk and return them decrypted.

    Opens user's passwords file in read-binary mode, transforms the
    lines into a list, iterates through it and decrypts the passwords
    one by one using :func:`fernet_decrypt` from :mod:`crypto`. Then,
    returns the list of decrypted passwords.

    :param user: username.
    :type user: string
    :param master_password: master password to be used in decryption.
    :type master_password: string
    :param salt: user's salt.
    :type salt: bytes
    :return: the list of decrypted passwords.
    :rtype: list of bytes
    """
    decrypted_passwords = []

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "passwords/" + user + ".txt")

    with open(filename, "rb") as passwords_file:
        encrypted_passwords = passwords_file.readlines()
        for password in encrypted_passwords:
            decrypted_password = crypto.fernet_decrypt(password,
                                                       master_password,
                                                       salt)
            decrypted_passwords.append(decrypted_password)
    return decrypted_passwords


def display_passwords(decrypted_passwords):
    """Display decrypted passwords on screen.

    Iterates through the decrypted passwords list, converting the items
    to strings and adjusting them to look nice.

    :param decrypted_passwords: list containing decrypted passwords.
    :type decrypted_passwords: list of bytes
    """
    print("Here are your registered passwords:")
    for item in decrypted_passwords:
        service = str(item).split(":")[0][2:]
        password = str(item).split(":")[1][:-1]
        display_string = service + password.rjust(50 - len(service), ".")
        print(display_string)
    return

def delete_password(user, service, decrypted_passwords):
    """Delete chosen password from disk file.

    Iterates through list of decrypted passwords, grab the index of
    service chosen by the user, then opens password file and, using the
    ``readlines()`` method, stores the passwords in a variable. Then,
    erases the password by using its index and replacing it with an
    empty byte and, finally, write the new lines to file using
    ``writelines()`` method.

    :param user: username.
    :type user: string
    :param service: service's name for the password to be erased.
    :type service: string
    :param decrypted_passwords: decrypted passwords list.
    :type decrypted_passwords: list of bytes
    """
    for decrypted_password in decrypted_passwords:
        if service.encode("utf-8") in decrypted_password:
            index = decrypted_passwords.index(decrypted_password)

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "passwords/" + user + ".txt")

    with open(filename, "rb") as passwords_file:
        password_lines = passwords_file.readlines()
        password_lines[index] = bytes(0)
    with open(filename, "wb") as passwords_file:
        passwords_file.writelines(password_lines)
