import requests
from bs4 import BeautifulSoup
import urllib.request
import traceback

class Scrapper:

    TRACE_PER_WARNING = False

    def __init__(self, url, folder):
        """
        :param url: String of the targeted website
        :param folder: Folder where link's content will be stored
        """
        self.url = url
        self.folder = folder

    def scrap_links_in_url(self):
        """

        Scrap all links from a target website

        :return: List of string corresponding to all links in the webpage
        """
        session = requests.Session()
        session.headers[
            'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        page_content = session.get(self.url).content
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



# Main
if __name__ == "__main__":

    scrap = Scrapper("http://index-of.es/Attacks/403%20Forbidden%20Attack/", "data")

    links = scrap.scrap_links_in_url()

    scrap.retrieve_urls(links)
