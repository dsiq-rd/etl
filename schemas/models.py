from sqlalchemy import create_engine as db, Column, Integer,ForeignKey, String, Boolean, databases, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import config

Base = declarative_base()
#Set which environment are you using
environment = config.environment_type.get('development')

# Creating Engine Connection
engine = db(environment.get('postgres'))
Session = sessionmaker(bind=engine)
session = Session()

class TimeStamp(object):
	created_date = Column(Integer, default=datetime.utcnow().strftime('%Y%m%d'))
	created_time = Column(Integer, default=datetime.utcnow().strftime('%H%M%S'))
	updated_date = Column(Integer, default=datetime.utcnow().strftime('%Y%m%d'), onupdate=datetime.utcnow().strftime('%Y%m%d'))
	updated_time = Column(Integer, default=datetime.utcnow().strftime('%H%M%S'), onupdate=datetime.utcnow().strftime('%H%M%S'))
	created_by = Column(String, default='app')
	updated_by = Column(String, default='app')

class ClientMain(Base):
	__tablename__ = 'client'
	id = Column(Integer, primary_key=True)
	first_name = Column(String)
	last_name = Column(String)
	email = Column(String, unique=True, nullable=False)
	company = Column(String)
	gst_number = Column(String, unique=True)
	address1 = Column(String)
	address2 = Column(String)
	state = Column(String)
	city = Column(String)
	zipcode = Column(String)
	country = Column(String)
	status = Column(String)

class ClientUser(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	first_name = Column(String)
	last_name = Column(String)
	pid = Column(String, unique=True) # Used for storing public id 
	password = Column(String, nullable=False)
	email = Column(String, unique=True, nullable=False)
	status = Column(String)

class DsiqApp(Base):
	__tablename__ = 'apps'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	version = Column(String)
	releasedate = Column(DateTime)

class ClientSubscription(Base):
	__tablename__ = 'subscription'
	id = Column(Integer, primary_key=True)
	client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
	apps_id = Column(Integer, ForeignKey('apps.id'), nullable=False)

class ClientBilling(TimeStamp, Base):
	__tablename__ = 'clientbilling'
	id = Column(Integer, primary_key=True)
	client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
	apps_id = Column(Integer, ForeignKey('apps.id'), nullable=False)
	type = Column(String)
	amount = Column(Float)

# Client Tables developed for specific clients level information:

class TokenBlackList(Base):
	__tablename__ = 'blacklist'
	__bind_key__ = 'client'
	id = Column(Integer, primary_key=True)
	jti = Column(String(36), nullable=False)
	token_type = Column(String(10), nullable=False)
	user_identity = Column(String, nullable=False)
	revoked = Column(Boolean)
	expires = Column(DateTime)
	epoch_expires = Column(Integer)
	client_id = Column(String)
	
# Need to figure out if we can create a join across DB or else we need to create a single record at insertion.

class Channel(Base):
	__tablename__ = 'channel'
	__bind_key__ = 'client'
	id = Column(Integer, primary_key=True)
	parent_company = Column(String)
	channel_region = Column(String)
	channel_country = Column(String)
	channel_country_code = Column(String)
	channel_website = Column(String)
	channel_seller_website = Column(String)
	channel_api_endpoint = Column(String)
	channel_marketplace_id = Column(String)
	channel_developer_id = Column(String)
	channel_AWS_client_id = Column(String)
	channel_aws_secret_key = Column(String)
	channel_api_id = Column(String)

class ChannelAccess(Base):
	__tablename__ = 'channelaccess'
	__bind_key__ = 'client'
	id = Column(Integer, primary_key=True)
	channel_id = Column(Integer)
	channel_auth_token = Column(String)
	channel_secret_key = Column(String)
	channel_merchant_id = Column(String)
	channel_username = Column(String)
	channel_password = Column(String)
	channel_last_run = Column(Boolean, default=False)
	sqs_endpoint = Column(String)

class ClientProducts(Base):
	__tablename__ = 'productmaster'
	__bind_key__ = 'client'
	id = Column(Integer, primary_key=True)
	manufacturer_id = Column(String)
	product_name = Column(String)
	product_brands = Column(String)
	product_description = Column(String)
	product_price = Column(Float)
	product_mrp = Column(Float)
	product_currency = Column(Float)

class mwsProcessLog(Base):
	__tablename__ = 'amzmwsprocesslog'
	__bind_key__ = 'client'
	id = Column(Integer, primary_key=True)
	ReportType = Column(String)
	ReportProcessingStatus = Column(String)
	EndDate = Column(DateTime)
	Scheduled = Column(Boolean)
	ReportRequestId = Column(String)
	StartDate = Column(DateTime)
	SubmittedDate = Column(DateTime)
	RequestId = Column(String)

class sqsProcessLog(Base):
	__tablename__ = 'amzsqsprocesslog'
	__bind_key__ = 'client'
	id = Column(Integer, primary_key=True)
	MessageId = Column(String)
	ReceiptHandle = Column(String)
	MD5OfBody = Column(String)
	attributetimestamp = Column(String)
	NotificationType = Column(String)
	UniqueId = Column(String, unique=True)
	PublishTime = Column(DateTime)
	SellerId = Column(String)
	ReportRequestId = Column(String)
	ReportType = Column(String)
	ReportId = Column(String)
	ReportProcessingStatus = Column(String)
	is_deleted = Column(Boolean)

class jobMain(Base,TimeStamp):
	__tablename__ = 'joblrequestlogger'
	__bind_key__ = 'client'
	id = Column(Integer, primary_key=True)
	channel_id = Column(Integer)

class jobType(Base):
	__tablename__ = 'jobtype'
	id = Column(Integer, primary_key=True)
	jobId = Column(Integer, ForeignKey('jobMain.id'), nullable=False)
	jobType = Column(String)

class modelHelper:
	def getallClients(self):
		query = session.query(ClientMain).all()
		return query
