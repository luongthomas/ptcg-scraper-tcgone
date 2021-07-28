import os.path
import sys
import re
import string
from urllib.request import Request, urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from time import sleep



legendary_heartbeat = False
amazing_volt = False
vivid_voltage = False
shiny_star_v = False
shining_fates = False
silver_lance = False
skyscraping_perfection = True

url = link_prefix = filename_regex = links_output = output_directory = ""
output_yaml = set_id = set_name = set_pio_id = set_enum_id = set_abbr = ""

main_page_file = "bulbapedia_page.html"
soup_output = "bulbapedia_soup.html"

if legendary_heartbeat:
    url = "https://bulbapedia.bulbagarden.net/wiki/Legendary_Heartbeat_(TCG)"
    link_prefix = "(Legendary Heartbeat"
    filename_regex = r'https:\/\/bulbapedia\.bulbagarden\.net\/wiki\/(.*)_\(Legendary_Heartbeat_(\d+)\)'
    links_output = "legendary_heartbeat_links.txt"
    output_directory = "./legendary_heartbeat"

    output_yaml = "dcc.yaml"
    set_id = "451"
    set_name = "Legendary Heartbeat"
    set_pio_id = "lhe"
    set_enum_id = "LEGENDARY_HEARTBEAT"
    set_abbr = "LHE"

elif amazing_volt:
    url = "https://bulbapedia.bulbagarden.net/wiki/Vivid_Voltage_(TCG)"
    link_prefix = "(Amazing Volt Tackle"
    filename_regex = r'https:\/\/bulbapedia\.bulbagarden\.net\/wiki\/(.*)_\(Amazing_Volt_Tackle_(\d+)\)'
    links_output = "amazing_volt_tackle_links.txt"
    output_yaml = "dbb.yaml"
    output_directory = "./amazing_volt"
    set_id = "450"
    set_name = "Amazing Volt Tackle"
    set_pio_id = "avt"
    set_enum_id = "AMAZING_VOLT_TACKLE"
    set_abbr = "AVT"
    main_page_file = "bulbapedia_amazing_volt_tackle_page.html"
    soup_output = "bulbapedia_amazing_volt_tackle_soup.html"

elif vivid_voltage:
    url = "https://bulbapedia.bulbagarden.net/wiki/Vivid_Voltage_(TCG)"
    link_prefix = "(Vivid Voltage"
    filename_regex = r'https:\/\/bulbapedia\.bulbagarden\.net\/wiki\/(.*)_\(Vivid_Voltage_(\d+)\)'
    links_output = "vivid_voltage_links.txt"
    output_directory = "./vivid_voltage"
    output_yaml = "434-vivid-voltage.yaml"
    set_id = "434"
    set_name = "Vivid Voltage"
    set_pio_id = "viv"
    set_enum_id = "VIVID_VOLTAGE"
    set_abbr = "VIV"
    main_page_file = "bulbapedia_vivid_voltage_page.html"
    soup_output = "bulbapedia_vivid_voltage_soup.html"

elif shiny_star_v:
    url = "https://bulbapedia.bulbagarden.net/wiki/Shiny_Star_V_(TCG)"
    link_prefix = "(Shiny Star V"
    filename_regex = r'https:\/\/bulbapedia\.bulbagarden\.net\/wiki\/(.*)_\(Shiny_Star_V_(\d+)\)'
    links_output = "shiny_star_v_links.txt"
    output_directory = "./shiny_star_v"
    output_yaml = "435-shiny-star-v.yaml"
    set_id = "435"
    set_name = "Shiny Star V"
    set_pio_id = "ssv"
    set_enum_id = "SHINY_STAR_V"
    set_abbr = "SSV"
    main_page_file = "bulbapedia_shiny_star_v_page.html"
    soup_output = "bulbapedia_shiny_star_v_soup.html"
    

    #https://bulbapedia.bulbagarden.net/wiki/Alcrem_(Shining_Fates_73)
    #https://bulbapedia.bulbagarden.net/wiki/Rowlet_(Shining_Fates_SV1)
    #
