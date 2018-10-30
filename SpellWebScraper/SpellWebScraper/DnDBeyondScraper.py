from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import SpellClass
import os

class DnDBeyondWebScraper():
    def __init__(self):
        self.spell_list = []
        self.spell_url_list = []
        self.spell_excpetion_url_list = []

    def simple_get(self, url):
        try:
            with closing(get(url, stream=True)) as resp:
                if self.is_good_response(resp):
                    return resp.content
                else:
                    return None
        except RequestException as e:
            self.log_error('Error during requests to {0} : {1}'.format(url, str(e)))

    def is_good_response(self, resp):
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200 and content_type is not None and content_type.find('html') > -1)

    def log_error(self, e):
        print(e)
    
    def scrape_spell(self, soup):
        print("scrape_spell")
        return

    def scrape_spell_list(self, url):
        soup = BeautifulSoup(self.simple_get(url), 'html.parser')
        spell_contents = soup.find_all('div', attrs = {'class':'row spell-name'})

        for c in spell_contents:
            spell_url = c.find('a')
            self.spell_url_list.append('https://www.dndbeyond.com'+ spell_url['href'])
            #print(spell_url['href'])

        
        for i in range(2, 25):
            page_number = f"?page={str(i)}"
            newUrl = url + page_number
            soup = BeautifulSoup(self.simple_get(newUrl), 'html.parser')
            spell_contents = soup.find_all('div', attrs = {'class':'row spell-name'})

            for c in spell_contents:
                spell_url = c.find('a')
                self.spell_url_list.append('https://www.dndbeyond.com'+ spell_url['href'])

        print("Scraped spell URLs")

    def write_spells_to_file(self):
        pyDir = os.path.dirname(__file__)
        relPath = "_data\\_spells\\"
        absRelPath = os.path.join(pyDir, relPath)

        for sp in self.spell_list:
            fileName = os.path.join(absRelPath, (sp.name.replace("/","-").replace(" ", "-")+".txt"))
            with open(fileName, "w") as text_file:
                text_file.write(sp.to_discord_string().decode('ascii',errors='ignore'))
                #char map error on raise dead

    def create_spell_from_html(self, url):
        try:
            soup = BeautifulSoup(self.simple_get(url), 'html.parser')

            spell_name = soup.find('div', attrs = {'class':'page-heading'}).find('h1', attrs = {'class':'page-title'}).text.strip()
            spell_level = soup.find('div', attrs = {'class':'ddb-statblock-item ddb-statblock-item-level'}).find('div', attrs = {'class':'ddb-statblock-item-value'}).text.strip()
            spell_casting_time = soup.find('div', attrs = {'class':'ddb-statblock-item ddb-statblock-item-casting-time'}).find('div', attrs = {'class':'ddb-statblock-item-value'}).text.strip()
            spell_range = soup.find('div', attrs = {'class':'ddb-statblock-item ddb-statblock-item-range-area'}).find('div', attrs = {'class':'ddb-statblock-item-value'}).text.strip()
            spell_components = soup.find('div', attrs = {'class':'ddb-statblock-item ddb-statblock-item-components'}).find('div', attrs = {'class':'ddb-statblock-item-value'}).find('span', attrs = {'class':'component-asterisks'}).text.strip()
            spell_duration = soup.find('div', attrs = {'class':'ddb-statblock-item ddb-statblock-item-duration'}).find('div', attrs = {'class':'ddb-statblock-item-value'}).text.strip()
            spell_school = soup.find('div', attrs = {'class':'ddb-statblock-item ddb-statblock-item-school'}).find('div', attrs = {'class':'ddb-statblock-item-value'}).text.strip()
            spell_attack_save = soup.find('div', attrs = {'class':'ddb-statblock-item ddb-statblock-item-attack-save'}).find('div', attrs = {'class':'ddb-statblock-item-value'}).text.strip()
            spell_damage_effect = soup.find('div', attrs = {'class':'ddb-statblock-item ddb-statblock-item-damage-effect'}).find('div', attrs = {'class':'ddb-statblock-item-value'}).text.strip()

            spell_description = soup.find('div', attrs = {'class':'more-info-content'}).text.strip()

            #Clean strings
            #Some spells need duration to be cleaned
            spell_duration = spell_duration.lstrip()
            spell_duration = ' '.join(spell_duration.split())

            spell_range = spell_range.replace(" ", "")
            sp_r_split = spell_range.split("\n")

            if(len(sp_r_split) == 3):
                spell_range = sp_r_split[0] + " - " + sp_r_split[2]

            print(spell_name)
            #print(spell_level)
            #print(spell_casting_time)
            #print(spell_range)
            #print(spell_components)
            #print(spell_duration)
            #print(spell_school)
            #print(spell_attack_save)
            #print(spell_description)
            #print()

            newSpell = SpellClass.SpellClass(spell_name, spell_level, spell_casting_time,
                                         spell_range, spell_components, spell_duration,
                                         spell_school, spell_attack_save, spell_description)

            self.spell_list.append(newSpell)

        except Exception as e:
            print(f"Exception on: {url}")
            print(e)
            self.spell_excpetion_url_list.append(url)

            

ws = DnDBeyondWebScraper()

#get all cantrips from master spell list
raw_html = ws.simple_get('https://www.dndbeyond.com/spells')
soup = BeautifulSoup(raw_html, 'html.parser')

ws.scrape_spell_list('https://www.dndbeyond.com/spells')
#ws.create_spell_from_html(ws.spell_url_list[0])

for s in ws.spell_url_list:
    ws.create_spell_from_html(s)

ws.write_spells_to_file()

pyDir = os.path.dirname(__file__)
relPath = "_data\\"
absRelPath = os.path.join(pyDir, relPath)
fileName = os.path.join(absRelPath, "failed_spells.txt")

with open(fileName, "w") as text_file:
    for sp in ws.spell_excpetion_url_list:
        text_file.write(sp)


print("\n Done")
