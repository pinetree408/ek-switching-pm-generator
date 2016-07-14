#-*- coding: utf-8 -*-
import re
import copy

def change_complete_korean(word):

    enH = "rRseEfaqQtTdwWczxvg"
    enB_list = [
        'k', 'o', 'i', 'O', 'j',
        'p', 'u', 'P', 'h', 'hk',
        'ho', 'hl', 'y', 'n', 'nj',
        'np', 'nl', 'b', 'm', 'ml',
        'l'
    ]
    enF_list = [
        '', 'r', 'R', 'rt', 's',
        'sw', 'sg', 'e', 'f', 'fr',
        'fa', 'fq', 'ft', 'fx', 'fv',
        'fg', 'a', 'q', 'qt', 't',
        'T', 'd', 'w', 'c', 'z',
	'x', 'v', 'g'
    ]
    #word = word.decode('utf-8')
    result = ''
    for i in range(len(word)):
        char_code = ord(word[i])
	if char_code < 44032 or char_code > 55203:
            result = ''
            break
	char_code = char_code - 44032
	enH_code = char_code / 588
	enBF_code = char_code % 588
	enB_code = enBF_code / 28
	enF_code = enBF_code % 28
	
	result = result + enH[enH_code]+enB_list[enB_code]+enF_list[enF_code]

    return result


def is_complete_korean(word, word_frequency, option):

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
                temp = temp[len(m.group(0)):]
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



def wrapper(args):
    return is_complete_korean(*args)


def calculator(input_file, option):
    f = open(input_file, 'r')
    lines = f.readlines()

    input_seq = []
    for line in lines:
	temp = []
        if option == 0:
            words = line.split('	')
	    temp.append(words[1])
	    temp.append(words[2])
        else:
            dic = line.decode('utf-8').split('\n')[0]
            temp.append(change_complete_korean(dic))
            temp.append(0)
	temp.append(option)
	input_seq.append(temp)

    from multiprocessing import Pool
    pool = Pool(processes = 8)
    result = pool.map(wrapper, input_seq)

    final_result = {}
    for i in range(len(result)):
	if result[i][0] in final_result.keys():
            for key in final_result[result[i][0]].keys():
                for sub_key in final_result[result[i][0]][key].keys():
                    if result[i][1][key][sub_key] != 0:
                        updated = final_result[result[i][0]][key][sub_key]
                        updated = updated + result[i][1][key][sub_key]
                        del final_result[result[i][0]][key][sub_key]
		        final_result[result[i][0]][key][sub_key] = updated
        else:
            final_result[result[i][0]] = {}
            for key in result[i][1].keys():
                final_result[result[i][0]][key] = {}
                for sub_key in result[i][1][key].keys():
                    final_result[result[i][0]][key][sub_key] = result[i][1][key][sub_key]

    temp_final_result = copy.deepcopy(final_result)
    change_final_result = {}
    for key in temp_final_result.keys():
        for sub_key in temp_final_result[key].keys():
            if sub_key in change_final_result.keys():
                for trb_key in temp_final_result[key][sub_key].keys():
                    updated = change_final_result[sub_key][trb_key]
                    updated = updated + temp_final_result[key][sub_key][trb_key]
		    del change_final_result[sub_key][trb_key]
		    change_final_result[sub_key][trb_key] = updated
            else:
                change_final_result[sub_key] = temp_final_result[key][sub_key]

    for key in change_final_result.keys():
        sum_c = 0.0
        for sub_key in change_final_result[key].keys():
            sum_c = sum_c + change_final_result[key][sub_key]
        for sub_key in change_final_result[key].keys():
            updated_c = (change_final_result[key][sub_key] / sum_c) * 100
            del change_final_result[key][sub_key]
	    change_final_result[key][sub_key] = round(updated_c, 2)
    f.close()
    return change_final_result
