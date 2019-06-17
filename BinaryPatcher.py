#!/usr/bin/python3
from pathlib import Path
from os import walk
from re import finditer
from types import MethodType
from random import choice

def readBinaryFile( path ):


    filename = Path( path ).resolve()
    print( "Opening file: {}".format(filename) )

    o = ''
    try:
        with open( filename, "rb") as f:
            o = f.read()
        return bytes(o)
    except Exception as e:
        return None

def printDirectory(path):

    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        break

    for filename in filenames:
        print( "  • {}".format( filename ) )

    print( "" )

def printError(msg):
    print( "[ERROR] {}".format(msg) )

def findMultiple(s, c):
    X = [ m.start() for m in finditer(c, s)]
    print( "Index found: {}".format( X ) )
    return X

    # return [pos for pos, char in enumerate(s) if char == c]

def editBinary(raw_binary):

    find_this = input("Find hex (Ex: caf3b4be ): ").replace(" ", "").lower()
    try:
        find_this_raw = bytes.fromhex( find_this )
    except Exception as e:
        print( "[EXCEPTION] Hex string not valid. {}".format(e) )
        return raw_binary

    if len(find_this_raw) == 0:
        print( "Empty string..." )
        return raw_binary

    indexes_result = findMultiple(raw_binary, find_this_raw)
    if len(indexes_result) > 1:
        print( "Found {} results... Search more bytes.".format( len(indexes_result) ) )
        return raw_binary
    elif len(indexes_result) == 0:
        print( "No results for \"{}\" in binary...".format( find_this ) )
        return raw_binary

    index_result = indexes_result[0]

    chunk_before = raw_binary[:index_result]
    chunk_after = raw_binary[ index_result + len(find_this_raw) : ]

    # print( chunk_before )
    # print( chunk_after )


    print( "Found \"{}\" at index {}".format( find_this, index_result ) )
    new_chunk = input("Replace chunk with?  (Ex: de4dbe3f )\n> ").replace(" ", "").lower().strip()


    # o = ''
    # try:
    #     with open( filename, "rb") as f:
    #         o = f.read()
    #     return bytes(o)
    # except Exception as e:
    #     return None
    try:
        new_chunk_raw = bytes.fromhex( new_chunk )
    except Exception as e:
        print( "[EXCEPTION] Hex string not valid. {}".format(e) )
        return raw_binary



    if len(new_chunk_raw) != len(find_this_raw):

        print("Length of new binary will be different?")
        if len(new_chunk_raw) > len(find_this_raw):
            print( "New binary will be {} bytes bigger.".format( len(new_chunk_raw) - len(find_this_raw) ) )
        else:
            print( "New binary will be {} bytes shorter.".format( len(find_this_raw) - len(new_chunk_raw) ) )

        inputChoice = input( "Are you sure to replace (N/y)?\n> " )
        confirm_sure = not (inputChoice == 'y')

        if confirm_sure:
            print( "Ok. Current update is discarted." )
            return raw_binary

        print( "Replacing \"{}\" with \"{}\".".format( find_this, new_chunk ) )

    final_raw = chunk_before + new_chunk_raw + chunk_after

    # print(  len(raw_binary) )
    # print(  len(final_raw) )



    # print( raw_binary[index_result:index_result+5] )


    return final_raw

def RandomString(l = 5):
    return ''.join( [ choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for _ in range(l) ] )


banner = """ ____  _                          _____      _       _
|  _ \(_)                        |  __ \    | |     | |
| |_) |_ _ __   __ _ _ __ _   _  | |__) |_ _| |_ ___| |__   ___ _ __
|  _ <| | '_ \ / _` | '__| | | | |  ___/ _` | __/ __| '_ \ / _ \ '__|
| |_) | | | | | (_| | |  | |_| | | |  | (_| | || (__| | | |  __/ |
|____/|_|_| |_|\__,_|_|   \__, | |_|   \__,_|\__\___|_| |_|\___|_|
                           __/ |
                          |___/                                      \n"""


def Main():

    current_dir_obj = Path( '.' ).resolve()
    current_dir = str(current_dir_obj) + '/'

    print( banner )

    print( "Current directory: {}\n".format( current_dir ) )
    printDirectory( current_dir_obj )

    path_file = input('Insert path: ').strip()


    original_binary = readBinaryFile( path_file )

    if original_binary is None:
        printError("File can\'t be read or file not found.")
        exit()

    original_length = len(original_binary)

    if original_length == 0:
        print("Empty file.")
        exit()


    print( "File is {} bytes long.".format(original_length) )

    raw_binary = original_binary
    other_patches = True
    while other_patches:

        raw_binary = editBinary( raw_binary )

        inputChoice = input('Do you need to change other bytes? (Y/n)\n> ').lower().strip()
        other_patches = not (inputChoice == 'n')

    if raw_binary == original_binary:
        print( "No changes." )
        exit()

    while True:
        inputChoice = input( "Save updates? (Y/n)" )
        save_it = not (inputChoice == 'n')

        if not save_it:
            inputChoice = input( "Are you sure? (N/y)" )
            confirm_sure = not (inputChoice == 'y')

            if not confirm_sure:
                print( "Ok. I don't save any changes.\nBye." )
                exit()

        else:
            break

    print( "Let's save changes." )

    backup_path = path_file + '_' + RandomString() + '.BAK'

    if save_it:
        print( "Opening file \"{}\"".format(path_file) )
        with open( path_file , 'wb' ) as f_out:
            print( "Opening backup file \"{}\"".format(backup_path) )
            with open( backup_path, 'wb' ) as f_out_bak:
                f_out.write( raw_binary )
                f_out_bak.write( original_binary )

        print( "Updates are written in \"{}\".\nBackup file is \"{}\"".format(path_file, backup_path ) )

    return

if __name__ == '__main__':
    try:
        Main()
    except KeyboardInterrupt as e:
        print("")
        exit()
