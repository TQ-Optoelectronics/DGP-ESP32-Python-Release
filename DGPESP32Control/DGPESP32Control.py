import asyncio
from typing import Union
from enum import Enum
from DGPESP32BLE import DGPESP32BLE

__loop = asyncio.new_event_loop()

def connect_device(scan_timeout: float = 1.0) -> bool:
    return __loop.run_until_complete(DGPESP32BLE.scan_and_connect(timeout=scan_timeout))

def __read_value(char: DGPESP32BLE.ProjectorControlCharEnum) -> str:
    return __loop.run_until_complete(
        DGPESP32BLE.read_characteristic_value(
            char.value
        )
    )

def __write_value(char: DGPESP32BLE.ProjectorControlCharEnum, value: str) -> bool:
    __loop.run_until_complete(
        DGPESP32BLE.write_characteristic_value(
            char.value,
            value
        )
    )
    value_ret = __loop.run_until_complete(
        DGPESP32BLE.read_characteristic_value(
            char.value
        )
    )
    return value_ret == value


def device_name() -> str:
    # Read-only property
    return __read_value(DGPESP32BLE.DeviceInformationCharEnum.DEVICE_NAME)

def firmware_revision() -> str:
    # Read-only property
    return __read_value(DGPESP32BLE.DeviceInformationCharEnum.FIRMWARE_REVISION)

def manufacturer_name() -> str:
    # Read-only property
    return __read_value(DGPESP32BLE.DeviceInformationCharEnum.MANUFACTURER_NAME)

def power(en: Union[None, bool] = None) -> bool:
    # R/W property
    if en is None:
        # Get value
        return __read_value(DGPESP32BLE.ProjectorControlCharEnum.POWER) == '1'
    else:
        # Set value
        en = '1' if en else '0'
        return __write_value(
            DGPESP32BLE.ProjectorControlCharEnum.POWER,
            en
        )

class ProjectorModeEnum(Enum):
    UNKNOWN     = 0 # Unknown mode. Generally means the projector is off.
    CONTROL     = 1 # Playing mode.
    PROGRAMMING = 2 # Programming mode.

def mode(new_mode: Union[None, ProjectorModeEnum] = None) -> Union[ProjectorModeEnum, bool]:
    # R/W property
    if new_mode is None:
        # Get value
        return ProjectorModeEnum(int(__read_value(DGPESP32BLE.ProjectorControlCharEnum.MODE)))
    else:
        # Set value
        power(False)
        __write_value(
            DGPESP32BLE.ProjectorControlCharEnum.MODE,
            str(new_mode.value)
        )
        power(True)
        return mode() == new_mode # Check if the mode was set correctly

def light_output(en: Union[None, bool] = None) -> bool:
    # R/W property
    if mode() != ProjectorModeEnum.CONTROL:
        raise RuntimeError('Cannot read/write light output when projector is not in control mode.')
    
    if en is None:
        # Get value
        return __read_value(DGPESP32BLE.ProjectorControlCharEnum.LIGHT_OUTPUT) == '1'
    else:
        # Set value
        en = '1' if en else '0'
        return __write_value(
            DGPESP32BLE.ProjectorControlCharEnum.LIGHT_OUTPUT,
            en
        )
    
def r_brightness(new_brightness: Union[None, int] = None) -> Union[int, bool]:
    # R/W property
    if mode() != ProjectorModeEnum.CONTROL:
        raise RuntimeError('Cannot read/write red brightness when projector is not in control mode.')
    
    if new_brightness is None:
        # Get value
        return int(__read_value(DGPESP32BLE.ProjectorControlCharEnum.R_BRIGHTNESS))
    else:
        # Set value
        if new_brightness < 0 or new_brightness > 1023:
            raise ValueError('Red brightness must be between 0 and 1023.')
        return __write_value(
            DGPESP32BLE.ProjectorControlCharEnum.R_BRIGHTNESS,
            str(new_brightness)
        )
    