elif shining_fates:
    url = "https://bulbapedia.bulbagarden.net/wiki/Shining_Fates_(TCG)"
    link_prefix = "(Shining Fates"
    filename_regex = r'https:\/\/bulbapedia\.bulbagarden\.net\/wiki\/(.*)_\(Shining_Fa[t]?es_([\d\w]+)\)'
    output_directory = "./shining_fates"
    links_output = f"./shiny_star_v_links.txt"
    output_yaml = f"./435-shining_fates.yaml"
    set_id = "435"
    set_name = "Shining Fates"
    set_pio_id = "shf"
    set_enum_id = "SHINING_FATES"
    set_abbr = "SHF"
    main_page_file = f"{output_directory}/bulbapedia_shining_fates_page.html"
    soup_output = f"{output_directory}/bulbapedia_shining_fates_soup.html"

elif silver_lance:
    url = "https://bulbapedia.bulbagarden.net/wiki/Chilling_Reign_(TCG)"
    set_name = "Silver Lance"
    link_prefix = f"({set_name}"
    filename_regex = r'https:\/\/bulbapedia\.bulbagarden\.net\/wiki\/(.*)_\(Silver_Lance_([\d\w]+)\)'
    name = "silver_lance"
    output_directory = f"./{name}"
    links_output = f"./{name}_links.txt"
    output_yaml = f"./js6k-{name}.yaml"
    set_id = "js6k"
    set_pio_id = "sil"
    set_enum_id = f"{name.upper()}"
    set_abbr = set_pio_id.upper()
    main_page_file = f"./bulbapedia_{name}_page.html"
    soup_output = f"./bulbapedia_{name}_soup.html"

elif skyscraping_perfection:
    url = "https://bulbapedia.bulbagarden.net/wiki/Evolving_Skies_(TCG)"
    set_name = "Skyscraping Perfection"
    link_prefix = f"({set_name}"
    filename_regex = r'https:\/\/bulbapedia\.bulbagarden\.net\/wiki\/(.*)_\(Skyscraping_Perfection_([\d\w]+)\)'
    name = "skyscraping_perfection"
    output_directory = f"./{name}"
    links_output = f"./{name}_links.txt"
    output_yaml = f"./s7D-{name}.yaml"
    set_id = "s7D"
    set_pio_id = "spe"
    set_enum_id = f"{name.upper()}"
    set_abbr = set_pio_id.upper()
    main_page_file = f"./bulbapedia_{name}_page.html"
    soup_output = f"./bulbapedia_{name}_soup.html"


# https://bulbapedia.bulbagarden.net/wiki/Chilling_Reign_(TCG)

debug = True
def debug_print(message="\n"):
    if debug:
        print(message)





link_base = 'https://bulbapedia.bulbagarden.net/wiki/'


def set_directory_to_current_script_location():
    os.chdir(sys.path[0])

def make_safe_url(url):
    if 'é' in url:
        parts = url.split('é')

        safe_e = quote('é')
        return safe_e.join(parts)
    else:
        return url

def get_links():
    if os.path.isfile(links_output) and os.stat(links_output).st_size != 0:
        links = open(links_output, "r").readlines()
        return links

    safe_url = make_safe_url(url)

    req = Request(safe_url, headers={'User-Agent': 'Mozilla/5.0'})
    
    webpage = urlopen(req).read()
    html = webpage.decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")


    links = []
    for td in soup.find_all('td'):
        for a in td.find_all('a'):
            title = a.get('title', '')
            if title and link_prefix in title:
                link = link_base + title.replace(' ', '_')
                
                links.append(link)

    if not os.path.isfile(main_page_file):
        with open(main_page_file, 'w+') as f:
            f.write(html)

    if not os.path.isfile(soup_output):
        with open(soup_output, "w+") as f:
            f.write(soup.get_text())

    if not os.path.isfile(links_output):
        with open(links_output, "w+") as f:
            for link in links:
                f.write(link + '\n')
    
    return links

def get_and_save_page(url, filename, directory="./output"):
    if not os.path.exists("./pages"):
        os.makedirs("./pages")
        
    full_path = f"./pages/{filename}"
    
    if "page_does_not_exist" in url:
        return False

    if not os.path.isfile(full_path):
        url = make_safe_url(url)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        html = webpage.decode("utf-8")

        with open(full_path, "w+") as f:
            f.write(html)
            debug_print(f"downloading {full_path}")
            sleep(1)
    else:
        debug_print(f"skip {filename}")
    
    return True


