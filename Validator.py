import queue
import threading
import requests

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'  # white
Y = '\033[33m'  # yellow

q = queue.Queue()
valid_proxies = []

# Ask the user for the file path
file_path = input("Enter the path to the file containing proxies (e.g., proxy_list.txt): ")

# Ask the user for the number of proxies to validate
num_proxies = int(input("Enter the number of proxies you want to validate: "))

with open(file_path, "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)

def check_proxies():
    global q, valid_proxies
    while not q.empty() and len(valid_proxies) < num_proxies:
        proxy = q.get()
        try:
            res = requests.get("http://ipinfo.io/json", proxies={"http": proxy, "https": proxy}, timeout=5)

        except requests.RequestException:
            continue

        if res.status_code == 200:
            print(f"{G}{proxy}")
            valid_proxies.append(proxy)

# Use a fixed number of threads
num_threads = 10

# Start threads for proxy validation
threads = []
for _ in range(num_threads):
    t = threading.Thread(target=check_proxies)
    t.start()
    threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()

# Save valid proxies to a file
with open("valid-proxy.txt", "w") as valid_file:
    valid_file.write("\n".join(valid_proxies))

print(f"\n{C}Proxy validation complete. Valid proxies saved in {Y}valid-proxy.txt")
