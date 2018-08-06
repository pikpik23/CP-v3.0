'''Main Program'''
from sheetsBackend import init, editTable, append, printValues


def main():
    '''Edit this to change the program.'''
    data = [["fred", 1],
            ["john", 2],
            ["Bob", 3]]

    append(data)
    printValues()

    # Do something


if __name__ == '__main__':
    init()  # Must always be run first
    main()
