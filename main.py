from google import search
import os, errno, uuid
import requests
from urllib2 import HTTPError

#from bs4 import BeautifulSoup


from bing_search_api import BingSearchAPI


# api = BingSearchAPI('YOU_API_KEY')
# result =  api.searchImage('sunshine')
# print(result.json)

def get_search(text = None, stop = 1000, lang='en'):
    return search(text, stop=stop, lang=lang)

def process_search(search=None, folder=None):
    if search is None:
        return

    if folder is None:
        return

    try:
        os.makedirs(folder)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(folder):
            pass
        else:
            raise

    try:
        for url in search:
            local_filename = folder + "/" + uuid.uuid4().__str__().split('-')[4] + '_' + url.split('/')[-1].split('?')[0]

            print(url, local_filename)

            try:
                r = requests.get(url, stream=True)

                f = open(local_filename, 'wb')
                for chunk in r.iter_content(chunk_size=512 * 1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                f.close()
            except requests.exceptions.SSLError, e:
                print("SSL Error for", url)
            except requests.exceptions.InvalidSchema, e:
                print("Invalid Schema:", url)
            except requests.exceptions.ConnectionError, e:
                print("Connection Error:", url)
    except HTTPError, e:
        print("HTTP Error Occurred: ", e)


def main():
    s = get_search('filetype:pdf resume java c#')
    process_search(s, folder="./out")



if __name__ == "__main__":
    main()
