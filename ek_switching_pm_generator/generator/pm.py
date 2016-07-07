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

    print 'test0'
    for line in lines:
        dic = line.decode('utf-8').split('\n')[0]
        frq = ''.join(result)
        if dic == frq:
            print dic + ':' + frq
            f.close()
            return 1
    f.close()
    return 0


def is_complete_korean(word):

    regH = "[rRseEfaqQtTdwWczxvg]"
    regB = "hk|ho|hl|nj|np|nl|ml|k|o|i|O|j|p|u|P|h|y|n|b|m|l";
    regF = "rt|sw|sg|fr|fa|fq|ft|fx|fv|fg|qt|r|R|s|e|f|a|q|t|T|d|w|c|z|x|v|g|";

    regex = "("+regH+")("+regB+")(("+regF+")(?=("+regH+")("+regB+"))|("+regF+"))";

    import re
    c = re.compile(regex)

    english = len(word) 
    korean = 0
    m = c.match(word)
    if bool(m) == True:
        matched = m.group(0)
	korean = len(matched)

    return [english, korean]



def calculator(frequency_file, k_dict_file):
    f = open(frequency_file, 'r')
    lines = f.readlines()

    result = []
    for line in lines:
        words = line.split('	')
        ick = is_complete_korean(words[1])
	ick.append(change_complete_korean(words[1], k_dict_file))
        result.append(ick)

    final_result = {}
    for i in range(len(result)):
	if result[i][0] in final_result.keys():
            if not(result[i][1] in final_result[result[i][0]].keys()):
	        final_result[result[i][0]][result[i][1]] = [1, result[i][2]]
            else:
                before_updated = final_result[result[i][0]][result[i][1]]
                updated = before_updated[0] + 1
		updated_ick = before_updated[1] + result[i][2]
                del final_result[result[i][0]][result[i][1]]
                final_result[result[i][0]][result[i][1]] = [updated, updated_ick] 
        else:
            final_result[result[i][0]] = {result[i][1] : [1, result[i][2]]}

    for key in final_result.keys():
        sum = 0.0
        for sub_key in final_result[key].keys():
            sum = sum + final_result[key][sub_key][0]
        for sub_key in final_result[key].keys():
            updated = (final_result[key][sub_key][0] / sum) * 100
	    updated_ick = (final_result[key][sub_key][1] / float(final_result[key][sub_key][0])) * 100
            del final_result[key][sub_key]
	    final_result[key][sub_key] = [round(updated, 2), updated_ick]

    f.close()
    return final_result
