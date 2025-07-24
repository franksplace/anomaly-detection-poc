# POC for Anomaly Detection in Log Files

## Configuration of Environment

### Requirements

- Python3
- pip

### Setup

```
checkout code
cd ./anomaly-detect-poc
# Setup python virtual environment and install pip packages
./pyme 
source py/bin/activate && ./pyme
```

## Usage

### convert_macos_logs_to_csv.py

Convert MacOS Logs into CSV for processing by the Anomaly Detection script

```
log show --style syslog --info --debug > macos_log.txt
./convert_macos_logs_to_csv.py --input_file macos_log.txt --output_file macos_log.csv
```

### convert_syslog_to_csv.py

Convert standard Syslog Logs into CSV for processing by the Anomaly Detection script

```
./convert_syslog_to_csv.py --input_file syslog --output_file syslog.csv
```


### detect_log_anomalies.py

Detection of anomalies on the log file.   The larger the file is better based on current POC.

```
./detect_log_anomalies.py --input_file logfile.csv --output_file logfile-with-anomalies.vsv
```

The following are new columns added and the explanation:
- anomaly_label (boolean)- 0 is normal and 1 is anomalous 
- anomaly_score - scoring value for each record (higher indicates more anomaly-like)


## Beyond POC

To move beyond the POC the storage of the anomalies would be need to be structued into a dataset and stored in a data source to be queried for each new log file processed.  As today the POC just reads one file and processes the file based on what is it that file.  
