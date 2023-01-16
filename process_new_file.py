
import pandas as pd
from fuzzywuzzy import fuzz
from parse_requests import parse_requests


def process_new_file(path, parse_csv_filename, final_csv_filename):
    # parse the new file
    parse_requests(path=path, csv_name=parse_csv_filename)
    df_new_requests = pd.read_csv(parse_csv_filename)

    # read in the existing groups
    df_existing_requests = pd.read_csv('PHASE3_requests_with_secondary_groups.csv')

    # find the request matches that are most similar
    request_best_matches = [] # [currid, matchid, ratio, groupid, secondarygroupid]
    for i in range(0, len(df_new_requests)):
        current_request_id = df_new_requests['RequestID'][i]
        current_request_text = df_new_requests['RequestCleanNoStop'][i]
        best_match = []
        for j in range(0, len(df_existing_requests)):
            existing_request_id = df_existing_requests['RequestID'][j]
            existing_request_group_id = df_existing_requests['GroupID'][j]
            existing_request_secondary_group_id = df_existing_requests['SecondaryGroupID'][j]
            existing_request_text = df_existing_requests['RequestCleanNoStop'][j]
            ratio = fuzz.token_sort_ratio(current_request_text, existing_request_text)
            match = [current_request_id, existing_request_id, ratio, existing_request_group_id,
                existing_request_secondary_group_id]
            if len(best_match) == 0 or match[2] > best_match[2]:
                best_match = match
        request_best_matches.append(best_match)

    # write results to csv
    df_best_matches = pd.DataFrame(request_best_matches, columns = [
        'RequestID',
        'MatchedRequestID',
        'SimilarityRatio',
        'GroupID',
        'SecondaryGroupID'])
    df_new_requests = pd.merge(df_new_requests, df_best_matches, on = 'RequestID')[[
        'DocumentID',
        'DocumentName',
        'RequestID',
        'MatchedRequestID',
        'SimilarityRatio',
        'GroupID',
        'SecondaryGroupID',
        'RequestRaw',
        'RequestRaw',
        'RequestClean',
        'RequestCleanNoStop']]
    df_new_requests.to_csv(final_csv_filename, index=False)

    return 0

def main():
    process_new_file(path='NewFiles/',
        parse_csv_filename='NEWFILES_requests.csv',
        final_csv_filename='NEWFILES_groups.csv')

    return 0

if __name__ == "__main__":
    main()
