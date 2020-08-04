from jobs.mws_api import mwsRequestMaker
from mws import MWSError

kwargs = {
		'access_key':'AKIAJG6GTCJEJZOID4ZA',
		'secret_key':'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',
		'account_id':'A3RLDUMUDRLH0Y',
		'region':'IN',
		'mws_auth_token':'amzn.mws.b8b8fd5d-4732-ffb9-3bc7-e662d0ac4aa4'
		}
try:
	req = mwsRequestMaker.requestReports(kwargs)
except MWSError as e:
	res = e.response
	# print(res.reason)
	# print(res.status_code)
	print(res.text)
	# print(res.url)


