

def group_secondary_requests():
    ### SECONDARY GROUPING ###
    # for now just test with the first primary group
    #df_requests_with_groups = df_requests_with_groups.query('GroupID == 1')

    # run the secondary similarity algorithm for each group
    max_group_id = df_requests_with_groups['GroupID'].max()
    print(max_group_id) # 450
    for i in range(1, max_group_id+1):
        df_current_group = df_requests_with_groups.query('GroupID == '+str(i))
        print(df_current_group)
        break

    return 0

def main():
    group_secondary_requests()

    return 0

if __name__ == "__main__":
    main()
