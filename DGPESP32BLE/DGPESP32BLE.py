import asyncio
from typing import Union
from enum import Enum
from bleak import BleakScanner
from bleak import BleakClient

__client: BleakClient = None

class ServicesEnum(Enum):
    DEVICE_INFORMATION = '0000180A-0000-1000-8000-00805F9B34FB'.lower()
    PROJECTOR_CONTROL  = 'C49F0000-2978-46D2-A12A-F2C0C1FB910E'.lower()
    NETWORK            = 'BDA10000-14EA-11EE-BE56-0242AC120002'.lower()
    SYSTEM             = '7BD10000-D266-4800-91E4-A8681B58673E'.lower()

class DeviceInformationCharEnum(Enum):
    DEVICE_NAME       = '00002A00-0000-1000-8000-00805F9B34FB'.lower()
    FIRMWARE_REVISION = '00002A26-0000-1000-8000-00805F9B34FB'.lower()
    MANUFACTURER_NAME = '00002A29-0000-1000-8000-00805F9B34FB'.lower()
    
class ProjectorControlCharEnum(Enum):
    POWER        = 'C49F0001-2978-46D2-A12A-F2C0C1FB910E'.lower()
    MODE         = 'C49F0002-2978-46D2-A12A-F2C0C1FB910E'.lower()
    LIGHT_OUTPUT = 'C49F0003-2978-46D2-A12A-F2C0C1FB910E'.lower()
    R_BRIGHTNESS = 'C49F0004-2978-46D2-A12A-F2C0C1FB910E'.lower()
    G_BRIGHTNESS = 'C49F0005-2978-46D2-A12A-F2C0C1FB910E'.lower()
    B_BRIGHTNESS = 'C49F0006-2978-46D2-A12A-F2C0C1FB910E'.lower()
    VIDEO_ADDR   = 'C49F0007-2978-46D2-A12A-F2C0C1FB910E'.lower()
    # VIDEO_FPS    = 'C49F0008-2978-46D2-A12A-F2C0C1FB910E'.lower() # DON'T USE
    # PROG_FREQ    = 'C49F0009-2978-46D2-A12A-F2C0C1FB910E'.lower() # DON'T USE

class NetworkCharEnum(Enum):
    WIFI_MODE = 'BDA10001-14EA-11EE-BE56-0242AC120002'.lower()
    WIFI_SSID = 'BDA10002-14EA-11EE-BE56-0242AC120002'.lower()
    WIFI_PASS = 'BDA10003-14EA-11EE-BE56-0242AC120002'.lower()
    IP        = 'BDA10004-14EA-11EE-BE56-0242AC120002'.lower()
    PORT      = 'BDA10005-14EA-11EE-BE56-0242AC120002'.lower()

class DGPBLESystemChar(Enum):
    NVS_RESET = '7BD10001-D266-4800-91E4-A8681B58673E'.lower()


async def scan_and_connect(timeout: float) -> bool:
    global __client
    
    DEVICE_ADV_NAME = "DGP-ESP32"
    devices = await BleakScanner.discover(timeout)
    for d in devices:
        if d.name == DEVICE_ADV_NAME:
            __client = BleakClient(d.address)
            await __client.connect()
            return True
            
    return False

async def disconnect():
    await __client.disconnect()

async def read_characteristic_value(uuid: str) -> str:
    return (await __client.read_gatt_char(uuid)).decode()

async def write_characteristic_value(uuid: str, value: str):
    await __client.write_gatt_char(uuid, value.encode('utf-8'))
