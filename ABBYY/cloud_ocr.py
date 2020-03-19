import requests
from lxml import html, etree
import time
from io import BytesIO

# http://ocrsdk.com/documentation/apireference/processImage/
DEFAULT_EXPORT_FORMAT='rtf'

class CloudOCR:
	"""
	See http://ocrsdk.com/documentation/apireference/
	"""
	base_url = "http://cloud.ocrsdk.com"

	def __init__(self, application_id, password):
		self.session = requests.Session()
		self.auth = (application_id, password)

	def processImage(self, file, **kwargs):
		return self._postfile('processImage', file, **kwargs).pop()

	def submitImage(self, file, **kwargs):
		return self._postfile('submitImage', file, **kwargs).pop()

	def processDocument(self, **kwargs):
		return self._get('processDocument', **kwargs).pop()

	def processBusinessCard(self, file, **kwargs):
		return self._postfile('processBusinessCard', file, **kwargs).pop()

	def processTextField(self, file, **kwargs):
		return self._postfile('processTextField', file, **kwargs).pop()

	def processBarcodeField(self, file, **kwargs):
		return self._postfile('processBarcodeField', file, **kwargs).pop()

	def processCheckmarkField(self, file, **kwargs):
		return self._postfile('processCheckmarkField', file, **kwargs).pop()

	def processFields(self, **kwargs):
		return self._get('processFields', **kwargs).pop()

	def processMRZ(self, files, **kwargs):
		return self._postfile('processMRZ', files, **kwargs).pop()

	def getTaskStatus(self, **kwargs):
		return self._get('getTaskStatus', **kwargs).pop()

	def listTasks(self, **kwargs):
		return self._get('listTasks', **kwargs)

	def deleteTask(self, **kwargs):
		return self._get('deleteTask', **kwargs).pop()

	def listFinishedTasks(self, **kwargs):
		return self._get('listFinishedTasks', **kwargs)

	def _postfile(self, method, file, **kwargs):
		reply = self.session.post('{base_url}/{method}'.format(base_url=self.base_url, method=method), auth=self.auth, params=kwargs, files=file)
		return self._process_reply(reply)

	def _get(self, method, **kwargs):
		reply = self.session.get('{base_url}/{method}'.format(base_url=self.base_url, method=method), auth=self.auth, params=kwargs)
		return self._process_reply(reply)

	def _process_reply(self, reply):
		# raise if authentication failed, server error, ...
		reply.raise_for_status()

		xml = etree.fromstring(reply.content)
		if xml.xpath('//error/message'):
			raise Exception(xml.xpath('//error/message')[0].text)

		elements = xml.xpath('//response')
		if elements.__len__() != 1:
			raise Exception("Bad server response:" + reply)

		response = []
		for element in elements[0]:
			response.append(dict(list(zip(list(element.keys()), list(element.values())))))
		return response

	# helper functions
	def wait_for_task(self, task, delay_between_status_check=1, timeout=300):
		taskId = task['id']
		for i in range(timeout):
			task = self.getTaskStatus(taskId=taskId)
			if task['status'] == 'InProgress' or  task['status'] == 'Queued':
				delay_between_status_check = int(task['estimatedProcessingTime'])
				time.sleep(delay_between_status_check)
			elif task['status'] == 'NotEnoughCredits':
				raise Exception('NotEnoughCredits')
			else:
				return task
		raise Exception("OCR Timed out")

	def process_and_download(self, file, timeout=300, **kwargs):
		if 'exportFormat' in list(kwargs.keys()):
			formats = kwargs['exportFormat']
		else:
			formats = DEFAULT_EXPORT_FORMAT
		formats = formats.split(',')

		task = self.processImage(file=file, **kwargs)
		result = self.wait_for_task(task, timeout=timeout)

		urls_keys = [key for key in list(result.keys()) if key.startswith('resultUrl')]
		urls = list(zip(formats, list(map(result.__getitem__, urls_keys))))

		streams = dict()
		for format, url in urls:
			result = self.session.get(url)
			streams[format] = BytesIO(result.content)
		return streams
