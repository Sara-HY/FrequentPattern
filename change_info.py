"""
团队和主题多是会随着时间⽽动态变化。请你根据⾃⼰所定的时
间段（五年，三年，两年或是⼀年）描述团队的构成状况以及其
研究主题的变化情况。
"""

import codecs
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from utils import load_data, load_teams, pat
from topic import load_stopwords, parse_topic


def get_teams_every_year(data, base_year=2017, delta_year=11):
    teams_every_year = {}
    team_set = load_teams()
    for item in data:
        year = item['year']
        if year not in teams_every_year:
            teams_every_year[year] = set()
        if set(item['author']) in team_set:
            value = item['author']
            value.sort()
            teams_every_year[year].add(','.join(value))
    for k in list(teams_every_year.keys()):
        if k <= base_year - delta_year:
            teams_every_year.pop(k)
    return teams_every_year


def write_team_change_info(teams_every_year, write_path='./data/change_info/team_change'):
    team_change = sorted(teams_every_year.items(), key=lambda x: x[0])
    with codecs.open(write_path, 'w', encoding='utf8') as f:
        for item in team_change:
            f.write(str(item[0]) + '\n')
            teams = list(item[1])
            teams.sort()
            f.write('\n'.join(teams))
            f.write('\n##################################\n')


def get_topic_change(data,
                     base_year=2017,
                     delta_year=11,
                     lda_path='./data/topic/model/lda.model',
                     dict_path='./data/topic/titles.dict'):
    teams_every_year = get_teams_every_year(data, base_year, delta_year)
    team_exists_years = {}
    for v in teams_every_year.values():
        for team in v:
            if team not in team_exists_years:
                team_exists_years[team] = 1
            else:
                team_exists_years[team] += 1
    # ignore the teams who have published papers for less than three years
    for k in list(team_exists_years.keys()):
        if team_exists_years[k] < 3:
            team_exists_years.pop(k)
    teams = list(team_exists_years.keys())
    team_topics = {}

    # load lda, dictionary and stop words
    lda = LdaModel.load(lda_path)
    dict = Dictionary.load(dict_path)
    stop_words = load_stopwords()
    for team in teams:
        team_topics[team] = {}

    for item in data:
        authors = item['author']
        authors.sort()
        team = ','.join(authors)
        if team in team_topics and item['year'] > base_year - delta_year:
            if item['year'] not in team_topics[team]:
                team_topics[team][item['year']] = []
            team_topics[team][item['year']].append(get_topic(lda, item['title'], dict, stop_words))

    return team_topics


def write_topic_change(team_topics, write_path='./data/change_info/topic_change'):
    with codecs.open(write_path, 'w', encoding='utf8') as f:
        for team in team_topics:
            f.write(team)
            f.write('\n-----------------------------------------------------------\n')
            year_and_topics = sorted(team_topics[team].items(), key=lambda x: x[0])
            for (year, topics) in year_and_topics:
                topics = list(topics)
                f.write(str(year) + ': ')
                f.write(','.join(topics))
                f.write('\n')
            f.write('###################################################\n')


def get_topic(lda, doc, dic, stop_words):
    doc = pat.sub('', doc).lower()
    words = [w for w in doc.split() if w not in stop_words]
    title_bow = dic.doc2bow(words)
    topic = max(lda[title_bow], key=lambda x: x[1])
    return parse_topic(lda.print_topic(topic[0]))


if __name__ == '__main__':
    data = load_data()
    write_team_change_info(get_teams_every_year(data))
    write_topic_change(get_topic_change(data))
