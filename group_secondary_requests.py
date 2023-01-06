
import pandas as pd
from group_requests import group_similar_strings


def group_secondary_requests():
    # read in the request data with primary groups
    df_requests_with_groups = pd.read_csv('requests_with_groups.csv')

    # filter out any meaningless groups which have 10% or less requests than the largest group
    invalid_group_threshold = df_requests_with_groups.query('GroupID == 1')['GroupID'].count() *.2
    valid_groups_max_id = df_requests_with_groups.groupby(['GroupID']).count().query(
        'RequestID >= '+str(invalid_group_threshold))['RequestID'].count()
    df_requests_with_groups = df_requests_with_groups.query('GroupID <= '+str(valid_groups_max_id))

    # run the secondary similarity algorithm for each group
    df_requests_with_secondary_groups = pd.DataFrame()
    max_group_id = df_requests_with_groups['GroupID'].max()
    for i in range(1, max_group_id+1):
        # filter for the current group
        df_current_group = df_requests_with_groups.query('GroupID == '+str(i)).copy(deep=True)

        # get each request for the current group
        current_requests = df_current_group['RequestCleanNoStop'].tolist()
        # split each request into a unique list of words
        current_requests_words = []
        for j in range(0, len(current_requests)):
            current_requests_words.append([*set(current_requests[j].split())])
        # find the frequency for each word within the requests
        word_freq = {}
        for word_list in current_requests_words:
            for word in word_list:
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1
        # filter out the most common words
        unique_word_threshold = len(current_requests) *.9
        secondary_grouping_stop_words = []
        for key, value in word_freq.items():
            if value > unique_word_threshold:
                secondary_grouping_stop_words.append(key)
        # remove the stopwords from each request
        current_requests_no_stop = []
        for j in range(0, len(current_requests_words)):
            current_requests_no_stop.append(' '.join([wl for wl in current_requests_words[j] \
                if wl not in secondary_grouping_stop_words]))
        # add the requests with secondary stopwords removed as a new column in the df
        df_current_group['RequestCleanNoStop_SecNoStop'] = current_requests_no_stop

        # run the similarity algorithm
        df_secondary_groups = group_similar_strings(
            threshold = 90,
            min_group_size = 1,
            df = df_current_group,
            id_column_name = 'RequestID',
            str_column_name = 'RequestCleanNoStop_SecNoStop',
            new_column_name = 'SecondaryGroupID')

        # join the groups data back to the orginal request df
        df_current_group = pd.merge(df_current_group, df_secondary_groups,
            on = 'RequestID')[[
                'GroupID',
                'SecondaryGroupID',
                'DocumentName',
                'RequestID',
                'RequestCleanNoStop_SecNoStop',
                'RequestClean',
                'RequestCleanNoStop',
                'RequestRaw']]

        # if no rows have been appended to the empty dataframe, copy the current df
        if df_requests_with_secondary_groups.empty:
            df_requests_with_secondary_groups = df_current_group
        # else, append the current df
        else:
            df_requests_with_secondary_groups = pd.concat([
                df_requests_with_secondary_groups,
                df_current_group])

    # order the dataframe
    df_requests_with_secondary_groups = df_requests_with_secondary_groups.sort_values(
        ['GroupID', 'SecondaryGroupID', 'DocumentName', 'RequestID'],
        ascending = [True, True, True, True])

    # save results to csv file
    df_requests_with_secondary_groups.to_csv('requests_with_secondary_groups.csv', index=False)

    return 0

def main():
    group_secondary_requests()

    return 0

if __name__ == "__main__":
    main()
