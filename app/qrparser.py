from app import app
import os
import numpy as np
import pdftotext

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
    with open(os.path.join(app.config['UPLOAD_PATH'], pdf_file), "rb") as f:
        pdf = pdftotext.PDF(f)
        codes = get_codes(pdf)
        codes = [code.replace('"', '""') for code in codes]
        np.savetxt(
            f"{app.config['SPLITTED_PATH']}/splitted_{pdf_file.split('.')[0]}",
            codes, fmt='"%s"', delimiter=",")
