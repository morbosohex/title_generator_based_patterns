import csv
import random
from tqdm import trange
from pathlib import Path
from itertools import combinations_with_replacement
from itertools import permutations
from collections import defaultdict
from pprint import pprint
from collections import Counter

from title_generator.kw_generator.Config import Config
config = Config()


def get_labels(config):
    whole_labels = config.type_of_label
    # whole_labels = list(config.kw_threshold.keys())
    print(f'build-in dictionary labels: {whole_labels}')

    # remove some label from whold labels
    labels = list(filter(lambda s: s not in ['country', 'currency', 'ship'],
                         whole_labels))
    print(f'Updated labels:{labels}')
    return labels


def sample_pattern(labels):
    # get init patterns for method one
    patterns = defaultdict(set)
    for i in trange(5, 11):
        pattern_name = 'words-' + str(i)
        for j in range(10):
            patterns[pattern_name].add(' '.join(random.sample(labels, i)))
    return patterns


def pattern_for_label_num(labels, init_label_num, *must_include):
    # get init patterns for method two
    patterns = list(permutations(labels, init_label_num))
    # given a list of labels user want to include certainly
    result = [pattern for pattern in patterns
              if set(must_include).issubset(set(pattern))]
    print(f"Must inculde labels of Initial Patterns: {' '.join(must_include)}")
    print(f'\nNumber of Initial Patterns: {len(result)}\n')
    return result


def filter_patterns(unique_patterns, **kwargs):
    # drop some patterns based given label and label's max_duplicated_label
    # if bigger than max_duplicated_label then drop this pattern
    # kargs -> {'product': 3}
    raw_patterns = []
    for pattern in unique_patterns:
        counter = Counter(pattern)
        is_drop = all([counter[label] < kwargs[label]
                       for label in kwargs if label in counter])
        if not is_drop:
            continue
        else:
            raw_patterns.append(pattern)
    return raw_patterns


def combinations_patterns(patterns,
                          min_words_num=5,
                          max_words_num=9,
                          max_num_unique_label=4,
                          max_duplicated_label=3,
                          lowest_priority=10,
                          **kwargs):
    # expand patterns for method two
    cnt = 0
    total_patterns = []
    for words_num in trange(min_words_num, max_words_num):
        print(f'*** patterns for words - {words_num} ***')
        result = []
        for j in range(len(patterns)):
            temp_patterns = list(combinations_with_replacement(
                patterns[j], words_num))
            result += [tp for tp in temp_patterns
                       if len(set(tp)) >= max_num_unique_label]
        # drop duplicated pattern from result and assign it to unique_patterns
        unique_patterns = list(set(result))

        # filter pattern using some rules
        raw_patterns = filter_patterns(unique_patterns, **kwargs)

        cnt += len(raw_patterns)

        # formating each pattern from unique_patterns to final pattern format
        final_patterns = convert_raw_patterns_to_patterns(
            raw_patterns, words_num, lowest_priority)

        print(f'Num of final patterns for words - {words_num}: \
            {len(final_patterns)}')

        total_patterns += final_patterns

        # dump patterns for each group grouped by words num
        patterns_backup_path = Path('./patterns/')
        if not patterns_backup_path.is_dir():
            patterns_backup_path.mkdir()
        dump_patterns(final_patterns, patterns_backup_path / f'patterns-{words_num}.csv')
        print('Dump completly!\n')

        final_patterns = []

    print(f'Total Num of patterns: {cnt}')

    return total_patterns


def convert_raw_patterns_to_patterns(raw_patterns, words_num, priority_limit):
    language = 'en'
    group = 'words-' + str(words_num)
    final_patterns = [['',
                       language,
                       'priority-' +
                       str(random.randint(1, priority_limit)) + '|' + group]
                      for _ in range(len(raw_patterns))]

    for i, pattern in enumerate(raw_patterns):
        pattern_str = ' '.join(pattern)
        pattern_str_index = 0
        final_patterns[i][pattern_str_index] = pattern_str
    return final_patterns


def product_pattern(patterns):
    # expand patterns for methond one
    update_patterns = defaultdict(list)
    for pattern_name, pattern in patterns.items():
        pprint(f'pattern {pattern_name} >>>')
        pattern_list = list(pattern)
        num_pattern = len(pattern)

        for i in trange(num_pattern):
            main_pattern = pattern_list[i]
            update_patterns[pattern_name].append(main_pattern)

            main_pattern_labels = main_pattern.split()
            main_pattern_len = len(main_pattern_labels)

            update_patterns[pattern_name] += list(
                combinations_with_replacement(
                    main_pattern_labels, main_pattern_len))
    pprint([len(v) for k, v in update_patterns.items()])
    return update_patterns


def dump_patterns(final_patterns, filename):
    # save list of list pattern to a csv file
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([["keyphrase", "lang", "topics", "tags"]])
        writer.writerows(final_patterns)


if __name__ == '__main__':

    labels = get_labels(config)

    # initial pattern setup
    # number of labels in each pattern of no-duplicated label
    init_label_num = 5
    # label must contained in each unique pattern
    must_include = ['product', 'quantity', 'style', 'other']

    patterns = pattern_for_label_num(labels,
                                     init_label_num,
                                     *must_include)

    # expand pattern setup
    # minimum words in each pattern
    min_words_num = 7

    # maximum words in each pattern
    max_words_num = 10

    # maximum unique labels in each pattern
    max_num_unique_label = 3

    # lowest priority of each pattern
    # 1 means highest
    priority_limit = 10

    # maximum number of duplicated labels
    kwargs = config.kw_threshold

    # update_patterns = product_pattern(patterns)
    total_patterns = combinations_patterns(patterns,
                                           min_words_num,
                                           max_words_num,
                                           max_num_unique_label,
                                           priority_limit,
                                           **kwargs)
    output_dir = 'patterns.csv'
    dump_patterns(total_patterns, output_dir)