pokemon_files = []


def get_pokemon_page(url):
    filename = ''
    
    match = re.match(filename_regex, url)
    if match:
        pokemon_id = f"{match.group(1)}_{match.group(2)}"
        filename = f"{pokemon_id}.html"
        if filename not in pokemon_files:
            success = get_and_save_page(url, filename, output_directory)
            if success:
                pokemon_files.append(filename)
            else:
                pokemon_files.append("PLACEHOLDER")


ID_SUFFIX = 'id_suffix'
CARD_ID = 'id'
PIO_ID = 'pioId'
ENUM_ID = 'enumId'
NAME = 'name'
NUMBER = 'number'
TYPES = 'types'
SUPER_TYPE = 'superType'
SUB_TYPES = 'subTypes'
RARITY = 'rarity'
EVOLVES_FROM = 'evolvesFrom'
HP = 'hp'
RETREAT_COST = 'retreatCost'
MOVES = 'moves'

CARD_TEXT = 'text'

MOVES = 'moves'
MOVE_COST = 'cost'
MOVE_NAME = 'moveName'
MOVE_TEXT = 'moveText'
MOVE_DAMAGE = 'moveDamage'

ABILITY_NAME = 'abilityName'
ABILITY_TEXT = 'abilityText'

WEAKNESS_TYPE = 'weaknessType'
WEAKNESS_VALUE = 'weaknessValue'

RESISTANCE_TYPE = 'resistanceType'
RESISTANCE_VALUE = 'resistanceValue'


def yaml_header():
    with open(output_yaml, "w+") as f:
        f.write(f"set:\n")
        f.write(f"  id: {set_id}\n")
        f.write(f"  name: {set_name}\n")
        f.write(f"  pioId: {set_pio_id}\n")
        f.write(f"  enumId: {set_enum_id}\n")
        f.write(f"  abbr: {set_abbr}\n")
        f.write(f"cards:\n")

def set_up_links_and_yaml():
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    os.chdir(output_directory)

    if not os.path.isfile(links_output) or os.stat(links_output).st_size == 0:
        links = get_links()
    else:
        with open(links_output) as f:
            links = f.read().splitlines()

    for link in links:
        get_pokemon_page(link)
        
    yaml_header()
    



def remove_extra_spaces(text):
    text = " ".join(text.split())
    if text.endswith(" ."):
        text = text.replace(" .", ".")
    return text.strip()

# Python program to illustrate the intersection 
# of two lists in most simple way 
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def remove_weird_characters(text):
    text = text.replace('é', 'e')
    new_text = text.replace('\xa0', ' ')
    return remove_extra_spaces(re.sub(r'[^A-Za-z0-9\- \']+', '', new_text))
    

def get_card_text(text_node):
    # This will also include the image alt text for energies
    card_lines = text_node.findAll(text=True)

    alt_texts = text_node.findAll('a')
    
    full_text = ''
    insert_alt_text = False

    while(len(card_lines)):
        line = card_lines[0]

        if len(line.strip()) < 1:
            card_lines.pop(0)
            continue
        elif insert_alt_text and alt_texts:
            if '(TCG)' not in alt_texts[0].get('title'):
                typing = alt_texts[0].get('title')
                letter = convert_to_short_type(typing)
                if letter:
                    full_text += f' [{letter}]'
            alt_texts.pop(0)
            insert_alt_text = False
        else:
            full_text += f' {line.strip()}'
            insert_alt_text = True
            card_lines.pop(0)

    return full_text.strip()


def get_name(soup):
    node = get_node_for_text(soup, 'Card name', element='th')
    try:
        if node:
            raw_name = node.find_next('td').get_text()
            name = remove_weird_characters(raw_name)
            return name
        else:
            # Handle Trainers
            raw_name = soup.find('td', {'align': 'center'}).find_next('td', {'align': 'center'}).find_next('big').get_text()
            name = remove_weird_characters(raw_name)
            return name
    except:
        raw_name = soup.find('h1', id='firstHeading').get_text()
        name = remove_weird_characters(raw_name)
        if '(' in name:
            return name.split('(')[0]
        else:
            return name
    

