import re
import csv
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def log_analyze(file, threshold=10, output_csv='results.csv', top_n=5):
    try:
        with open(file, 'r') as f:
            logs = f.readlines()

        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        endpoint_pattern = r'\"(?:GET|POST|PUT|DELETE|HEAD|OPTIONS) ([^\s]+)'
        fail_pattern = r'(401|Invalid credentials)'
        date_pattern = r'\d{2}/[A-Za-z]{3}/\d{4}:\d{2}'

        ips, endpoints, timestamps = [], [], []
        failed_attempts = Counter()
        errors = Counter()

        for log in logs:
            ip = re.search(ip_pattern, log)
            if ip:
                ips.append(ip.group())

            endpoint = re.search(endpoint_pattern, log)
            if endpoint:
                endpoints.append(endpoint.group(1))

            if re.search(fail_pattern, log) and ip:
                failed_attempts[ip.group()] += 1

            # Extract and process timestamps
            timestamp = re.search(date_pattern, log)
            if timestamp:
                time_obj = datetime.strptime(timestamp.group(), '%d/%b/%Y:%H')
                timestamps.append(time_obj)

            # Extract HTTP status codes
            status_code = re.search(r'\s(\d{3})\s', log)
            if status_code:
                errors[status_code.group(1)] += 1

        ip_count = Counter(ips)
        ep_count = Counter(endpoints)

        most_ep, most_ep_count = ep_count.most_common(1)[0] if ep_count else (None, 0)
        suspicious_ips = {ip: cnt for ip, cnt in failed_attempts.items() if cnt > threshold}
        hourly_trend = Counter(t.hour for t in timestamps)

        # Plot Requests by IP
        plt.figure(figsize=(10, 6))
        top_ips = ip_count.most_common(top_n)
        sns.barplot(x=[ip[0] for ip in top_ips], y=[ip[1] for ip in top_ips])
        plt.title('Top IP Addresses by Request Count')
        plt.xlabel('IP Address')
        plt.ylabel('Request Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # Plot Hourly Trend
        plt.figure(figsize=(10, 6))
        hours, counts = zip(*sorted(hourly_trend.items()))
        plt.plot(hours, counts, marker='o', linestyle='-', color='b')
        plt.title('Hourly Request Trend')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Requests')
        plt.grid()
        plt.xticks(range(24))
        plt.tight_layout()
        plt.show()

        # Plot HTTP Status Code Distribution
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(errors.keys()), y=list(errors.values()), palette='muted')
        plt.title('HTTP Status Code Distribution')
        plt.xlabel('Status Code')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()

        # Plot Endpoint Access Frequency
        plt.figure(figsize=(10, 6))
        top_endpoints = ep_count.most_common(top_n)
        sns.barplot(x=[ep[0] for ep in top_endpoints], y=[ep[1] for ep in top_endpoints], palette='coolwarm')
        plt.title('Top Accessed Endpoints')
        plt.xlabel('Endpoint')
        plt.ylabel('Access Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # Save to CSV
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Top Requests by IP'])
            writer.writerow(['IP Address', 'Requests'])
            writer.writerows(ip_count.most_common(top_n))
            writer.writerow([])

            writer.writerow(['Top Endpoint'])
            writer.writerow(['Endpoint', 'Access Count'])
            if most_ep:
                writer.writerow([most_ep, most_ep_count])
            writer.writerow([])

            writer.writerow(['Hourly Request Trend'])
            writer.writerow(['Hour', 'Requests'])
            writer.writerows(sorted(hourly_trend.items()))
            writer.writerow([])

            writer.writerow(['HTTP Status Code Analysis'])
            writer.writerow(['Status Code', 'Count'])
            writer.writerows(errors.items())
            writer.writerow([])

            writer.writerow(['Suspicious IPs'])
            writer.writerow(['IP Address', 'Failed Logins'])
            writer.writerows(suspicious_ips.items())

        print(f"\nResults saved to {output_csv}")

    except FileNotFoundError:
        print("Log file not found.")
    except Exception as e:
        print(f"Error: {e}")

log_file = 'Python/sample.log'
log_analyze(log_file, top_n=10)
