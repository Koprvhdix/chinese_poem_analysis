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

    def classified_poem_by_comment(self):
        # 用来存储分类结果，之后还将进行人工校验
        answer_file = codecs.open(u'answer_file.txt', 'w', 'utf-8')  # answer_file.txt存的是人工校验后的。

        # 从赏析中获取抒情还是叙事的特征，方法：含【抒】字，或者含两个【情】字的为抒情诗，其他的为叙事诗，记录在最后一行。
        poem_dir = u'poem'
        answer_statistic = [0, 0]  # 抒情诗的数量和叙事诗的数量

        answer_str = u''

        for poem_name in self.poem_name_list:

            final_path = u'poem/' + poem_name
            answer = 0
            key_vector = [0, 0]  # 第一个为【抒】字的数量，第二个为【情】字的数量

            file_open = codecs.open(poem_dir + '/' + poem_name, 'rw', 'utf-8')
            file_read = file_open.readlines()
            file_open.close()
            for key in file_read[3]:
                if key == u'抒':
                    if answer == 0:
                        answer = 1
                    key_vector[0] += 1
                if key == u'情':
                    key_vector[1] += 1
                    if answer == 0 and key_vector[1] == 2:
                        answer = 1

            if answer == 0:
                answer_str += (u'叙事诗' + '\t' + poem_name + '\n')
            else:
                answer_str += (u'抒情诗' + '\t' + poem_name + '\n')

            key_vector.append(answer)
            answer_statistic[answer] += 1
            # 写入文件 为了校验方便
            final_str = u''
            file_read[3] += '\n'
            if answer == 0:
                file_read[3] += u'叙事诗' + u' ' + str(key_vector[0]).decode('ascii').encode('utf-8') + \
                                u' ' + str(key_vector[1]).decode('ascii').encode('utf-8')
            else:
                file_read[3] += u'抒情诗' + u' ' + str(key_vector[0]).decode('ascii').encode('utf-8') + \
                                u' ' + str(key_vector[1]).decode('ascii').encode('utf-8')
            for lines in file_read:
                final_str += lines
            file_open = codecs.open(final_path, 'w', 'utf-8')
            file_open.write(final_str)
            file_open.close()
        answer_file.write(answer_str)
        print answer_statistic
        answer_file.close()

if __name__ == '__main__':
    poem_process = ProcessPoem()
    poem_process.process_raw_poem()
    poem_process.classified_poem_by_comment()
