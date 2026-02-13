import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
'''server = pd.read_json("F:\Meghops LTD\Dataset-Scrap\stackoverflow_scraper\stackoverflow_scraper\output\serverfault-related.json", orient='records')
# Ensure 'related_tags' column is a list of lists (if stored as strings, convert them)
server['tags'] = server['tags'].apply(lambda x: eval(x) if isinstance(x, str) else x)

# Extract the column as a list of lists
related_tags_list = server['tags'].tolist()

# Remove duplicates at row level first (avoid redundant lists)
unique_related_tags = [list(set(sublist)) for sublist in related_tags_list]

# Flatten into a single list and remove duplicates
flat_tags = list(set(tag for sublist in unique_related_tags for tag in sublist))

# Display the result
print(flat_tags)
'''

cloud_logging_tags = [
    'syslog', 'rsyslog', 'syslog-ng', 'logrotate', 'dmesg',
    'journald', 'systemd-journald', 'auditd', 'audit', 'fail2ban',
    'selinux', 'apparmor', 'permissions', 'sudo', 'acl',
    'luks', 'ecryptfs', 'rootkit', 'rkhunter', 'chkrootkit',
    'tripwire', 'clamav', 'firewall', 'iptables', 'nftables',
    'ufw', 'firewalld', 'pf (OpenBSD packet filter)', 'snort', 'suricata',
    'tcp-wrappers', 'pam', 'ssh'
]

# Print the list
print(cloud_logging_tags)

# Function to c
#check question count for each tag on Server Fault
def check_tag_question_count(tags):
    base_url = "https://unix.stackexchange.com/questions/tagged/{}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    valid_tags = []
    max_retries = 3  # Limit retries to prevent long waits
    wait_time = 10  # Increase wait time per retry to avoid rate limits

    session = requests.Session()
    session.headers.update(headers)

    for tag in tags:
        url = base_url.format(tag)
        print(f"Checking tag: {tag} -> {url}")

        retry_count = 0
        while retry_count < max_retries:
            try:
                response = session.get(url, timeout=15)

                if response.status_code == 429:  # Too Many Requests
                    print(f"429 Too Many Requests. Waiting {wait_time} seconds before retrying...")
                    time.sleep(wait_time)
                    retry_count += 1
                    continue  # Retry the same tag

                if response.status_code != 200:
                    print(f"Failed to fetch tag {tag}. Status code: {response.status_code}")
                    break  # Move to the next tag

                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract question count using the correct structure
                count_elem = soup.select_one("div.fs-body3.flex--item.fl1.mr12.sm\\:mr0.sm\\:mb12")
                if count_elem:
                    count_text = count_elem.get_text(strip=True).replace(',', '').split()[0]
                    try:
                        question_count = int(count_text)
                        if question_count > 0:
                            valid_tags.append({"Tag": tag, "Questions": question_count})
                            print(f"✅ Found {question_count} questions for '{tag}'")
                        else:
                            print(f"⚠️ No questions found for '{tag}', skipping...")
                    except ValueError:
                        print(f"❌ Failed to parse question count for '{tag}'")
                else:
                    print(f"⚠️ No question count found for '{tag}', skipping...")
                break  # Exit retry loop
            except requests.exceptions.RequestException as e:
                print(f"❌ Request failed for {tag}: {e}")
                retry_count += 1
                time.sleep(wait_time)
                continue

        time.sleep(5)  # Increased delay to prevent rate limiting

    return valid_tags

# Run the script
valid_tags = check_tag_question_count(cloud_logging_tags)
print("\nFinal Summary:")
for tag_data in valid_tags:
    print(f"{tag_data['Tag']}: {tag_data['Questions']} questions")

print(f"\nExtracted {len(valid_tags)} valid tags.")

# Save to CSV
df = pd.DataFrame(valid_tags)
df.to_csv("unix-device-tags.csv", index=False)
print("Saved to unix-device-tags")
