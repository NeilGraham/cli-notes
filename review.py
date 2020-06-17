
# Review Module
#   Reviews Logs of Information Non-Linearly


# Local Modules
from functions import data_manager as DM
from functions import logical_procedures as LP
from functions import user_interface as UI
from functions import input_manager as IM

# NonLocal Modules
import math
import time
import curses


def overview(win):
    pass

def main(win, debug=False):
    # Initial log position and name of user
    position = 'general/'
    #log.set_pos(position + '/log1.txt')
    # Gather all logs and bumps with respect to position
    file_paths, log_paths = DM.gather_paths(position)
    logs_all = DM.gather_logs(file_paths, log_paths)

    # Chosen Logs
    logs_chsn = []
    # Weight of all positional logs
    weight_all = LP.total_weight(logs_all)
    # Alert Log
    log_alrt = ''
    # Typed Log
    log_typd = ''
    # Highlighted Log (-1 means no log highlighted)
    highlight = -1
    # First run
    first_run = True
    while True:

        # Terminal Width and Height
        x, y = UI.term_dimensions()
        # Printable Width
        p_wdth = LP.get_wdth(x, 52)
        p_mrgn = LP.get_mrgn(x, 52)

        # Full Height of terminal
        y_left = y
        # Height of header, divider, divider margin, and bottom margin
        #h['header'], h['divider'], h['divider_mrgn'], h['bottom_mrgn'] = 2,1,1,3
        h_header, h_divider, h_dividermrgn, h_bottommrgn = 2, 1, 1, 3
        y_left = y_left - h_header - h_divider - h_dividermrgn - h_bottommrgn
        # Height of Alert Log
        if len(log_alrt) > 0:
            y_left -= len(UI.split_lines(log_alrt, p_wdth, x)) + 1
        # Height of Typed Log
        y_left -= len(UI.split_lines(log_typd, p_wdth, x))

        # Spacing Between each log
        spacing_btwn = 1
        # Height of Chosen Logs
        log_end, y_left = check_chsn(logs_chsn, y_left, spacing_btwn, p_wdth, x)

        # If log_end was not set...
        if log_end == -1:
            # ... not enough logs are chosen, therefore choose more logs
            logs_all, logs_chsn, weight_all, log_end, y_left = choose_logs(
            logs_all, logs_chsn, weight_all, y_left, spacing_btwn, p_wdth, x)

        # If this is the first run, go through again
        if first_run:
            first_run = False
            continue

        # If highlight is out of range, set it back to nothing
        if highlight >= log_end:
            highlight = -1

        # Clear and print each part of the terminal screen
#    _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _    #

        # NEW STABLE
        UI.clear_screen(win)
        #'''
        info_dict = {}
        info_dict['x'] = x
        if highlight >= 0:
            info_dict['bump_count'] = logs_chsn[highlight][2]
            info_dict['position'] = DM.log_position(position, logs_chsn[highlight][1])
        else:
            info_dict['none_selected'] = True
        UI.print_info(info_dict, x, win)
        #'''
        #print_header(win, position, name, x)
        UI.new_line(win)
        for i in range(0, int(y_left/2)):
            UI.new_line(win)
            y_left -= 1
        for i in range(0, log_end):
            is_highlighted = False
            if i == highlight:
                is_highlighted = True
            # print_center(highlighted, section, bump, switch, p_wdth, p_mrgn, x, win)
            UI.print_center(is_highlighted, logs_chsn[i][0], logs_chsn[i][2], True, p_wdth, p_mrgn, x, win)
            UI.new_line(win)
            for c in range(0, spacing_btwn):
                UI.new_line(win)
        for i in range(0, y_left):
            UI.new_line(win)
        if len(log_alrt) > 0:
            UI.print_divider(win, x)
            UI.print_center(False, log_alrt, 10, True, p_wdth, p_mrgn, x, win)
            UI.new_line(win)
        UI.print_divider(win, x)
        UI.new_line(win)
        '''if len(log_typd.split()) > 0:
            if log_typd.split()[0][0] == '-':
                print_left(True, log_typd, 5, p_wdth, p_mrgn, x, win)
        else:
            print_left(False, log_typd, 5, p_wdth, p_mrgn, x, win)'''
        # print_left(highlighted, section, bump, p_wdth, p_mrgn, x, win):
        UI.print_left(False, log_typd, 5, p_wdth, p_mrgn, x, win)
        if highlight > -1:
            pass
        else:
            UI.print_cursor(win)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

        # Only returns if it gets some form of keyboard input
        key = IM.get_input(win)
        if key == 'KEY_RESIZE':
            continue
        elif key == 'KEY_UP':
            if highlight == -1:
                highlight = log_end - 1
            else:
                highlight -= 1
            continue
        elif key == 'KEY_DOWN':
            if highlight == log_end - 1:
                highlight = -1
            else:
                highlight += 1
            continue
        elif key == 'KEY_RIGHT' or key == 'KEY_LEFT':
            if highlight >= -1:
                logs_chsn = logs_chsn[log_end:]
                first_run = True
                continue
        elif key == 'KEY_BACKSPACE' or ord(key) == 127:
            log_typd = log_typd[:-1]
            continue
        #ESCAPE Key
        elif ord(key) == 27:
            exit()
        #ENTER Key
        elif ord(key) == 10:
            if highlight > -1:
                #position = 'general/'
                #logs_chsn[highlight][1] = index in notes.txt
                DM.bump_log(position, logs_chsn[highlight][1])
                #logs_chsn[highlight][2] = bump count
                logs_chsn[highlight][2] += 1

            else:
                if len(log_typd) > -1:
                    DM.new_log(position, log_typd)
                    log_typd = ''
            continue
        log_typd += str(key)


def check_chsn(logs_chsn, y_left, spacing_btwn, wdth, x):
    # Height of each log in Chosen Logs and Spacing inbetween
    log_end = -1
    for i in range(0, len(logs_chsn)):
        y_aftr = y_left - spacing_btwn - len(UI.split_lines(logs_chsn[i][0], wdth, x))
        if y_aftr < 0:
            log_end = i
            break
        else:
            y_left = y_aftr
    return log_end, y_left

def choose_logs(logs_all, logs_chsn, weight_all, y_left, spacing_btwn, wdth, x):
    while True:
        if len(logs_all) == 0:
            log_end = len(logs_chsn)
            break
        indx = LP.choosewrt_weight(logs_all, weight_all)
        logs_chsn.append(logs_all.pop(indx))
        weight_all -= LP.weight_conv(logs_chsn[-1][2])
        y_aftr = y_left - spacing_btwn - len(UI.split_lines(logs_chsn[-1], wdth, x))
        if y_aftr < 0:
            log_end = len(logs_chsn) - 1
            break
        else:
            y_left = y_aftr
    return logs_all, logs_chsn, weight_all, log_end, y_left