def g_brightness(new_brightness: Union[None, int] = None) -> Union[int, bool]:
    # R/W property
    if mode() != ProjectorModeEnum.CONTROL:
        raise RuntimeError('Cannot read/write green brightness when projector is not in control mode.')
    
    if new_brightness is None:
        # Get value
        return int(__read_value(DGPESP32BLE.ProjectorControlCharEnum.G_BRIGHTNESS))
    else:
        # Set value
        if new_brightness < 0 or new_brightness > 1023:
            raise ValueError('Green brightness must be between 0 and 1023.')
        return __write_value(
            DGPESP32BLE.ProjectorControlCharEnum.G_BRIGHTNESS,
            str(new_brightness)
        )
    
def b_brightness(new_brightness: Union[None, int] = None) -> Union[int, bool]:
    # R/W property
    if mode() != ProjectorModeEnum.CONTROL:
        raise RuntimeError('Cannot read/write blue brightness when projector is not in control mode.')
    
    if new_brightness is None:
        # Get value
        return int(__read_value(DGPESP32BLE.ProjectorControlCharEnum.B_BRIGHTNESS))
    else:
        # Set value
        if new_brightness < 0 or new_brightness > 1023:
            raise ValueError('Blue brightness must be between 0 and 1023.')
        return __write_value(
            DGPESP32BLE.ProjectorControlCharEnum.B_BRIGHTNESS,
            str(new_brightness)
        )
    
def video_address(new_address: Union[None, int] = None) -> Union[int, bool]:
    # R/W property
    if mode() != ProjectorModeEnum.CONTROL:
        raise RuntimeError('Cannot read/write video address when projector is not in control mode.')
    
    if new_address is None:
        # Get value
        return int(__read_value(DGPESP32BLE.ProjectorControlCharEnum.VIDEO_ADDR))
    else:
        # Set value
        return __write_value(
            DGPESP32BLE.ProjectorControlCharEnum.VIDEO_ADDR,
            str(new_address)
        )

class WiFiModeEnum(Enum):
    OFF = 0 # Wi-Fi is off.
    STA = 1 # Station mode.
    AP  = 2 # Access point mode.

def wifi_mode(new_mode: Union[None, WiFiModeEnum] = None) -> Union[WiFiModeEnum, bool]:
    # R/W property
    if new_mode is None:
        # Get value
        return WiFiModeEnum(int(__read_value(DGPESP32BLE.NetworkCharEnum.WIFI_MODE)))
    else:
        # Set value
        return __write_value(
            DGPESP32BLE.NetworkCharEnum.WIFI_MODE,
            str(new_mode.value)
        )
    
def wifi_ssid(new_ssid: Union[None, str] = None) -> Union[str, bool]:
    # R/W property
    if new_ssid is None:
        # Get value
        return __read_value(DGPESP32BLE.NetworkCharEnum.WIFI_SSID)
    else:
        # Set value
        return __write_value(
            DGPESP32BLE.NetworkCharEnum.WIFI_SSID,
            new_ssid
        )
    
def wifi_password(new_password: Union[None, str] = None) -> Union[str, bool]:
    # R/W property
    if new_password is None:
        # Get value
        return __read_value(DGPESP32BLE.NetworkCharEnum.WIFI_PASS)
    else:
        # Set value
        return __write_value(
            DGPESP32BLE.NetworkCharEnum.WIFI_PASS,
            new_password
        )
    
def ip() -> str:
    # Read-only property
    return __read_value(DGPESP32BLE.NetworkCharEnum.IP)

def port() -> int:
    # Read-only property
    return int(__read_value(DGPESP32BLE.NetworkCharEnum.PORT))

def nvs_reset():
    # Write-only property
    __write_value(
        DGPESP32BLE.DGPBLESystemChar.NVS_RESET,
        '1'
    )