def get_type_node(soup):
    node = soup.find('span', {'lang': 'ja'})
    if node:
        type_node = node.find_next('a')
        return type_node
    return None


def get_typing(type_node):
    try:
        raw_type = remove_extra_spaces(type_node.attrs['title'])
        return convert_to_short_type(raw_type)
    except:
        return None


def get_stage_node(soup):
    valid_stages = [
        'Basic Pokémon (TCG)',
        'Stage 1 Pokémon (TCG)',
        'Stage 2 Pokémon (TCG)',
        'Pokémon VMAX (TCG)'
    ]
    stage_nodes = soup.find_all(attrs={"title":lambda x: x and x in valid_stages})

    if stage_nodes:
        return stage_nodes[0]
    else:
        return None


def get_stage(stage_node):
    return remove_extra_spaces(stage_node.get_text())


def get_evolves_from(soup):
    nodes = soup.find_all('small')
    for node in nodes:
        if 'Evolves from' in node.get_text():
            # target = node.find('a').attrs['title']
            target = node.find('a').get_text()
            
            evolves_from = target.rstrip(' (TCG)')
            return evolves_from
    return None


def get_node_for_text(soup, target_text, element='th'):
    return soup.find(element, text=lambda x: x and remove_extra_spaces(x) == target_text)

def get_hp_node(soup):
    node = get_node_for_text(soup, 'Hit Points')
    if not node:
        node = get_node_for_text(soup, 'HP')
    if not node:
        # Shining Fates
        node = get_node_for_text(soup, 'HP', element='span')
    return node


def get_hp(hp_node):
    if hp_node:
        hp = hp_node.find_next_sibling('td')
        if not hp:
            # Shining Fates
            hp = hp_node.find_next('td')

        if hp:
            return remove_extra_spaces(hp.get_text())
    return None


def get_weakness_node(soup):
    return get_node_for_text(soup, 'weakness', element='small')

def get_weakness(weakness_node):
    if weakness_node:
        weakness = weakness_node.find_next('a').attrs['title']

        if weakness:
            weakness = remove_extra_spaces(weakness)
            return convert_to_short_type(weakness)
    return None



def get_resistance_node(soup):
    return get_node_for_text(soup, 'resistance', element='small')

def get_resistance(resistance_node):
    if resistance_node:
        resistance = resistance_node.find_next('a').attrs['title']

        if resistance:
            resistance = remove_extra_spaces(resistance)
            return convert_to_short_type(resistance)
    return None


def get_retreat_cost_node(soup):
    return get_node_for_text(soup, 'retreat cost', element='small')


def get_retreat_cost(retreat_cost_node):
    cost = 0
    if retreat_cost_node:
        cost = len(retreat_cost_node.parent.find_all('img'))

    return cost



def get_retreat_node(soup):
    return get_node_for_text(soup, 'retreat', element='small')

def get_retreat(retreat_node):
    if retreat_node:
        retreat = retreat_node.find_next('a').attrs['title']

        if retreat:
            return remove_extra_spaces(retreat)
    return None


def get_rarity(soup):
    rarities = {
        'RRR': 'Ultra Rare',
        'C': 'Common',
        'U': 'Uncommon',
        'RR': 'Ultra Rare',
        'R': 'Rare Holo',
        'SR': 'Secret Rare',
        'A': 'Rare Holo'
    }
    try:
        node = get_node_for_text(soup, 'Japanese rarity', 'b')
        if not node:
            # TODO: Make this search for case insensitive
            node = get_node_for_text(soup, 'Japanese Rarity', 'b')
        if not node:
            node = get_node_for_text(soup, 'Rarity', 'b')
        rarity_node = node.find_next('a')
        rarity = rarity_node.attrs['title']
        if not rarities.get(rarity):
            return rarity
        else:
            return rarities[rarity]
    except Exception as e:
        return 'PLACEHOLDER'



def get_card_text_node(soup):
    return soup.find(id="Card_text")

def get_ability_node(soup):
    sibling = get_card_text_node(soup).find_next("table")
    ability_node = sibling.find_next(title="Ability")
    if not ability_node:
        return ability_node

    ability_node_text = ability_node.parent.parent.get_text()
    
    if 'Trivia' in ability_node_text and 'Origin' in ability_node_text:
        return None
    
    return ability_node
    

