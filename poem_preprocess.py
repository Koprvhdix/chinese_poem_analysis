# coding: utf-8

import os
import codecs

poem_dir = 'get_poem/poem'
file_list = os.listdir(poem_dir)
for item in file_list:
    file_open = codecs.open(poem_dir + '/' + item, 'rw', 'utf-8')
    file_read = file_open.readlines()
    if len(file_read) > 2:
        print item
    else:
        content = file_read[0]
        index1 = content.find(u"《")
        index2 = content.find(u"《", index1 + 1)
        content = content[:index2]
        print content
    break
