import requests
from bs4 import BeautifulSoup
import urllib.request
import traceback
import sys

class Scrapper:

    TRACE_PER_WARNING = False

    def __init__(self, url, folder):
        """
        :param url: String of the targeted website
        :param folder: Folder where link's content will be stored
        """
        self.url = url
        self.folder = folder
        self.session = requests.Session()

    def basic_soup(self):
        """

        Basic BeautifulSoup scraper without any specification

        """
        #Scrap content
        content = self.session.get(self.url).content
        soup = BeautifulSoup(content, "html.parser")
        return soup


    def scrap_login_csrf(self,login_url,login_information):
        """

        Allow to scrap a website based on a specific csrf TOKEN to bypass login restriction

        :param login_url : String > login page url
        :param login_information: Dictionary > login payload
        """

        #Identify the client to the website via the payload
        self.post(login_url, data=login_information)
        #Scrap content
        content = self.session.get(self.url).content
        soup = BeautifulSoup(content, "html.parser")
        return soup


    def scrap_links_in_url(self):
        """

        Scrap all links from a target website

        :return: List of string corresponding to all links in the webpage
        """
        self.session.headers[
            'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        page_content = self.session.get(self.url).content
        soup = BeautifulSoup(page_content, "html.parser")
        return [link["href"] for link in soup.find_all("a", href=True)]

    def filter_only_file_extention(self, links, file_extent):
        """
        :param links: List of all link to filter
        :param file_extent: required extention file to have
        :return List of string corresponding to all links in the webpage filtered
        """
        size = len(links)
        for i in range(size):
            if file_extent not in links[i]:
                links.remove(links[i])
        return links


    def retrieve_urls(self, links):
        """

        Retrieve all links content into files

        :param links: List of all link to retrieve
        :return: None
        """
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        for k, lk in enumerate(links):

            if lk[0] == "/":
                inc = ""
            else:
                inc = "/"

            try:
                if lk[:4] != "http":
                    urllib.request.urlretrieve(self.url + lk, self.folder + inc + lk)
                else:
                    urllib.request.urlretrieve(lk, self.folder + inc + lk)
            except Exception as e:
                print("[WARN] couldn't retrieve "+lk)
                if self.TRACE_PER_WARNING:
                    print(str(e))
                    traceback.print_tb(e.__traceback__)



def download_url_links_content(scrap):
    """
    Download all content from all links found into an url
    """
    links = scrap.scrap_links_in_url()

    scrap.retrieve_urls(links)
    return "Retrieve Successful !"

def get_all_links(scrap):
    return scrap.scrap_links_in_url()

def demo(scrap):
    scrap = Scrapper("http://index-of.es/Attacks/403%20Forbidden%20Attack/", "data")

    links = scrap.scrap_links_in_url()

    scrap.retrieve_urls(links)
    return "Demo Over, you can found newly downloaded pdf into %s" % (scrap.folder)

features = [download_url_links_content, demo, get_all_links]

# Main
if __name__ == "__main__":
    argc = len(sys.argv)
    if argc != 4:
        print("usage : ./python3 Scrapy.py <actionID> <url> <folder>")
        print("   > actionID: Number of the desired action to be executed by Scrapy")
        print("       > 0 : Download all content from all links found into an url")
        print("       > 1 : Demonstration of Scrapy by downloading some files from a website")
        print("       > 2 : Get all links contained within an url")
        print("   > url: String of the targeted website")
        print("   > folder: Folder to store possible outputs (downloads, files, ...)")
    else:
        scrap = Scrapper(sys.argv[2], sys.argv[3])
        ID = int(sys.argv[1])
        try:
            print(features[ID](scrap))
        except IndexError:
            print("/!\\ =====> Invalid action ID : %d isn't supported <===== /!\\" % (ID))
