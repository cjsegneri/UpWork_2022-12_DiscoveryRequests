
from itertools import combinations
import pandas as pd
from fuzzywuzzy import fuzz


def group_similar_strings(threshold, min_group_size, df, id_column_name, str_column_name):
    # create initial pairing dictionary where every request is paired with itself
    paired = {}
    list_of_tuples = []
    for i in df.index:
        list_of_tuples.append((df[id_column_name][i], df[str_column_name][i]))
        paired[df[str_column_name][i]] = ({(df[id_column_name][i],
            df[str_column_name][i])})

    # group requests together if the fuzzy matching algorithm meets threshold
    for a,b in combinations(list_of_tuples, 2):
        if fuzz.token_sort_ratio(a[1],b[1]) >= threshold:
            paired[a[1]].add(b)
            paired[b[1]].add(a)

    # find the best groupings of unique requests
    groups = []
    ungrouped = set(list_of_tuples)
    while ungrouped:
        best_group = {}
        for request in ungrouped:
            g = paired[request[1]] & ungrouped
            for c in g.copy():
                g &= paired[c[1]]
            if len(g) > len(best_group):
                best_group = g
        if len(best_group) < min_group_size:
            break
        ungrouped -= best_group
        groups.append(best_group)

    # convert the list of sets of tuples into a list of lists
    groups_list = []
    for i in range(0,len(groups)):
        for r in groups[i]:
            groups_list.append([i+1, r[0]])
    #print(groups_list)

    # convert the list of lists into a dataframe
    return pd.DataFrame(groups_list, columns = ['GroupID', id_column_name])

def group_requests():
    # read in the parsed request data
    df_requests = pd.read_csv('requests.csv')

    df_groups = group_similar_strings(
        threshold = 90,
        min_group_size = 1,
        df = df_requests,
        id_column_name = 'RequestID',
        str_column_name = 'RequestCleanNoStop')
    # print(df_groups.info())
    # print(df_groups)

    # join the groups data back to the orginal request df
    df_requests_with_groups = pd.merge(df_requests, df_groups,
        on = 'RequestID')[[
            'GroupID',
            'DocumentName',
            'RequestID',
            'RequestClean',
            'RequestCleanNoStop',
            'RequestRaw']]
    #print(df_requests_with_groups.info())
    #print(df_requests_with_groups)

    # order the dataframe
    df_requests_with_groups = df_requests_with_groups.sort_values(
        ['GroupID', 'DocumentName', 'RequestID'],
        ascending = [True, True, True])

    # save results to csv file
    df_requests_with_groups.to_csv('requests_with_groups.csv', index=False)

    return 0

def main():
    group_requests()

    return 0

if __name__ == "__main__":
    main()
