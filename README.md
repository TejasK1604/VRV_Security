# Log Analysis Script

## Overview

This project is a Python script designed for log file analysis, created as part of VRV Security's Python Intern Assignment. The script efficiently parses web server logs to extract and analyze key insights, including request counts by IP address, most accessed endpoints, and detection of suspicious activities such as brute force login attempts.

The goal is to showcase proficiency in **file handling**, **string manipulation**, and **data analysis**, which are crucial for cybersecurity programming tasks.

---

## Features

1. **Count Requests per IP Address**:
   - Parses the log file to extract IP addresses and calculates the number of requests made by each.
   - Displays the results in descending order of request counts.
   - Example output:
     ```
     IP Address           Request Count
     192.168.1.1          234
     203.0.113.5          187
     ```

2. **Identify the Most Frequently Accessed Endpoint**:
   - Extracts endpoints (e.g., URLs or resource paths) from the log file.
   - Identifies and displays the endpoint with the highest number of accesses.
   - Example output:
     ```
     Most Frequently Accessed Endpoint:
     /home (Accessed 403 times)
     ```

3. **Detect Suspicious Activity**:
   - Identifies potential brute force login attempts by:
     - Searching for log entries with failed login attempts (e.g., HTTP status code 401 or "Invalid credentials").
     - Flagging IPs exceeding a configurable threshold of failed login attempts (default: 10).
   - Example output:
     ```
     Suspicious Activity Detected:
     IP Address           Failed Login Attempts
     192.168.1.100        56
     203.0.113.34         12
     ```

4. **Visual Analysis**:
   - Plots insights using Matplotlib and Seaborn for easier interpretation:
     - **Top IP Addresses by Request Count**: Bar chart of IP addresses with the most requests.
     - **Hourly Request Trend**: Line graph showing request trends over time.
     - **HTTP Status Code Distribution**: Bar chart for frequency of HTTP status codes.
     - **Top Accessed Endpoints**: Bar chart of the most frequently accessed endpoints.

5. **Output Results**:
   - Outputs analysis results in a clear format in the terminal.
   - Saves results to a CSV file (`log_analysis_results.csv`) with the following structure:
     - **Requests per IP**: Columns - IP Address, Request Count
     - **Most Accessed Endpoint**: Columns - Endpoint, Access Count
     - **Suspicious Activity**: Columns - IP Address, Failed Login Count
     - **Hourly Trends**: Columns - Hour, Number of Requests
     - **HTTP Status Codes**: Columns - Status Code, Frequency

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/log-analysis-script.git
