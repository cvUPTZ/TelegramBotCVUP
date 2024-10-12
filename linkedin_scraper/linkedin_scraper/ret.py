# # import re
# # from bs4 import BeautifulSoup

# # def clean_and_compact_html_from_file(input_file, output_file):
# #     # Read HTML from input file
# #     with open(input_file, 'r', encoding='utf-8') as file:
# #         html_text = file.read()

# #     # Parse HTML with BeautifulSoup
# #     soup = BeautifulSoup(html_text, 'html.parser')
    
# #     # Remove all script and style elements
# #     for script_or_style in soup(["script", "style"]):
# #         script_or_style.decompose()
    
# #     # Remove all attributes except 'href' from <a> tags
# #     for tag in soup.find_all(True):
# #         if tag.name == 'a':
# #             allowed_attrs = ['href']
# #             tag.attrs = {key: value for key, value in tag.attrs.items() if key in allowed_attrs}
# #         else:
# #             tag.attrs = {}
    
# #     # Remove empty tags
# #     for tag in soup.find_all():
# #         if len(tag.get_text(strip=True)) == 0 and tag.name not in ['br', 'hr']:
# #             tag.decompose()
    
# #     # Get the cleaned HTML
# #     cleaned_html = str(soup)
    
# #     # Remove extra whitespace and newlines
# #     cleaned_html = re.sub(r'\s+', ' ', cleaned_html)
# #     cleaned_html = re.sub(r'>\s+<', '><', cleaned_html)
    
# #     # Write cleaned HTML to output file
# #     with open(output_file, 'w', encoding='utf-8') as file:
# #         file.write(cleaned_html.strip())

# #     print(f"Cleaned HTML has been written to {output_file}")

# # # Example usage:
# # clean_and_compact_html_from_file('input.html', 'output_cleaned.html')

# # import requests

# # # Replace these variables with your actual values
# # authorization_code = 'AQRYq-JVxnzTBlXOZsXGodrUV0oWhwk3Vt16Lo4GHMo8RF3QMepMgRzJSP4ou0wOcG1y8MMVje1ALZ8psE3Go3GzjGuFPTZn97Srwr1BFJKR9OjWlmX1EWQzHQHyGxfin8G37FUY7bXl5sebSKPijsUjXV5C14rlqGHsDhueqf4LxYRxqCu3LleG1Vwu2-4D3SagFAGpRkuqLDW2bks'  # The code you received in the URL
# # redirect_uri = 'https://b24-lcccvg.bitrix24.fr'
# # client_id = '78755cuf6hwldq'
# # client_secret = 'IonAGUSMO6Y6Euhs'  # Your LinkedIn app's client secret

# # url = "https://www.linkedin.com/oauth/v2/accessToken"
# # payload = {
# #     'grant_type': 'authorization_code',
# #     'code': authorization_code,
# #     'redirect_uri': redirect_uri,
# #     'client_id': client_id,
# #     'client_secret': client_secret
    
# # }

# # headers = {
# #     'Content-Type': 'application/x-www-form-urlencoded'
# # }

# # response = requests.post(url, data=payload, headers=headers)

# # if response.status_code == 200:
# #     access_token = response.json().get('access_token')
# #     print("Access Token:", access_token)
# # else:
# #     print("Error:", response.text)*µ

# # import requests
# # import certifi
# # from requests.packages.urllib3.exceptions import InsecureRequestWarning
# # import ssl

# # # Disable SSL warnings if using verify=False (only for testing purposes)
# # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# # # LinkedIn access token (replace with your actual access token)
# # access_token = 'AQV66iIy9zjX81CxjO8Bp5WJvFT5MXxu_qHUyChpWqAZGYjt6puqtlv8ZA_dNtC1xALxu7fZJLwLfgkXm2iemAEzAozYHjW5_cqRcTWgbMScOewxFVq5Y6QOwVpv5f0p-4maamrOl7BbmPBussL74OX9gk5MCIJxluVoshJwoAGS3c8PFt0UvWF_r8dNTFXRO_bn8jEF70YpGatOenpWAdtPTQSq_vmB2-vSAmjwrnzzuPZNfkrSIXT6c2HxISTr86WPDQRgSiqchmK0uitHRaXC4sVt0Ousv8N35M3KXz-iYQcqYZM9n1H_kkNft5bwY6VlMjPoFD6mu98niGqMNPSY4XYw4g'

