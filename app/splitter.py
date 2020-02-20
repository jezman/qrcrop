from PyPDF2 import PdfFileWriter, PdfFileReader
from datetime import datetime
import os
import shutil
from qrparse import create_csv
from app import app


def getCoordinations(vertical):
    if vertical:
        return {'x_left': 21, 'x_right': 119,
                'y_top': 822, 'y_bottom': 652,
                'qr_range': 186, 'orientation': 'vertical', 'qr_count': 4}
    else:
        return {'x_left': 21, 'x_right': 190,
                'y_top': 822, 'y_bottom': 723,
                'qr_range': 118, 'orientation': 'horizontal', 'qr_count': 6}


def processingUploadFolder(orientation):
    files = [fl for fl in os.listdir(app.config['UPLOAD_PATH']) if fl.endswith('.pdf')]

    checkPath(app.config['SPLITTED_PATH'])
    checkPath(app.config['UPLOAD_PATH'])

    for filename in files:
        create_csv(filename)
        splitFile(filename, orientation)
        os.remove(os.path.join(app.config['UPLOAD_PATH'], filename))

    date = datetime.today().strftime('%d-%m-%Y-%m-%d-%H-%M')
    archivedName = '{}/Splitted_{}'.format(app.config['COMPRESSED_PATH'], date)
    shutil.make_archive(archivedName, 'zip', app.config['SPLITTED_PATH'])
    shutil.rmtree(app.config['SPLITTED_PATH'])
    shutil.rmtree(app.config['UPLOAD_PATH'])

    return '{}.zip'.format(archivedName)


def splitFile(filename, vertical):
    with open(os.path.join(app.config['UPLOAD_PATH'], filename), 'rb') as in_f:
        input1 = PdfFileReader(in_f)
        input2 = PdfFileReader(in_f)
        input3 = PdfFileReader(in_f)
        input4 = PdfFileReader(in_f)
        input5 = PdfFileReader(in_f)
        input6 = PdfFileReader(in_f)

        pdfObjects = [input1, input2, input3, input4, input5, input6]
        pdfWriter = PdfFileWriter()

        numPages = PdfFileReader(in_f).numPages

        for page in range(numPages):
            coordinates = getCoordinations(vertical)
            count = 0

            while count < coordinates['qr_count']:
                qrObj = getQR(pdfObjects[count], page, coordinates)
                pdfWriter.addPage(qrObj)

                coordinates['y_top'] -= coordinates['qr_range']
                coordinates['y_bottom'] -= coordinates['qr_range']

                count += 1

        with open('{}/Splitted_{}'.format(app.config['SPLITTED_PATH'], filename), 'wb') as out_f:
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
