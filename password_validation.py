import re
pwd= input("Enter the password: ")
pwd_len= len(pwd)
is_valid= False

while True:
    if pwd_len < 7 or pwd_len >20: break
    elif not re.search('[A-Z]', pwd): break
    elif not re.search('[a-b]', pwd): break
    elif not re.search('[0-9]', pwd): break
    elif not re.search('[!@#$]',pwd): break
    else:
        is_valid=True
        break
if is_valid:
    print("password is valid")
else:
    print("Password is invalid")
        