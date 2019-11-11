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
st.text('注意：⭕️需要进行选择')

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

    st.subheader('⚪️模版生成\n')
    st.subheader('step 1: 词类筛选\n')
    labels = get_labels(config)
    must_include_label = st.multiselect('⭕️选出你认为必须要包含的类别', tuple(labels))

    st.subheader("step 2: 标题模版规则限制\n")
    min_words_num = st.slider('\n⭕️请选择模版的最小词数，建议3个', 1, 10, 3)
    max_words_num = st.slider('\n⭕️请选择模版的最大词数，建议10个', 1, 10, 10)
    max_num_unique_label = st.slider('\n⭕️请选择模版中最多不超过的类别数, 建议3个', 1, 10, 3)

    st.subheader("step 3: 规则汇总：\n")
    st.write('- 模版必须要包含的类别:', ', '.join(must_include_label))
    st.write('- 模版最短有:', min_words_num, '个词组成')
    st.write('- 模版最长有:', max_words_num, '个词组成')
    st.write('- 模版中最多不超过:', max_num_unique_label, '个类别的词')

    if st.button('\n🔍生成模版'):
        with st.spinner('生成中...'):
            patterns = pattern(labels,
                               must_include_label,
                               min_words_num,
                               max_words_num,
                               max_num_unique_label)
        patterns_file = './patterns.csv'
        dump_patterns(patterns, patterns_file)
        st.success('生成完成!')
        st.write('共生成模版数量', len(patterns), "个")

    # For titles generate
    st.subheader('🔵标题生成\n')

    st.subheader('step 1: 关键词输入\n')
    keywords_str = st.text_input('Keywords',
        'apple,laptop,MacBook Air,Retina,siver,gray,15 inch,16Gb')
    keywords = re.split(r',|, ', keywords_str)

    st.subheader('step 2: 关键词筛选')
    drop_keywords = st.multiselect('⭕️选出要剔除的关键词', tuple(keywords))
    final_keywords = list(set(keywords).difference(set(drop_keywords)))
    st.text('最终用于生成标题的关键词')
    st.write(pd.DataFrame({'keywords': final_keywords}))

    st.subheader('step 3: 标题生成\n')
    num_titles_option = st.radio("\n⭕️请选择生成的标题数量？",
                                 ('5', '10', '30', '50'))
    num_titles = int(num_titles_option)
    verbose = False

    patterns_file = './patterns.csv'

    kw_clf = load_dictionary(config)
    label_keywords = kw_clf.classifier(final_keywords)

    if st.button('\n🔍生成标题'):
        titles = generate(label_keywords,
                          patterns_file,
                          num_titles,
                          verbose)
        st.text('标题生成完成!')

        title_eval_result = [[title, structure, priority, 0, 0, 0]
                             for title, structure, priority in titles]
        title_eval_result_df = pd.DataFrame(title_eval_result)
        title_eval_result_df.to_csv('title_eval_result.csv',
                                    index=False,
                                    header=['title',
                                            'structure',
                                            'priority',
                                            'eval_title',
                                            'eval_struc',
                                            'eval_prior'])

    st.subheader('step 4: 标题评估阶段\n')
    filename = 'title_eval_result.csv'
    if Path(filename).is_file():
        data = pd.read_csv(filename)

        update_data = []
        for i, row in data.iterrows():
            title, struc, prior, eval_title, eval_struc, eval_prior = row
            st.markdown('---' * 10)
            st.write(f'**标题{i + 1}: {title}**')
            eval_title = st.radio("\n⭕️标题是否合格？",
                                  ('yes', 'no'), key=str(i))
            st.write(f'构成形式:', struc)
            eval_struc = st.radio("\n⭕️构成形式是否合格？",
                                  ('yes', 'no'), key=str(i + 1))
            st.write(f'优先级和词数:', prior)
            eval_prior = st.radio("\n⭕️优先级是否合格？",
                                  ('yes', 'no'), key=str(i + 2))
            update_data.append([title, struc, prior,
                                eval_title, eval_struc, eval_prior])
        title_eval_result_update_df = pd.DataFrame(update_data)
        title_eval_result_update_df.to_csv('title_eval_result.csv',
                                           index=False,
                                           header=['title',
                                                   'structure',
                                                   'priority',
                                                   'eval_title',
                                                   'eval_struc',
                                                   'eval_prior'])
        st.table(title_eval_result_update_df)

    st.subheader('step 5: 关键词分类评估阶段\n')
    if label_keywords:
        correct_rate = defaultdict(float)
        for i, (label, keywords) in enumerate(label_keywords):
            if keywords:
                st.text(f'关键词类别: {label}')
                correct_keywords = st.multiselect('⭕️选出分类正确的关键词',
                                                  tuple(keywords), key=i)
                correct_rate[label] = len(correct_keywords) / (
                    len(keywords) + 0.01)
        st.text('关键词分类器正确率')
        df_clf_result = pd.DataFrame(correct_rate.items(), columns=[
            'keywords_label', 'correct_rate'])
        st.table(df_clf_result)
        df_clf_result.to_csv('kwclf_eavl_result.csv',
                             index=False,
                             header=['keywords_label', 'correct_rate'])


if __name__ == '__main__':
    main()
