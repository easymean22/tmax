import os
import sys

def findIndex():
    # snmpwalk.py -> current_status -> findIndex()
    # result = ['index', 'interface_description']
    result = []
    sys.path.append(os.path.dirname(__file__))
    f = open('../current_status', 'r')
    lines = f.readlines()
    for line in lines:
        if line.startswith('1.3.6.1.2.1.2.2.1.2.'):
            key, value = line.split(' = ')
            key = key.replace('1.3.6.1.2.1.2.2.1.2.','')
            value = value.replace('\n','')
            result.append([key, value])
    return result

if __name__ == "__main__":
    print(findIndex())