def get_ability_name_node(ability_node):
    if ability_node:
        ability_name_node = ability_node.find_next('span', {'class': 'explain'})
        return ability_name_node

def get_ability_name(ability_name_node):
    if ability_name_node:
        node = ability_name_node.parent.parent.parent
        text = node.get_text()
        ability_name = remove_weird_characters(text)
        return ability_name

def get_ability_text_node(ability_name_node):
    if ability_name_node:
        return ability_name_node.find_next('table', {'style': 'padding: 3px; background:#FFF;'})

def get_ability_text(ability_text_node):
    # Yaml generator does not accept double quotes
    if ability_text_node:
        ability_text = get_card_text(ability_text_node)

        raw_text = remove_extra_spaces(ability_text)
        return raw_text.replace('"', "'")

def get_attack_nodes(card_text_node=None, ability_node=None):
    attack_nodes = []
    
    skip_first = False

    if ability_node:    
        main_node = ability_node
        skip_first = True
    else:
        main_node = card_text_node
    
    if main_node:
        count = 0
        node = main_node.find_next('span', {'lang': 'ja'})
        first_node = node
        while node and (first_node.get_text() != node.get_text() or count == 0):
            if skip_first and count == 0:
                pass
            else:
                attack_nodes.append(node)
            node = node.find_next('span', {'lang': 'ja'})
            count += 1

    return attack_nodes


def find_next_attack_node(current_node):
    return current_node.find_next('table', {
        'width': '100%', 
        'cellspacing': '0',
        'style': 'background: transparent;'
    })


def get_attacks(attack_nodes):
    attacks = []

    for attack_node in attack_nodes:
        attack = {}
        node = attack_node.parent.parent.parent

        attack_name_and_damage = remove_extra_spaces(re.sub(r'[^A-Za-z0-9 \-\'×\+\-]+', '', node.get_text()))
        attack_name_and_damage.replace('×', 'x')
        attack_damage = attack_name_and_damage.rsplit(" ", 1)
        if attack_damage[-1][:-1].isdigit():
            attack[MOVE_DAMAGE] = attack_damage[-1]
            attack[MOVE_NAME] = attack_damage[0]
        else:
            attack[MOVE_NAME] = attack_name_and_damage
        

        move_cost = get_attack_cost(attack_node)
        if len(move_cost):
            attack[MOVE_COST] = move_cost

        attack_description_text = get_attack_description(attack_node)
        if attack_description_text:
            attack[MOVE_TEXT] = attack_description_text

        attacks.append(attack)
    
    return attacks
    

def convert_to_short_type(long_type):
    switcher = {
        'Fighting': 'F',
        'Lightning': 'L',
        'Water': 'W',
        'Colorless': 'C',
        'Fire': 'R',
        'Grass': 'G',
        'Psychic': 'P',
        'Metal': 'M',
        'Darkness': 'D',
        'Fairy': 'Y',
        'Dragon': 'N'
    }
    return switcher.get(long_type, '')


def get_attack_cost(attack_node):
    move_cost = []
    energy_costs = attack_node.parent.parent.parent.find_all('a')

    for cost in energy_costs:
        energy_type = cost.get('title')
        short_energy_type = convert_to_short_type(energy_type)
        move_cost.append(short_energy_type)

    return move_cost


def get_attack_description(attack_node):
    # Check if there is description text for attack
    next_attack_node = find_next_attack_node(attack_node)
    attack_description_node = next_attack_node.find_next("td")

    attack_description_attrs = {
        'class': ['roundy'],
        'colspan': '3',
        'style': 'padding: 3px; background:#FFF;'
    }

    attack_description_text = ''

    if attack_description_node.attrs == attack_description_attrs:
        text = get_card_text(attack_description_node)
        attack_description_text = remove_extra_spaces(text)
        
    return attack_description_text



