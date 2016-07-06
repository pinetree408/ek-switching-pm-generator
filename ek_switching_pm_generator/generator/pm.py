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
	if (len(matched) == 5):
            print matched
	korean = korean + len(matched)

    return [english, korean]



def calculator(file):
    f = open(file, 'r')
    lines = f.readlines()

    result = []
    for line in lines:
        words = line.split('	')
        result.append(is_complete_korean(words[1]))

    final_result = {}
    for i in range(len(result)):
	if result[i][0] in final_result.keys():
            if not(result[i][1] in final_result[result[i][0]].keys()):
	        final_result[result[i][0]][result[i][1]] = 1
            else:
                updated = final_result[result[i][0]][result[i][1]] + 1
                del final_result[result[i][0]][result[i][1]]
                final_result[result[i][0]][result[i][1]] = updated
        else:
            final_result[result[i][0]] = {result[i][1] : 1}

    for key in final_result.keys():
        sum = 0.0
        for sub_key in final_result[key].keys():
            sum = sum + final_result[key][sub_key]
        for sub_key in final_result[key].keys():
            updated = (final_result[key][sub_key] / sum) * 100
            del final_result[key][sub_key]
	    final_result[key][sub_key] = round(updated, 2)

    return final_result

is_complete_korean('the')
is_complete_korean('system')
is_complete_korean('dltkddbs')
