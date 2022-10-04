import os
import sys
import csv
import time
from tabulate import tabulate
from pyfiglet import Figlet
from numpy import random

FIELDNAMES = ("email", "password", "site")
FIELDNAMES_WITH_ID = ["ID"] + list(FIELDNAMES)
modes = ["password_manager", "password_generator"]
Features = [
    "Add_password",  # completed
    "Search_for_password",  # completed
    "Show_all_passwords",  # completed
    "password_generator",  # completed
    "Settings",  # completed
    "Exit",  # completed
]
passwords_database_path = "./passwords.csv"
password_file = "./password.txt"
generator_config_path = "./pswd_config.txt"
table_formats = [
    "plain",
    "simple",
    "github",
    "grid",
    "fancy_grid",
    "pipe",
    "orgtbl",
    "jira",
    "presto",
    "pretty",
    "psql",
    "rst",
    "mediawiki",
    "moinmoin",
    "youtrack",
    "html",
    "unsafehtml",
    "latex",
    "latex_raw",
    "latex_booktabs",
    "latex_longtable",
    "textile",
    "tsv",
]


def main():
    I = get_theme()  # sets the selected theme for the user

    # Password screen
    os.system("cls" if os.name == "nt" else "clear")
    f = Figlet(font="starwars", width=110)  # ASCII font for mode name
    print(f.renderText("Password\nManager"))  # ASCII font for mode name
    time.sleep(2)

    if not os.path.isfile(passwords_database_path):  # checks if the database exists
        # new user login
        print(
            "The program has detected that this is your first login please"
            " create a pasword:"
        )
        password = input("-->")
        with open(password_file, "w") as infile:
            infile.write(password)
    else:
        # existing user login
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            f = Figlet(font="starwars", width=110)  # ASCII font for mode name
            print(f.renderText("Password\nManager"))  # ASCII font for mode name
            with open(password_file, "r") as p:
                password_record = p.read()
            print("_____________________", "________Login________", sep="\n")
            password = input("Password:")
            if password == password_record:
                break
            else:
                os.system("cls" if os.name == "nt" else "clear")
                f = Figlet(font="starwars", width=110)  # ASCII font for mode name
                print(f.renderText("Password\nManager"))
                print("Please try again.")
                time.sleep(1.5)

    # main menu
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        if not os.path.isfile(passwords_database_path):  # checks if the database exists
            main_menu_list = [
                [i + 1, x]
                for i, x in enumerate(Features)
                if x in ["Add_password", "Settings", "password_generator", "Exit"]
            ]  # shows only four options if the database is not generated yet
        else:
            main_menu_list = [
                [i + 1, x] for i, x in enumerate(Features)
            ]  # shows all the available features if the database exists

        f = Figlet(font="starwars", width=110)  # ASCII font for mode name
        print(f.renderText("Password\nManager"))
        print(
            tabulate(main_menu_list, tablefmt=table_formats[I])
        )  # displays the main menu dinamically using tabluate

        if not os.path.isfile(passwords_database_path):
            try:
                main_menu = int(input("Select using the number of choice: "))
            except ValueError:
                os.system("cls" if os.name == "nt" else "clear")
                print(
                    f"please select {Features.index('Add_password') + 1},{Features.index('password_generator')+1}"
                    f"{Features.index('Settings') + 1} or {Features.index('Exit') + 1}"
                )
                time.sleep(2)
                continue
            else:
                if not main_menu in [
                    Features.index("Add_password") + 1,
                    Features.index("Settings") + 1,
                    Features.index("Exit") + 1,
                    Features.index("password_generator") + 1,
                ]:
                    os.system("cls" if os.name == "nt" else "clear")
                    print(
                        f"please select {Features.index('Add_password') + 1},"
                        f"{Features.index('Settings') + 1} or {Features.index('Exit') + 1}"
                    )
                    time.sleep(2)
                    continue
        else:
            try:
                main_menu = int(input("Select using the number of choice: "))
            except ValueError:
                os.system("cls" if os.name == "nt" else "clear")
                print(f"please select from 1 to {len(Features)}")
                time.sleep(2)
                continue
            else:
                if not 0 < main_menu < len(Features) + 1:
                    os.system("cls" if os.name == "nt" else "clear")
                    print(f"please select from 1 to {len(Features)}")
                    time.sleep(2)
                    continue

        if (
            main_menu == Features.index("Add_password") + 1
        ):  # loads the add password menu
            os.system("cls" if os.name == "nt" else "clear")
            print("Please enter your account info.")
            email = input("Email: ")
            password = input("Password: ")
            site = input("Site: ")
            add_record(email, password, site)

        elif (
            main_menu == Features.index("Search_for_password") + 1
        ):  # loads the search for password menu
            new_field_names = list(FIELDNAMES) + ["<--"]
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                f = Figlet(font="ogre", width=110)  # ASCII font for mode name
                print(f.renderText("Filter mode:"))  # ASCII font for mode name
                print("You can only search by the exact word.")
                field_with_num = [
                    [str(i), f" {x.capitalize()}" + ""]
                    for i, x in enumerate(new_field_names)
                ]  # displays the fields to filter on.
                print(tabulate(field_with_num, tablefmt=table_formats[I]))
                try:
                    field = int(
                        input(
                            "\nPlease select one of the fields to filter (using the number): "
                        )
                    )  # error checking for
                except ValueError:
                    os.system("cls" if os.name == "nt" else "clear")
                    print("You've entered a wrong choice, try again.")
                    time.sleep(2)
                    continue
                if field not in [x for x in range(len(new_field_names))]:
                    print("You've entered a wrong choice, try again.")
                    time.sleep(2)
                    continue
                elif field == 3:
                    break
                else:
                    os.system("cls" if os.name == "nt" else "clear")
                    by = input("Enter exact search: ")
                    filtered_records = filter_records(field=FIELDNAMES[field], by=by)
                    display_with_tabulate(filtered_records, I)
                    back = input("<--")

        elif main_menu == Features.index("password_generator") + 1:
            os.system("cls" if os.name == "nt" else "clear")
            F = Figlet(font="starwars", width=110)  # ASCII font for mode name
            print(F.renderText("Password\nGenerator"))
            input("Press Enter to generate: ")
            animate_loading_pswd_gen()
            os.system("cls" if os.name == "nt" else "clear")
            generated_password = password_generator()
            print(F.renderText("Password\nGenerator"))
            print(generated_password)
            input("\n\n\n\n<--")
            continue

        elif (
            main_menu == Features.index("Show_all_passwords") + 1
        ):  # loads the entire databse stored using tabulate.
            os.system("cls" if os.name == "nt" else "clear")
            all_data = get_records()  # parses the csv file into list of dictionarys.
            display_with_tabulate(
                all_data, I
            )  # displays the list of dictionarys using tabulate theme.
            input("<--")  # allows user to go back after hitting enter

        elif main_menu == Features.index("Exit") + 1:  # leaves the program
            os.system("cls" if os.name == "nt" else "clear")
            sys.exit()

        elif main_menu == Features.index("Settings") + 1:  # loads the settings menu
            settings_menu = [
                [1, "Change login password"],
                [2, "Change grid theme"],
                [3, "Password format"],
                [4, "<--"],
            ]  # opethions in the settings menu
            while True:
                I = (
                    get_theme()
                )  # sets the selected theme for the user (inside the settings menu for emidiate effect.)
                os.system("cls" if os.name == "nt" else "clear")
                print(tabulate(settings_menu, tablefmt=table_formats[I]))
                try:
                    choose = int(
                        input("Choose number: ")
                    )  # error checking for correct input type(int)
                except ValueError:
                    os.system("cls" if os.name == "nt" else "clear")
                    print(
                        f"Please select a number between 1 and {len(settings_menu)}"
                    )  # error message to explain the problem to the user.
                    time.sleep(2)
                    continue
                else:
                    if choose == 1: # change login password
                        with open(password_file, "r") as pass_:
                            pasword_infile = pass_.read()
                        while True:   
                            os.system("cls" if os.name == "nt" else "clear")
                            want = input("Do you want to change your current password (yes/no)?").strip().lower()
                            if not want in ["yes","y","no","n"]:
                                os.system("cls" if os.name == "nt" else "clear")
                                print(f"Please enter one of: ",
                                    *["yes", "y", "no", "n"],
                                    sep="\n",)
                                time.sleep(2)
                                continue
                            if want in ["yes","y"]:
                                current_password = input("Current password: ")
                                if current_password == pasword_infile:
                                    new_password = input("New Password: ")
                                    save_ = input("Are you sure you want to save changes?")
                                    if not want in ["yes","y","no","n"]:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(f"Please enter one of: ",
                                            *["yes", "y", "no", "n"],
                                            sep="\n",)
                                        time.sleep(2)
                                        continue
                                    if want in ["yes","y"]:
                                        animate_loading_screen()
                                        with open(password_file,"w") as file_:
                                            file_.write(new_password)
                                        continue
                                        
                                    else:
                                        continue

                                else:
                                    os.system("cls" if os.name == "nt" else "clear")
                                    print(f"The password you entered is wrong.\nPlease try again.")
                                    time.sleep(2)
                                    continue
                            else:
                                break
                    elif choose == 2:  # directs to the theme selection screen.
                        while True:
                            os.system("cls" if os.name == "nt" else "clear")
                            print(
                                tabulate(
                                    [[i, x] for i, x in enumerate(table_formats)]
                                    + [[23, "<--"]],
                                    tablefmt=table_formats[I],
                                )
                            )  # diplays the available theme options with an exit option.
                            try:
                                choose_theme = int(
                                    input("choose a grid format: ")
                                )  # error checking for input type(int).
                            except ValueError:
                                os.system("cls" if os.name == "nt" else "clear")
                                print(
                                    f"Please enter an integer from 0 to {len(table_formats)+1}"
                                )
                                time.sleep(2)
                                continue
                            else:
                                if choose_theme in [
                                    x for x in range(len(table_formats))
                                ]:  # error checking out of appropriate range.
                                    save_theme(
                                        choose_theme
                                    )  # saves the selected theme in a file for future display.
                                    break
                                elif choose_theme == 23:
                                    break
                                else:
                                    os.system("cls" if os.name == "nt" else "clear")
                                    print(f"Please enter an integer from 0 to 23")
                                    time.sleep(2)
                                    continue
                    elif choose == 3:  # modify properties of the password to be saved.
                        while True:
                            length, lower, upper, num, special = get_status()
                            table_label = ["Stauts", "Applied Format"]
                            os.system("cls" if os.name == "nt" else "clear")

                            print(
                                tabulate(
                                    [
                                        [f"{length}", "length_of_password"],
                                        [f"{lower}", "Lower Case"],
                                        [f"{upper}", "Upper Case"],
                                        [f"{num}", "Numbers"],
                                        [f"{special}", "Special Characters"],
                                    ],
                                    headers=table_label,
                                    tablefmt=table_formats[I],
                                )
                            )
                            prompt = (
                                input("Do you want to modify Yes/No?").lower().strip()
                            )
                            if prompt == "yes" or prompt == "y":
                                os.system("cls" if os.name == "nt" else "clear")
                                print(
                                    "You can modify numerical settings with integers\n"
                                    "and choice with (yes/y) and (no/n)"
                                )
                                time.sleep(3)
                                length_up = input(
                                    tabulate(
                                        [[f"{length}", "length_of_password"]],
                                        headers=table_label,
                                        tablefmt=table_formats[I],
                                    )
                                )
                                try:
                                    if not 0 < int(length_up) < 99:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(f"Please enter a whole number between 1 and 99")
                                        time.sleep(1)
                                        continue

                                except ValueError:
                                    os.system("cls" if os.name == "nt" else "clear")
                                    print(f"Please enter a whole number between 1 and 99")
                                    time.sleep(1)
                                    continue
                                else:
                                    os.system("cls" if os.name == "nt" else "clear")
                                    lower_up = input(
                                        tabulate(
                                            [
                                                [f"{length_up}", "length_of_password"],
                                                [f"{lower}", "Lower Case"],
                                            ],
                                            headers=table_label,
                                            tablefmt=table_formats[I],
                                        )
                                    )
                                    lower_up_disp = (
                                        "✔"
                                        if lower_up == "yes" or lower_up == "y"
                                        else "X"
                                    )
                                    if not lower_up in ["yes", "y", "no", "n"]:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(
                                            f"Please enter one of: ",
                                            *["yes", "y", "no", "n"],
                                            sep="\n",
                                        )
                                        time.sleep(1)
                                        continue
                                    else:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        upper_up = input(
                                            tabulate(
                                                [
                                                    [
                                                        f"{length_up}",
                                                        "length_of_password",
                                                    ],
                                                    [f"{lower_up_disp}", "Lower Case"],
                                                    [f"{upper}", "Upper Case"],
                                                ],
                                                headers=table_label,
                                                tablefmt=table_formats[I],
                                            )
                                        )
                                        upper_up_disp = (
                                            "✔"
                                            if upper_up == "yes" or upper_up == "y"
                                            else "X"
                                        )
                                        if not upper_up in ["yes", "y", "no", "n"]:
                                            os.system("cls" if os.name == "nt" else "clear")
                                            print(
                                                f"Please enter one of: ",
                                                *["yes", "y", "no", "n"],
                                                sep="\n",
                                            )
                                            time.sleep(1)
                                            continue
                                        else:
                                            os.system("cls" if os.name == "nt" else "clear")
                                            num_up = input(
                                                tabulate(
                                                    [
                                                        [
                                                            f"{length_up}",
                                                            "length_of_password",
                                                        ],
                                                        [
                                                            f"{lower_up_disp}",
                                                            "Lower Case",
                                                        ],
                                                        [
                                                            f"{upper_up_disp}",
                                                            "Upper Case",
                                                        ],
                                                        [f"{num}", "Numbers"],
                                                    ],
                                                    headers=table_label,
                                                    tablefmt=table_formats[I],
                                                )
                                            )
                                            num_up_disp = (
                                                "✔"
                                                if num_up == "yes" or num_up == "y"
                                                else "X"
                                            )
                                            if not num_up in ["yes", "y", "no", "n"]:
                                                os.system("cls" if os.name == "nt" else "clear")
                                                print(
                                                    f"Please enter one of: ",
                                                    *["yes", "y", "no", "n"],
                                                    sep="\n",
                                                )
                                                time.sleep(1)
                                                continue
                                            else:
                                                os.system("cls" if os.name == "nt" else "clear")
                                                special_up = input(
                                                    tabulate(
                                                        [
                                                            [
                                                                f"{length_up}",
                                                                "length_of_password",
                                                            ],
                                                            [
                                                                f"{lower_up_disp}",
                                                                "Lower Case",
                                                            ],
                                                            [
                                                                f"{upper_up_disp}",
                                                                "Upper Case",
                                                            ],
                                                            [
                                                                f"{num_up_disp}",
                                                                "Numbers",
                                                            ],
                                                            [
                                                                f"{special}",
                                                                "Special Characters",
                                                            ],
                                                        ],
                                                        headers=table_label,
                                                        tablefmt=table_formats[I],
                                                    )
                                                )
                                                special_up_disp = (
                                                    "✔"
                                                    if special_up == "yes"
                                                    or special_up == "y"
                                                    else "X"
                                                )
                                                if not special_up in ["yes", "y", "no", "n"]:
                                                    os.system("cls" if os.name == "nt" else "clear")
                                                    print(
                                                        f"Please enter one of: ",
                                                        *["yes", "y", "no", "n"],
                                                        sep="\n",
                                                    )
                                                    time.sleep(1)
                                                    continue
                                                else:
                                                    while True:
                                                        os.system("cls" if os.name == "nt" else "clear")
                                                        print(
                                                            tabulate(
                                                                [
                                                                    [
                                                                        f"{length_up}",
                                                                        "length_of_password",
                                                                    ],
                                                                    [
                                                                        f"{lower_up_disp}",
                                                                        "Lower Case",
                                                                    ],
                                                                    [
                                                                        f"{upper_up_disp}",
                                                                        "Upper Case",
                                                                    ],
                                                                    [
                                                                        f"{num_up_disp}",
                                                                        "Numbers",
                                                                    ],
                                                                    [
                                                                        f"{special_up_disp}",
                                                                        "Special Characters",
                                                                    ],
                                                                ],
                                                                headers=table_label,
                                                                tablefmt=table_formats[
                                                                    I
                                                                ],
                                                            )
                                                        )
                                                        save = input(
                                                            "Do you want to save your prefrences?\n"
                                                        )
                                                        if not save in ["yes", "y", "no", "n"]:
                                                            os.system("cls" if os.name == "nt" else "clear")
                                                            print(
                                                                f"Please enter one of: ",
                                                                *[
                                                                    "yes",
                                                                    "y",
                                                                    "no",
                                                                    "n",
                                                                ],
                                                                sep="\n",
                                                            )
                                                            time.sleep(1)
                                                            continue
                                                        if save in ["yes", "y"]:
                                                            os.system("cls" if os.name == "nt" else "clear")
                                                            animate_loading_screen()
                                                            os.system(
                                                                "cls"
                                                                if os.name == "nt"
                                                                else "clear"
                                                            )
                                                            os.system("cls" if os.name == "nt" else "clear")
                                                            print("Saved prefrences.")
                                                            with open(
                                                                generator_config_path,
                                                                "w",
                                                            ) as pen_:
                                                                pen_.writelines(
                                                                    [
                                                                        length_up
                                                                        + "\n",
                                                                        lower_up + "\n",
                                                                        upper_up + "\n",
                                                                        num_up + "\n",
                                                                        special_up,
                                                                    ]
                                                                )

                                                            break
                                                        else:
                                                            break
                            elif prompt == "no" or prompt == "n":
                                break

                            else:
                                os.system("cls" if os.name == "nt" else "clear")
                                print(f"please select yes/y or no/n")
                                time.sleep(2)
                                continue
                    elif choose == 4:  # exits the program
                        break


