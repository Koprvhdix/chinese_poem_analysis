# coding: utf-8
import logging
from gensim import corpora, models

import codecs

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class ClassifyPoem(object):
    def __init__(self, aim_poem=None):
        self.aim_poem = aim_poem
        self.lda = None
        self.dictionary = None
        self.punctuation = [u'；', u'。', u'，', u'\n']

    def delete_punctuation(self, poem):
        poem_to_list = list()
        for key in poem:
            if key not in self.punctuation:
                poem_to_list.append(key)
        return poem_to_list

    def train_poem(self):
        train_file_open = codecs.open('train_poem.txt', 'rw', 'utf-8')
        train_poem = train_file_open.readlines()
        train_set = list()

        for poem_item in train_poem:
            train_set.append(self.delete_punctuation(poem_item))

        self.dictionary = corpora.Dictionary(train_set)
        corpus = [self.dictionary.doc2bow(text) for text in train_set]
        self.lda = models.LdaModel(corpus, id2word=self.dictionary, num_topics=10)

    def test_aim_poem(self):
        self.train_poem()
        new_list = self.delete_punctuation(self.aim_poem)
        corpus = self.dictionary.doc2bow(new_list)
        score_set = sorted(self.lda[corpus], key=lambda tup: -1 * tup[1])
        if len(score_set) < 4:
            print len(score_set), u'抒情诗', self.aim_poem
        else:
            print len(score_set), u'叙事诗', self.aim_poem

    def test_all_test_poem(self):
        self.train_poem()
        test_file_open = codecs.open('test_poem.txt', 'rw', 'utf-8')
        test_poem = test_file_open.readlines()
        for poem_item in test_poem:
            new_list = self.delete_punctuation(poem_item)
            corpus = self.dictionary.doc2bow(new_list)
            score_set = sorted(self.lda[corpus], key=lambda tup: -1 * tup[1])
            if len(score_set) < 4:
                print len(score_set), u'抒情诗', poem_item
            else:
                print len(score_set), u'叙事诗', poem_item


if __name__ == '__main__':
    test_classify_poem = ClassifyPoem()
    test_classify_poem.test_all_test_poem()
