#Website Comparison Tool

This is a Python script that compares two websites by analyzing their content and performing various checks. It uses libraries such as requests, selenium, BeautifulSoup, and difflib to retrieve web page data, capture screenshots, compare HTML content, and analyze differences.

# Prerequisites
Before running the script, make sure you have the following:

- Python 3.x installed on your system
- The required Python libraries installed. You can install them using pip:

`pip install requests selenium webdriver_manager beautifulsoup4 difflib
`
- Chrome web browser installed (required for Selenium WebDriver)

# Usage
- Clone or download the script to your local machine.
- Open a terminal or command prompt and navigate to the directory where the script is located.
- Run the script using the following command:
`python script_name.py
`
- The script will prompt you to enter the URLs of the two websites you want to compare. Enter the URLs as requested.

- The script will then perform the following steps:

   > => Validate the URLs and check if they are accessible.

   > => Retrieve the HTML content of the websites.

   > => Capture full-page screenshots of both websites.

   > => Compare the HTML content for differences and generate an HTML diff file.

   > => Analyze the content for clickable links, clickable buttons, and visible images.

   > => Retrieve and compare the URLs of the web pages within each website.

- The script will output the results to the console and save the screenshots, HTML diff, and URL comparison files in the same directory.

# License
- This script is released under the MIT License.


# Acknowledgments
This script was developed using various open-source libraries and resources. The following libraries were used:

- requests
- selenium
- webdriver_manager
- BeautifulSoup
- difflib
Special thanks to the authors and contributors of these libraries for their valuable work.

Please note that this script is provided as-is and no guarantees are made regarding its functionality or accuracy. Use it responsibly and at your own risk.
