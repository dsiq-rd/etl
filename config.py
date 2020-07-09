# All system configutation

def SQLAlchemyBinds(client_id):
	results = {
		"core": "postgresql://postgres:Maisha123@localhost",
		"client": "postgresql://postgres:Maisha123@localhost/client" + str(client_id) 
		}
	return results

environment_type = {
	"development": {
		"postgres": "postgresql://postgres:Maisha123@localhost",
		"broker": "redis://user:Maisha123@localhost:6379/0",
		"backend": "db+postgres://postgres:Maisha123@localhost/postgres",
		"MWS_DEVELOPER_ID": "403292020257",
		"MWS_ACCESS_KEY_ID": "AKIAJG6GTCJEJZOID4ZA",
		"MWS_CLIENT_SECRET_KEY": "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",
		"AWS_SECRET_KEY": "aws",
		"AWS_SECRET_ACCESS_CODE": "aws",
		"SQLALCHEMY_TRACK_MODIFICATIONS": False,
		"JWT_ALGORITHM": "RS256",
		"JWT_BLACKLIST_ENABLED": True,
		"JWT_BLACKLIST_TOKEN_CHECKS": ['access', 'refresh']
	},
	"staging": {
		"postgres": "stagingdb",
		"SECRET_KEY": "aws",
		"ACCESS_CODE": "aws",
		"SQLALCHEMY_TRACK_MODIFICATIONS": False,
		"JWT_SECERET_KEY" : ""
	},
	"production": {
		"postgres": "production",
		"SECRET_KEY": "secretkey",
		"ACCESS_CODE": "Access Code",
		"SQLALCHEMY_TRACK_MODIFICATIONS": False,
		"JWT_SECERET_KEY" : ""
	}
	}