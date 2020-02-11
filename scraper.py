import re
import lxml.html
import urllib
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib.request
import requests
import urllib.robotparser
import nltk

# nltk.download()

all_urls = dict()

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation requred.
    links = list()

    try:
        parsed = urlparse(url)
        robot = parsed.scheme + "://" + parsed.netloc + "/robot.txt"
        print(robot)
        temp = urllib.request.urlopen(robot)
        print(temp.info())
    except:
        print("no robot")


    html = urllib.request.urlopen(url, timeout = 10)
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.findAll('a'):
        new_link = link.get('href')
        if(is_valid(new_link)):
            try:
                temp = urllib.request.urlopen(new_link, timeout = 10)
                if(temp.getcode() == 200 and (all_urls.get(new_link) == None)):
                    new_soup = BeautifulSoup(temp, "html.parser")

                    tokens = nltk.tokenize.word_tokenize(new_soup.get_text())

                    print(tokens)

                    links.append(new_link)
                    all_urls[new_link] = 1
            except Exception as ex:
                print(type(ex))
                # print("error 404")
            # links.append(new_link)


    # links = list()
    # if(resp.status >= 600 and resp.status <= 606):
    #     print(resp.error)
    # else:
    #     if(resp.raw_response):
    #         if(resp.raw_response.status_code == 200):
    #             content = urllib.request.urlopen(url).read()
    #             html = lxml.html.document_fromstring(content)
    #             urls = html.xpath('//a/@href')
    #             print(list(urls))
    #             for item in urls:
    #                 if(is_valid(item)):
    #                     #x = requests.request('GET', item)
    #                     #if(x.status_code == 200):
    #                     req = requests.request('GET', item)
    #                     if(req == 200):
    #                         links.append(item)

    return links

def is_valid(url):
    try:

        parsed = urlparse(url)

        if parsed.scheme not in set(["http", "https"]):
            return False

        valid = ['.ics.uci.edu/', '.cs.uci.edu/', '.informatics.uci.edu/', '.stats.uci.edu/', 'today.uci.edu/department/information_computer_sciences/']

        for sub in valid:
            if(sub in url):
                return not re.match(
                    r".*\.(css|js|bmp|gif|jpe?g|ico"
                    + r"|png|tiff?|mid|mp2|mp3|mp4"
                    + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                    + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                    + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                    + r"|epub|dll|cnf|tgz|sha1"
                    + r"|thmx|mso|arff|rtf|jar|csv"
                    + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
