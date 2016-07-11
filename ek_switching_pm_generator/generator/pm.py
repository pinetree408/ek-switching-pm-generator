#-*- coding: utf-8 -*-

def change_complete_korean(word, file):

    enH = "rRseEfaqQtTdwWczxvg"
    regH = "[" + enH + "]"

    enB_list = [
        'k', 'o', 'i', 'O', 'j',
        'p', 'u', 'P', 'h', 'hk',
        'ho', 'hl', 'y', 'n', 'nj',
        'np', 'nl', 'b', 'm', 'ml',
        'l'
    ]
    enB = {}
    for i in range(len(enB_list)):
        enB[enB_list[i]] = i
    regB = "hk|ho|hl|nj|np|nl|ml|k|o|i|O|j|p|u|P|h|y|n|b|m|l";

    enF_list = [
        '', 'r', 'R', 'rt', 's',
        'sw', 'sg', 'e', 'f', 'fr',
        'fa', 'fq', 'ft', 'fx', 'fv',
        'fg', 'a', 'q', 'qt', 't',
        'T', 'd', 'w', 'c', 'z',
	'x', 'v', 'g'
    ]
    enF = {}
    for i in range(len(enF_list)):
        enF[enF_list[i]] = i
    regF = "rt|sw|sg|fr|fa|fq|ft|fx|fv|fg|qt|r|R|s|e|f|a|q|t|T|d|w|c|z|x|v|g|";

    regex = "("+regH+")("+regB+")(("+regF+")(?=("+regH+")("+regB+"))|("+regF+"))";

    import re
    c = re.compile(regex)
    result = []
    while len(word) != 0:
        m = c.match(word)
	if bool(m) == True:
            char_code = 44032 + enH.index(m.group(1)) * 588 + enB[m.group(2)] * 28
            if m.group(3):
                char_code = char_code + enF[m.group(3)]
            result.append(unichr(char_code))
            word = word.split(m.group(0))[1]
        else:
            return 0

    f = open(file, 'r')
    lines = f.readlines()

    for line in lines:
        dic = line.decode('utf-8').split('\n')[0]
        frq = ''.join(result)
        if dic == frq:
            f.close()
            return 1
    f.close()
    return 0


def is_complete_korean(word, word_frequency, option):
    regH = "[rRseEfaqQtTdwWczxvg]"
    regB = "hk|ho|hl|nj|np|nl|ml|k|o|i|O|j|p|u|P|h|y|n|b|m|l";
    regF = "rt|sw|sg|fr|fa|fq|ft|fx|fv|fg|qt|r|R|s|e|f|a|q|t|T|d|w|c|z|x|v|g|";

    regex = "("+regH+")("+regB+")(("+regF+")(?=("+regH+")("+regB+"))|("+regF+"))";

    import re
    c = re.compile(regex)
    
    english = len(word)

    result = {}
    for i in range(len(word)):
	if i == 0:
            continue
        temp = word[0:i+1]
        korean = 0
	while len(temp) != 0:
            m = c.match(temp)
	    if bool(m) == True:
                korean = korean + len(m.group(0))
                temp = temp.split(m.group(0))[1]
            else:
                break
        final = {}
	if korean == 0:
            if option == 0:
                final[0] = 1.0 * (float(word_frequency) / 1000000000)
            else:
                final[0] = 1.0
        else:
            final[0] = 0.0
        for j in range(i+1):
            if j == 0:
                continue
            if j + 1 == korean:
                if option == 0:
                    final[j+1] = 1.0 * (float(word_frequency) / 1000000000)
                else:
		    final[j+1] = 1.0
            else:
                final[j+1] = 0.0
        result[i+1] = final
    return [english, result]


def calculator(frequency_file, k_dict_file, option):
    f = open(frequency_file, 'r')
    lines = f.readlines()

    result = []
    sum = 0.0
    for line in lines:
        words = line.split('	')
        ick = is_complete_korean(words[1], words[2], option)
        sum = sum + float(words[2])
        result.append(ick)
    print sum


    final_result = {}
    for i in range(len(result)):
	if result[i][0] in final_result.keys():
            for key in final_result[result[i][0]].keys():
                for sub_key in final_result[result[i][0]][key].keys():
                    if result[i][1][key][sub_key] != 0:
                        updated = final_result[result[i][0]][key][sub_key]
                        del final_result[result[i][0]][key][sub_key]
		        final_result[result[i][0]][key][sub_key] = updated + result[i][1][key][sub_key]
        else:
            final_result[result[i][0]] = {}
            for key in result[i][1].keys():
                final_result[result[i][0]][key] = {}
                for sub_key in result[i][1][key].keys():
                    final_result[result[i][0]][key][sub_key] = result[i][1][key][sub_key]
    del final_result[1]

    import copy
    temp_final_result = copy.deepcopy(final_result)
    change_final_result = {}
    for key in temp_final_result.keys():
        for sub_key in temp_final_result[key].keys():
            if sub_key in change_final_result.keys():
                for trb_key in temp_final_result[key][sub_key].keys():
                    updated = change_final_result[sub_key][trb_key]
		    del change_final_result[sub_key][trb_key]
		    change_final_result[sub_key][trb_key] = updated + temp_final_result[key][sub_key][trb_key]
            else:
                change_final_result[sub_key] = temp_final_result[key][sub_key]

    for key in change_final_result.keys():
        sum = 0.0
        for sub_key in change_final_result[key].keys():
            sum = sum + change_final_result[key][sub_key]#[0]
        for sub_key in change_final_result[key].keys():
            updated = (change_final_result[key][sub_key] / sum) * 100
            del change_final_result[key][sub_key]
	    change_final_result[key][sub_key] = round(updated, 2)
    f.close()
    return [final_result, change_final_result]
