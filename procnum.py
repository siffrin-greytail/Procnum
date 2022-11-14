#!/usr/bin/python3
import os
from os import stat
from pwd import getpwuid
import re

# PROCNUM #

def main():

    # File management functions

    def safePrint(content):
        print(content)
        with open('./saved-output.txt', 'a') as outfile:
            print(content, file=outfile)

    def endInput():
        with open('./saved-output.txt', 'a') as outfile:
            outfile.write('\n' + '---end of command---' + '\n')

    # MAIN OPTIONS

    def listProc():
        processes = os.listdir('/proc')
        restricted = set()
        restricted.update(['fs', 'bus', 'irq', 'net', 'sys', 'tty', 'acpi', 'asound', 'driver', 'sysvipc', 'pressure', 'dynamic_debug', 'self', 'thread-self'])
        def findOwner(filename):
            return getpwuid(stat(filename).st_uid).pw_name
        for item in processes:
            if os.path.isdir(os.path.join('/proc', item)):
                if item not in restricted:
                    with open('/proc/' + item + '/cmdline', 'r') as f:
                        commandline = f.read()
                    with open('/proc/' + item + '/comm', 'r') as f :
                        command = f.read()
                    safePrint(item + ' ' + findOwner('/proc/' + item) + ' ' + 'command: ' + command + ' ' + 'cmdline: ' + commandline)
                    safePrint('')

    def listThreads():
        pid = input('Please enter PID: ')
        safePrint('')
        for i in os.listdir('/proc/' + pid + '/task/'):
            with open('/proc/' + pid + '/task/' + i + '/comm', 'r') as f:
                safePrint(i + ' ' + 'command: ' + f.read())

    def listMaps():
        pid = input('Please enter PID: ')
        safePrint('')
        with open('/proc/' + pid + '/maps') as f:
            safePrint(f.read())
        return

    def sharedObjects():
        processes = os.listdir('/proc')
        restricted = set()
        objict = []
        objictset = set()
        restricted.update(['fs', 'bus', 'irq', 'net', 'sys', 'tty', 'acpi', 'asound', 'driver', 'sysvipc', 'pressure', 'dynamic_debug', 'self', 'thread-self'])
        for item in processes:
            if os.path.isdir(os.path.join('/proc', item)) and item not in restricted:
                with open('/proc/' + item + '/maps', 'r') as f:
                    content = f.read()
                splitted = re.split(' |\n', content)
                for item in splitted:
                    if '.so' in item and item not in objictset:
                        objict.append(item)
                        objictset.add(item)
        for item in objict:
            safePrint(item)

    # EXTRA FUNCTIONS

    def saveOutput():
        if 'y' in input('Keep Procnum output file? [yes]/no: '):
            print('')
            print('Output appended to ./saved-output.txt')
            print('')
            return
        else:
            os.remove('./saved-output.txt')
            print('')
            print('The file saved-output.txt has been deleted')
            print('')
            return


    # START OF MAIN FUNCTION!!!

    print('')
    print('██████╗░██████╗░░█████╗░░█████╗░███╗░░██╗██╗░░░██╗███╗░░░███╗')
    print('██╔══██╗██╔══██╗██╔══██╗██╔══██╗████╗░██║██║░░░██║████╗░████║')
    print('██████╔╝██████╔╝██║░░██║██║░░╚═╝██╔██╗██║██║░░░██║██╔████╔██║')
    print('██╔═══╝░██╔══██╗██║░░██║██║░░██╗██║╚████║██║░░░██║██║╚██╔╝██║')
    print('██║░░░░░██║░░██║╚█████╔╝╚█████╔╝██║░╚███║╚██████╔╝██║░╚═╝░██║')
    print('╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░╚════╝░╚═╝░░╚══╝░╚═════╝░╚═╝░░░░░╚═╝')
    print('')

    while True:

        print('####################')
        print('Options: ')
        print('')
        print(' 1) List all running processes')
        print(' 2) List all running threads of a given process')
        print(' 3) Output contents of maps file in given PID')
        print(' 4) List all loaded shared objects within all processes')
        print(' 5) Quit')
        print('')
        option = int(input('Choose Option: '))
        print('')
        if option == 1:
            listProc()
            endInput()
        elif option == 2:
            listThreads()
            endInput()
        elif option == 3:
            listMaps()
            endInput()
        elif option == 4:
            sharedObjects()
            endInput()
        else:
            saveOutput()
            print('Exiting...')
            return
        

if __name__ == '__main__':
    main()