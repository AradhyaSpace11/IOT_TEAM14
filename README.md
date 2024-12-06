# **Setup Instructions**

Follow these steps to set up and run the project.

---

## **1. Clone the Required Repositories**

First, clone the [Ultralytics](https://github.com/ultralytics/ultralytics) repository:

```bash
git clone https://github.com/ultralytics/ultralytics.git
cd ultralytics
```

Now, clone the **IOT_TEAM14** repository:

```bash
git clone https://github.com/AradhyaSpace11/IOT_TEAM14.git
cd IOT_TEAM14
```

## **2. Install Required Python Libraries**

Install the dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## **3. Download the Mobile App**

Download the **"IP Webcam"** app from the Google Play Store.

## **4. Configure the Mobile App**

1. Turn on the mobile hotspot on your phone.
2. Set the stream resolution to **640x480** in the app's settings.
3. Start the stream and note the URL (e.g., `http://192.168.1.100:8080/video`).

## **5. Connect Your Laptop/PC to the Hotspot**

Ensure your laptop/PC is connected to the mobile hotspot created by your phone.

## **6. Connect The ESP32 to the Servo**

1. Connect Brown Wire to ESP32's GND
2. Connect Red Wire to ESP32's 3.3v
3. Connect Orange Wire to ESP32's D18

## **7. Update the ESP32 Code**

1. Open the `.ino` file provided in the **IOT_TEAM14** repository.
2. Replace the Wi-Fi credentials in the code with your mobile hotspot's details:

```cpp
const char* ssid = "YourHotspotSSID";
const char* password = "YourHotspotPassword";
```

3. Install all required Arduino libraries for the code to compile successfully:
   - **ESP32Servo**
   - **WiFi**
   - **ESPAsyncWebServer**
4. Upload the updated code to your ESP32 using the Arduino IDE.

## **8. Run the Python Script**

Navigate to the **IOT_TEAM14** directory:

```bash
cd IOT_TEAM14
python offboard.py
```

## **9. Notes**

- Ensure your laptop/PC and ESP32 are both connected to the same mobile hotspot.
- Verify that the ESP32 is running and that the mobile app stream is active.
- If you encounter any issues, feel free to open an issue in the repository.
