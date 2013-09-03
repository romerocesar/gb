# import the data access layer (DAL)
from dal import mongo, test

# DB access config. This data access object (DAO) will be used for all
# DB access in the orders app. This allows us to transparently change
# the DB from Mongo to Postgres or anything else by simply changing
# this line and not changing anything in the application layer. For
# example, enable the test DAO by simply uncommenting the following
# line. Also, you have the option of bootstraping the DB by cleaning
# it up and loading it with test data by simply passing True to the
# constructor. See dal/mongo.py to see the data being loaded. NOTE:
# only enable this in a dev/test environment - never in production
# dao = test.TestOrdersDAO()
dao = mongo.MongoOrdersDAO(True)