# # # Set the headers with the access token
# # headers = {
# #     'Authorization': f'Bearer {access_token}',
# #     'Connection': 'Keep-Alive'
# # }

# # # LinkedIn API endpoint for profile
# # url = 'https://api.linkedin.com/v2/me'

# # try:
# #     # Make the request to LinkedIn API, using certifi's certificate bundle for SSL verification
# #     response = requests.get(url, headers=headers, timeout=10, verify=certifi.where())
    
# #     # Check if the request was successful
# #     if response.status_code == 200:
# #         # Parse the JSON response
# #         profile_data = response.json()
# #         print("Profile Data:", profile_data)
# #     else:
# #         # Print error details if the request failed
# #         print("Error:", response.status_code, response.text)

# # except requests.exceptions.SSLError as ssl_err:
# #     print(f"SSL Error: {ssl_err}")
# #     print("Try updating your certifi package: pip install --upgrade certifi")
    
# #     # Optionally, you can try to make the request without SSL verification (NOT recommended for production)
# #     # response = requests.get(url, headers=headers, timeout=10, verify=False)
# #     # print("Response without SSL verification:", response.text)

# # except requests.exceptions.RequestException as e:
# #     # Handle any exceptions that occur during the request
# #     print(f"Request failed: {e}")

# # # Print SSL certificate information
# # try:
# #     import socket
# #     cert = ssl.get_server_certificate(('api.linkedin.com', 443))
# #     print("Server certificate:")
# #     print(cert)
# # except Exception as e:
# #     print(f"Failed to retrieve server certificate: {e}")


# import urllib3
# import certifi

# http = urllib3.PoolManager(
#     cert_reqs='CERT_REQUIRED',
#     ca_certs=certifi.where()
# )

# url = 'https://api.linkedin.com/v2/me'
# headers = {
#     'Authorization': f'Bearer {access_token}',
#     'Connection': 'Keep-Alive'
# }

# response = http.request('GET', url, headers=headers)
# print(response.status)
# print(response.data)


# # import ssl
# # import socket
# # import certifi

# # def verify_cert(hostname, port=443):
# #     context = ssl.create_default_context(cafile=certifi.where())
# #     with socket.create_connection((hostname, port)) as sock:
# #         with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
# #             cert = secure_sock.getpeercert()
# #     print(f"Certificate for {hostname} is valid")
#     return cert

# # try:
# #     cert = verify_cert('api.linkedin.com')
# #     print("Certificate details:")
# #     for key, value in cert.items():
# #         print(f"{key}: {value}")
# # except ssl.SSLCertVerificationError as e:
# #     print(f"Certificate verification failed: {e}")
# # except Exception as e:
# #     print(f"An error occurred: {e}")





# from flask import Flask, jsonify, send_from_directory
# import usb.core
# import usb.util
# import usb.backend.libusb1
# import logging

# app = Flask(__name__)

# # Set up logging
# logging.basicConfig(level=logging.DEBUG)

# # Constants
# XIAOMI_VENDOR_ID = 0x2717
# USB_DEBUGGING_CMD = b'\x01\x00\x00\x00\x08\x00\x00\x00\x2E\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00host::\x00'

# # Helper function to get USB device
# def get_usb_device(vendor_id):
#     backend = usb.backend.libusb1.get_backend(find_library=lambda x:"my_telegram_bot\linkedin_scraper\linkedin_scraper\libusb-1.0.dll")
#     if backend is None:
#         raise RuntimeError("LibUSB backend not found. Please install libusb.")
    
