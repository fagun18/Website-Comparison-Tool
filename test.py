import os
import re
import time
import requests
from bs4 import BeautifulSoup
from difflib import HtmlDiff
from urllib.parse import urljoin
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from PIL import Image, ImageChops


class WebsiteComparer:
    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument("--headless")

    def validate_url(self, url):
        pattern = re.compile(
            r"^(https?://)?"
            r"((([a-zA-Z0-9_-]+)\.)+[a-zA-Z]{2,})"
            r"(/([a-zA-Z0-9_./-]+)*)?$"
        )
        return bool(re.match(pattern, url))

    def get_page_urls(self, url):
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

    def check_broken_links(self, driver):
        links = driver.find_elements_by_tag_name("a")
        broken_links = []
        for link in links:
            href = link.get_attribute("href")
            if href:
                response = requests.head(href)
                if response.status_code != 200:
                    broken_links.append(href)
        return broken_links

    def analyze_page_load_times(self, driver, url):
        driver.get(url)
        navigation_start = driver.execute_script("return window.performance.timing.navigationStart")
        load_event_end = driver.execute_script("return window.performance.timing.loadEventEnd")
        page_load_time = (load_event_end - navigation_start) / 1000
        print(f"Page load time for {url}: {page_load_time:.2f} seconds")

    def compare_websites(self, url1, url2):
        if not self.validate_url(url1) or not self.validate_url(url2):
            print("Invalid URL(s).")
            return

        if url1 == url2:
            print("Please enter two different URLs for website 1 and website 2.")
            return

        driver1 = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=self.options)
        driver2 = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=self.options)

        # Compare broken links
        broken_links1 = self.check_broken_links(driver1)
        broken_links2 = self.check_broken_links(driver2)
        print("Broken links in Website 1:", broken_links1)
        print("Broken links in Website 2:", broken_links2)

        # Analyze page load times
        self.analyze_page_load_times(driver1, url1)
        self.analyze_page_load_times(driver2, url2)

        driver1.get(url1)
        driver2.get(url2)

        # Check for differences in page content
        diff = HtmlDiff()
        website1_html = driver1.page_source
        website2_html = driver2.page_source
        content_diff = diff.make_file(website1_html.splitlines(), website2_html.splitlines())
        with open("content_diff.html", "w", encoding="utf-8") as file:
            file.write(content_diff)
        print("Content differences saved to content_diff.html.")

        # Check for visual differences using screenshots
        driver1.save_screenshot("screenshot1.png")
        driver2.save_screenshot("screenshot2.png")

        image1 = Image.open("screenshot1.png")
        image2 = Image.open("screenshot2.png")

        diff_image = ImageChops.difference(image1, image2)
        if diff_image.getbbox():
            diff_image.save("visual_diff.png")
            print("Visual differences saved to visual_diff.png.")
        else:
            print("No visual differences.")

        # Compare page URLs
        website1_page_urls = self.get_page_urls(url1)
        website2_page_urls = self.get_page_urls(url2)
        self.save_page_urls(url1, website1_page_urls, "website1_page_urls.txt")
        self.save_page_urls(url2, website2_page_urls, "website2_page_urls.txt")

        driver1.quit()
        driver2.quit()

    def save_page_urls(self, url, page_urls, filename):
        with open(filename, "w") as file:
            file.write(f"Page URLs for {url}:\n")
            for page_url in page_urls:
                file.write(page_url + "\n")
        print(f"Page URLs saved to {filename}.")


if __name__ == "__main__":
    comparer = WebsiteComparer()
    url1 = input("Enter the first website URL: ")
    url2 = input("Enter the second website URL: ")
    comparer.compare_websites(url1, url2)
