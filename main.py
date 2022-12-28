
from PyPDF2 import PdfFileReader

def get_pdf_text(path):
    pdf_reader = PdfFileReader(path)

    pdf_list = []

    for i in range(0,pdf_reader.numPages):
        page = pdf_reader.getPage(i).extractText()
        # if it's the first page, remove the footer
        if i == 0:
            page = page.split('Filing #')[0]

        pdf_list.append(page)
    
    return ' '.join(pdf_list)

def main():
    #pdf_text = get_pdf_text('DiscoveryDocuments/BUCHANAN & BUCHANAN, P.A..pdf')
    pdf_text = get_pdf_text('DiscoveryDocuments/ANDREW J. GORMAN & ASSOCIATES.pdf')

    print(pdf_text)

    # loop through given directory and collect all the file names

    # get the text for every file name

    # for every document, extract the list of discovery requests

    return 0

if __name__ == "__main__":
    main()
