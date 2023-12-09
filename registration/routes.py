import requests
from fastapi import APIRouter
from config.database import collection_status
from pydantic import BaseModel, Field
import configparser
import json

class DeviceRegistration:
    def __init__(self, mac_address: dict) -> None:
        self.collection_status = collection_status
        self.mac_address = mac_address

        # Get the Controller URL
        config = configparser.ConfigParser()
        config.read('/Users/prashantm2/Desktop/FastAPI-Agent/config.ini')
        self.CONTROLLER_URL = config['URL']['contoller']

        # Header
        self.HEADER = {'Content-Type': 'application/json'}

    def register_device(self):
        macid_json_data = json.loads(self.mac_address)

        response = requests.post(self.CONTROLLER_URL+"/agent-registration", data=self.mac_address, headers=self.HEADER)
        if response.status_code == 200:
            status_dict = {
                "macid": macid_json_data["macid"],
                "token": response.json()["access_token"],
                "is_active": False
            }
            self.collection_status.insert_one(status_dict)

class MACID(BaseModel):
    macid: str = Field(min_length=12, max_length=12)

# Endpoint
device_registration_router = APIRouter()
@device_registration_router.post("/send-device-registration-request")
async def register_device(macid: MACID):
    mac_id = macid.model_dump_json()
    device = DeviceRegistration(mac_id)
    device.register_device()