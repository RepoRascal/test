import requests
from urllib.parse import urlparse

# Extract domain from a URL
def extract_domain(url):
    return urlparse(url).netloc

# Fetch subdomains from crt.sh
def get_subdomains_from_crtsh(domain):
    try:
        response = requests.get(f"https://crt.sh/?q=%.{domain}&output=json")
        if response.status_code == 200:
            json_data = response.json()
            # Extract name_value (subdomain) from each certificate
            return [item['name_value'] for item in json_data]
        return []
    except requests.RequestException:
        return []

def main():
    # Load domains from the input file
    with open('h1_web_fix1.txt', 'r') as file:
        urls = file.readlines()

    domains = [extract_domain(url.strip()) for url in urls]
    wildcard_subdomains = []

    for domain in domains:
        subdomains = get_subdomains_from_crtsh(domain)
        # Filter subdomains that have wildcards
        wildcard_entries = [sub for sub in subdomains if '*' in sub]
        wildcard_subdomains.extend(wildcard_entries)

    # Save wildcard subdomains to an output file
    with open('wildcard_subdomains.txt', 'w') as out_file:
        for subdomain in wildcard_subdomains:
            out_file.write(f"{subdomain}\n")

    print(f"Found {len(wildcard_subdomains)} wildcard subdomains. Saved to wildcard_subdomains.txt.")

if __name__ == "__main__":
    main()
