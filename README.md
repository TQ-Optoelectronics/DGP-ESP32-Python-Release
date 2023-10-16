# DGP-ESP32-Python

This project contains the Python modules for controlling & uploading to the video projector.  

# Quick start guide
1. Install Python dependencies
    ```
    pip install -r requirements.txt
    ```
2. Power on the projector module
3. Run `sample_upload.py` to upload the sample image to the projector.
    ```
    python sample_upload.py
    ```
    When the script is executed, it automatically scans and connects to the projector with BLE.  
    At the first time, PIN code needs to be entered (default 123456).
    Then it tells you the Wi-Fi SSID & Password provided by the projector module.  
    Connect to its Wi-Fi, and press Enter to start uploading the sample files.  

# Modules
## DGPESP32BLE
*DGPESP32BLE* contains the BLE information of the DGP-ESP32.  
You can find the UUID of the BLE services & characteristics here.
## DGPESP32Control
*DGPESP32Control* contains the functions to properly read/write the properties of the video projector.  
You can refer to its implementation to build your own APP.
## DGPESP32Upload
*DGPESP32Upload* contains the functions to properly upload a new binary to the video projector.  
You can refer to its implementation to build your own APP.  
NOTE: The binary should be generated with *TQ DLP3021EVM-Compilation-Library*
