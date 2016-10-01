# coding: utf-8

import os
import codecs

if __name__ == '__main__':
    poem_dir = 'poem'
    poem_file_list = os.listdir(poem_dir)

    for file_item in poem_file_list:
        file_open = codecs.open(poem_dir + '/' + file_item, 'rw', 'utf-8')
        file_read = file_open.readlines()
        file_open.close()

        print file_item
        count = 1  # 获取注解里的词
        start = 0
        word_comment_line = file_read[1]
        word = u''
        test_str = u''
        for i in range(len(word_comment_line)):
            if word_comment_line[i] == u'、':  # 从'、'开始计算
                start = 1
                word = u''
            elif word_comment_line[i] == u'：' and start == 1:  # 最近出现的顿号加冒号才有意义
                start = 0
                test_str += (u' ' + word)
            elif start == 1:
                word += word_comment_line[i]
