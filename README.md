# Splunk2FIR

The **Splunk2FIR** Splunk application provides a custom command that integrates with [FIR (Fast Incident Response)](https://github.com/certsocietegenerale/FIR) to automatically create nuggets based on Splunk search results. It leverages a Python script to send data from Splunk to FIR.

## Features
- Creates nuggets in FIR using search results from Splunk.
- Includes a custom macro for easier integration into Splunk queries.
- Automatically imports _time and _raw fields from Splunk into FIR for accurate timestamping, detailed logging, and seamless integration of the logs into the Timeline of the incident in FIR—allowing for better incident tracking and analysis. 

---
## Installation and Configuration
### 1. Download and Install the App:
- Download the app package (`Splunk2FIR.spl`) from the [Releases page](https://github.com/kilanmundera/Splunk2FIR/releases).
- Log in to your Splunk instance and navigate to **Apps > Manage Apps**.
- Click **Install app from file**, then select the `.spl` file and upload it.
- Click **Install** to complete the process.

### 2. Setting FIR URL and API Token
The `splunk2fir.py` script is located in the app's `bin/` directory. This script handles the communication between Splunk and FIR, sending data via HTTP POST requests.

You must set the FIR instance URL and the API token :

- **FIR URL**: Modify the `FIR_NUGGETS_URL` variable to point to your FIR instance's API endpoint.
- **API Token**: Update the `API_TOKEN` variable with your FIR API token.

## Debugging and Logs
The script includes logging functionality (commented out by default). If you need to enable logging, uncomment the `logging.*` lines and adjust the log file path if necessary.

---

## Usage
### **Using the `splunk2fir` Custom Command with the `splunk2fir(2)` Macro**

The app provides a macro called `splunk2fir(2)` for easier usage in Splunk searches. This macro is used to simplify the process of passing values to FIR.

#### Arguments:
- `fir_id`: The ID of the FIR incident.
- `fir_interpretation`: The description or interpretation of the event to be sent to FIR. Must be double quoted.


### Example SPL Search with Macro:
```spl
index=your_index sourcetype=your_sourcetype
| [...] (An SPL query to isolate the event(s) you'd like to push as a nugget; one nugget per event)
| `splunk2fir("1", "Test nugget from Splunk")`
```

This will automatically convert the required fields and pass them to the `splunk2fir` command behind the scenes.

### **The `splunk2fir` Custom Command**
The `splunk2fir(2)` macro calls the `splunk2fir` command that launches the Python script `splunk2fir.py`.

### The Python Script (`splunk2fir.py`)
The `splunk2fir.py` script is located in the app's `bin/` directory. This script handles the communication between Splunk and FIR, sending data via HTTP POST requests.

The script expects the following arguments:

- **arg1**: The raw data of the event (the `_raw` field, automaticaly extracted)
- **arg2**: The event timestamp (the `_time` field, automaticaly extracted).
- **arg3**: The FIR incident ID (the first argument of the `splunk2fir(2)` macro)
- **arg4**: The nugget description (the second argument of the `splunk2fir(2)` macro)

You can debug or test the script manually by setting environment variables:
```bash
export SPLUNK_ARG_8="raw event data"
export SPLUNK_ARG_9=$(date +%s)  # Current Unix timestamp
export SPLUNK_ARG_10="1"  # FIR incident ID
export SPLUNK_ARG_11="Test description"
python3 /path/to/splunk2fir.py
```
