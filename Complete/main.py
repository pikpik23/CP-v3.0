'''Main Program'''
from sheetsBackend import init, editTable, append, printValues


def main():

    data = [["fred", 123],
            ["john", 453],
            ["Bob", 567]]

    editTable(data)
    append(data)
    printValues()

    # Do something


if __name__ == '__main__':
    init()  # Must always be run first
    main()
