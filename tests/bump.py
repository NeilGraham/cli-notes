
def main():
    count = 0
    action = {'type':None, 'options':[], ''}
    while action != 'exit':
        action = input('')
        if action == '':
            count += 1
        if action == 'p':
            print('\r\r\r')
            print(count)
        if
        if action[0:2] == 'ft':


# RETURNS parsed
# Parsing a string into multiple types
def parse_sections(string, types, delim='+', ordered=False, incl_delim=False, ignore_str=True):

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
