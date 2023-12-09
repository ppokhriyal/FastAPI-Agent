from pymongo import MongoClient

client = MongoClient()
db = client.agent
"""Collection of agent registration status"""
collection_status = db["status"]