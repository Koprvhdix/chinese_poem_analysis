# coding: utf-8

import os
import codecs

if __name__ == '__main__':
    poem_dir = 'poem'
    poem_file_list = os.listdir(poem_dir)
    poem_list = list()

    for file_item in poem_file_list:
        file_open = codecs.open(poem_dir + '/' + file_item, 'rw', 'utf-8')
        file_read = file_open.readlines()
        file_open.close()

        poem = file_read[0]
        index1 = poem.find(u'，', 0)
        index2 = poem.find(u'。', 0)
        length = index2 - index1 - 1
        if length != 5 and length != 7:
            print file_item, length
