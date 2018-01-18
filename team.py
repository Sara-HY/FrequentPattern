"""
在找到各自的研究者群体后，我们希望找到经常性在一起合作的
学者，将之称为‘团队’。请你根据研究者合作发表论文次数为根据
进行频繁模式挖掘，找出三个人以上的‘团队’。
"""

import codecs
from pyfpgrowth import find_frequent_patterns
from utils import load_author_list


def find_team(data, freq=5, file_path='./data/author_list/team'):
    """
    find team according to the freq with fp-growth algorithm
    """
    teams = find_frequent_patterns(data, freq)
    with codecs.open(file_path, 'w', encoding='utf8') as f:
        for team in teams:
            # team size should be greater than 3
            if len(team) >= 3:
                f.write(','.join(team) + '\n')


if __name__ == '__main__':
    data = load_author_list()
    find_team(data)
