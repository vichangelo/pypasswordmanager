import os
import crypto


def input_new_password():
    new_service = input("Please write the name of the service of the new "
                        + "password.\n")
    while True:
        new_password = input("Now write the new password.\n")
        renew_password = input("Please confirm the password.\n")
        if new_password == renew_password:
            break
        else:
            print("Inconsistency detected, try again.")
    return new_service + ":" + new_password


def write_new_password(user, service_password, master_password, salt):
    service_password = service_password.encode("utf-8")
    encrypted_password = crypto.fernet_encrypt(service_password,
                                               master_password, salt)

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "passwords/" + user + ".txt")

    with open(filename, "ab") as passwords_file:
        passwords_file.write(encrypted_password + "\n".encode("utf-8"))
    return


def read_passwords(user, master_password, salt):
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
    print("Here are your registered passwords:")
    for item in decrypted_passwords:
        service = str(item).split(":")[0][2:]
        password = str(item).split(":")[1][:-1]
        display_string = service + password.rjust(50 - len(service), ".")
        print(display_string)
    return

def delete_password(user, service, decrypted_passwords):
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
