import os
import click
from pathlib import Path

import title_generator.csv as csv
from title_generator.kw_generator.generator_objects import KeywordSets
from .generator_objects import KeywordsCombination
from .generator_objects import Keywords
from .generator_objects import Keyword
from .generator_objects import Pattern
from title_generator.kw_generator.Config import Config
from title_generator.kw_generator.keyword_classifier import Keywords_Classifier
config = Config()
__author__ = 'lin'


def load_dictionary(config):
    keyword_clf = Keywords_Classifier(config.full_dic_dir)
    keyword_clf.build_keyword_dict()
    return keyword_clf


def read_patterns_csv(filepath, keyword_sets):
    return [Pattern(row[0], row[1], row[2] if len(row) > 1 else "",
                    keyword_sets)
            for row in csv.get_rows(filepath)]


def read_patterns_list(patterns, keyword_sets):
    return [Pattern(row[0], row[1], row[2] if len(row) > 1 else "",
                    keyword_sets)
            for row in patterns]


def read_keywords_list(label, keywords_list):
    # for kw_clf interface
    keywords = [Keyword(keyword, {'en'}) for keyword in keywords_list]
    return Keywords(label, keywords)


def read_keywords_csv(filepath, keyword_set_name):
    keywords = [Keyword(row[0],
                        set([lang for lang in row[1].split("|")]))
                for row in csv.get_rows(filepath)]
    return Keywords(keyword_set_name, keywords)


def path_join(path1, path2):
    root_dir = Path(path1)
    return root_dir / path2


def read_keyword_sets(dir):
    files = os.listdir(dir)
    keywords = []
    for filepath in files:
        if filepath[-4:] == '.csv':
            keywords.append(read_keywords_csv(
                path_join(dir, filepath), filepath[:-4]))
    return KeywordSets(keywords)


def read_keyword_sets_v2(label_keywords):
    # for kw_clf interface
    keywords = []
    for label, keywords_list in label_keywords:
        keywords.append(read_keywords_list(label, keywords_list))
    return KeywordSets(keywords)


def generate_combinations(root_dir,
                          pattern_file="patterns.csv",
                          verbose=False):
    keyword_sets = read_keyword_sets(
        path_join(root_dir, "keyword_placeholders"))
    patterns = read_patterns_csv(
        path_join(root_dir, pattern_file), keyword_sets)
    return KeywordsCombination(patterns).generate(verbose)


def generate_combinations_v2(label_keywords,
                             pattern_file="patterns.csv",
                             verbose=False):
    # for kw_clf interface
    keyword_sets = read_keyword_sets_v2(label_keywords)

    patterns = read_patterns_csv(path_join(
        Config().root_dir, pattern_file), keyword_sets)
    return KeywordsCombination(patterns).generate(verbose)


def save_combinations(filepath, generatedResult):
    exportedRows = csv.save_csv(filepath,
                 [
                     [
                         keyphrase,
                         "|".join(sorted(infos.lang)),
                         "|".join(sorted(infos.topics)),
                         "|".join(sorted(infos.tags))
                     ] for keyphrase, infos in iter(sorted(generatedResult.items()))
                 ],
                 ["keyphrase", "lang", "topics", "tags"])
    click.echo("Number of generated Phrases : " + str(exportedRows))