def add_record(email: str, password: str, site: str):
    """
    this is a funtion wich stores the accounts info as a row in
    a csv file and creates the file if its doesnt exist.
    params:

    :email: this is the email field

    :password: this is the password field

    :site: this is the website field
    """
    with open(passwords_database_path, "a", newline="") as f:
        pen = csv.DictWriter(
            f, fieldnames=FIELDNAMES_WITH_ID
        )  # creating Dictwriter object

        csvread = open(passwords_database_path, "r")
        if (
            not csvread.readline()
        ):  # checking if the database is empty if so write the headings
            pen.writeheader()
        csvread.close()

        csvread = open(passwords_database_path, "r")
        read = csv.DictReader(csvread, FIELDNAMES_WITH_ID)
        id_num = list()
        for _ in read:
            line = read.line_num
            id_num.append(line)
        try:
            ID = id_num[-1]
            pen.writerow({"ID": ID, "email": email, "password": password, "site": site})
        except IndexError:
            pen.writerow({"ID": 1, "email": email, "password": password, "site": site})

        csvread.close()


def display_with_tabulate(records: list[dict[str]], I) -> None:
    """
    displays a list of dictionaries in a comprehenisble form for the user.
    params
    :records: the list of dicts containing the account information.
    """
    display_list = [[val for i, val in x.items()] for x in records]
    print(tabulate(display_list, headers=FIELDNAMES, tablefmt=table_formats[I]))


