import requests
from urllib.parse import urlparse
import concurrent.futures

# Extract domain from a URL
def extract_domain(url):
    return urlparse(url).netloc

# Fetch subdomains from crt.sh
def get_subdomains_from_crtsh(domain):
    try:
        response = requests.get(f"https://crt.sh/?q=%.{domain}&output=json")
        if response.status_code == 200:
            json_data = response.json()
            # Extract name_value (subdomain) from each certificate and filter wildcard entries
            return [item['name_value'] for item in json_data if '*' in item['name_value']]
        return []
    except requests.RequestException:
        return []

def main():
    # Load domains from the input file
    with open('h1_web_fix1.txt', 'r') as file:
        urls = file.readlines()

    domains = [extract_domain(url.strip()) for url in urls]
    wildcard_subdomains = []

    # Using ThreadPoolExecutor to speed up fetching subdomains
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_domain = {executor.submit(get_subdomains_from_crtsh, domain): domain for domain in domains}
        for future in concurrent.futures.as_completed(future_to_domain):
            wildcard_entries = future.result()
            wildcard_subdomains.extend(wildcard_entries)

    # Save wildcard subdomains to an output file
    with open('wildcard_subdomains.txt', 'w') as out_file:
        for subdomain in wildcard_subdomains:
            out_file.write(f"{subdomain}\n")

    print(f"Found {len(wildcard_subdomains)} wildcard subdomains. Saved to wildcard_subdomains.txt.")

if __name__ == "__main__":
    main()
