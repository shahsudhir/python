#import the regular expressions
import re   
#take email input form the user   
email= input("Enter the email address: ")
#Initializing validation flag
is_valid=False
#email validation pattern
while True:
    pattern= r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    #check if the email matches the pattern
    if not re.match(pattern,email):
        break
    else:
        is_valid= True
        break
    #print validation result
if is_valid:
    print("email address is valid")
else:
    print("Email address is invalid")


   
    
    