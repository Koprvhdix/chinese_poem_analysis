# coding: utf-8

import os
import codecs

if __name__ == '__main__':
    poem_dir = 'get_poem/poem'
    file_list = os.listdir(poem_dir)
    for item in file_list:
        file_open = codecs.open(poem_dir + '/' + item, 'rw', 'utf-8')
        file_read = file_open.readlines()
        if len(file_read) > 2:
            print item
        else:
            content = file_read[0]

            final_content = u''
            final_path = 'poem/' + item
            start = 0
            for i in range(len(content)):
                if start == 1:
                    if content[i] == '>':
                        start = 0
                    continue
                if content[i] == '<':
                    start = 1
                elif content[i] == ' ' or content[i] == u'':
                    continue
                elif content[i] == u'【':
                    final_content += '\n'
                    final_content += content[i]
                elif content[i] == u'《' and content[i - 1] == '>' and i > 4:
                    break
                else:
                    final_content += content[i]
            file_open = codecs.open(final_path, 'w', 'utf-8')
            file_open.write(final_content)