#     dev = usb.core.find(idVendor=vendor_id, backend=backend)
#     if dev is None:
#         raise RuntimeError(f"Device with Vendor ID {hex(vendor_id)} not found.")
    
#     return dev

# # Helper function to enable USB debugging
# def enable_usb_debugging(dev):
#     try:
#         dev.set_configuration()
#     except usb.core.USBError as e:
#         raise RuntimeError(f"Failed to set configuration: {str(e)}")

#     try:
#         dev.write(1, USB_DEBUGGING_CMD)
#     except usb.core.USBError as e:
#         raise RuntimeError(f"Failed to send command: {str(e)}")
    
#     try:
#         response = dev.read(0x81, 64, timeout=5000)
#         return response
#     except usb.core.USBError as e:
#         raise RuntimeError(f"Failed to read response: {str(e)}")

# @app.route('/')
# def index():
#     return send_from_directory('.', 'EV BORNES.html')

# @app.route('/enable_debugging', methods=['POST'])
# def enable_debugging():
#     try:
#         logging.info("Attempting to enable USB debugging...")
#         dev = get_usb_device(XIAOMI_VENDOR_ID)
#         response = enable_usb_debugging(dev)
        
#         if b'OKAY' in response:
#             logging.info("USB Debugging enabled successfully.")
#             return jsonify({"success": True, "message": "USB Debugging enabled successfully"}), 200
#         else:
#             logging.error(f"Unexpected response: {response}")
#             return jsonify({"success": False, "message": "Failed to enable USB Debugging: Unexpected response"}), 500

#     except RuntimeError as e:
#         logging.error(str(e))
#         return jsonify({"success": False, "message": str(e)}), 500
#     except Exception as e:
#         logging.exception("An unexpected error occurred")
#         return jsonify({"success": False, "message": f"Unexpected error: {str(e)}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)









# from flask import Flask, render_template, request, jsonify
# import time

# app = Flask(__name__)

# # Simulate USB Debugging process
# @app.route('/simulate_usb_debugging', methods=['POST'])
# def simulate_usb_debugging():
#     vendor_id = request.json.get('vendorId')
#     command = request.json.get('command')

#     log = []
#     def add_log(message, color):
#         timestamp = time.strftime('%H:%M:%S')
#         log.append({'time': timestamp, 'message': message, 'color': color})

#     add_log('Initializing USB communication...', '#569cd6')
#     time.sleep(1)
#     add_log(f'Detecting device with Vendor ID: 0x{vendor_id}', '#4ec9b0')
#     time.sleep(1.5)
#     add_log('Device detected. Establishing connection...', '#4ec9b0')
#     time.sleep(1)
#     add_log('Connection established. Sending USB debugging command:', '#4ec9b0')
#     add_log(f'Command: {command}', '#ce9178')
#     time.sleep(2)
#     add_log('Command sent. Waiting for device response...', '#4ec9b0')
#     time.sleep(1.5)
#     add_log('Device acknowledged. USB Debugging enabled successfully.', '#4ec9b0')
#     time.sleep(1)
#     add_log('Closing connection...', '#569cd6')
#     time.sleep(1)
#     add_log('Process completed. USB Debugging is now enabled on the device.', '#3dc9b0')

#     return jsonify(log)

# # Simulate disabling Verify Apps over USB
# @app.route('/disable_verify_apps_over_usb', methods=['POST'])
# def disable_verify_apps_over_usb():
#     vendor_id = request.json.get('vendorId')
#     command = request.json.get('command')

#     log = []
#     def add_log(message, color):
#         timestamp = time.strftime('%H:%M:%S')
#         log.append({'time': timestamp, 'message': message, 'color': color})

