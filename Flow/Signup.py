import inquirer
from User import User_operations
from Data_Validators import user_data_validators

def Signup():
    import os; os.system('cls' if os.name == 'nt' else 'clear')
    questions = [
        inquirer.Text(
            name="ID",
            message="Enter your ID: ",
            validate=lambda answers, current: user_data_validators.validate_id_number(current)
        ),
        inquirer.Text(
            name="fname",
            message="Enter your first name",
            validate=lambda answers, current: user_data_validators.validate_name(current)
        ),
        inquirer.Text(
            name="lname",
            message="Enter your last name",
            validate=lambda answers, current: user_data_validators.validate_name(current)
        ),
        inquirer.Text(
            name="email",
            message="Enter your email",
            validate=lambda answers, current: user_data_validators.validate_email(current)
        ),
        inquirer.Text(
            name="password",
            message="Enter your password"
        ),
        inquirer.Text(
            name="confirm_password",
            message="Confirm your password"
        ),
        inquirer.Text(
            name="mobile",
            message="Enter your mobile number",
            validate=lambda answers, current: user_data_validators.validate_egyptian_mobile(current)
        )
    ]

    answers = inquirer.prompt(questions)

    if answers["password"] != answers["confirm_password"]:
        print("Passwords don't match\n")
        Signup()

    if User_operations.user_exists(answers["email"]):
        print("User Already Exists\n")
        
    else:
        print("User added successfully\n")
        User_operations.insert_user(answers)
    