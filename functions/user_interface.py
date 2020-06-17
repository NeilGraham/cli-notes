
# User Interface (UI)
#   Used to print to the console


# Local Modules
from . import logical_procedures as LP
from . import data_manager as DM

# NonLocal Modules
import subprocess
import curses



#   _____________________________________________________________________   #

def term_dimensions():
    rows, cols = subprocess.check_output(['stty', 'size']).split()
    return int(cols), int(rows)

def clear_screen(win):
    # Clears the screen for screen to be printed on
    win.clear()

def refresh_screen(win):
    win.refresh()

#   _____________________________________________________________________   #

def print_header(win, position, name, x):
    category = LP.get_category(position)
    category = category[0].upper() + category[1:]
    new_line(win)
    mrgn = 2
    spacing = ' ' * (x-len(category)-len(name)-(mrgn*2))
    win.addstr(' ' * mrgn + category + spacing + name)
    new_line(win)

def print_divider(win, x):
    try:
        win.addstr('  ' + '-' * (x - 4))
        new_line(win)
    except:
        pass

def print_cursor(win):
    win.addstr('_', curses.A_BLINK)

#   _____________________________________________________________________   #


# Fitting as much information carrying key_value pairs in 3 lines
# + if cannot fit 'indication that rest of info can't be fit', don't print next restraining piece of information
def print_info(dictionary, x, win):
    x_left = x
    #y_left includes the current log being written to
    y_left = 3
    for key, value in dictionary.items():
        x_after = x_left
        string = ''
        if x_left == x:
            pass
        else:
            string += ', '
        string += str(key) + ':' + str(value)
        x_after -= len(string)
        # if cannot print anymore info on line
        if x_after < 0:
            # go to next line
            new_line(win)
            y_left -= 1

            # if comma is in front of string, remove comma
            if string[:2] == ', ':
                string = string[2:]

            # if cannot print anymore info at all
            if y_left == 0:
                # append indication that rest of info can't be fit
                if x_left >= 3:
                    win.addstr(' ' * (x_left - 3) + '...')
                elif x_left == 2:
                    win.addstr('..')
                elif x_left == 1:
                    win.addstr('.')
                break
            # if cannot fit string on next line
            elif len(string) > x:
                # do not print anymore info at all
                for i in range(0,y_left-1):
                    new_line(win)
                break
            else:
                # print the next piece of info on the next line
                win.addstr(string)
                x_left = x - len(string)
        else:
            win.addstr(string)
            x_left = x_after
    if y_left > 0:
        for i in range(0,y_left - 1):
            new_line(win)

# ---
def print_left(highlighted, section, bump, wdth, mrgn, x, win):
    lines = split_lines(section, wdth, x)
    if highlighted:
        for i in range(0, len(lines)):
            if x > wdth and (x % 2) == 1:
                win.addstr(' ' * (mrgn - 3))
            else:
                win.addstr(' ' * (mrgn - 2))
            win.addstr(' ', curses.A_STANDOUT)
            win.addstr(' ')
            win.addstr(lines[i], curses.color_pair(LP.bump_color(bump)))
            if i < len(lines) - 1:
                new_line(win)
    else:
        for i in range(0, len(lines)):
            win.addstr(' ' * mrgn + lines[i], curses.color_pair(LP.bump_color(bump)))
            if i < len(lines) - 1:
                new_line(win)

# ---
def print_center(highlighted, section, bump, switch, wdth, mrgn, x, win):
    lines = split_lines(section, wdth, x)
    if highlighted:
        for i in range(0, len(lines)):
            if x > wdth and (x % 2) == 1:
                win.addstr(' ' * (mrgn - 3))
            else:
                win.addstr(' ' * (mrgn - 2))
            win.addstr(' ', curses.A_STANDOUT)
            win.addstr(' ' * (int((x-len(lines[i]))/2) - mrgn + 1))
            if x > wdth and (x % 2) == 1:
                win.addstr(' ')
            if x % 2 != len(lines[i]) % 2:
                if i < len(lines) - 1:
                    if switch == True:
                        switch = False
                    else:
                        win.addstr(' ')
                        switch = True
            win.addstr(lines[i], curses.color_pair(LP.bump_color(bump)))
            if i < len(lines) - 1:
                new_line(win)
    else:
        for i in range(0, len(lines)):
            win.addstr(' ' * int((x-len(lines[i]))/2))
            if x % 2 != len(lines[i]) % 2:
                if i < len(lines) - 1:
                    if switch == True:
                        switch = False
                    else:
                        win.addstr(' ')
                        switch = True
            win.addstr(lines[i], curses.color_pair(LP.bump_color(bump)))
            if i < len(lines) - 1:
                new_line(win)

#   _____________________________________________________________________   #

def split_lines(section, wdth, x):
    # Returns a list of each line with respect to the lines width
    lines = []
    while True:
        hyphen = False
        if len(section) <= wdth:
            lines.append(section)
            if len(section) == wdth:
                lines.append('')
            break
        else:
            line = ''
            r_indx = -1
            l_indx = -1
            if section[wdth] != ' ':
                cnt = 1
                hit = False
                while True:
                    if section[wdth - cnt] == ' ':
                        if r_indx == -1:
                            r_indx = wdth - cnt + 1
                        hit = True
                        cnt += 1
                    elif hit: # and section[wdth - cnt] != ' '
                        l_indx = wdth - cnt + 1
                        break
                    elif cnt == wdth:
                        l_indx = wdth - 1
                        r_indx = wdth - 1
                        hyphen = True
                        break
                    else: cnt += 1
            else:
                if len(section) > wdth+1:
                    if section[wdth - 1] != ' ' and section[wdth + 1] != ' ':
                        if len(section) > wdth + 1:
                            r_indx = wdth + 1
                        else: r_indx = wdth
                    else: r_indx = wdth
                else: r_indx = wdth
                cnt = 1
                while True:
                    if section[wdth - cnt] != ' ':
                        l_indx = wdth - cnt + 1
                        break
                    else:
                        cnt += 1
            line = section[:l_indx]
            section = section[r_indx:]
            if hyphen:
                line += '-'
            lines.append(line)
    return lines

'''
def divide_evenly(lines):
    words = []
    lines_new =
    char_cnt = 0
    for i in range(0,len(lines)):
        for c in range(0,len(lines[i])):
            words.append(lines[i][c])
            char_cnt += lines[i][c] + 1
'''

#   _____________________________________________________________________   #

def new_line(win):
    try:
        win.addstr('\n')
    except:
        pass
        

global name

name = 'Neil Graham'

#   _____________________________________________________________________   #
#    _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _  _    #
#    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _    #
# Free Software
