
# Logical Procedures (LP)
#    Used for executing general purpose logical procedures



# NonLocal Modules
import random

# -------------------------------- #

def weight_conv(bump):
    return (10*bump)**(1/2)+1

def total_weight(logs_all):
    # Returns the total weight of all positional logs
    weight_all = 0
    for i in range(0, len(logs_all)):
        weight_all += weight_conv(logs_all[i][1])
    return weight_all

# -------------------------------- #

def get_wdth(x, max_wdth):
    wdth = 0
    if x > max_wdth + 4:
        if (x % 2) == 0:
            wdth = max_wdth
        elif x % 2 == 1:
            wdth = max_wdth+1
    else:
        wdth = x - 4
    return wdth

def get_mrgn(x, max_wdth):
    mrgn = 0
    if x > max_wdth + 4:
        if (x % 2) == 0:
            mrgn = int((x - max_wdth) / 2)
        elif x % 2 == 1:
            mrgn = int((x - max_wdth+1) / 2)
    else:
        mrgn = 2
    return mrgn

# -------------------------------- #

def hor_info(x, max_wdth):
    wdth = 0
    mrgn = 0
    if x > max_wdth + 4:
        if (x % 2) == 0:
            wdth = max_wdth
            mrgn = int((x - wdth) / 2)
        elif x % 2 == 1:
            wdth = max_wdth+1
            mrgn = int((x - wdth) / 2)
    else:
        wdth = x - 4
        mrgn = 2
    return wdth, mrgn

# --------------------------------- #

def choosewrt_weight(logs_all, weight_all):
    rand_num = random.uniform(0, weight_all)
    num = 0
    for i in range(0, len(logs_all)):
        num += weight_conv(logs_all[i][1])
        if num > rand_num:
            return i - 1
    return len(logs_all) - 1


# --------------------------------- #

def bump_color(bump_count):
    if bump_count >= 10:
        return 232
    return bump_count + 246

# --------------------------------- #

def folder_layers(position):
    layers = 0
    for i in range(0,len(position)):
        if position[i] == '/':
            layers += 1
    return layers

# --------------------------------- #

def get_category(position):
    # Start from 2nd to last character in position string and move
    #  backwards to find the next '/'
    start = 0
    for i in range(2,len(position)+1):
        if position[-i] == '/':
            start = len(position) - i + 1
            break
    return position[start:-1]
