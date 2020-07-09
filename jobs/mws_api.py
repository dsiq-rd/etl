from sqlalchemy import create_engine as db, Column, Integer, ForeignKey, String, Boolean, databases, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from schemas.models import ClientMain, Channel, ChannelAccess, sqsProcessLog, mwsProcessLog
from pathlib import Path
import pandas as pd
import config
import mws
import os
import time

Base = declarative_base()
environment = config.environment_type.get('development')

# Creating Engine Connection
engine = db(environment.get('postgres'))
Session = sessionmaker(bind=engine)
session = Session()

class mwsRequestMaker:

	def requestReports(kwargs):
		response = []
		reportType = ['_GET_MERCHANT_LISTINGS_ALL_DATA_',
		'_GET_MERCHANT_LISTINGS_DEFECT_DATA_']
		# '_GET_REFERRAL_FEE_PREVIEW_REPORT_',
		# '_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_',
		# '_GET_SELLER_FEEDBACK_DATA_',
		# '_GET_AFN_INVENTORY_DATA_',
		# '_GET_STRANDED_INVENTORY_LOADER_DATA_',
		# '_GET_EXCESS_INVENTORY_DATA_',
		# '_GET_GST_MTR_B2B_CUSTOM_',
		# '_GET_GST_MTR_B2C_CUSTOM_']

		reportobj = mws.Reports(
			kwargs['access_key'],
			kwargs['secret_key'],
			kwargs['account_id'],
			region=kwargs['region'],
			auth_token=kwargs['mws_auth_token']
			)
		
		for typeOfReport in reportType:
			request = reportobj.request_report(typeOfReport)
			response.append(request.parsed)
			time.sleep(2)	
		
		return responseProcessor.mwsResponseProcessor(response, '1')


	def requestOrder(self, kwargs):
		reportList = kwargs['request_list']	
		response = []

		ordersobj = mws.Ordersmws.Reports(
			access_key = kwargs['access_key'],
			secret_key = kwargs['secret_key'],
			account_id = kwargs['account_id'],
			region = kwargs['region']
			)

	def requestProducts(self, kwargs):
		productsobj = mws.Products(
			access_key = kwargs['access_key'],
			secret_key = kwargs['secret_key'],
			account_id = kwargs['account_id'],
			region = kwargs['region']
			)

	def submitFeeds(self, kwargs):
		feedObj = mws.Products(
			access_key = kwargs['access_key'],
			secret_key = kwargs['secret_key'],
			account_id = kwargs['account_id'],
			region = kwargs['region']
			)

class responseProcessor:

	#Processing Response Based on Request.
	def mwsResponseProcessor(responses, client):
		if responses:
			dataDict = {
			 		'ReportType':[], 
			 		'ReportProcessingStatus':[], 
			 		'StartDate':[], 
			 		'EndDate':[], 
			 		'Scheduled':[], 
			 		'ReportRequestId':[], 
			 		'SubmittedDate':[],
			 		'RequestId':[]
			 		}
			for response in responses:
				dataDict['ReportType'].append(response.ReportRequestInfo.getvalue('ReportType'))
				dataDict['ReportProcessingStatus'].append(response.ReportRequestInfo.getvalue('ReportProcessingStatus'))
				dataDict['StartDate'].append(response.ReportRequestInfo.getvalue('StartDate'))
				dataDict['EndDate'].append(response.ReportRequestInfo.getvalue('EndDate'))
				dataDict['Scheduled'].append(response.ReportRequestInfo.getvalue('Scheduled'))
				dataDict['ReportRequestId'].append(response.ReportRequestInfo.getvalue('ReportRequestId'))
				dataDict['SubmittedDate'].append(response.ReportRequestInfo.getvalue('SubmittedDate'))
				dataDict['RequestId'].append(response.ReportRequestInfo.getvalue('RequestId'))

		#Adding Data to mwsProcessLog Tables
			print(dataDict)
			responsedf = pd.DataFrame(dataDict)
			print(responsedf)
			ModelObj = mwsProcessLog()
			engine = db(environment.get('postgres') + '/client' + client)
			Session = sessionmaker(bind=engine)
			session = Session()
			session.bulk_insert_mappings(ModelObj, responsedf.to_dict(orient="records"))
			session.commit()
			session.close()