import csv
import re
import os
import streamlit as st
import pandas as pd
import random
from pathlib import Path
from collections import defaultdict
from title_generator.kw_generator.Config import Config
from title_generator.pattern_generator import pattern_for_label_num
from title_generator.pattern_generator import get_labels
from title_generator.pattern_generator import combinations_patterns
from title_generator.pattern_generator import dump_patterns
from title_generator.kw_generator import load_dictionary
from title_generator.kw_generator import generate_combinations_v2
from title_generator.kw_generator import save_combinations


config = Config()
st.title('Title Generator Based Patterns')
st.text('Note：⭕️ means need to interactive!')

# For patterns generate
@st.cache
def pattern(labels, must_include_label,
            min_words_num, max_words_num,
            max_num_unique_label,
            init_label_num=4,
            priority_limit=10):

    patterns = pattern_for_label_num(labels, init_label_num,
                                     *must_include_label)

    kwargs = config.kw_threshold

    total_patterns = combinations_patterns(patterns,
                                           min_words_num,
                                           max_words_num,
                                           max_num_unique_label,
                                           priority_limit,
                                           **kwargs)
    return total_patterns


def generate(label_keywords,
             patterns_file,
             num_titles,
             verbose=False):

    combinations = generate_combinations_v2(label_keywords,
                                            patterns_file,
                                            verbose)

    if len(list(iter(combinations.items()))) < num_titles:
        num_titles = len(list(iter(combinations.items())))

    result = random.sample(list(iter(combinations.items())), num_titles)
    format_combinations = [[keyphrase,
                            "|".join(sorted(infos.topics)),
                            "|".join(sorted(infos.tags))]
                           for keyphrase, infos in result]
    return format_combinations


def save_eval_result(data):
    with open("title_eval_result.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def main():

    st.subheader('⚪️Pattern Generation\n')
    st.subheader('step 1: Filter Category of Words\n')
    labels = get_labels(config)
    must_include_label = st.multiselect('⭕️Choose Category of Must included:', tuple(labels))

    st.subheader("step 2: Rule of Patterns\n")
    min_words_num = st.slider('\n⭕️Please Choose Minimum Number of Words \
        in Each Patterns: (suggested 3)', 1, 10, 3)
    max_words_num = st.slider('\n⭕️Please Chooose Maximum Number of Words \
        in Each Patterns: (suggested 10)', 1, 10, 10)
    max_num_unique_label = st.slider('\n⭕️Please Choose Maximum Number of Unique Category \
        in Each Patterns: (suggested 3)', 1, 10, 3)

    st.subheader("step 3: Summary：\n")
    st.write('- Must included Category in Patterns:', ', '.join(must_include_label))
    st.write('- Minimum Number of Category:', min_words_num)
    st.write('- Maximum Number of Category:', max_words_num)
    st.write('- Max Number of Unique Category:', max_num_unique_label)

    if st.button('\n🔍Generate Patterns'):
        with st.spinner('Generating...'):
            patterns = pattern(labels,
                               must_include_label,
                               min_words_num,
                               max_words_num,
                               max_num_unique_label)
        patterns_file = './patterns.csv'
        dump_patterns(patterns, patterns_file)
        st.success('Done!')
        st.write('Total Number of Patterns:', len(patterns))

    # For titles generate
    st.subheader('🔵Title Generation\n')

    st.subheader('step 1: Keywords Input\n')
    keywords_str = st.text_input('Keywords',
        'apple,laptop,MacBook Air,Retina,siver,gray,15 inch,16Gb')
    keywords = re.split(r',|, ', keywords_str)

    st.subheader('step 2: Keywords Filter')
    drop_keywords = st.multiselect('⭕️Choose Keywords That Need to Drop', tuple(keywords))
    final_keywords = list(set(keywords).difference(set(drop_keywords)))
    st.text('Final Keywords to Generate Titles')
    st.write(pd.DataFrame({'keywords': final_keywords}))

    st.subheader('step 3: Title Generate\n')
    num_titles_option = st.radio("\n⭕️Please Choose Number of Titles That to Generate？",
                                 ('5', '10', '30', '50'))
    num_titles = int(num_titles_option)
    verbose = False

    patterns_file = './patterns.csv'

    kw_clf = load_dictionary(config)
    label_keywords = kw_clf.classifier(final_keywords)

    if st.button('\n🔍Generate Titles'):
        titles = generate(label_keywords,
                          patterns_file,
                          num_titles,
                          verbose)
        st.text('Done!')

        for i, (title, structure, priority) in enumerate(titles):
            st.markdown('---' * 10)
            st.write(f'**Titles{i + 1}: {title}**')
            st.write(f'Patterns Structure:', structure)
            st.write(f'Priority or Number of words:', priority)


if __name__ == '__main__':
    main()
