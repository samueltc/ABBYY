from ABBYY import CloudOCR
from PIL import Image
import sys, os
from io import StringIO

def extract_and_ocr(filename, region):
	application_id = os.environ['ABBYY_APPLICATION_ID']
	password = os.environ['ABBYY_PASSWORD']
	ocr_engine = CloudOCR(application_id=application_id, password=password)

	image = Image.open(filename)
	region_data = image.crop(region)
	stream = StringIO()
	region_data.save(stream, 'JPEG')
	stream.seek(0)

	post_file = {'temp.jpg': stream}
	result = ocr_engine.process_and_download(post_file,exportFormat='txt')

	return result['txt'].read()

if __name__=='__main__':
	if '-demo' in sys.argv:
		print(extract_and_ocr('test.png', (30,325,725,400)))
	elif len(sys.argv) == 2:
		configs = eval(sys.argv[1])
		for filename, region in configs:
			print(filename, region, "result:", extract_and_ocr(filename, region))
	else:
		print("example:")
		print("python " + sys.argv[0] + " \"[('test.png', (30,325,725,400)), ('test.png', (730, 385,800,600))]\"")
