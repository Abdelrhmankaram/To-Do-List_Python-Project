import inquirer
from User import User, User_operations
from User import Admin
from Data_Validators import user_data_validators
from Flow import User_flow
from Flow import Admin_flow

def Login():
    import os; os.system('cls' if os.name == 'nt' else 'clear')
    questions = [
        inquirer.Text(
            name="email",
            message="Enter your email",
            validate=lambda answers, current: user_data_validators.validate_email(current)
        ),
        inquirer.Password(
            name="password",
            message="Enter your password",
        )
    ]

    answers = inquirer.prompt(questions)

    logged_user = User_operations.check_login(answers["email"], answers["password"])

    if logged_user is not False:
        print("Logged in successfully\n")
        logged_user = logged_user.iloc[0]
        role = logged_user["Role"]

        if role == "User":
            print("Logged in as a user\n")
            user = User(
                str(int(logged_user["ID"])), logged_user["First Name"], logged_user["Last Name"], logged_user["Email"], logged_user["Password"], logged_user["Mobile Number"]
                )
            User_flow.User_flow(user)

        else:
            print("Logged in as an admin\n")
            admin = Admin(
                str(int(logged_user["ID"])), logged_user["First Name"], logged_user["Last Name"], logged_user["Email"], logged_user["Password"], logged_user["Mobile Number"]
                )
            Admin_flow.Admin_flow(admin)
    else:
        print("Invalid email or password\n")
