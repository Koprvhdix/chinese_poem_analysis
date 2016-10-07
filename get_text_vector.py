# coding: utf-8

import os
import codecs

if __name__ == '__main__':
    poem_dir = 'poem'
    poem_file_list = os.listdir(poem_dir)

    poem_list = list()
    count = 0

    for file_item in poem_file_list:
        file_open = codecs.open(poem_dir + '/' + file_item, 'rw', 'utf-8')
        file_read = file_open.readlines()
        file_open.close()

        word_list = list()

        poem_line = file_read[0]
        state = 0
        index = 0
        for i in range(len(poem_line)):
            if poem_line[i] == u'作':
                state = 1
            elif poem_line[i] == u'：' and state == 1:
                state = 2
            elif poem_line[i] == u' ' and state == 2:
                state = 3
                index = i
                break
            elif poem_line[i] == u'，' and state == 2:
                index = i
                break

        if state == 3:
            index += 1
        if state == 2:
            index2 = poem_line.find(u'。', index)
            length = index2 - index - 1
            index -= length

        poem_str = u''
        for i in range(index, len(poem_line) - 1):
            if poem_line[i] == u' ':
                continue
            else:
                poem_str += poem_line[i]

        print poem_str
