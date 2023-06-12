import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from difflib import HtmlDiff
import re
from urllib.parse import urljoin
import sys


def validate_url(url):
    pattern = re.compile(
        r"^(https?://)?"
        r"((([a-zA-Z0-9_-]+)\.)+[a-zA-Z]{2,})"
        r"(/([a-zA-Z0-9_./-]+)*)?$"
    )
    return bool(re.match(pattern, url))


def get_full_page_screenshot(driver, file_path):
    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    driver.save_screenshot(file_path)
    driver.set_window_size(original_size['width'], original_size['height'])


def get_page_urls(url):
    response = requests.get(url)

    if response.status_code != 200:
        print("Error: Website could not be accessed.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")

    page_urls = []
    for link in links:
        href = link.get("href")
        if href and not href.startswith("#"):
            page_url = urljoin(url, href)
            if page_url not in page_urls:
                page_urls.append(page_url)

    return page_urls


def save_page_urls(url, page_urls, filename):
    with open(filename, "w") as file:
        file.write("Page URLs for " + url + ":\n")
        for page_url in page_urls:
            file.write(page_url + "\n")
    print("Page URLs saved to " + filename)


def compare_page_urls(file1, file2):
    with open(file1, "r") as file:
        urls1 = set(line.strip() for line in file.readlines())

    with open(file2, "r") as file:
        urls2 = set(line.strip() for line in file.readlines())

    missing_urls = urls1 - urls2

    if missing_urls:
        print("The following URLs are missing in website2_page_urls.txt:")
        for url in missing_urls:
            print(url)
    else:
        print("All URLs from website1_page_urls.txt are present in website2_page_urls.txt.")


def compare_websites(url1, url2):
    # Validate URLs
    if not validate_url(url1) or not validate_url(url2):
        print("Invalid URL(s).")
        return

    if url1 == url2:
        print("Please enter two different URLs for website 1 and website 2.")
        return

    # Get data for website 1
    print("Getting data for website 1...")
    response1 = requests.get(url1)

    if response1.status_code != 200:
        print("Error: Website 1 could not be accessed.")
        return

    website1_data = response1.text

    # Get data for website 2
    print("Getting data for website 2...")
    response2 = requests.get(url2)

    if response2.status_code != 200:
        print("Error: Website 2 could not be accessed.")
        return

    website2_data = response2.text

    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver1 = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver2 = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # Take full page screenshots
    print("Taking screenshots...")
    get_full_page_screenshot(driver1, "screenshot1.png")
    print("Screenshot 1 saved.")
    get_full_page_screenshot(driver2, "screenshot2.png")
    print("Screenshot 2 saved.")

    driver1.quit()
    driver2.quit()

    # Content Comparison (using BeautifulSoup and HtmlDiff)
    print("\nContent Comparison:")

    if website1_data == website2_data:
        print("The websites have identical content.")
    else:
        print("The websites have different content.")

        # Automated Testing (using BeautifulSoup and HtmlDiff)
        print("\nAutomated Testing:")

        soup1 = BeautifulSoup(website1_data, "html.parser")
        soup2 = BeautifulSoup(website2_data, "html.parser")

        # Find all links and check if they are clickable
        links1 = soup1.find_all("a")
        links2 = soup2.find_all("a")

        for link in links1:
            if not link.has_attr("href"):
                print("Link not clickable on Website 1: ", link)

        for link in links2:
            if not link.has_attr("href"):
                print("Link not clickable on Website 2: ", link)

        # Find all buttons and check if they are clickable
        buttons1 = soup1.find_all("button")
        buttons2 = soup2.find_all("button")

        for button in buttons1:
            if not button.has_attr("onclick"):
                print("Button not clickable on Website 1: ", button)

        for button in buttons2:
            if not button.has_attr("onclick"):
                print("Button not clickable on Website 2: ", button)

        # Find all images and check if they are visible
        images1 = soup1.find_all("img")
        images2 = soup2.find_all("img")

        for image in images1:
            if not image.has_attr("src"):
                print("Image not seen on Website 1: ", image)

        for image in images2:
            if not image.has_attr("src"):
                print("Image not seen on Website 2: ", image)

        # Full Differences Comparison
        print("\nFull Differences Comparison:")

        diff = HtmlDiff()
        diff_output = diff.make_file(website1_data.splitlines(), website2_data.splitlines())

        with open("full_differences.html", "w", encoding="utf-8") as file:
            file.write(diff_output)
        print("Full differences saved to full_differences.html.")

        # Compare page URLs
        print("\nComparing Page URLs:")
        website1_page_urls = get_page_urls(url1)
        website2_page_urls = get_page_urls(url2)
        save_page_urls(url1, website1_page_urls, "website1_page_urls.txt")
        save_page_urls(url2, website2_page_urls, "website2_page_urls.txt")
        compare_page_urls("website1_page_urls.txt", "website2_page_urls.txt")


if __name__ == "__main__":
    url1 = input("Enter the first website URL: ")
    url2 = input("Enter the second website URL: ")

    compare_websites(url1, url2)
