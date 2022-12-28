
import os
import re
from PyPDF2 import PdfFileReader

def get_pdf_text(path):
    pdf_reader = PdfFileReader(path, strict=False)

    pdf_list = []

    for i in range(0,pdf_reader.numPages):
        page = pdf_reader.getPage(i).extractText()
        # if it's the first page, remove the footer
        if i == 0:
            page = page.split('Filing #')[0]

        pdf_list.append(page+'  ')
    
    return ' '.join(pdf_list)

def main():
    #pdf_text = get_pdf_text('DiscoveryDocuments/Chartwell Law.pdf')
    #print(pdf_text)

    # loop through given directory and collect all the file names
    path = 'DiscoveryDocuments/'

    dir_list = os.listdir(path)

    #print(len(dir_list)) # 57 documents in total

    # get the raw text for discovery document
    discovery_text_list = []
    for i in range(0, len(dir_list)):
        pdf_path = path + dir_list[i]

        discovery_text = get_pdf_text(pdf_path)

        discovery_text_list.append(discovery_text)
    
    # manually verify the text for each document was read in correctly
    # j = 56
    # print('Document Name: ' + dir_list[j] + '\n\n\n')
    # print(discovery_text_list[j])

    # for every document, extract the list of discovery requests
    discovery_requests_list = []
    for i in range(0, len(discovery_text_list)):
        regex = r'[0-9][0-9]?\.[ \t]{1,}(?:.|\n)*?\.(?:[ ]{2,}|\t|\n)'

        regex_matches = re.findall(regex, discovery_text_list[i])
        
        discovery_requests_list.append(regex_matches)

    # manually verify the requests list for each document
    j = 0
    print('Document Name: ' + dir_list[j] + '\n\n\n')
    for i in range(0, len(discovery_requests_list[j])):
        print('[[' + discovery_requests_list[j][i] + ']]\n')

    # clean the requests text
        # remove whitespace at the beginning and end of each request
        # replace all whitespace (spaces, tabs, newlines) with a single space

    # identify and remove stopwords

    return 0

if __name__ == "__main__":
    main()
