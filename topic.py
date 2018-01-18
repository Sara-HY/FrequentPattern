"""
每⼀篇论⽂都会涉及到⼀个或多个主题，请你先定出主题词，
然后根据每个‘团队’发表的论⽂的情况，提炼出这个团队最常涉猎
的主题。
"""

import codecs
import re
import json
from utils import load_data, load_teams, pat

from gensim.corpora import Dictionary
from gensim.models import LdaModel


def load_stopwords(file_path='./data/topic/stop_words'):
    stop_words = codecs.open(file_path, 'r', encoding='utf8').readlines()
    stop_words = [w.strip() for w in stop_words]
    return stop_words


def train(data, save_path='./data/topic/'):
    train_data = []
    stop_words = load_stopwords()
    for item in data:
        words = pat.sub('', item['title']).lower().split()
        train_data.append([w for w in words if w not in stop_words])

    dictionary = Dictionary(train_data)
    dictionary.save(save_path + 'titles.dict')
    corpus = [dictionary.doc2bow(text) for text in train_data]
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=10)
    lda.save(save_path + 'model/lda.model')
    return lda


def load_team_works(data, team_path='./data/author_list/team'):
    team_set = load_teams(team_path)
    team_papers = {}
    for item in data:
        authors = item['author']
        for team in team_set:
            if team.issubset(set(authors)):
                key = list(team)
                key.sort()
                key = ','.join(key)
                if key not in team_papers:
                    team_papers[key] = []
                team_papers[key].append(item['title'])
                break
    return team_papers


def get_topics(lda, team_papers, dict_path='./data/topic/titles.dict'):
    team_topics = {}
    stop_words = load_stopwords()
    dictionary = Dictionary.load(dict_path)
    for team in team_papers.keys():
        if team not in team_topics:
            team_topics[team] = []
        papers = team_papers[team]
        for title in papers:
            words = [w for w in title.split() if w not in stop_words]
            title_bow = dictionary.doc2bow(words)
            topic_prob = max(lda[title_bow], key=lambda x: x[1])
            str_topic = lda.print_topic(topic_prob[0])
            team_topics[team].append(parse_topic(str_topic))
    return team_topics


def parse_topic(str_topic, idx=3):
    p = re.compile(r'\"(.+?)\"')
    topics = re.findall(p, str_topic)
    return ' '.join(topics[0:idx])


if __name__ == '__main__':
    lda = LdaModel.load('./data/topic/model/lda.model')
    for topic in lda.print_topics():
        print(topic)
    data = load_data()
    team_papers = load_team_works(data)
    with codecs.open('./data/topic/team_topics.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(get_topics(lda, team_papers)))
