
import pandas as pd


def group_secondary_requests():
    # read in the request data with primary groups
    df_requests_with_groups = pd.read_csv('requests_with_groups.csv')
    print(df_requests_with_groups.info())
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
