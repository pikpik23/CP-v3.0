from app import *

def test_function():
    lname = reset_log()

    path = 'resources/static/LOG_'
    extension = '.db'
    lname = lname.strip(path) # strip the path
    lname = lname.strip(extension) # strip db extension

    try:
        lname = float(lname)
        lname += 1
    except ValueError:
        pass


    new_lname = path+str(lname)+extension

    print(new_lname)


if __name__ == '__main__':
    test_function()