# -*- coding: utf-8 -*-
from pathlib import Path
from flashtext import KeywordProcessor
from collections import defaultdict
from tqdm import tqdm


class Keywords_Classifier:

    def __init__(self, dic_dir):
        self.dic_dir = Path(dic_dir)
        self.keywords_dict = {}
        self.processor = None
        self.label_dict = defaultdict(set)
        self.label_dict['other'] = set()
        type_of_dic = [i.stem for i in self.dic_dir.glob('*.dic')]
        for label in type_of_dic:
            self.label_dict[label] = set()

    def build_keyword_dict(self):
        '''Read a text file that contains specific dictionary
        which words or phrase is arranged by line by line'''

        dic_files = self.dic_dir.glob(('**/*.dic'))
        pbar = tqdm(dic_files)
        for dic_file in pbar:
            with dic_file.open() as f:
                dic_name = dic_file.stem
                dic_value = [word.strip() for word in f.readlines()]
                self.keywords_dict[dic_name] = dic_value
            pbar.set_description(f"Loading {dic_name} Dict Completely!\n")
        self.processor = KeywordProcessor(case_sensitive=False)
        self.processor.add_keywords_from_dict(self.keywords_dict)

    def query(self, phrase):
        '''Query keyword to get related category'''

        cat = self.processor.extract_keywords(phrase)
        return cat

    def classifier(self, keywords):
        '''Input a list of keywords, output a dict
        key of dict is label of word, value of dict is set of keywords'''

        for i, keyword in enumerate(keywords):
            result = self.query(keyword)
            if result:
                for each_label in result:
                    self.label_dict[each_label].add(keyword)
            else:
                self.label_dict['other'].add(keyword)

        return self.label_dict.items()


if __name__ == '__main__':

    from title_generator.kw_generator.Config import Config
    config = Config()
    phrase = 'ThingyClub Simple Design'
    keyword_clf = Keywords_Classifier(config.dic_dir)
    keyword_clf.build_keyword_dict()
    cat = keyword_clf.query(phrase)
    print(cat)
    keywords = ['shoes', 'boots', 'sandals', 'stiletto', 'heels']
    print(keyword_clf.classifier(keywords))

