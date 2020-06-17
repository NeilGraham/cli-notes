
# File Manager (FM)
#   For reading from, writing, or appending to files


# NonLocal Modules
import os

# Returns all lines
def get_all(nfile):
    with open(nfile + '.txt', 'r') as f:
        objects = f.readlines()
        for i in range(0, len(objects)):
            objects[i] = objects[i][:-1]
        return objects

# Returns a line with respect to index
def get_substring(nfile, index):
    with open(nfile + '.txt', 'r') as f:
        content = f.readlines()
        return content[index][:-1]

# Returns index of the first line to match a substring parameter
def get_index(nfile, substring):
    with open(nfile + '.txt', 'r') as f:
        content = f.readlines()
        for i in range(0, len(content)):
            if substring == content[i]:
                return i
        return -1

# Appends a new line to a file
def append_substring(nfile, substring):
    with open(nfile + '.txt', 'a') as f:
        f.write(substring + '\n')

# Replaces line at index contents with substring
def edit_substring(nfile, index, substring):
    with open(nfile + '.txt', 'r') as rf:
        entire = rf.read()
        start, end = index_position(entire, index)
        with open(nfile + '.txt', 'w') as wf:
            wf.write(entire[:start] + str(substring) + entire[end:])

# Return the contents of a line while removing that line from the file
def file_pop(nfile, index):
    item = ''
    with open(nfile + '.txt', 'r') as rf:
        entire = rf.read()
        start, end = index_position(entire, index)
        with open(nfile + '.txt', 'w') as wf:
            item = entire[start:end]
            wf.write(entire[:start-1] + entire[end:])
    return item

# ---------------------------------------------- #

# Changes directory (mimics terminal's cd)
def change_directory(ndirectory):
    os.chdir(ndirectory)

# Delete an entire file
def remove_file(nfile):
    os.remove(nfile + '.txt')

# Delete an entire directory along with it's sub-file structure
def remove_directory(ndir):
    os.remove(ndir)

# List all files and folders inside of the current directory
def list_all():
    names = []
    for name in os.listdir('.'):
        names.append(name)
    return names

# List all directories
def list_directories():
    #With respect to current directory, returns
    #a list of all subdirectories
    directories = []
    for name in os.listdir('.'):
        if os.path.isdir(name):
            directories.append(name)
    return directories

# List all files
def list_files():
    files = []
    for name in os.listdir('.'):
        if os.path.isfile(name):
            files.append(name)
    return files

# Return the number of lines in a file
def file_length(nfile):
   with open(nfile + '.txt', 'r') as f:
       return len(f.readlines())

# ---------------------------------------------- #

# Return index of text among potentially multiple lines
def index_position(text, index):
    #Returns the position(index1:index2) of an index
    count = 0
    start = 0
    end = 0
    for i in range(0, len(text)):
        if text[i] == '\n':
        # '\n' is a single character
            if count == index:
                end = i
                return start, end
            count += 1
            if count == index:
                start = i + 1
        else:
            print('\n')
    return -1
