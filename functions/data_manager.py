
# Data Management
#    Reads and writes data to the data folder

# Local Modules
import file_manager as FM
import logical_procedures as LP

# NonLocal Modules
import datetime

# Gather data paths at position
def gather_paths(position):
    # cd to position and gather log paths and strengths
    FM.change_directory('data/' + position)
    paths = FM.get_all('notes')

    # separate paths information by comma and put into list
    for i in range(0,len(paths)):
        paths[i] = paths[i].split(',')
        paths[i].insert(2,i)
        for n in range(0, len(paths[i])):
            paths[i][n] = int(paths[i][n])

    # find number of layers position is from data folder
    layers = LP.folder_layers(position)

    # cd back to logs folder (could be any of the ordered data folders)
    FM.change_directory('../' * layers + 'ordered/logs/')
    # get all file names in logs folder
    file_names = FM.list_files()

    # find number in each file name (take out .txt and convert to int)
    for i in range(0,len(file_names)):
        for n in range(0,len(file_names[i])):
            if file_names[i][n] == '.':
                file_names[i] = int(file_names[i][:n])
                break

    # file_paths is for knowing the filename for the first
    file_paths = []
    log_paths = []

    # store each necessary file name in file_paths
    for i in range(0,len(file_names)):
        for n in range(0,len(paths)):
            if paths[n][0] == file_names[i]:
                file_paths.append(file_names[i])
                break

    # setup log_paths for each file in file_paths
    for i in range(0,len(file_paths)):
        log_paths.append([])

    # organize log and strength with their respective file
    for i in range(0,len(file_paths)):
        for n in range(0,len(paths)):
            if paths[n][0] == file_paths[i]:
                log_paths[i].append([paths[n][1], paths[n][2], paths[n][3]])

    # cd back to bumplog folder
    FM.change_directory('../../../')

    return file_paths, log_paths


# Gather logs from ordered data
def gather_logs(file_paths, log_paths):
    # cd to logs folder
    FM.change_directory('data/ordered/logs/')
    logs = []
    for i in range(0,len(file_paths)):
        gathered_data = FM.get_all(str(file_paths[i]))
        for n in range(0,len(log_paths[i])):
            path = log_paths[i][n][0]
            log = gathered_data[path]
            index = log_paths[i][n][1]
            bump = log_paths[i][n][2]
            # For each log, holds the string, and index at notes.txt file, bump count
            logs.append([log,index,bump])
            print(gathered_data[path])
    FM.change_directory('../../../')
    return logs

# ----------------------------------------------------- #

# Add 1 to the bump count of a log
def bump_log(position, index):
    FM.change_directory('data/' + position)
    file_line = FM.get_substring('notes', index)
    count = 0
    for i in range(0,len(file_line)):
        if file_line[i] == ',':
            count += 1
            if count == 2:
                bump_count = int(file_line[i+1:]) + 1
                FM.edit_substring('notes', index, file_line[:i+1] + str(bump_count))
                break
    layers = LP.folder_layers(position)
    FM.change_directory('../' * (layers + 1))


def new_log(position, log):
    #
    FM.change_directory('data/ordered/logs/')
    #Find the
    files = FM.list_files()
    file_chsn = 0
    for i in range(0,len(files)):
        for n in range(0,len(files[i])):
            if files[i][n] == '.':
                file_num = int(files[i][:n])
                if file_num > file_chsn:
                    file_chsn = file_num
    if FM.file_length(str(file_chsn)) == 10:
        file_chsn += 1
    FM.append_substring(str(file_chsn), log)
    #
    FM.change_directory('../dates/')
    FM.append_substring(str(file_chsn), get_time())
    FM.change_directory('../coord/')
    # WILL BE EDITED IN FUTURE
    FM.append_substring(str(file_chsn), '40.5698452,-105.10956120000003')
    index = FM.file_length(str(file_chsn)) - 1
    FM.change_directory('../../' + position)
    FM.append_substring('notes', str(file_chsn) + ',' + str(index) + ',0')
    # go to main directory
    FM.change_directory('../' * (LP.folder_layers(position) + 1))



# ------------------------------------------------------ #

def log_position(position, index):
    FM.change_directory('data/' + position)
    position = []
    log_data = FM.get_substring('notes', index)
    for i in range(1, (len(position) - 1)):
        if log_data[-i] == ',':
            position = log_data[:-i].split(',')
            break
    # go to main directory
    FM.change_directory('../' * (LP.folder_layers(position) + 2))
    return position

def get_time():
    now = datetime.datetime.now()
    return(now.strftime('%m/%d/%Y %H:%M'))
