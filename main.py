import functions
l = 10

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_path = 'data.txt'
    data = functions.openfile(file_path)
    print(functions.preproccesing(data,l))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
