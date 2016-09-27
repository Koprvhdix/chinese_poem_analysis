# coding: utf-8

import os
import codecs

if __name__ == '__main__':
    ignore_poem = list()

    poem_dir = 'get_poem/poem'
    file_list = os.listdir(poem_dir)
    # delete the <p> and space. add \n to comment and appreciation.
    # 将空格和<p>之类的删掉，将【注释】和【韵解】还有【赏析】分行
    for item in file_list:
        file_open = codecs.open(poem_dir + '/' + item, 'rw', 'utf-8')
        file_read = file_open.readlines()
        if len(file_read) > 2:
            ignore_poem.append(item)
        else:
            content = file_read[0]

            final_content = u''
            final_path = 'poem/' + item
            start = 0  # 删掉html标注
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

    # 用来存储分类结果
    answer_file = codecs.open('answer_file.txt', 'w', 'utf-8')

    # 从赏析中获取抒情还是叙事的特征，方法：含【抒】字，或者含两个【情】字的为抒情诗，其他的为叙事诗，记录在最后一行。
    poem_dir = 'poem'
    file_list = os.listdir(poem_dir)
    answer_statistic = [0, 0]  # 抒情诗的数量和叙事诗的数量

    for item in file_list:
        if item in ignore_poem:
            print item
            continue

        final_path = 'poem/' + item
        answer = 0
        key_vector = [0, 0]  # 第一个为【抒】字的数量，第二个为【情】字的数量

        file_open = codecs.open(poem_dir + '/' + item, 'rw', 'utf-8')
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

        answer_file.write((item + ' ' + str(answer) + '\n').decode('ascii').encode('utf-8'))

        key_vector.append(answer)
        answer_statistic[answer] += 1
        # 写入文件 为了校验方便
        final_str = u''
        file_read[3] += '\n'
        if answer == 0:
            file_read[3] += u'叙事诗' + u' ' + str(key_vector[0]).decode('ascii').encode('utf-8') +\
                        u' ' + str(key_vector[1]).decode('ascii').encode('utf-8')
        else:
            file_read[3] += u'抒情诗' + u' ' + str(key_vector[0]).decode('ascii').encode('utf-8') + \
                        u' ' + str(key_vector[1]).decode('ascii').encode('utf-8')
        for lines in file_read:
            final_str += lines
        file_open = codecs.open(final_path, 'w', 'utf-8')
        file_open.write(final_str)
        file_open.close()
    print answer_statistic
    answer_file.close()
