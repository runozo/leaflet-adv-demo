from pymongo import MongoClient

engine = MongoClient(host="ghiro.beatmatic.it", port=27017,
                     ssl=True, ssl_certfile='client_mongod_nocrypt.pem')
