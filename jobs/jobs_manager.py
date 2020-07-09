from sqlalchemy import create_engine as db, Column, Integer, ForeignKey, String, Boolean, databases, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from schemas.models import ClientMain, Channel, ChannelAccess
from datetime import datetime
from jobs.mws_api import mwsRequestMaker
import config

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
		clientData = {}
		for client in Clients:
			engine = db(environment.get('postgres')+ '/client' + str(client.id))
			Session = sessionmaker(bind=engine)
			session = Session()
			cData = (session.query(Channel).join(ChannelAccess,ChannelAccess.channel_id == Channel.id).all())
			session.close()			
			
			for c in cData: 
				print(c.__dict__)