import inquirer
from Data_Operations import *
from Hashing import *
from Task import *
from User import *
from Flow import Login, Signup
import warnings
warnings.filterwarnings("ignore")

while True:
    import os; os.system('cls' if os.name == 'nt' else 'clear')
    session = inquirer.prompt([inquirer.List(
        name="Log in or Sign up",
        message="Welcome to your To-Do List Application!!",
        choices=["Login", "Sign Up"]
    )])

    if list(session.values())[0] == "Login":
        Login()
    else:
        Signup()