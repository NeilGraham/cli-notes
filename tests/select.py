# RETURNS parsed
# Parsing a string into multiple types
def type_expression(string, types, delim=None, ordered=False, incl_delim=False, \
ignore_str=True):

    if isinstance(delim, str): delim = [delim]

    parsed = []; test_not = {}

    for name, patterns in types.items():
        if isinstance(patterns,str):
            types[name] = [patterns]
        test_not[name] = []
        for j in range(0,len(types[name])):
            item = types[name][j]
            if len(item) > 0 and item[0] == '!':
                test_not[name].append(True)
                types[name][j] = types[name][j][1:]
            else: test_not[name].append(False)

    start, wait = 0, 0
    no_type = ''
    in_str = False
    for i in range(0,len(string)):
        if string[i] == '\"': in_str = not in_str
        if wait:
            wait -= 1
            continue
        passed_delim = False
        for j in range(0,len(delim)):
            delim_item = delim[j]
            if string[i:i+len(delim_item)] == delim_item or i == len(string)-1 \
            and j == len(delim)-1:
                if ignore_str and in_str: continue
                if i==len(string)-1 and string[i:i+len(delim_item)]!=delim_item \
                and j == len(delim)-1:
                    i += 1
                passed_delim = True

                selected = string[start:i]
                wait = len(delim_item)-1
                start = i + len(delim_item)

                passed_type = False
                for name, patterns in types.items():
                    for k in range(0,len(patterns)):
                        item = patterns[k]

                        passed_test = False
                        if test_not[name][k]:
                            if not contains(patterns[k],selected):passed_test=True
                        else:
                            if contains(patterns[k],selected):passed_test=True

                        if passed_test:
                            if len(no_type) > 0:
                                parsed.append({'type':None, 'content':no_type})
                                no_type = ''
                            parsed.append({'type':name, 'content':selected})
                            passed_type = True
                            break
                    if passed_type: break
                if not passed_type: no_type += selected
                if string[i:i+len(delim_item)] == delim_item and incl_delim:
                    if len(no_type) > 0:
                        parsed.append({'type':None, 'content':no_type})
                        no_type = ''
                    parsed.append({'type':'delim', 'content':delim_item})
            if passed_delim: break
    if len(no_type) > 0:
        parsed.append({'type':None, 'content':no_type})

def contains(pattern, string):
    start = 0
    end = len(string)

    if isinstance(pattern, str):
        pattern = pattern.split('*')

    if len(pattern) == 1:
        if string == pattern: return True
        else: return False

    if len(pattern[0]) > 0:
        if string[:len(pattern[0])] != pattern[0]: return False
        start = len(pattern[0])
    pattern = pattern[1:]

    if len(pattern[-1]) > 0:
        if string[-len(pattern[-1]):] != pattern[-1]: return False
        end = len(string) - len(pattern[-1])
    pattern = pattern[:-1]

    if len(pattern) == 0:
        return True

    wait = 0
    for i in range(start,end):

        if len(pattern) == 0:
            break
        elif len(pattern[0]) == 0:
            pattern = pattern[1:]
            continue
        if wait: wait -= 1; continue
        elif string[i:i+len(pattern[0])] == pattern[0]:
            wait += len(pattern[0])
            pattern = pattern[1:]

    if len(pattern) == 0: return True
    else: return False
