# -*- coding: utf-8 -*-
import re
import copy


class Generator:

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

    regH = "[rRseEfaqQtTdwWczxvg]"
    regB = "hk|ho|hl|nj|np|nl|ml|k|o|i|O|j|p|u|P|h|y|n|b|m|l"
    regF = "rt|sw|sg|fr|fa|fq|ft|fx|fv|fg|qt|r|R|s|e|f|a|q|t|T|d|w|c|z|x|v|g|"

    def __init__(self):
        enB_dict = {}
        for i in range(len(self.enB_list)):
            enB_dict[self.enB_list[i]] = i
        enF_dict = {}
        for i in range(len(self.enF_list)):
            enF_dict[self.enF_list[i]] = i
        self.enB = enB_dict
        self.enF = enF_dict
        regH_block = "("+self.regH+")"
        regB_block = "("+self.regB+")"
        regF_item_first = "("+self.regF+")"
        regF_item_second = "(?=("+self.regH+")("+self.regB+"))|("+self.regF+")"
        regF_block = "(" + regF_item_first + regF_item_second + ")"
        self.regex = regH_block + regB_block + regF_block

    def change_complete_korean(self, word):

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
            enH_char = self.enH[enH_code]
            enB_char = self.enB_list[enB_code]
            enF_char = self.enF_list[enF_code]
            result = result + enH_char + enB_char + enF_char
        return result

    def is_complete_korean(self, args):
        word = args[0]
        word_frequency = args[1]
        option = args[2]

        c = re.compile(self.regex)

        english = len(word)

        result = {}
        for i in range(len(word)):
            if i == 0:
                continue
            temp = word[0:i+1]
            korean = 0
            while len(temp) != 0:
                m = c.match(temp)
                if bool(m):
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

    def calculator(self, input_file, option):

        f = open(input_file, 'r')
        lines = f.readlines()

        result = []
        for line in lines:
            args = []
            if option == 0:
                words = line.split('\t')
                args.append(words[1])
                args.append(words[2])
            else:
                dic = line.decode('utf-8').split('\n')[0]
                args.append(self.change_complete_korean(dic))
                args.append(0)
            args.append(option)
            result.append(self.is_complete_korean(args))

        final_result = {}
        for i in range(len(result)):
            if result[i][0] in final_result.keys():
                for key in final_result[result[i][0]].keys():
                    for sub_key in final_result[result[i][0]][key].keys():
                        if result[i][1][key][sub_key] != 0:
                            updated = final_result[result[i][0]][key][sub_key]
                            updated += result[i][1][key][sub_key]
                            del final_result[result[i][0]][key][sub_key]
                            final_result[result[i][0]][key][sub_key] = updated
            else:
                final_result[result[i][0]] = {}
                for key in result[i][1].keys():
                    final_result[result[i][0]][key] = {}
                    for sub_key in result[i][1][key].keys():
                        korean_freq = result[i][1][key][sub_key]
                        final_result[result[i][0]][key][sub_key] = korean_freq

        temp_result = copy.deepcopy(final_result)
        change_final_result = {}
        for key in temp_result.keys():
            for sub_key in temp_result[key].keys():
                if sub_key in change_final_result.keys():
                    for trb_key in temp_result[key][sub_key].keys():
                        updated = change_final_result[sub_key][trb_key]
                        updated += temp_result[key][sub_key][trb_key]
                        del change_final_result[sub_key][trb_key]
                        change_final_result[sub_key][trb_key] = updated
                else:
                    change_final_result[sub_key] = temp_result[key][sub_key]

        for key in change_final_result.keys():
            sum_c = 0.0
            for sub_key in change_final_result[key].keys():
                sum_c += change_final_result[key][sub_key]
            for sub_key in change_final_result[key].keys():
                updated_c = (change_final_result[key][sub_key] / sum_c) * 100
                del change_final_result[key][sub_key]
                change_final_result[key][sub_key] = round(updated_c, 2)
        f.close()
        return change_final_result
