
import pandas as pd


def aggregate_groups():
    # read in the requests with their primary and secondary groupings
    df_requests_with_secondary_groups = pd.read_csv('PHASE3_requests_with_secondary_groups.csv')

    print(df_requests_with_secondary_groups.info())
    print(df_requests_with_secondary_groups)

    return 0

def main():
    aggregate_groups()

    return 0

if __name__ == "__main__":
    main()
