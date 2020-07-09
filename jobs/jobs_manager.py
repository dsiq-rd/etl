from sqlalchemy import create_engine as db, Column, Integer, ForeignKey, String, Boolean, databases, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from schemas.models import ClientMain, Channel, ChannelAccess
from datetime import datetime
from jobs.mws_api import mwsRequestMaker
import config
import pandas as pd

Base = declarative_base()

#Set which environment are you using
environment = config.environment_type.get('development')

# Creating Engine Connection
engine = db(environment.get('postgres'))
Session = sessionmaker(bind=engine)
session = Session()

class clientManager:
    #Get all Client List
	def clientCollator():
		Clients = session.query(ClientMain).all()
		session.close()
		return Clients

	def getClientDetails():

		#Get all Client Details
		Clients = clientManager.clientCollator()
		clientAccess = {}
		mwsObject = {}
		
		for client in Clients:

			engine = db(environment.get('postgres')+ '/client' + str(client.id))
			Session = sessionmaker(bind=engine)
			session = Session()

			#Channel Access information collected
			access = session.query(ChannelAccess).all()
			session.close()
			alist = []
			channels = []
			# for all clients that have channel access setup
			# Creating a list of unique channel ids
			if access:
				mwsObject['client'+str(client.id)] = []
				for a in access:
					
					channels = session.query(Channel).filter(Channel.id == a.channel_id).first()
					session.close()

					mwsObject['client'+str(client.id)].append(
						{
						a.channel_id:
							{
							'access_key': channels.channel_AWS_client_id,
							'secret_key': channels.channel_aws_secret_key,
							'account_id': a.channel_merchant_id,
							'mws_auth_token': a.channel_auth_token,
							'region': channels.channel_country_code,
							'sqsQueueUrl': a.sqs_endpoint,
							'developer_id': channels.channel_developer_id,
							'marketplace_id': channels.channel_marketplace_id
							}
						}
					)
		print(mwsObject)	
		return mwsObject