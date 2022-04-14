import pandas as pd
import re


def add_entityLabels(some_dict, a_dict):
    composition = a_dict['labels']['acts']
    #print(composition)
    intent = ''
    some_dict['entityLabels'] = []
    for it, m in enumerate(composition):
        if it == 0:
            intent = m['name']
        for n in m['args']:
            entityName = n['key']
            # Search the first position in discussion
            try:
                if (not n['val'] == "-1") :  # Exclusion of unpresented data for reliability
                    match = re.search(re.escape(n['val']), some_dict['text'])
                    startCharIndex = match.span()[0]
                    endCharIndex = match.span()[1] - 1  # Last char inclused
                    # Save it
                    some_dict["intentName"] = intent
                    some_dict['entityLabels'].append({"startCharIndex": startCharIndex,
                                     "endCharIndex": endCharIndex,
                                     "entityName": entityName})
            except:
                some_dict["intentName"] = 'None'
    return some_dict


def to_dict(a_dict):
    some_dict = {}
    some_dict['text'] = a_dict['text']
    some_dict = add_entityLabels(some_dict, a_dict)
    return some_dict


def main():
    df = pd.read_json('../data/frames.json')

    data = []
    for m_index, m_value in df['turns'].iteritems():
        for n_index, n_value in enumerate(df['turns'].iloc[m_index]):
            #print(m_index, n_index)
            data.append(to_dict(df['turns'].iloc[m_index][n_index]))

    pd.DataFrame(data).to_json('data.json',orient='records')


if __name__ == "__main__":
    main()