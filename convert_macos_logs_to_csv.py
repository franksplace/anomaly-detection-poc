#!/usr/bin/env python3

import csv
import re
import argparse

log_line_pattern = re.compile(
    r'^(?P<date>\d{4}-\d{2}-\d{2}) '
    r'(?P<time>\d{2}:\d{2}:\d{2}\.\d{6}-\d{4})\s+'
    r'(?P<host>\S+) '
    r'(?P<process>[^\[]+)\[(?P<pid>\d+)\]:\s'
    r'(?P<message>.*)$'
)

def convert_log_to_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Date','Time','Host','Process','PID','Message'])

        for line in infile:
            match = log_line_pattern.match(line)
            if match:
                writer.writerow([
                    match.group('date'),
                    match.group('time'),
                    match.group('host'),
                    match.group('process').strip(),
                    match.group('pid'),
                    match.group('message').strip()
                ])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert macOS logs to CSV.')
    parser.add_argument('--input_file', required=True, help='Path to log input file')
    parser.add_argument('--output_file', required=True, help='Path to output CSV')
    args = parser.parse_args()

    convert_log_to_csv(args.input_file, args.output_file)

