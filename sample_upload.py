import os
import math
import time
from tqdm import tqdm
from DGPESP32Control import DGPESP32Control
from DGPESP32Upload import DGPESP32Upload

def upload_file(file_path: str, address: int) -> bool:
    size = os.stat(file_path).st_size
    n_iter = math.ceil(size/4096)
    bytes_sent = 0
    for bytes_sent in tqdm(DGPESP32Upload.upload_file(file_path, address), total=n_iter):
        pass
    if bytes_sent != size:
        return False
    else:
        return True

connected = DGPESP32Control.connect_device()
if connected:
    wifi_ssid = DGPESP32Control.wifi_ssid()
    wifi_pass = DGPESP32Control.wifi_password()
    print(f'Please connect to Wi-Fi')
    print(f'SSID = {wifi_ssid}')
    print(f'Password = {wifi_pass}')
    input('Press enter to continue')

    DGPESP32Control.mode(DGPESP32Control.ProjectorModeEnum.PROGRAMMING)
    succeeded = upload_file('sample_upload/tq.img', 0x01280000)
    if succeeded:
        succeeded = upload_file('sample_upload/flash_header_0x80000_0x9FFFF.img', 0x00080000)
    DGPESP32Control.mode(DGPESP32Control.ProjectorModeEnum.CONTROL)
    DGPESP32Control.video_address(0x01280000)
    pass
