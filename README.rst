=====
ABBYY
=====

This package contain a wrapper to the ABBYY Cloud OCR API <http://ocrsdk.com/documentation/apireference/> and some helper functions.

EXAMPLE
=======

    >>> from ABBYY import CloudOCR
    >>> ocr_engine = CloudOCR(application_id='YOUR_ABBYY_APPLICATION_ID', password='YOUR_ABBY_APPLICATION_PASSWORD')
    >>> pdf = open('budget1988.pdf', 'rb')
    >>> file = {pdf.name: pdf}
    >>> result = ocr_engine.process_and_download(file, exportFormat='xml,pdfTextAndImages', language='French')
    >>> result
    {'xml': <_io.BytesIO object at 0x2e2e290>, 'pdfSearchable': <_io.BytesIO object at 0x2e2e2f0>}