def save_super_sub_types(soup, data):
    soup = soup.find(id='Card_text')
    if soup.find_previous('a', {
        'title': 'Stage 1 Pokémon (TCG)'
    }):
        data[SUB_TYPES].extend(['EVOLUTION', 'STAGE1'])
        data[SUPER_TYPE] = 'POKEMON'
    elif soup.find_previous('a', {
        'title': 'Stage 2 Pokémon (TCG)'
    }):
        data[SUB_TYPES].extend(['EVOLUTION', 'STAGE2'])
        data[SUPER_TYPE] = 'POKEMON'
    elif soup.find_previous('a', {
        'title': 'Pokémon VMAX (TCG)'
    }):
        data[SUB_TYPES].extend(['EVOLUTION', 'VMAX'])
        data[SUPER_TYPE] = 'POKEMON'
    elif soup.find_previous('a', {
        'title': 'Pokémon V (TCG)'
    }):
        data[SUB_TYPES].extend(['BASIC', 'POKEMON_V'])
        data[SUPER_TYPE] = 'POKEMON'
    elif soup.find_previous('a', {
        'title': 'Stadium card (TCG)'
    }):
        data[SUB_TYPES].append('STADIUM')
        data[SUPER_TYPE] = 'TRAINER'
    elif soup.find_previous('a', {
        'title': 'Pokémon Tool card (TCG)'
    }):
        data[SUB_TYPES].append('POKEMON_TOOL')
        data[SUB_TYPES].append('ITEM')
        data[SUPER_TYPE] = 'TRAINER'
    elif soup.find_previous('a', {
        'title': 'Item card (TCG)'
    }):
        data[SUB_TYPES].append('ITEM')
        data[SUPER_TYPE] = 'TRAINER'
    elif soup.find_previous('a', {
        'title': 'Supporter card (TCG)'
    }):
        data[SUB_TYPES].append('SUPPORTER')
        data[SUPER_TYPE] = 'TRAINER'
    elif soup.find_previous('a', {
        'title': 'Basic Pokémon (TCG)'
    }):
        data[SUB_TYPES].extend(['BASIC'])
        data[SUPER_TYPE] = 'POKEMON'
    elif soup.find_previous('a', {
        'title': 'Special Energy card (TCG)'
    }):
        # TODO: Handle case for normal energies
        data[SUB_TYPES].extend(['SPECIAL_ENERGY'])
        data[SUPER_TYPE] = 'ENERGY'

    return data


def convert_to_enum_id(name, id):
    name = name.upper().strip()
    name_id = name + '_' + str(id)
    name_id = name_id.replace(' ', '_')
    name_id = name_id.replace('.', '')
    name_id = name_id.replace('’', '_')
    name_id = name_id.replace("'", '_')
    name_id = name_id.replace("-", '_')
    

    return name_id

def create_placeholder_data():
    data = {}

    PLACEHOLDER = "PLACEHOLDER"

    data[ID_SUFFIX] = PLACEHOLDER
    data[NAME] = PLACEHOLDER
    data[TYPES] = PLACEHOLDER
    data[HP] = PLACEHOLDER
    data[SUPER_TYPE] = PLACEHOLDER
    data[SUB_TYPES] = [PLACEHOLDER]
    data[EVOLVES_FROM] = PLACEHOLDER
    data[WEAKNESS_TYPE] = PLACEHOLDER
    data[RESISTANCE_TYPE] = PLACEHOLDER
    data[RETREAT_COST] = PLACEHOLDER
    data[RARITY] = PLACEHOLDER
    data[ABILITY_NAME] = PLACEHOLDER        
    data[ABILITY_TEXT] = PLACEHOLDER
    
    data[MOVES] = [{
        MOVE_NAME: PLACEHOLDER,
        MOVE_DAMAGE: 0,
        MOVE_TEXT: PLACEHOLDER,
        MOVE_COST: "C"
    }]
    
    data[CARD_TEXT] = PLACEHOLDER

    return data


# Prevent reprints within in the same set
added_copies = []

def is_shiny_star_v_reprint(soup):
    title = soup.find('title').get_text()
    skip_card = False
    if title in added_copies:
        skip_card = True
    elif "Shiny Star V" in title:
        skip_card = False
    else:
        skip_card = True

    added_copies.append(title)
    return skip_card

