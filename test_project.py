from project import add_record,get_records,get_status

def test_add_record():
    assert add_record(email = "someone@gmail.com",password = "password",site= "www.google.com") == None

def test_get_records():
    assert get_records()[0] == {'ID': '1', 'email': 'someone@gmail.com', 'password': 'password', 'site': 'www.google.com'}

def test_get_status():
    assert get_status() == ["7", "✔", "✔", "✔", "✔"]
