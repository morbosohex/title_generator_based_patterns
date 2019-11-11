# -*- coding: utf-8 -*-


class Config(object):
    dic_dir = 'dic/'
    full_dic_dir = 'title_generator/kw_generator/dic/'
    root_dir = '.'

    type_of_label = ['shape',
                     'quantity',
                     'material',
                     'product',
                     'size',
                     'group',
                     'scene',
                     'style',
                     'color',
                     'other']
    # Threshold set for keywords filter
    kw_threshold = {
        'shape': 2,
        'quantity': 3,
        'product': 4,
        'color': 2,
        'group': 4,
        'material': 3,
        'scene': 2,
        'size': 2,
        'style': 3,
        'other': 3
    }

    # number of titles
    num_titles = 1