def filter_records(field: str, by: str) -> list:
    """
    Filters the entire database for exact matches
    """
    with open(passwords_database_path, "r") as f:
        database = csv.DictReader(f)
        filter_func = lambda x: True if x[field] == by else False
        matches = filter(filter_func, database)
        matches = [x for x in matches]
        return matches


def get_records():
    """
    Gets all the records stored in the database.
    """
    with open(passwords_database_path, "r") as f:
        csvread = csv.DictReader(f)
        all_records = [x for x in csvread]
        return all_records


def save_theme(index: int):
    """ 
    saves the selected table theme to prefrences.txt
    params:
    :index: the index of theme to be saved
     """
    with open("prefrences.txt", "w") as pref:
        pref.write(str(index))


def get_theme() -> int:
    """ 
    retrieves the saved theme from the prefrences.txt file 
    if the request failed it returns a defualt of 4.
     """
    try:
        with open("prefrences.txt", "r") as reading:
            return int(reading.read())
    except (ValueError, FileNotFoundError):
        return 4


def get_status():
    """ 
    gets the password generator settings saved in the pswd_config.txt file 
    if the request fails a defualt value is returned.
     """
    try:
        with open(generator_config_path, "r") as inside:
            x = inside.readlines()
            x = map(lambda x: x.replace("\n", ""), x)
            x = list(x)
            length = [x[0]]
            temp = x[1:]
            temp = map(lambda x: "✔" if (x == "yes" or x == "y") else "X", temp)
            return length + list(temp)

    except FileNotFoundError:
        return ["7", "✔", "✔", "✔", "✔"]


