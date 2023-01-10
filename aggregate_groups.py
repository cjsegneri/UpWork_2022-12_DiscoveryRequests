
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

    return 0

def main():
    aggregate_groups()

    return 0

if __name__ == "__main__":
    main()
