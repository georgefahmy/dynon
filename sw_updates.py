import requests
import re
import os
from bs4 import BeautifulSoup


check_url = "https://www.dynonavionics.com/skyview-hdx-software-updates-us-packages.php"


def archive_old_sw_updates():
    sw_updates_path = f"/Users/GFahmy/Desktop/RV-7_Plans/SkyView/sotware_updates/software/"
    archive_folder = (
        "/Users/GFahmy/Desktop/RV-7_Plans/SkyView/sotware_updates/software/archived_sw_updates/"
    )
    existing_sw_files = [file for file in os.listdir(sw_updates_path) if file.startswith("SkyView")]
    if not existing_sw_files:
        print("No SW to archive")
        return
    for file in existing_sw_files:
        os.rename(sw_updates_path + file, archive_folder + file)
    print("Archived old SW versions")
    return


def generate_download_url(download_href):
    dn = f"https://dynonavionics.com/{download_href}"
    fn = f"/Users/GFahmy/Desktop/RV-7_Plans/SkyView/sotware_updates/software/{download_href.split('/')[-1]}"
    return (dn, fn)


soup = BeautifulSoup(requests.get(check_url).content, "html.parser")

non_hw4_section = soup.find_all(string=re.compile("Hardware Revisions 1/2/3", flags=re.I))[0]
non_hw4_download_url = non_hw4_section.parent.parent.parent.find_all(string=re.compile("HDX1100"))[
    0
].parent.parent.get("href")

hw4_section = soup.find_all(string=re.compile("Hardware Revision 4", flags=re.I))[0]
hw4_download_url = hw4_section.parent.parent.parent.find_all(string=re.compile("HDX1100"))[
    0
].parent.parent.get("href")

download_non_hw4_url, non_hw4_filename = generate_download_url(non_hw4_download_url)
download_hw4_url, hw4_filename = generate_download_url(hw4_download_url)


archive_old_sw_updates()

print(f"\nDownloading {non_hw4_filename.split('/')[-1]}")

with open(non_hw4_filename, "wb+") as out_file:
    content = requests.get(download_non_hw4_url, stream=True).content
    out_file.write(content)
    print(f"Success!\nFile saved to {non_hw4_filename}")

print(f"\nDownloading {hw4_filename.split('/')[-1]}")
with open(hw4_filename, "wb+") as out_file:
    content = requests.get(download_hw4_url, stream=True).content
    out_file.write(content)
    print(f"Success!\nFile saved to {hw4_filename}")
