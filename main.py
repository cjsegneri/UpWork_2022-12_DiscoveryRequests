
from PyPDF2 import PdfFileReader

def get_pdf_text(path):
    pdf_reader = PdfFileReader(path)

    pdf_list = []

    for i in range(0,pdf_reader.numPages):
        # if it's the first page, remove the footer

        pdf_list.append(pdf_reader.getPage(i).extractText())
    
    return ' '.join(pdf_list)

def main():
    pdf_text = get_pdf_text('DiscoveryDocuments/BUCHANAN & BUCHANAN, P.A..pdf')

    print(pdf_text)

    # loop through given directory and collect all the file names

    # get the text for every file name

    # for every document, extract the list of discovery requests

    return 0

if __name__ == "__main__":
    main()