def password_generator() -> str:
    """
    generates a password of length n (number of letters) and using a
    password pool determined by the user.
    First the function tries to access the config file if it fails it loads the default
    the attribs are processed to become boolean and int and is then used to generate the
    final password depending on the configurations chosen by the user.
    """
    try:
        with open(generator_config_path, "r") as f:
            x = f.readlines()
            x = map(lambda x: x.replace("\n", ""), x)
            x = list(x)
            length = x[0]
            lower, upper, number, special = x[1:]
    except FileNotFoundError:
        length, lower, upper, number, special = "7", "yes", "yes", "yes", "yes"

    temp = [lower, upper, number, special]
    temp = map(lambda x: x == "yes" or x == "y", temp)
    temp = list(temp)

    pass_format = {
        "lower_alpha": "abcdefghijklmnopqrstuvwxyz",
        "upper_alpha": "abcdefghijklmnopqrstuvwxyz".upper(),
        "special_chars": r"!@#$%^&*()<>,./?~=-",
        "numbers": "0123456789",
    }

    password_pool = (
        pass_format["lower_alpha"] * temp[0]
        + pass_format["upper_alpha"] * temp[1]
        + pass_format["numbers"] * temp[2]
        + pass_format["special_chars"] * temp[3]
    )

    final_pass = ""
    try:
        for _ in range(int(length)):
            choice_ = random.choice(list(password_pool))
            final_pass += choice_
    except ValueError:
        return "You havent picked any prefrences!"
    else:
        return final_pass


