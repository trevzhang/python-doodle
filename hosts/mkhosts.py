import concurrent.futures
from ping3 import ping
import os
def read_ip_addresses_from_file(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r') as file:
        return set(file.read().splitlines())

def ping_and_get_fastest_ips(ip_addresses, domain_names, num_fastest=2, max_workers=10):
    response_times = {}

    def ping_ip(ip):
        try:
            response_time = ping(ip)
            if response_time is not None:
                response_times[ip] = response_time
        except Exception as e:
            print(f"Error pinging {ip}: {e}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(ping_ip, ip) for ip in ip_addresses]
        concurrent.futures.wait(futures)

    fastest_ips = sorted(response_times.items(), key=lambda x: x[1])[:num_fastest]
    hosts_file_content = ''
    for domain in domain_names:
        for ip, _ in fastest_ips:
            hosts_file_content += f"{ip}\t{domain}\n"

    return hosts_file_content

# Example usage for the first set of IP addresses and domain names
ip_addresses_set1 = read_ip_addresses_from_file('themoviedb_ip.txt')
ip_addresses_set1 = ip_addresses_set1.union({'18.239.36.98', '108.160.169.178', '18.165.122.73', '13.249.146.88', '13.224.167.74', '13.249.146.96', '99.86.4.122', '108.160.170.44', '108.160.169.54', '98.159.108.58', '13.226.225.4', '31.13.80.37', '202.160.128.238', '13.224.167.16', '199.96.63.53', '104.244.43.6', '18.239.36.122', '66.220.149.32', '108.157.14.15', '202.160.128.14', '52.85.242.44', '199.59.149.207', '54.230.129.92', '54.230.129.11', '103.240.180.117', '66.220.148.145', '54.192.175.79', '143.204.68.100', '31.13.84.2', '18.239.36.64', '52.85.242.124', '54.230.129.83', '18.165.122.27', '13.33.88.3', '202.160.129.36', '108.157.14.112', '99.86.4.16', '199.59.149.237', '199.59.148.202', '54.230.129.74', '202.160.128.40', '199.16.156.39', '13.224.167.108', '192.133.77.133', '168.143.171.154', '54.192.175.112', '128.242.245.43', '54.192.175.108', '54.192.175.87', '199.59.148.229', '143.204.68.22', '13.33.88.122', '52.85.242.73', '18.165.122.87', '168.143.162.58', '103.228.130.61', '128.242.240.180', '99.86.4.8', '104.244.46.52', '199.96.58.85', '13.226.225.73', '128.121.146.109', '69.30.25.21', '13.249.146.22', '13.249.146.87', '157.240.12.5', '3.162.38.113', '143.204.68.72', '104.244.43.52', '13.224.167.10', '3.162.38.31', '3.162.38.11', '3.162.38.66', '202.160.128.195', '162.125.6.1', '104.244.43.128', '18.165.122.23', '99.86.4.35', '108.160.165.212', '108.157.14.27', '13.226.225.44', '157.240.9.36', '13.33.88.37', '18.239.36.92', '199.59.148.247', '13.33.88.97', '31.13.84.34', '124.11.210.175', '13.226.225.52', '31.13.86.21', '108.157.14.86', '143.204.68.36'})
domain_names_set1 = [
    "tmdb.org",
    "api.tmdb.org",
    "themoviedb.org",
    "api.themoviedb.org",
    "www.themoviedb.org",
    "auth.themoviedb.org"
]
hosts_content_set1 = ping_and_get_fastest_ips(ip_addresses_set1, domain_names_set1, num_fastest=3)

# Example usage for the second set of IP addresses and domain names
ip_addresses_set2 = read_ip_addresses_from_file('image_tmdb_ip.txt')
ip_addresses_set2 = ip_addresses_set2 .union({'89.187.162.242', '169.150.249.167', '143.244.50.209', '143.244.50.210', '143.244.50.88', '143.244.50.82', '169.150.249.165', '143.244.49.178', '143.244.49.179', '143.244.50.89', '143.244.50.212', '169.150.207.215', '169.150.249.163', '143.244.50.85', '143.244.50.91', '143.244.50.213', '169.150.249.164', '169.150.249.162', '169.150.249.166', '143.244.49.183', '143.244.49.177', '143.244.50.83', '138.199.9.104', '169.150.249.169', '143.244.50.214', '79.127.213.217', '143.244.50.87', '143.244.50.84', '169.150.249.168', '143.244.49.180', '143.244.50.86', '143.244.50.90', '143.244.50.211'})
domain_names_set2 = [
    "image.tmdb.org",
    "images.tmdb.org"
]
hosts_content_set2 = ping_and_get_fastest_ips(ip_addresses_set2, domain_names_set2, num_fastest=2)

# Write the content to the hosts file
hosts_file_path = "hosts"
with open(hosts_file_path, "w") as hosts_file:
    hosts_file.write("127.0.0.1\tlocalhost\n")
    hosts_file.write(hosts_content_set1)
    hosts_file.write(hosts_content_set2)

