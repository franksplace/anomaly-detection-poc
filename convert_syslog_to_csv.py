#!/usr/bin/env python3

import csv
import re
import argparse

# Regular expression for standard syslog format: "Month Day Time Host Process[PID]: Message"
syslog_pattern = re.compile(r'^(\w{3})\s+(\d{1,2})\s+(\d{2}:\d{2}:\d{2})\s+(\S+)\s+([\w\-/.]+)(?:\[(\d+)\])?:\s+(.*)$')

def convert_syslog_to_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Month', 'Day', 'Time', 'Host', 'Process', 'PID', 'Message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for line in infile:
            match = syslog_pattern.match(line)
            if match:
                month, day, time, host, process, pid, message = match.groups()
                writer.writerow({
                    'Month': month,
                    'Day': day,
                    'Time': time,
                    'Host': host,
                    'Process': process,
                    'PID': pid or '',
                    'Message': message.strip()
                })

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert syslog files to CSV format.')
    parser.add_argument('--input_file', required=True, help='Path to the input syslog file')
    parser.add_argument('--output_file', required=True, help='Path to the output CSV file')

    args = parser.parse_args()
    convert_syslog_to_csv(args.input_file, args.output_file)

