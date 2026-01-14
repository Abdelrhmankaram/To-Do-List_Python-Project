# import inquirer

# name = inquirer.List(
#     name="name",
#     message="hello?",
#     choices=[
#         "world",
#         "wrold",
#         "woorld"
#     ]
# )

# if list(inquirer.prompt([name]).values())[0] == "world":
#     print("Correct choice")
# else:
#     print("Incorrect choice")

from User import *

a = Admin("30309201401394", "Abdelrahman", "Karam", "abdelrhmankaram171@gmail.com", "password", "01224386240")

print(Admin_operations.view_all_users())