## **Documentation for Phone Number Geolocation Extraction Script**

This script extracts geolocation details of mobile phone numbers from two sources: findandtrace.com and mobilenumbertracker.com, and writes the data to a CSV file.


### **Required Libraries**

The script requires the following libraries to be imported:



* time: for measuring the execution time of the script.
* json: for parsing JSON data.
* requests: for making HTTP requests.
* pandas: for reading the CSV file containing the phone numbers.
* tqdm: for showing a progress bar during the extraction process.
* concurrent.futures.ThreadPoolExecutor: for implementing multithreading to speed up the extraction process.
* bs4.BeautifulSoup: for parsing HTML data.


### **API Description**

The script uses two URLs to extract geolocation data for phone numbers:



* URL: the primary source of cellular location details is findandtrace.com. This URL is used to extract the telecoms circle state and the SIM card distributed location for a given phone number.
* URL_2: the secondary source of cellular location details is mobilenumbertracker.com. This URL is used to extract the state, service provider, city, latitude, and longitude for a given phone number.


### **Input**

The input to the script is a CSV file containing a list of phone numbers. The phone numbers should be in a column named phone_num. The file should be named kfy_data_addition.csv and should be located in the same directory as the script.


### **Output**

The script writes the extracted geolocation data to a CSV file named data_addition.csv. The columns in this file are as follows:

* phone_num,
* source_1_telecoms_circle_state,
* source_1_sim_card_distributed_at,
* source_2_state,
* source_2_service_provider,
* source_2_city,source_2_latitude,
* source_2_longitude


### **Execution**

To run the script, simply run the following command in the terminal:

Copy code
<code>python phone_number_geolocation_extraction_script.py</code>


### **Multithreading**

The script uses multithreading to speed up the extraction process. The maximum number of workers is set to 100, which means that the script will use up to 100 threads to extract geolocation data. This can be changed by modifying the max_workers parameter in the ThreadPoolExecutor constructor.


### **Execution Time**

The script measures the execution time and prints it to the console upon completion. The execution time includes the time taken to read the CSV file, extract the geolocation data, and write it to a CSV file.

Documentation link : https://docs.google.com/document/d/1z5CDXHyrj0ab6Sap1lTG_-VJH4DpYFZ_RXqbtvJTrYw/edit#
