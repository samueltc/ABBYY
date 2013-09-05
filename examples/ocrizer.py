from ABBYY import CloudOCR
import argparse
import os

if __name__=="__main__":
	parser = argparse.ArgumentParser(description='ABBYY CloudOCR')
	parser.add_argument('--application_id', help='Application ID')
	parser.add_argument('--password', help='Password')
	parser.add_argument('--language', help='Specifies recognition language of the document.')
	parser.add_argument('--textType', help='Specifies the type of the text on a page.')
	parser.add_argument('--exportFormat', help='Specifies the export format.')
	parser.add_argument('--pdfPassword', help='Contains a password for accessing password-protected images in PDF format.')
	parser.add_argument('--inputFilename', help='', required=True)
	args = parser.parse_args()

	if 'ABBY_APPLICATION_ID' in os.environ.keys():
		application_id = os.environ['ABBY_APPLICATION_ID']
	else:
		application_id = args.application_id

	if 'ABBY_PASSWORD' in os.environ.keys():
		password = os.environ['ABBY_PASSWORD']
	else:
		password = args.password

	ocr_engine = CloudOCR(application_id, password)

	api_parameters = ['language', 'textType', 'exportFormat', 'pdfPassword']
	parameters = dict(filter(lambda x: x[0] in api_parameters and x[1] is not None, args._get_kwargs()))
	
	input_file = open(args.inputFilename, 'rb')
	post_file = {input_file.name: input_file}
	result = ocr_engine.process_and_download(post_file, **parameters)
	for format, content in result.iteritems():
		output_filename = '{name}.{extension}'.format(name='.'.join(input_file.name.split('.')[:-1]), extension=format)
		with open(output_filename, 'wb') as output_file:
			output_file.write(content)
			output_file.close()
		 