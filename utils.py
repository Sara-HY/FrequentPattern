import codecs
import pickle
import csv
import re

confs = ['IJCAI', 'AAAI', 'COLT', 'CVPR', 'NIPS', 'KR', 'SIGIR', 'KDD']
pat = re.compile("[\.~`!@#$%^&*()_+\-={}\[\]|\\\\;:'\",<>/?]")


# parse the papers to JSON Obejcts
def parse_data(data_path, write_path='./data/data.pkl'):
    data = []
    with codecs.open(data_path, 'r', encoding='utf8') as f:
        author, title, year, conf = [], None, None, None
        for line in f.readlines():
            # add a paper information
            if line.startswith('#'): 
                if len(author) != 0 and conf in confs:
                    data.append({
                        'author': author.copy(),
                        'title': title,
                        'year': year,
                        'conf': conf
                    })
                    author.clear()
            else:
                key, value = line.replace('\n', '').split('\t')
                if key == 'author':
                    author.append(value)
                else:
                    if key == 'year':
                        year = int(value)
                    elif key == 'title':
                        title = value
                    else:
                        conf = value
        # add the last paper information
        if len(author) != 0 and conf in confs:
            data.append({
                'author': author,
                'title': title,
                'year': year,
                'conf': conf
            })
    data.sort(key=lambda x: x['year'])
    with codecs.open(write_path, 'wb') as f:
        pickle.dump(data, f)
    return data


# write the authors of every paper
def write_author_list(data, file_path='./data/author_list/list.csv'):
    with codecs.open(file_path, 'w', encoding='utf8') as f:
        csv_writer = csv.writer(f)
        for item in data:
            csv_writer.writerow(item['author'])


# load the paper obejcts
def load_data(data_path='./data/data.pkl'):
    f = codecs.open(data_path, 'rb')
    data = pickle.load(f)
    f.close()
    return data


# load the authors of every paper
def load_author_list(file_path='./data/author_list/list.csv'):
    author_list = []
    with codecs.open(file_path, 'r', encoding='utf8') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            author_list.append(row)
    return author_list


# load the authors of every team
def load_teams(team_path='./data/author_list/team'):
    team_set = []
    teams = codecs.open(team_path, 'r', encoding='utf8').readlines()
    for team in teams:
        authors = team.replace('\n', '').split(',')
        team_set.append(set(authors))
    return team_set


if __name__ == '__main__':
    # parse_data('./data/FilteredDBLP.txt')
    data = load_data()
    write_author_list(data)