def animate_loading_screen():
    frames = [
        "🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥 0%",
        "🟩🟥🟥🟥🟥🟥🟥🟥🟥🟥 10%",
        "🟩🟩🟥🟥🟥🟥🟥🟥🟥🟥 20%",
        "🟩🟩🟩🟥🟥🟥🟥🟥🟥🟥 30%",
        "🟩🟩🟩🟩🟥🟥🟥🟥🟥🟥 40%",
        "🟩🟩🟩🟩🟩🟥🟥🟥🟥🟥 50%",
        "🟩🟩🟩🟩🟩🟩🟥🟥🟥🟥 60%",
        "🟩🟩🟩🟩🟩🟩🟩🟥🟥🟥 70%",
        "🟩🟩🟩🟩🟩🟩🟩🟩🟥🟥 80%",
        "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟥 90%",
        "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 100%",
    ]
    for frame in frames:
        os.system("cls" if os.name == "nt" else "clear")
        print(frame)
        time.sleep(0.1)
    os.system("cls" if os.name == "nt" else "clear")
    print("DONE!")
    time.sleep(0.5)

def animate_loading_pswd_gen():
    frames = [
        "🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥 0%",
        "🟩🟥🟥🟥🟥🟥🟥🟥🟥🟥 10%",
        "🟩🟩🟥🟥🟥🟥🟥🟥🟥🟥 20%",
        "🟩🟩🟩🟥🟥🟥🟥🟥🟥🟥 30%",
        "🟩🟩🟩🟩🟥🟥🟥🟥🟥🟥 40%",
        "🟩🟩🟩🟩🟩🟥🟥🟥🟥🟥 50%",
        "🟩🟩🟩🟩🟩🟩🟥🟥🟥🟥 60%",
        "🟩🟩🟩🟩🟩🟩🟩🟥🟥🟥 70%",
        "🟩🟩🟩🟩🟩🟩🟩🟩🟥🟥 80%",
        "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟥 90%",
        "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 100%",
    ]
    for frame in frames:
        os.system("cls" if os.name == "nt" else "clear")
        F = Figlet(font="starwars", width=110)  # ASCII font for mode name
        print(F.renderText("Password\nGenerator"))
        print(frame)
        time.sleep(0.1)
    os.system("cls" if os.name == "nt" else "clear")
    print(F.renderText("Password\nGenerator"))
    print("DONE!")
    time.sleep(0.5)

def display_password_generator():
    os.system("cls" if os.name == "nt" else "clear")
    F = Figlet(font="starwars", width=110)  # ASCII font for mode name
    print(F.renderText("Password\nGenerator"))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        os.system("cls" if os.name == "nt" else "clear")
        sys.exit()


# account storage system with a password generator
