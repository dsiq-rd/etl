import mws
import xml.etree.ElementTree as et
from datetime import datetime
import time

class mwsRequestMaker:

	def reportRequestMaker(self, kwargs):
		response_processor = mwsRequestProcessor()

		mwsObject = mws.Reports(
			kwargs['access_key'],
			kwargs['secret_key'],
			kwargs['account_id'],
			region=kwargs['region'],
			auth_token=kwargs['mws_auth_token']
			)

		for reportTypes in typesOfReports:
			response = mwsObject.request_report(reportTypes)
			processor = response_processor.getReportProcessor(response)	
			time.sleep(2.5)


class mwsRequestProcessor:
	def getReportProcessor(self, kwargs):
		pass


