
import os
import re
import docx
from PyPDF2 import PdfFileReader
import pandas as pd


def get_pdf_text(path):
    pdf_reader = PdfFileReader(path, strict=False)
    # read in the pdf page by page
    pdf_list = []
    for i in range(0,pdf_reader.numPages):
        page = pdf_reader.getPage(i).extractText()
        # if it's the first page, remove the footer
        if i == 0:
            page = page.split('Filing #')[0]
        pdf_list.append(page+'  ')
    # join all the pdf pages into a single string
    return ' '.join(pdf_list)

def get_doc_text(path):
    doc_reader = docx.Document(path)
    # read in the doc paragraph by paragraph
    doc_list = []
    for p in doc_reader.paragraphs:
        doc_list.append(p.text)
    # join all the doc paragraphs into a single string
    return '\n'.join(doc_list)

def parse_requests():
    # loop through given directory and collect all the file names
    path = 'DiscoveryDocuments/'
    dir_list = os.listdir(path)
    #print(len(dir_list)) # 57 documents in total

    # get the raw text for all the discovery document pdfs
    dir_list_pdf = [f for f in dir_list if '.pdf' in f]
    discovery_text_list = []
    for i in range(0, len(dir_list_pdf)):
        pdf_path = path + dir_list_pdf[i]
        discovery_text = get_pdf_text(pdf_path)
        discovery_text_list.append([dir_list_pdf[i], discovery_text])
    
    # get the raw text for all the discover document word files
    dir_list_doc = [f for f in dir_list if '.doc' in f]
    for i in range(0, len(dir_list_doc)):
        doc_path = path + dir_list_doc[i]
        discovery_test = get_doc_text(doc_path)
        discovery_text_list.append([dir_list_doc[i], discovery_test])
    #print(discovery_text_list[-3:])

    # find the indexes for the pdfs that text could not be extracted from
    broken_pdf_indexes = []
    for i in range(0, len(discovery_text_list)):
        if 'the' not in discovery_text_list[i][1]:
            broken_pdf_indexes.append(i)

    # remove pdfs that text could not be extracted from
    discovery_text_list = [x for i,x in enumerate(discovery_text_list)\
        if i not in broken_pdf_indexes]
    print(discovery_text_list[-3])

    # manually verify the text for each document was read in correctly
    # j = 29
    # print('Document Name: ' + dir_list[j] + '\n\n\n')
    # print(discovery_text_list[j])
    # return 0

    # for every document, extract a list of discovery requests
    discovery_requests_list = []
    for i in range(0, len(discovery_text_list)):
        # this regex matches the requests format
        regex = r'[0-9][0-9]?\.[ \t]{1,}(?:.|\n)*?\.(?=[ ]{2,}|\t|\n| \t| \n| [0-9])'
        regex_matches = re.findall(regex, discovery_text_list[i][1])
        # if there are no matches, then use a slightly different regex
        # that accounts for no space between the number and the request
        if len(regex_matches) == 0:
            regex = r'[0-9][0-9]?\.[ \t]{0,}(?:.|\n)*?\.(?=[ ]{2,}|\t|\n| \t| \n| [0-9])'
            regex_matches = re.findall(regex, discovery_text_list[i][1])
        discovery_requests_list.append([discovery_text_list[i][0], regex_matches])

    # manually verify the requests list for each document
    j = 53
    print(discovery_requests_list[j])
    # for i in range(0, len(discovery_requests_list[j][1])):
    #     print('[[[' + discovery_requests_list[j][1][i] + ']]]\n--------------------\n')
    # print('Document Name: ' + discovery_requests_list[j][0])
    return 0

    # get summary statistics
    # from statistics import mean
    # sum_list = []
    # for i in range(0, len(discovery_requests_list)):
    #     sum_list.append(len(discovery_requests_list[i]))
    # print('\n\nTotal number of documents parsed in: '+str(len(sum_list)))
    # print('Total number of requests parsed out of the documents: '+str(sum(sum_list)))
    # print('Average number of requests per document: '+str(mean(sum_list)))
    # print('\nList containing the total number of requests per document:')
    # print(sum_list)

    # merge requests into a single list
    requests = []
    for i in range(0,len(discovery_requests_list)):
        for j in range(0,len(discovery_requests_list[i][1])):
            requests.append([discovery_requests_list[i][0], discovery_requests_list[i][1][j]])

    # temporarily filter for the first 20 requests
    #requests = requests[:20]

    # clean the requests text
    requests_clean = []
    for i in range(0,len(requests)):
        r = requests[i][1]
        # lowercase all characters
        r = r.lower()
        # remove whitespace at the beginning and end of each request
        r = r.strip()
        # replace all whitespace (spaces, tabs, newlines) with a single space
        r = ' '.join(r.split())
        # remove request number at the beginning of the string
        r = re.sub(r'^[0-9][0-9]?\.[ ]?', '', r)
        # remove all punctuation
        r = re.sub(r'[!\"#\＄%&\'\(\)\*\+,-\./:;<=>\?@\[\\\]\^_`{\|}~]', '', r)
        # append the clean request
        requests_clean.append([requests[i][0], r])
    #print(requests_clean)

    # create a list of every word in the requests
    # words = []
    # for i in range(0,len(requests_clean)):
    #     r = requests_clean[i].split()
    #     for j in range(0,len(r)):
    #         words.append(r[j])
    #print(words)

    # find the occurance count for each unique word
    # word_counts = dict()
    # for w in words:
    #     word_counts[w] = word_counts.get(w,0) + 1
    #print(word_counts)

    # get the most frequently occuring words
    #word_counts_sorted = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # manually verify the most frequently occuring words
    # for i in range(0,150):
    #     print(word_counts_sorted[i])

    # write the most frequently occuring words to a csv
    # import csv
    # with open('stop_words.csv', 'w') as f:
    #     writer = csv.writer(f, delimiter=',', lineterminator='\n')
    #     for i in range(0,200):
    #         row = [word_counts_sorted[i][0], word_counts_sorted[i][1]]
    #         writer.writerow(row)

    # create stop word list
    stop_words = [' the ',' of ',' a ',' to ',' in ',' or ',' as ',' for ',' is ',' have ',
    ' been ',' and ',' which ',' you ',' that ',' this ',' an ',' at ',' by ',' from ',
    ' your ',' was ',' not ',' has ',' andor ',' had ',' no ',' were ',' any ',' are ',
    ' all ',' on ',' he ',' with ',' she ',' did ']

    # remove stopwords
    requests_clean_no_stop = []
    # loop through each request
    for i in range(0,len(requests_clean)):
        request_no_stop = requests_clean[i][1]
        # loop through each stopword, and remove them from each request
        for j in range(0,len(stop_words)):
            request_no_stop = request_no_stop.replace(stop_words[j], ' ')
        # replace double spaces with a single space
        request_no_stop = ' '.join(request_no_stop.split())
        requests_clean_no_stop.append([requests_clean[i][0], request_no_stop])

    # manually verify that the requests have no stopwords
    # for i in range(0,len(requests_clean)):
    #     print(requests_clean[i])
    #     print(requests_clean_no_stop[i]+'\n\n')

    # create pandas dataframe with relevant request information
    requests_final = []
    for i in range(0,len(requests)):
        requests_final.append([
            i+1,
            requests[i][0],
            requests[i][1],
            requests_clean[i][1],
            requests_clean_no_stop[i][1]
        ])
    df_requests = pd.DataFrame(requests_final, columns=[
        'RequestID',
        'DocumentName',
        'RequestRaw',
        'RequestClean',
        'RequestCleanNoStop'
    ])
    df_requests['DocumentID'] = df_requests['DocumentName'].map(hash)
    # print(df_requests)

    # rearrange columns
    df_requests = df_requests[[
        'DocumentID',
        'DocumentName',
        'RequestID',
        'RequestRaw',
        'RequestClean',
        'RequestCleanNoStop']]

    # write results to csv
    df_requests.to_csv('requests.csv', index=False)

    return 0

def main():
    parse_requests()

    return 0

if __name__ == "__main__":
    main()
