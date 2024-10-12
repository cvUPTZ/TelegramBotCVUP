#!/bin/bash

# Ensure ADB is installed and in PATH
if ! command -v adb &> /dev/null; then
    echo "ADB is not installed or not in PATH. Please install Android SDK platform tools."
    exit 1
fi

# Check if device is connected
if ! adb devices | grep -q device; then
    echo "No device detected. Please connect your Realme C12 and ensure it's recognized by the computer."
    exit 1
fi

# Enable USB debugging
echo "Attempting to enable USB debugging..."

# Wake the device
adb shell input keyevent KEYCODE_WAKEUP

# Unlock the device (assuming no secure lock screen)
adb shell input keyevent 82

# Navigate to Settings
adb shell am start -n com.android.settings/.Settings

# Scroll to find Developer options (adjust the number of swipes as needed)
for i in {1..10}; do
    adb shell input swipe 500 1500 500 500
    sleep 0.5
done

# Tap on Developer options (coordinates may need adjustment)
adb shell input tap 500 500

# Scroll to find USB debugging option
for i in {1..5}; do
    adb shell input swipe 500 1500 500 500
    sleep 0.5
done

# Enable USB debugging (coordinates may need adjustment)
adb shell input tap 500 500

# Confirm the USB debugging prompt
adb shell input tap 800 1000

echo "USB debugging should now be enabled. Please check your device."

# Verify USB debugging status
if adb devices | grep -q "device$"; then
    echo "Success: USB debugging is now enabled!"
else
    echo "Error: USB debugging may not have been enabled successfully."
    echo "Please try again or consult Realme support for device-specific instructions."
fi