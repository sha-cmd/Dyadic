import pandas as pd
import re


def add_entityLabels(some_dict, a_dict):
    composition = a_dict['labels']['acts']
    intent = ''
    some_dict['entities'] = []
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
                    for it, c in enumerate(some_dict['text']):
                        if c.isspace():
                            spacePos.append(it)
                    match = re.search(re.escape(n['val']), some_dict['text'])
                    startCharIndex = match.span()[0]
                    endCharIndex = match.span()[1] - 1  # Last char inclused
                    startCharIndex = max([x for x in spacePos if x < startCharIndex])
                    endCharIndex = min([x for x in spacePos if x > endCharIndex])
                    # Save it
                    some_dict["intent"] = intent
                    some_dict['entities'].append({"startPos": startCharIndex,
                                     "endPos": endCharIndex,
                                     "entity": entityName})
            except:
                some_dict["intent"] = 'None'
    return some_dict


def to_dict(a_dict):
    some_dict = {}
    some_dict['text'] = a_dict['text']
    some_dict = add_entityLabels(some_dict, a_dict)
    return some_dict


def main():
    df = pd.read_json('data/frames.json')

    data_lst = []
    for m_index, m_value in df['turns'].iteritems():
        for n_index, n_value in enumerate(df['turns'].iloc[m_index]):
            if n_index % 2 == 0:
                data_lst.append(to_dict(df['turns'].iloc[m_index][n_index]))

    data = pd.DataFrame(data_lst)
    df_book = data.loc[data['intent'] == 'book'].sample(1000)
    df_none = data.loc[data['intent'] == 'None'].sample(100)
    book_nb = len(df_book)
    none_nb = len(df_none)
    df_train = pd.concat([df_book[:int(book_nb*0.75)], df_none[:int(none_nb*0.75)]])
    df_test = pd.concat([df_book[int(book_nb*0.75):], df_none[int(none_nb*0.75):]])
    pd.DataFrame(df_train).to_json('data/data_train.json', orient='records')
    pd.DataFrame(df_test).to_json('data/data_test.json', orient='records')


if __name__ == "__main__":
    main()