def parse_html_for_pokemon_data(pokemon_url):

    data = {
        SUB_TYPES: []
    }

    # If page doesn't have any data, generate dummy data
    if "PLACEHOLDER" in url:
        return create_placeholder_data()

    with open(pokemon_url) as fp:
        soup = BeautifulSoup(fp, "html.parser")

        data[ID_SUFFIX] = pokemon_url.rstrip(".html").split("_")[-1]

        if shiny_star_v and is_shiny_star_v_reprint(soup):
            # skip if reprint
            return None

        # NAME
        # name_node = get_name_node(soup)
        name = get_name(soup)
        data[NAME] = remove_extra_spaces(name)
        debug_print(data[NAME])


        # TYPE
        type_node = get_type_node(soup)
        if type_node:
            typing = get_typing(type_node)
            if typing:
                data[TYPES] = typing

                debug_print(data[TYPES])

        # HP
        hp_node = get_hp_node(soup)
        if hp_node:
            hp = get_hp(hp_node)
            data[HP] = hp
            debug_print(data[HP])

        # # STAGE
        # stage_node = get_stage_node(soup)
        # if stage_node:
        #     stage = get_stage(stage_node)
        #     data[SUB_TYPES].append(stage)
        #     debug_print(data[SUB_TYPES])

        # SUPER TYPE
        data = save_super_sub_types(soup, data)

        debug_print(data[SUPER_TYPE])
        debug_print(data[SUB_TYPES])

        # EVOLVES FROM
        evolution_types = [
            "STAGE1",
            "STAGE2",
            "VMAX"
        ]
        if len(set(data[SUB_TYPES]).intersection(evolution_types)) > 0:
            evolves_from = get_evolves_from(soup)
            if evolves_from:
                data[EVOLVES_FROM] = evolves_from
                debug_print(data[EVOLVES_FROM])


        # WEAKNESS
        weakness_node = get_weakness_node(soup)
        if weakness_node:
            weakness = get_weakness(weakness_node)
            if weakness:
                data[WEAKNESS_TYPE] = weakness
                debug_print(data[WEAKNESS_TYPE])

        # RESISTANCE
        resistance_node = get_resistance_node(soup)
        if resistance_node:
            resistance = get_resistance(resistance_node)
            if resistance:
                data[RESISTANCE_TYPE] = resistance
                debug_print(data[RESISTANCE_TYPE])
        
         # RETREAT COST
        retreat_cost_node = get_retreat_cost_node(soup)
        if retreat_cost_node:
            retreat_cost = get_retreat_cost(retreat_cost_node)
            data[RETREAT_COST] = retreat_cost
            debug_print(data[RETREAT_COST])


        # RARITY
        rarity = get_rarity(soup)
        data[RARITY] = rarity
        debug_print(data[RARITY])

        # ROOT Card Text 
        card_text_node = get_card_text_node(soup)

        # ABILITY
        ability_node = get_ability_node(soup)
        if ability_node:
            ability_name_node = get_ability_name_node(ability_node)
            ability_name = get_ability_name(ability_name_node)
            if ability_name:
                data[ABILITY_NAME] = ability_name
                debug_print(data[ABILITY_NAME])

            # ABILITY TEXT
            ability_text_node = get_ability_text_node(ability_name_node)
            ability_text = get_ability_text(ability_text_node)
            if ability_text:
                data[ABILITY_TEXT] = ability_text
                debug_print(data[ABILITY_TEXT])
        


        # ATTACKS
        if ability_node:
            attack_nodes = get_attack_nodes(ability_node=ability_node)
        else:
            attack_nodes = get_attack_nodes(card_text_node=card_text_node)

        if attack_nodes:
            attacks = get_attacks(attack_nodes)
            data[MOVES] = attacks

            for attack in data[MOVES]:
                if attack.get(MOVE_NAME):
                    debug_print(attack[MOVE_NAME])  
                if attack.get(MOVE_DAMAGE):
                    debug_print(attack[MOVE_DAMAGE])
                if attack.get(MOVE_TEXT):
                    debug_print(attack[MOVE_TEXT])
                if attack.get(MOVE_COST):
                    debug_print(attack[MOVE_COST])
                debug_print("\n")
            
              

        # TRAINER CARD TEXT
        swsh_print = "Sword & Shield print"
        swsh_print_node = get_node_for_text(soup, 'Sword & Shield print', element='th')

        if swsh_print_node:
            card_text_nodes = []
            max_loops = 4
            text_node = swsh_print_node

            # This is to make sure the text we get actually has content
            while (max_loops != 0 and len(text_node) < 25):
                text_node = text_node.find_next('table', {
                    'class': 'roundy',
                    'width': '100%',
                    'style': lambda x: x and x.startswith("background:#FFFFFF; border: 2px solid")
                })
                if len(text_node.get_text()) > 25:
                    break
                max_loops -= 1

            card_text_nodes.append(text_node)
        else:
            card_text_nodes = soup.find_all('table', {
                'class': 'roundy',
                'width': '100%',
                'style': lambda x: x and x.startswith("background:#FFFFFF; border: 2px solid")
            })
            if not len(card_text_nodes):
                card_text_nodes = soup.find_all('table', {
                'class': 'roundy',
                'width': '100%',
                'style': lambda x: x and x.startswith("background:#FFF; border: 2px solid")
            })
        
        if len(card_text_nodes):
            try:
                card_text_node = card_text_nodes[1]
            except:
                card_text_node = card_text_nodes[0]
            raw_card_text = remove_extra_spaces(card_text_node.get_text())
            card_text = raw_card_text.replace('"', "'")
            data[CARD_TEXT] = card_text
            debug_print(data[CARD_TEXT])
        

        return data