#     add_log('Initializing USB communication to disable Verify Apps over USB...', '#569cd6')
#     time.sleep(1)
#     add_log(f'Detecting device with Vendor ID: 0x{vendor_id}', '#4ec9b0')
#     time.sleep(1.5)
#     add_log('Device detected. Establishing connection...', '#4ec9b0')
#     time.sleep(1)
#     add_log('Connection established. Sending disable command for Verify Apps over USB:', '#4ec9b0')
#     add_log(f'Command: {command}', '#ce9178')
#     time.sleep(2)
#     add_log('Command sent. Waiting for device response...', '#4ec9b0')
#     time.sleep(1.5)
#     add_log('Device acknowledged. Verify Apps over USB disabled successfully.', '#4ec9b0')
#     time.sleep(1)
#     add_log('Closing connection...', '#569cd6')
#     time.sleep(1)
#     add_log('Process completed. Verify Apps over USB is now disabled on the device.', '#3dc9b0')

#     return jsonify(log)

# # Simulate enabling Install via USB
# @app.route('/enable_install_via_usb', methods=['POST'])
# def enable_install_via_usb():
#     vendor_id = request.json.get('vendorId')
#     command = request.json.get('command')

#     log = []
#     def add_log(message, color):
#         timestamp = time.strftime('%H:%M:%S')
#         log.append({'time': timestamp, 'message': message, 'color': color})

#     add_log('Initializing USB communication to enable Install via USB...', '#569cd6')
#     time.sleep(1)
#     add_log(f'Detecting device with Vendor ID: 0x{vendor_id}', '#4ec9b0')
#     time.sleep(1.5)
#     add_log('Device detected. Establishing connection...', '#4ec9b0')
#     time.sleep(1)
#     add_log('Connection established. Sending enable command for Install via USB:', '#4ec9b0')
#     add_log(f'Command: {command}', '#ce9178')
#     time.sleep(2)
#     add_log('Command sent. Waiting for device response...', '#4ec9b0')
#     time.sleep(1.5)
#     add_log('Device acknowledged. Install via USB enabled successfully.', '#4ec9b0')
#     time.sleep(1)
#     add_log('Closing connection...', '#569cd6')
#     time.sleep(1)
#     add_log('Process completed. Install via USB is now enabled on the device.', '#3dc9b0')

#     return jsonify(log)

# # Reset the simulation
# @app.route('/reset_simulation', methods=['POST'])
# def reset_simulation():
#     return jsonify({'message': 'Simulation reset. Ready to start a new process.'})

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)



# # redirect_uri = 'https://b24-lcccvg.bitrix24.fr'
# # client_id = '78755cuf6hwldq'
# # client_secret = 'IonAGUSMO6Y6Euhs'  # Your LinkedIn app's client secret


import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import webbrowser

load_dotenv()

class LinkedInClient:
    def __init__(self):
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
        self.redirect_uri = os.getenv('LINKEDIN_REDIRECT_URI')
        self.access_token = None

    def authorize(self):
        # Step 1: Direct user to LinkedIn's authorization page
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'profile email'
        }
        auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"
        print(f"Please visit this URL to authorize the application: {auth_url}")
        webbrowser.open(auth_url)

        # Step 2: Get the authorization code from the redirect URL
        auth_code = input("Enter the authorization code from the redirect URL: ")

        # Step 3: Exchange the authorization code for an access token
        token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            print("Authorization successful!")
        else:
            print(f"Authorization failed: {response.text}")

    def get_profile(self):
        if not self.access_token:
            print("Please authorize the application first.")
            return None

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def get_skills(self):
        # Note: LinkedIn's v2 API doesn't provide a direct endpoint for skills.
        # You would need to use the profile API and parse the information.
        print("LinkedIn API v2 doesn't provide a direct endpoint for skills.")
        print("You may need to parse this information from the full profile data.")
        return self.get_profile()

if __name__ == "__main__":
    client = LinkedInClient()
    client.authorize()
    
    profile = client.get_profile()
    if profile:
        print("Profile retrieved successfully:")
        print(profile)
    
    skills = client.get_skills()
    if skills:
        print("Full profile data (may contain skills information):")
        print(skills)