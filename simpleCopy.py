import cv2
import numpy as np
import pdf2image
import pytesseract
import PyPDF2
  
# opened file as reading (r) in binary (b) mode
file = open('info.pdf',
            'rb')
  
# store data in pdfReader
pdfReader = PyPDF2.PdfFileReader(file)
  
# count number of pages
totalPages = pdfReader.numPages
# Extract page 3 from PDF in proper quality

for x in range(totalPages, totalPages+1):
    print(x)
    page_3 = np.array(pdf2image.convert_from_path('info.pdf',
                                                first_page=x, last_page=x,
                                                dpi=300, grayscale=True)[0])

    # Inverse binarize for contour finding
    thr = cv2.threshold(page_3, 128, 255, cv2.THRESH_BINARY_INV)[1]
    pytesseract.tesseract_cmd = r'C:\Users\Dell\AppData\Local\Tesseract-OCR\tesseract.exe'
    # Find contours w.r.t. the OpenCV version
    cnts = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # STEP 1: Extract texts outside of the two tables

    # Mask out the two tables
    cnts_tables = [cnt for cnt in cnts if cv2.contourArea(cnt) > 10000]
    no_tables = cv2.drawContours(thr.copy(), cnts_tables, -1, 0, cv2.FILLED)

    # Find bounding rectangles of texts outside of the two tables
    no_tables = cv2.morphologyEx(no_tables, cv2.MORPH_CLOSE, np.full((21, 51), 255))
    cnts = cv2.findContours(no_tables, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    rects = sorted([cv2.boundingRect(cnt) for cnt in cnts], key=lambda r: r[1])

    # Extract texts from each bounding rectangle
    #print('\nExtract texts outside of the two tables\n')
    for (x, y, w, h) in rects:
        text = pytesseract.image_to_string(page_3[y:y+h, x:x+w],
                                        config='--psm 6', lang='Devanagari')
        text = text.replace('\n', '').replace('\f', '')

        #print('x: {}, y: {}, text: {}'.format(x, y, text))

    # STEP 2: Extract texts from inside of the two tables

    rects = sorted([cv2.boundingRect(cnt) for cnt in cnts_tables],
                key=lambda r: r[1])

    i_q = 0
    # Iterate each table
    for i_r, (x, y, w, h) in enumerate(rects, start=1):
        i_q = i_q + 1
        # Find bounding rectangles of cells inside of the current table
        cnts = cv2.findContours(page_3[y+2:y+h-2, x+2:x+w-2],
                                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        inner_rects = sorted([cv2.boundingRect(cnt) for cnt in cnts],
                            key=lambda r: (r[1], r[0]))

        # Extract texts from each cell of the current table
        #print('\nExtract texts inside table {}\n'.format(i_r))
        for (xx, yy, ww, hh) in inner_rects:

            # Set current coordinates w.r.t. full image
            xx += x
            yy += y

            # Get current cell
            cell = page_3[yy+2:yy+hh-2, xx+2:xx+ww-2]
            if yy+hh-2 <= yy+2 or xx+ww-2 <= xx +2:
                continue
            text = pytesseract.image_to_string(cell, config='--psm 6',
                                                lang='Devanagari')
            text = text.replace('\n', ',').replace('\f', '')
            
            with open('readme.txt', 'a') as f:
                f.write('text: {}\n'.format(text))
            