def write_out(data):
    with open(output_yaml, "a") as f:
        id_suffix = data[ID_SUFFIX]

        enum_id = convert_to_enum_id(data[NAME], id_suffix)

        f.write(f"- id: {set_id}-{id_suffix}\n")
        f.write(f"  pioId: {set_pio_id}-{id_suffix}\n")
        f.write(f"  enumId: {enum_id}\n")
        f.write(f"  name: {data[NAME]}\n")
        f.write(f"  number: '{id_suffix}'\n")

        if data.get(TYPES):
            f.write(f"  types: [{data[TYPES]}]\n")
            
        f.write(f"  superType: {data[SUPER_TYPE]}\n")
        f.write(f"  subTypes: [{', '.join(data[SUB_TYPES])}]\n")

        if data.get(EVOLVES_FROM):
            f.write(f"  evolvesFrom: {data[EVOLVES_FROM]}\n")    

        f.write(f"  rarity: {data[RARITY]}\n")

        if data.get(HP):
            f.write(f"  hp: {data[HP]}\n")
        if data.get(RETREAT_COST) is not None:
            f.write(f"  retreatCost: {data[RETREAT_COST]}\n")
        if data.get(ABILITY_NAME):
            f.write(f"  abilities:\n")
            f.write(f"  - type: Ability\n")
            f.write(f"    name: {data[ABILITY_NAME]}\n")
            f.write(f"    text: {data[ABILITY_TEXT]}\n")

        if data.get(MOVES):
            f.write(f"  moves:\n")
            
            for move in data[MOVES]:
                f.write(f"  - cost: [{', '.join(move[MOVE_COST])}]\n")
                f.write(f"    name: {move[MOVE_NAME]}\n")
                if move.get(MOVE_DAMAGE):
                    f.write(f"    damage: '{move[MOVE_DAMAGE]}'\n")
                if move.get(MOVE_TEXT):
                    f.write(f"    text: {move[MOVE_TEXT]}\n")
        
        if data.get(WEAKNESS_TYPE):
            f.write(f"  weaknesses:\n")
            f.write(f"  - type: {data[WEAKNESS_TYPE]}\n")
            f.write(f"    value: x2\n")
        
        if data.get(RESISTANCE_TYPE):
            f.write(f"  resistances:\n")
            f.write(f"  - type: {data[RESISTANCE_TYPE]}\n")
            f.write(f"    value: '-30'\n")

        if data.get(CARD_TEXT):
            f.write(f"  text: [{data[CARD_TEXT]}]\n")



def main():
    set_directory_to_current_script_location()
    set_up_links_and_yaml()


    count = 1
    SV_reset = False
    for url in pokemon_files:
        full_url = f"./pages/{url}"
        data = parse_html_for_pokemon_data(full_url)
        if data:
            write_out(data)
            
            if "SV" in url and not SV_reset:
                count = 1
                SV_reset = True
            if (str(count) not in full_url):
                raise Exception(f"ID MISMATCH between {count} and {full_url}")
            count += 1

main()
