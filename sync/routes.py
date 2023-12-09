from fastapi import APIRouter
from config.database import collection_status
from schema.schemas import list_serial
import configparser
import requests
import json

class SyncDeviceInfo:
    def __init__(self) -> None:
        # Get the Controller URL
        config = configparser.ConfigParser()
        config.read('/Users/prashantm2/Desktop/FastAPI-Agent/config.ini')
        self.CONTROLLER_URL = config['URL']['contoller']
        # Header
        self.HEADER = {'Content-Type': 'application/json'}
    
    def send_device_info(self):
        data_dict = {
            "hostname": "PrashantM2s-MacBook.local"
        }
        token = self.__get_token_from_db()
        response = requests.post(self.CONTROLLER_URL+"/sync-device-info", data=json.dumps(data_dict), headers={'Content-Type': 'application/json', "Authorization": f"Bearer {token}" })
        # Handle the response
        if response.status_code == 200:
            print(f"{response.json()}")
        else:
            print(f"Error sending device information: {response.status_code}")

    def __get_token_from_db(self) -> str:
        status = list_serial(collection_status.find())
        if len(status) > 0:
            return status[0]["token"]
        return status
# Endpoint
sync_info_router = APIRouter()
@sync_info_router.post("/send-sync-info")
async def sync_device_info():
    device_info = SyncDeviceInfo()
    device_info.send_device_info()