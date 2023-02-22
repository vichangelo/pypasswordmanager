import login
import ops


print("Welcome to the encrypted password manager written in python!")

user = login.input_user()
if login.is_new_user(user):
    login.write_new_user(user)
    master_password = login.create_master_password()
else:
    master_password = input("Please enter your super secret master "
                            + "password.\n")
user_salt = login.get_user_salt(user)
print("Success! You're in!")

while True:
    decrypted_passwords = ops.read_passwords(user, master_password,
                                             user_salt)
    ops.display_passwords(decrypted_passwords)
    decision = input("Now input C to create a new password or D to "
                     + "delete a password.\n")

    if decision == "C":
        service_password = ops.input_new_password()
        ops.write_new_password(user, service_password, master_password,
                               user_salt)

    if decision == "D":
        service = input("Enter the name of the service you want to delete "
                        + "the password from.\n")
        remaster_password = input("Now confirm your master password.")
        if remaster_password == master_password:
            ops.delete_password(user, service, decrypted_passwords)
        else:
            print("Incorrect master password.")


exit()
