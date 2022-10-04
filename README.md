# Password Manager
#### Video Demo:  <https://youtu.be/yBkXtMQIBHU>


## Introduction:

For my final cs50 project I have coded a CLI application which allows the user to record all their passwords. The task seemed daunting at first as I had no idea Where to start and what techniques to do. I was inspired to do this projecet by a youtuber who was talking about python projects. The application is actually very practical and functions as an effecient way to store different account passwords incase the user forgets.

## Main Features:

- Password protected access
- Add a new password with 3 fields (email, password and site)
- Display all passwords
- Password generators
- UI costumization using settings

## Road Map 

For this project I was met with many challanges and was lucky to have an excellent foundation through the course which armed with the sufficient knowledge to approach this project head on. Furthermore, my coding journey was the following:

- Brain Storming the main idea
- Preparing my workspace for the project
- Abstracting concepts into smaller units so that am able to focus on one task at a time
- Coding the login screen
- Coding the main menu 
  - Adding the features until everything was done
- testing the code for bugs and corner cases 

## My code

For my code I intially followed the cs50 recommended format of having a main fuction and a minimum of 3 custom functions. As the coding progressed I had many more custom functions:

- add a record function 
```
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
```
- display with tabulate function
```
def display_with_tabulate(records: list[dict[str]], I) -> None:
    """
    displays a list of dictionaries in a comprehenisble form for the user.
    params
    :records: the list of dicts containing the account information.
    """
    display_list = [[val for i, val in x.items()] for x in records]
    print(tabulate(display_list, headers=FIELDNAMES, tablefmt=table_formats[I]))


```
- filter records function 
```
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

```
- get records function
```
def get_records():
    """
    Gets all the records stored in the database.
    """
    with open(passwords_database_path, "r") as f:
        csvread = csv.DictReader(f)
        all_records = [x for x in csvread]
        return all_records

```
- save theme function 
```
def save_theme(index: int):
    """ 
    saves the selected table theme to prefrences.txt
    params:
    :index: the index of theme to be saved
     """
    with open("prefrences.txt", "w") as pref:
        pref.write(str(index))

```
- get status function
```
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
```
- password generator function
```
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

```
