import os
from datetime import datetime as dt

def saveToFile(data):
    f = open('replay/' + dt.now().__str__() + '.txt', 'w')
    for i in range(len(data)):
        if data[i] == None:
            f.write('\n')
        else:
            f.write(data[i] + '\n')
    f.close()

def replays():
    files = os.listdir('replay')
    print()
    for i in range(len(files)):
        print(i + 1, files[i])

    numReplay = int(input('\nNumber '))
    if numReplay == 0 or numReplay > len(files):
        return None
    else:
        file = files[numReplay - 1]
        f = open('replay/' + file, 'r')
        return list(f.readlines())