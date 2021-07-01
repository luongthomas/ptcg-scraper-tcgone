import os.path
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
from time import sleep
import requests

# url = "https://www.pokellector.com/sets/SWSH0-Vivid-Voltage"
url = "https://www.pokellector.com/sets/SWSH45-Shining-Fates"
#https://pod.pokellector.com/cards/299/Duraludon.SWSH0.129.36068.thumb.png
#https://pod.pokellector.com/cards/299/Duraludon.SWSH0.129.36068.png
#https://www.pokellector.com/card/Duraludon-Vivid-Voltage-SWSH0-129

#https://pkmncards.com/wp-content/uploads/en_US-SF-001-yanma.jpg
#https://pkmncards.com/wp-content/uploads/en_US-SF-002-yanmega.jpg

# link_prefix = "(Vivid Voltage"
# filename_regex = r'https:\/\/bulbapedia\.bulbagarden\.net\/wiki\/(.*)_\(Vivid_Voltage_(\d+)\)'

# image_link_regex = r'(https:\/\/pod.pokellector\.com\/cards\/299.*\.png)'
image_link_regex = r'(https:\/\/pkmncards\.com\/wp-content\/uploads\/en_US-SF-.*\.jpg)"'

set_name = "shining_fates"

links_output = "image_links.txt"
output_directory = f"./{set_name}"

# current_dir = "./image_scraper/"
current_dir = './'

main_page_file = f"{current_dir}{set_name}_image_page.html"
soup_output = f"{current_dir}{set_name}_soup.html"

debug = True
def debug_print(message="\n"):
    if debug:
        print(message)


# base_url = "https://www.pokellector.com"
base_url = "https://www.pkmncards.com"
# /card/Weedle-Vivid-Voltage-SWSH0-1"

def make_safe_url(url):
    if 'é' in url:
        parts = url.split('é')

        safe_e = quote('é')
        return safe_e.join(parts)
    else:
        return url

def get_links():
    try:
        if os.path.isfile(links_output):
            links = open(links_output, "r").readlines()
            if len(links) != 0:
                return links

        safe_url = make_safe_url(url)

        req = Request(safe_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        webpage = urlopen(req).read()
        html = webpage.decode("utf-8")

        soup = BeautifulSoup(html, "html.parser")


        image_links = []

        with open(main_page_file, "r") as f:
            webpage = f.read()
            links = list(re.findall(image_link_regex, webpage))
            
            for link in links:
                full_image_url = link.replace('.thumb', '')
                if link not in image_links:
                    image_links.append(full_image_url)
            
        for link in image_links:
            print(link)

        # for td in soup.find_all('td'):
        #     for a in td.find_all('a'):
        #         title = a.get('title', '')
        #         if title and link_prefix in title:
        #             link = link_base + title.replace(' ', '_')
                    
        #             links.append(link)

        if not os.path.isfile(main_page_file):
            with open(main_page_file, "w") as f:
                f.write(html)

        # if not os.path.isfile(soup_output):
        #     with open(soup_output, "w") as f:
        #         f.write(soup.get_text())

        if not os.path.isfile(links_output):
            with open(links_output, "w") as f:
                for link in image_links:
                    f.write(link + '\n')
        print('links')
        return image_links
    except Exception as e:
        print(e)


def get_and_save_page(url, filename, directory="./output"):
    full_path = f"{directory}/{filename}"
    
    if "page_does_not_exist" in url:
        return False

    if not os.path.isfile(full_path):
        url = make_safe_url(url)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        html = webpage.decode("utf-8")

        with open(full_path, "w") as f:
            f.write(html)
            debug_print(f"downloading {full_path}")
            sleep(1)
    else:
        debug_print(f"skip {filename}")
    
    return True


pokemon_files = []


# def get_pokemon_page(url):
    # filename = ''
    
    # match = re.match(filename_regex, url)
    # if match:
    #     pokemon_id = f"{match.group(1)}_{match.group(2)}"
    #     filename = f"{pokemon_id}.html"
    #     if filename not in pokemon_files:
    #         success = get_and_save_page(url, filename, output_directory)
    #         if success:
    #             pokemon_files.append(filename)
    #         else:
    #             pokemon_files.append("PLACEHOLDER")


def download_image(image_url, index, reset):

    # SHINING FATES
    if reset:
        image_name = f'{output_directory}/SV{index}.jpg'
    else:
        image_name = f'{output_directory}/{index}.jpg'

    img_data = requests.get(image_url).content
    with open(image_name, 'wb') as handler:
        handler.write(img_data)


def main():
    # if not os.path.isfile(links_output):
    links = get_links()
    # else:
    #     with open(links_output) as f:
    #         links = f.read().splitlines()

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    count = 1
    reset = False
    for link in links:
        download_image(link, count, reset)
        sleep(1)

        # SHINING FATES
        if count == 73 and not reset:
            count = 1
            reset = True
        else:
            count += 1 

        # get_pokemon_page(link)


    
    

try:
    main()
except Exception as e:
    print(e)

print("done")
# count = 1
# for url in pokemon_files:
    # full_url = f"{output_directory}/{url}"
    # data = main2(full_url)
    # write_out(data, count)
    # count += 1
