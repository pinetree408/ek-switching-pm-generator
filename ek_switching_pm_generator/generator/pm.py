#-*- coding: utf-8 -*-
import re
import copy

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

    c = re.compile(regex)

    result = {}
    for i in range(len(word)):
	if i == 0:
            continue
        temp = word[0:i+1]
        result = []
	while len(temp) != 0:
            m = c.match(temp)
	    if bool(m) == True:
                char_code = 44032 + enH.index(m.group(1)) * 588 + enB[m.group(2)] * 28
                if m.group(3):
                    char_code = char_code + enF[m.group(3)]
                result.append(unichr(char_code))
                temp = temp.split(m.group(0))[1]
            else:
                break

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



def is_complete_korean(word, word_frequency, option, file):

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
	change_korean_result = []
	while len(temp) != 0:
            m = c.match(temp)
	    if bool(m) == True:
                char_code = 44032 + enH.index(m.group(1)) * 588 + enB[m.group(2)] * 28
                if m.group(3):
                    char_code = char_code + enF[m.group(3)]
                change_korean_result.append(unichr(char_code))
                korean = korean + len(m.group(0))
                temp = temp.split(m.group(0))[1]
            else:
                break

        change_korean = 0.0
        if korean != 0:
            f = open(file, 'r')
            lines = f.readlines()

            frq = ''.join(change_korean_result)
            for line in lines:
                dic = line.decode('utf-8').split('\n')[0]
                if len(frq) > len(dic):
                    continue
                else:
                    if dic[0:len(frq)] == frq:
		        change_korean = 1.0 * (float(word_frequency) / 1000000000)
                        break
            f.close()

        final = {}
	if korean == 0:
            if option == 0:
                final[0] = [1.0 * (float(word_frequency) / 1000000000), 0.0]
            else:
                final[0] = [1.0, 0.0]
        else:
            final[0] = [0.0, 0.0]

        for j in range(i+1):
            if j == 0:
                continue
            if j + 1 == korean:
                if option == 0:
                    final[j+1] = [1.0 * (float(word_frequency) / 1000000000), change_korean]
                else:
		    final[j+1] = [1.0, change_korean]
            else:
                final[j+1] = [0.0, 0.0]
        result[i+1] = final
    print word_frequency
    return [english, result]


def wrapper(args):
    return is_complete_korean(*args)


def calculator(frequency_file, k_dict_file, option):
    f = open(frequency_file, 'r')
    lines = f.readlines()


    from multiprocessing import Pool
    pool = Pool(processes = 8)
    input_seq = []
    for line in lines:
        words = line.split('	')
	temp = []
	temp.append(words[1])
	temp.append(words[2])
	temp.append(option)
	temp.append(k_dict_file)
	input_seq.append(temp)

    result = pool.map(wrapper, input_seq)

    final_result = {}
    for i in range(len(result)):
	if result[i][0] in final_result.keys():
            for key in final_result[result[i][0]].keys():
                for sub_key in final_result[result[i][0]][key].keys():
                    if result[i][1][key][sub_key] != 0:
                        updated = final_result[result[i][0]][key][sub_key]
                        for index in range(len(result[i][1][key][sub_key])):
                            updated[index] = updated[index] + result[i][1][key][sub_key][index]
                        del final_result[result[i][0]][key][sub_key]
		        final_result[result[i][0]][key][sub_key] = updated
        else:
            final_result[result[i][0]] = {}
            for key in result[i][1].keys():
                final_result[result[i][0]][key] = {}
                for sub_key in result[i][1][key].keys():
                    final_result[result[i][0]][key][sub_key] = result[i][1][key][sub_key]
    #del final_result[1]

    temp_final_result = copy.deepcopy(final_result)
    change_final_result = {}
    for key in temp_final_result.keys():
        for sub_key in temp_final_result[key].keys():
            if sub_key in change_final_result.keys():
                for trb_key in temp_final_result[key][sub_key].keys():
                    updated = change_final_result[sub_key][trb_key]
                    for index in range(len(change_final_result[sub_key][trb_key])):
                        updated[index] = updated[index] + temp_final_result[key][sub_key][trb_key][index]
		    del change_final_result[sub_key][trb_key]
		    change_final_result[sub_key][trb_key] = updated
            else:
                change_final_result[sub_key] = temp_final_result[key][sub_key]

    for key in change_final_result.keys():
        sum_c = 0.0
	#sum_k = 0.0
        for sub_key in change_final_result[key].keys():
            sum_c = sum_c + change_final_result[key][sub_key][0]
            #sum_k = sum_k + change_final_result[key][sub_key][1]
        for sub_key in change_final_result[key].keys():
            updated_c = (change_final_result[key][sub_key][0] / sum_c) * 100
	    if change_final_result[key][sub_key][0] != 0.0:
                updated_k = (change_final_result[key][sub_key][1] / float(change_final_result[key][sub_key][0])) * 100
            else:
                updated_k = 0.0
            del change_final_result[key][sub_key]
	    change_final_result[key][sub_key] = [round(updated_c, 2), round(updated_k, 2)]
    f.close()
    return [final_result, change_final_result]
