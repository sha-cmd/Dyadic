#!/usr/bin/env python
"""Ce fichier nous permet de créer deux jeux de données pour LUIS. La particularité de ce travail reste que LUIS
demande des clés de dictionnaire différentes pour chaque jeu. Ainsi, nous traiterons deux jeux de données dans
une boucle unique. L’écriture est un peu déconcertante, mais cela permet d’avoir les bonnes clés pour LUIS et
d’optimiser le code pour qu’il soit rapide"""
import pandas as pd
import re

global size
size = 1000  # Nombre total d’intention book (train + test)

def add_entityLabels(some_train_dict, some_test_dict, a_dict):
    composition = a_dict['labels']['acts']
    intent = ''
    some_train_dict['entityLabels'] = []
    some_test_dict['entities'] = []
    for it, m in enumerate(composition):
        if it == 0:
            intent = m['name']
            intent = intent if not intent == 'inform' else 'book'
        for n in m['args']:
            entityName = n['key']
            # Search the first position in discussion
            try:
                if (not n['val'] == "-1") :  # Exclusion of unpresented data for reliability
                    spacePos = []
                    for it, c in enumerate(some_train_dict['text']):
                        if c.isspace():
                            spacePos.append(it)
                    match = re.search(re.escape(n['val']), some_train_dict['text'])
                    startCharIndex = match.span()[0]
                    endCharIndex = match.span()[1] - 1  # Last char inclused
                    startCharIndex = max([x for x in spacePos if x < startCharIndex]) + 1
                    endCharIndex = min([x for x in spacePos if x > endCharIndex]) - 1
                    # Save it
                    some_train_dict["intentName"] = intent
                    some_test_dict["intent"] = intent
                    some_train_dict['entityLabels'].append({"startCharIndex": startCharIndex,
                                                      "endCharIndex": endCharIndex,
                                                      "entityName": entityName})
                    some_test_dict['entities'].append({"startPos": startCharIndex,
                                     "endPos": endCharIndex,
                                     "entity": entityName})
            except:
                some_train_dict["intentName"] = 'None'
                some_test_dict["intent"] = "None"
                
    return some_train_dict, some_test_dict


def to_dict(a_dict):
    some_train_dict = {}
    some_train_dict['text'] = a_dict['text']
    some_test_dict = {}
    some_test_dict['text'] = a_dict['text']
    some_train_dict, some_test_dict = add_entityLabels(some_train_dict, some_test_dict, a_dict)
    return some_train_dict, some_test_dict


def sampling():
    global size
    df = pd.read_json('data/frames.json')
    # LUIS nécessite un format de dictionnaire pour l’entraînement différent de celui pour le test.
    # Ainsi nous avons, dans une même boucle traité de jeux de données, dont le tirage aléatoire donne
    # le même résultat grâce à la graine d’initialisation. Ainsi il n’y a pas de redondance dans les
    # échantillons, donc la séparation des 2 jeux est parfaite.
    data_lst = []
    data_test_lst = []
    for m_index, m_value in df['turns'].iteritems():
        for n_index, n_value in enumerate(df['turns'].iloc[m_index]):
            if n_index % 2 == 0:
                train_sample, test_sample = to_dict(df['turns'].iloc[m_index][n_index])
                data_lst.append(train_sample)
                data_test_lst.append(test_sample)
                
    # Format de fichier JSON conforme pour entraîner LUIS, la graine permet la reproductibilité
    data = pd.DataFrame(data_lst)  # jeu d’entraînement
    df_book = data.loc[data['intentName'] == 'book'].sample(size, random_state=42)
    df_none = data.loc[data['intentName'] == 'None'].sample(int(size/10), random_state=42)
    book_nb = len(df_book)
    none_nb = len(df_none)
    df_train = pd.concat([df_book[:int(book_nb*0.75)], df_none[:int(none_nb*0.75)]])
    pd.DataFrame(df_train).to_json('data/data_train.json', orient='records')

    # Format de fichier JSON conforme pour tester LUIS, la graine permet la reproductibilité
    data = pd.DataFrame(data_test_lst)  # jeu de test (avec d’autres clés)
    df_book = data.loc[data['intent'] == 'book'].sample(size, random_state=42)
    df_none = data.loc[data['intent'] == 'None'].sample(int(size/10), random_state=42)
    book_nb = len(df_book)
    none_nb = len(df_none)
    df_test = pd.concat([df_book[int(book_nb * 0.75):], df_none[int(none_nb * 0.75):]])
    pd.DataFrame(df_test).to_json('data/data_test.json', orient='records')


def main():
    sampling()

    
if __name__ == "__main__":
    main()
