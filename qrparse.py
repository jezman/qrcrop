import numpy as np
import pdftotext

UPLOAD_PATH = './originals'
SPLITTED_PATH = './splitted'
# symbols = {
#     '&': '&amp',
#     '\"': '&quot',
#     '\'': '&apos',
#     '>': '&gt',
#     '<': '&lt',
# }

to_remove = ['МОДЕЛЬ', 'РАЗМЕР', '--', '']


def get_codes(pdf):
    codes = list()

    for page in pdf:
        page = page.split('\n')
        page = [code.strip() for code in page if code not in to_remove]
        two_codes = ([''.join(page[i:i + 2]) for i in range(0, len(page), 2)])
        [codes.append(code) for code in two_codes]

    return codes


def create_csv(pdf_file):
    with open(UPLOAD_PATH + '/' + pdf_file, "rb") as f:
        pdf = pdftotext.PDF(f)
        codes = get_codes(pdf)
        codes = [code.replace('"', '""') for code in codes]
        np.savetxt(
            '{}/Splitted_{}.csv'.format(SPLITTED_PATH, pdf_file.split('.')[0]),
            codes, fmt='"%s"', delimiter=",")
