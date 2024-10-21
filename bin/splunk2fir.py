#!/usr/bin/env python3

# For debugging purpose, you can run the script manually and use os variables as arguments with :
# export SPLUNK_ARG_8="raw event example"  # _raw
# export SPLUNK_ARG_9=$(date +%s)  # Current Unix timestamp
# export SPLUNK_ARG_10="1"  # fir incident ID
# export SPLUNK_ARG_11="Example description for the nugget"  # Example description
# and then run the script with: python3 /path/to/the/script/splunk2fir.py

import os
import requests
import json
import datetime
import logging

# Setup logging
# logging.basicConfig(filename="/tmp/add_nugget_debug.log", level=logging.DEBUG)

# FIR API details
FIR_NUGGETS_URL = "https://<YOUR_FIR_INSTANCE>/api/nuggets"
API_TOKEN = "Token <the token provided by your FIR instance>"

def create_fir_nugget(fir_incident_id, message, event_time, description):
    """Create a nugget for the selected incident in FIR."""
    headers = {
        "X-Api": API_TOKEN, 
        "Content-Type": "application/json"
    }

    nugget_data = {
        "incident": fir_incident_id,
        "raw_data": message,
        "source": "Splunk",
        "interpretation": description,
        "description": description,
        "type": "event",
        "category": "alert",
        "start_timestamp": event_time
    }

    response = requests.post(FIR_NUGGETS_URL, headers=headers, data=json.dumps(nugget_data))
    if response.status_code == 201:
        print("Nugget created successfully!")
    else:
        print(f"Failed to create nugget. Status Code: {response.status_code}, Response: {response.text}")

def main():
    try:
#        logging.debug("Script started")

        # Read command-line arguments if present
        if len(os.sys.argv) > 1:
            raw_data = os.sys.argv[1]
            time_unix = os.sys.argv[2]
            fir_incident_id = os.sys.argv[3]
            fir_nugget_description = os.sys.argv[4]

# Can be useful to manually debug :
#        else:
#            # Fallback to environment variables if no arguments are passed
#            raw_data = os.environ.get('SPLUNK_ARG_8', '')  # _raw
#            time_unix = os.environ.get('SPLUNK_ARG_9', '')  # _time
#            fir_incident_id = os.environ.get('SPLUNK_ARG_10', '')  # incident ID
#            fir_nugget_description = os.environ.get('SPLUNK_ARG_11', '')  # description

#        logging.debug(f"raw_data: {raw_data}, time_unix: {time_unix}, fir_incident_id: {fir_incident_id}, fir_nugget_description: {fir_nugget_description}")
        
        if not raw_data or not time_unix or not fir_incident_id:
            logging.error("Missing required data.")
            return

        # Handle possible float timestamp from Splunk
        time_unix = float(time_unix)  # Convert to float first
        # Convert Unix timestamp to human-readable format
        event_time = datetime.datetime.utcfromtimestamp(int(time_unix)).strftime('%Y-%m-%d %H:%M:%S')
        
        # Create the nugget in FIR
        create_fir_nugget(fir_incident_id, raw_data, event_time, fir_nugget_description)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

