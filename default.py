import sys
import xbmcplugin
import xbmcgui
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://rodenttube.nl/videos/'

def fetch_video_links():
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href and href.endswith('.mp4'):
                title = href.rsplit('/', 1)[-1].replace('_', ' ')
                add_video_item(BASE_URL + href, title)
    except Exception as e:
        xbmcgui.Dialog().notification("RodentTube", f"Fout bij ophalen: {str(e)}", xbmcgui.NOTIFICATION_ERROR)

def add_video_item(url, title):
    li = xbmcgui.ListItem(title)
    li.setPath(url)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=False)

if __name__ == '__main__':
    fetch_video_links()
    xbmcplugin.endOfDirectory(int(sys.argv
                                  [1]))
