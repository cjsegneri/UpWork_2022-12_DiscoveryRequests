
import pandas as pd


def group_secondary_requests():
    # read in the request data with primary groups
    df_requests_with_groups = pd.read_csv('requests_with_groups.csv')
    #print(df_requests_with_groups)

    # filter out any meaningless groups which have 10% or less requests than the largest group
    invalid_group_threshold = df_requests_with_groups.query('GroupID == 1')['GroupID'].count() *.2
    valid_groups_max_id = df_requests_with_groups.groupby(['GroupID']).count().query(
        'RequestID >= '+str(invalid_group_threshold))['RequestID'].count()
    df_requests_with_groups = df_requests_with_groups.query('GroupID <= '+str(valid_groups_max_id))
    print(df_requests_with_groups)

    # run the secondary similarity algorithm for each group
    # max_group_id = df_requests_with_groups['GroupID'].max()
    # print(max_group_id) # 450
    # for i in range(1, max_group_id+1):
    #     df_current_group = df_requests_with_groups.query('GroupID == '+str(i))
    #     print(df_current_group)
    #     break

    return 0

def main():
    group_secondary_requests()

    return 0

if __name__ == "__main__":
    main()
