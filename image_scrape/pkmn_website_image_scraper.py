import os.path
from urllib.request import Request, urlopen
from urllib.parse import quote
from time import sleep
import requests

# https://tcg.pokemon.com/assets/img/expansions/chilling-reign/cards/en-us/SWSH06_EN_1-2x.jpg
# https://tcg.pokemon.com/assets/img/expansions/chilling-reign/cards/en-us/SWSH06_EN_2-2x.jpg

NUMBER_OF_CARDS_IN_SET = 233

url = "https://www.pokellector.com/sets/SWSH45-Shining-Fates"


set_name = "chilling_reign"

output_directory = f"./{set_name}"
current_dir = './'


debug = True
def debug_print(message="\n"):
    if debug:
        print(message)

def make_safe_url(url):
    if 'é' in url:
        parts = url.split('é')

        safe_e = quote('é')
        return safe_e.join(parts)
    else:
        return url

def get_links():
    links = []
    count = 1

    while (count <= NUMBER_OF_CARDS_IN_SET):
        link = f"https://tcg.pokemon.com/assets/img/expansions/chilling-reign/cards/en-us/SWSH06_EN_{count}-2x.jpg"
        links.append(link)
        debug_print(f"appended {link}")
        count += 1
    return links


def download_image(image_url, index):
    image_name = f'{output_directory}/{index}.jpg'

    img_data = requests.get(image_url).content
    with open(image_name, 'wb') as handler:
        handler.write(img_data)


def main():
    links = get_links()

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    count = 1
    for link in links:
        debug_print(f"downloading {link}")
        download_image(link, count)
        sleep(1)
        debug_print(f"done")
        count += 1 



try:
    main()
except Exception as e:
    print(e)

print("done")
