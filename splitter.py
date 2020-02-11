from PyPDF2 import PdfFileWriter, PdfFileReader
from datetime import datetime
import os
import shutil

UPLOAD_PATH = './originals'
SPLITTED_PATH = './splitted'
COMPRESSED_PATH = './compressed'
QR_COUNT = 4


def processingUploadFolder():
    files = [fl for fl in os.listdir(UPLOAD_PATH) if fl.endswith('.pdf')]

    checkPath(SPLITTED_PATH)
    checkPath(UPLOAD_PATH)

    for filename in files:
        splitFile(filename)
        os.remove(UPLOAD_PATH + '/' + filename)

    date = datetime.today().strftime('%d-%m-%Y-%m-%d-%H-%M')
    archivedName = '{}/Splitted_{}'.format(COMPRESSED_PATH, date)
    shutil.make_archive(archivedName, 'zip', SPLITTED_PATH)
    shutil.rmtree(SPLITTED_PATH)
    shutil.rmtree(UPLOAD_PATH)

    return '{}.zip'.format(archivedName)


def splitFile(filename):
    with open(UPLOAD_PATH + '/' + filename, 'rb') as in_f:
        input1 = PdfFileReader(in_f)
        input2 = PdfFileReader(in_f)
        input3 = PdfFileReader(in_f)
        input4 = PdfFileReader(in_f)

        pdfObjects = [input1, input2, input3, input4]
        pdfWriter = PdfFileWriter()

        numPages = PdfFileReader(in_f).numPages

        for page in range(numPages):
            coordinates = {'x_left': 21, 'x_right': 119,
                           'y_top': 822, 'y_bottom': 652,
                           'qr_range': 186}

            count = 0

            while count < QR_COUNT:
                qrObj = getQR(pdfObjects[count], page, coordinates)
                pdfWriter.addPage(qrObj)

                coordinates['y_top'] -= coordinates['qr_range']
                coordinates['y_bottom'] -= coordinates['qr_range']

                count += 1

        with open('{}/Splitted_{}'.format(SPLITTED_PATH, filename), 'wb') as out_f:
            pdfWriter.write(out_f)
            print('Complete {}'.format(filename))


def getQR(pdfReader, pageNum, coordinates):
    page = pdfReader.getPage(pageNum)
    page.cropBox.lowerLeft = (coordinates['x_left'], coordinates['y_top'])
    page.cropBox.upperRight = (coordinates['x_right'], coordinates['y_bottom'])
    return page


def checkPath(path):
    if not os.path.exists(path):
        os.makedirs(path)
