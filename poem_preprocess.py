# coding: utf-8

import os
import codecs


class ProcessPoem(object):
    def __init__(self):
        self.poem_name_list = list()
        self.poem_classified_result = dict()
        self.poem_word_dict = dict()

    def process_raw_poem(self):
        raw_poem_dir = 'get_poem/poem'
        poem_file_list = os.listdir(raw_poem_dir)
        # delete the <p> and space. add \n to comment and appreciation.
        # 将空格和<p>之类的删掉，将【注释】和【韵解】还有【赏析】分行
        for file_name in poem_file_list:
            raw_poem_open = codecs.open(raw_poem_dir + '/' + file_name, 'rw', 'utf-8')
            raw_poem_read = raw_poem_open.readlines()
            raw_poem_open.close()
            if len(raw_poem_read) > 2:
                continue
            else:
                content = raw_poem_read[0]

                poem_name = u''
                final_content = u''
                start = 0  # 用于删掉html

                poem_name_start = -1

                for i in range(len(content)):
                    if start == 1:
                        if content[i] == '>':
                            start = 0
                        continue

                    # 获取诗的名字
                    if content[i] == u'》' and poem_name_start == 1:
                        poem_name_start = 0
                    if poem_name_start == 1:
                        poem_name += content[i]
                    if content[i] == u'《' and poem_name_start == -1:
                        poem_name_start = 1

                    if content[i] == '<':
                        start = 1
                    elif content[i] == ' ' or content[i] == u'':
                        continue
                    elif content[i] == u'【':
                        final_content += '\n'  # Unix为\n，Windows是\r\n
                        final_content += content[i]
                    elif content[i] == u'《' and content[i - 1] == '>' and i > 4:
                        break
                    else:
                        final_content += content[i]
                poem_path = u'poem/' + poem_name
                poem_file = codecs.open(poem_path, 'w', 'utf-8')
                poem_file.write(final_content)
                poem_file.close()
                self.poem_name_list.append(poem_name)

if __name__ == '__main__':
    poem_process = ProcessPoem()
    poem_process.process_raw_poem()
