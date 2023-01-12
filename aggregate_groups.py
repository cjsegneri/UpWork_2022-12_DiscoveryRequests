
import pandas as pd


def aggregate_groups():
    # read in the requests with their primary and secondary groupings
    df_req_with_sec_groups = pd.read_csv('PHASE3_requests_with_secondary_groups.csv')
    # print(df_req_with_sec_groups.info())
    # print(df_req_with_sec_groups)

    # for each primary group, find the valid threshold for the secondary grouping
    df_valid_groups = pd.DataFrame()
    max_group_id = df_req_with_sec_groups['GroupID'].max()
    for i in range(1, max_group_id+1):
        # filter for the current group id
        df_current_group = df_req_with_sec_groups.query('GroupID == '+str(i))

        # get the counts for each unqiue pairing of groupid and secondarygroupid
        df_group_by_groups = df_current_group.groupby(
            ['GroupID', 'SecondaryGroupID'])['RequestID'].agg('count').reset_index()

        # calc the threshold by which a secondary group id is valid
        valid_threshold = df_group_by_groups['RequestID'].max() * .4

        # get the valid groupid/secondarygroupid combinations
        df_current_valid_groups = df_group_by_groups.query('RequestID >= '+str(valid_threshold))[[
            'GroupID',
            'SecondaryGroupID']]

        # if the valid_groups df is empty, create a new one
        if df_valid_groups.empty:
            df_valid_groups = df_current_valid_groups.copy(deep=True)

        # else append the rows to the existing valid_groups df
        else:
            df_valid_groups = pd.concat([df_valid_groups, df_current_valid_groups])

    # filter out any data that does not meet the valid secondary grouping thresholds
    df_req_with_sec_groups = pd.merge(df_req_with_sec_groups, df_valid_groups,
        on = ['GroupID', 'SecondaryGroupID'])

    # iterate over the entire dataframe and aggregate final results
    primary_group_id = []
    primary_group_name = []
    sub_group_1_id = []
    sub_group_1_example_a = []
    sub_group_1_example_b = []
    sub_group_2_id = []
    sub_group_2_example_a = []
    sub_group_2_example_b = []
    sub_group_3_id = []
    sub_group_3_example_a = []
    sub_group_3_example_b = []
    sub_group_4_id = []
    sub_group_4_example_a = []
    sub_group_4_example_b = []
    sub_group_5_id = []
    sub_group_5_example_a = []
    sub_group_5_example_b = []
    for i in range(1, max_group_id+1):
        # filter for the current group id
        df_current_group = df_req_with_sec_groups.query('GroupID == '+str(i))

        # aggregate the primarygroupid
        primary_group_id.append(i)

        # aggregate the primarygroupname by finding the top 10 most common words in the requests
        # create a list of every word in the requests
        words = []
        current_group_requests = df_current_group['RequestCleanNoStop'].tolist()
        for i in range(0,len(current_group_requests)):
            r = current_group_requests[i].split()
            for j in range(0,len(r)):
                words.append(r[j])
        # find the occurance count for each unique word
        word_counts = dict()
        for w in words:
            word_counts[w] = word_counts.get(w,0) + 1
        # get the top 10 most frequently occuring words
        word_counts_sorted = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        most_common_words = []
        for i in range(0,10):
            if i < len(word_counts_sorted):
                most_common_words.append(word_counts_sorted[i][0])
        primary_group_name.append(' '.join(most_common_words))

        # aggregate the subgroup1id
        min_sub_group_id = df_current_group['SecondaryGroupID'].min()
        max_sub_group_id = df_current_group['SecondaryGroupID'].max()
        sub_group_1_id.append(min_sub_group_id)

        # aggregate the subgroup1examplea
        df_current_sub_group = df_current_group.query('SecondaryGroupID == '+str(min_sub_group_id))
        sub_group_1_example_a.append(df_current_sub_group['RequestClean'].tolist()[0])

        # aggregate the subgroup1exampleb
        sub_group_1_example_b.append(df_current_sub_group['RequestClean'].tolist()[
            len(df_current_sub_group)-1])

        # determine if there is a second subgroup
        if max_sub_group_id - min_sub_group_id > 0:
            # aggregate the subgroup2id
            sub_group_2_id.append(min_sub_group_id+1)
            # aggregate the subgroup2examplea
            df_current_sub_group = df_current_group.query(
                'SecondaryGroupID == '+str(min_sub_group_id+1))
            sub_group_2_example_a.append(df_current_sub_group['RequestClean'].tolist()[0])
            # aggregate the subgroup2exampleb
            sub_group_2_example_b.append(df_current_sub_group['RequestClean'].tolist()[
            len(df_current_sub_group)-1])
        else:
            sub_group_2_id.append('NA')
            sub_group_2_example_a.append('NA')
            sub_group_2_example_b.append('NA')

        # determine if there is a third subgroup
        if max_sub_group_id - min_sub_group_id > 1:
            # aggregate the subgroup3id
            sub_group_3_id.append(min_sub_group_id+2)
            # aggregate the subgroup3examplea
            df_current_sub_group = df_current_group.query(
                'SecondaryGroupID == '+str(min_sub_group_id+2))
            sub_group_3_example_a.append(df_current_sub_group['RequestClean'].tolist()[0])
            # aggregate the subgroup2exampleb
            sub_group_3_example_b.append(df_current_sub_group['RequestClean'].tolist()[
            len(df_current_sub_group)-1])
        else:
            sub_group_3_id.append('NA')
            sub_group_3_example_a.append('NA')
            sub_group_3_example_b.append('NA')
        
        # determine if there is a fourth subgroup
        if max_sub_group_id - min_sub_group_id > 2:
            # aggregate the subgroup4id
            sub_group_4_id.append(min_sub_group_id+3)
            # aggregate the subgroup4examplea
            df_current_sub_group = df_current_group.query(
                'SecondaryGroupID == '+str(min_sub_group_id+3))
            sub_group_4_example_a.append(df_current_sub_group['RequestClean'].tolist()[0])
            # aggregate the subgroup4exampleb
            sub_group_4_example_b.append(df_current_sub_group['RequestClean'].tolist()[
            len(df_current_sub_group)-1])
        else:
            sub_group_4_id.append('NA')
            sub_group_4_example_a.append('NA')
            sub_group_4_example_b.append('NA')
        
        # determine if there is a fifth subgroup
        if max_sub_group_id - min_sub_group_id > 3:
            # aggregate the subgroup5id
            sub_group_5_id.append(min_sub_group_id+4)
            # aggregate the subgroup5examplea
            df_current_sub_group = df_current_group.query(
                'SecondaryGroupID == '+str(min_sub_group_id+4))
            sub_group_5_example_a.append(df_current_sub_group['RequestClean'].tolist()[0])
            # aggregate the subgroup5exampleb
            sub_group_5_example_b.append(df_current_sub_group['RequestClean'].tolist()[
            len(df_current_sub_group)-1])
        else:
            sub_group_5_id.append('NA')
            sub_group_5_example_a.append('NA')
            sub_group_5_example_b.append('NA')

    # print(primary_group_id)
    # print(primary_group_name)
    # print(sub_group_1_id)
    # print(sub_group_1_example_a)
    # print(sub_group_1_example_b)
    # print(sub_group_2_id)
    # print(sub_group_2_example_a)
    # print(sub_group_2_example_b)
    # print(sub_group_3_id)
    # print(sub_group_3_example_a)
    # print(sub_group_3_example_b)
    # print(sub_group_4_id)
    # print(sub_group_4_example_a)
    # print(sub_group_4_example_b)
    # print(sub_group_5_id)
    # print(sub_group_5_example_a)
    # print(sub_group_5_example_b)

    # convert the lists to a dataframe
    df_groups_final = pd.DataFrame({
        'PrimaryGroupID': primary_group_id,
        'PrimaryGroupName': primary_group_name,
        'SubGroup1ID': sub_group_1_id,
        'SubGroup1ExampleA': sub_group_1_example_a,
        'SubGroup1ExampleB': sub_group_1_example_b,
        'SubGroup2ID': sub_group_2_id,
        'SubGroup2ExampleA': sub_group_2_example_a,
        'SubGroup2ExampleB': sub_group_2_example_b,
        'SubGroup3ID': sub_group_3_id,
        'SubGroup3ExampleA': sub_group_3_example_a,
        'SubGroup3ExampleB': sub_group_3_example_b,
        'SubGroup4ID': sub_group_4_id,
        'SubGroup4ExampleA': sub_group_4_example_a,
        'SubGroup4ExampleB': sub_group_4_example_b,
        'SubGroup5ID': sub_group_5_id,
        'SubGroup5ExampleA': sub_group_5_example_a,
        'SubGroup5ExampleB': sub_group_5_example_b})
    # print(df_groups_final.info())
    # print(df_groups_final)

    # save results to csv file
    df_groups_final.to_csv('PHASE4_groups_final.csv', index=False)

    return 0

def main():
    aggregate_groups()

    return 0

if __name__ == "__main__":
    main()
