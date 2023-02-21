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
    with open("users.txt", "r", encoding="utf-8") as users_file:
        users_content = users_file.read()
        if user in users_content:
            return False
        else:
            return True


def write_new_user(user):
    with open("users.txt", "a", encoding="utf-8") as users_file:
        users_file.write(user + ":")
    return


def input_master_password():
    while True:
        master_password = input("Now, please input your master password. "
                                + "Don't worry, it will be encrypted, just "
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


def create_master_key(master_password):
    master_key = crypto.generate_master_key(master_password)
    with open("users.txt", "a", encoding="utf-8") as users_file:
        users_file.write(str(master_key) + "\n")
    return


def get_user_key(user):
    with open("users.txt", "r", encoding="utf-8") as users_file:
        for line in users_file.readlines():
            if user in line:
                user_key = line[len(user)+1:-1]
    return user_key


def verify_user_key(user_key):
    i = 0
    while i < 5:
        input_key = input("Now please insert your master password to access "
                          + "the manager.\n")
        verified_key = crypto.generate_master_key(input_key)
        if str(user_key) == str(verified_key):
            return True
        else:
            print("This try failed.")
        i += 1
    print("Too many failures, please try another username.")
    return False


def login():
    while True:
        user = input_user()
        if is_new_user(user):
            write_new_user(user)
            master_password = input_master_password()
            create_master_key(master_password)
        user_key = get_user_key(user)
        if verify_user_key(user_key):
            break

    print("Success! You're in!")
    return
