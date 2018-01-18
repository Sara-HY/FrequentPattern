"""
每⼀个会议都有各⾃的⽀持者，现在请你将每个会议各⾃的研
究者寻找出来，并且根据时间信息，看看哪些⼈依然活跃，哪些
⼈不再活跃。
"""

import os
import json
import codecs
from utils import load_data, confs


def find_researcher_of_conf(data):
    researchers = {}
    for item in data:
        conf = item['conf']
        if conf not in researchers:
            researchers[conf] = []
        researchers[conf].append(item)
    file_path = './data/researchers/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    for conf in confs:
        conf_researchers = {}
        for item in researchers[conf]:
            year = item['year']
            if year not in conf_researchers:
                conf_researchers[year] = set()
            conf_researchers[year] = conf_researchers[year].union(item['author'])
        for key in conf_researchers.keys():
            conf_researchers[key] = list(conf_researchers[key])
        active_list = []
        for item in conf_researchers.items():
            active_list.append({
                'year': int(item[0]),
                'authors': item[1]
            })
        active_list.sort(key=lambda x: x['year'])

        active = find_active_researchers(active_list, flag=0xff)

        # write researchers of each conference
        with codecs.open(file_path + conf + '.json', 'w', encoding='utf8') as f:
            f.write(json.dumps(active_list))

        # write active researchers of each conference
        with codecs.open(file_path + 'active/' + conf, 'w', encoding='utf8') as f:
            for r in active:
                f.write(r[0] + '\n')


def find_active_researchers(active_list, base_year=2007, flag=0):
    """
    Rank the authors of the conference and return the result.
    """
    researchers = {}
    for item in active_list:
        for r in item['authors']:
            if r not in researchers:
                researchers[r] = 1 << item['year'] - base_year
            else:
                researchers[r] = (1 << item['year'] - base_year) | researchers[r]
    active = sorted(researchers.items(), key=lambda x: x[1], reverse=True)

    # filter
    idx = 0
    while idx < len(active):
        if active[idx][1] < flag:
            break
        else:
            idx += 1
    return active[:idx]


if __name__ == '__main__':
    # load data
    data = load_data()
    find_researcher_of_conf(data)
