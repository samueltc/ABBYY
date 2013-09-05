ABBYY
=====

This package contain a wrapper to the ABBYY Cloud OCR API <http://ocrsdk.com/documentation/apireference/> and some helper functions.

EXAMPLE
========

    >>> from ABBYY import CloudOCR
    >>> ocr_engine = CloudOCR(application_id=', password='')
    >>> pdf = open('budget1988.pdf', 'rb')
    >>> file = {pdf.name: pdf}
    >>> result = ocr_engine.process_and_download(file, exportFormat='xml,pdfTextAndImages', language='French')
    >>> result['pdfSearchable'][0:10]
    '%PDF-1.5\n%'