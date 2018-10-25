from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import SpellClass

class GDnDWebScraper():
    def __init__(self):
        self.spell_dict = {}

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

    def create_spell(self, soup):
        try:
            spell_block = soup.findAll('div', attrs = {'class':'spell-block'})

            if(len(spell_block) == 0):
                return 

            sb_c = spell_block[0].contents[3] #spell_block[0].contents

            spell_name = spell_block[0].find('span').text
            spell_type = spell_block[0].find('em').text

            spell_casting_time = None #spell_block[0].contents[3].contents[4]
            spell_range = None #sb_contents.contents[8]
            spell_target = None #sb_contents.contents[12]
            spell_components = None #sb_contents.contents[16]
            spell_duration = None #sb_contents.contents[20]
            spell_saving_throw = None #sb_contents.contents[24]
            spell_concentration = None #sb_contents.contents[28]
            spell_description = None #sb_contents.contents[30]
            spell_higher_levels = None

            q = 0
            for i in range(0, len(sb_c)):
                if(sb_c.contents[i].string != None):
                    if('Casting time' in sb_c.contents[i].string and sb_c.contents[i].name == 'strong'):
                        i+= 1
                        spell_casting_time = sb_c.contents[i]

                    elif('Range' in sb_c.contents[i].string and sb_c.contents[i].name == 'strong'):
                        i+= 1
                        spell_range = sb_c.contents[i]

                    elif('Target' in sb_c.contents[i].string and sb_c.contents[i].name == 'strong'):
                        i+= 1
                        spell_target = sb_c.contents[i]

                    elif('Components' in sb_c.contents[i].string and sb_c.contents[i].name == 'strong'):
                        i+= 1
                        spell_components = sb_c.contents[i]

                    elif('Duration' in sb_c.contents[i].string and sb_c.contents[i].name == 'strong'):
                        i+= 1
                        spell_Duration = sb_c.contents[i]

                    elif('Saving throw' in sb_c.contents[i].string and sb_c.contents[i].name == 'strong'):
                        i+= 1
                        spell_saving_throw = sb_c.contents[i]

                    elif('Concentration' in sb_c.contents[i].string and sb_c.contents[i].name == 'strong'):
                        i+= 1
                        spell_concentration = sb_c.contents[i]

                    elif('At Higher Levels' in sb_c.contents[i].string and sb_c.contents[i].name == 'strong'):
                        i+= 1
                        spell_higher_levels = sb_c.contents[i]

                    else:
                        i+=1
                    q = i

            if(spell_higher_levels != None):
                if(sb_c.contents[q-4] != '</br>'):
                    spell_description = sb_c.contents[q-4]
                else:
                    spell_description = sb_c.contents[q-5]
            else:
                spell_description = sb_c.contents[q-1]

            print(spell_name)
            return  SpellClass.SpellClass(spell_name, spell_type, spell_casting_time, spell_range, spell_target, 
                          spell_components, spell_duration, spell_saving_throw, 
                          spell_concentration, spell_description)

        except Exception as e:
            print(e)
            return None

    def add_spells_to_dict(self, url_list):
        for url in url_list:
            soup = BeautifulSoup(self.simple_get(url), 'html.parser')
            spell = self.create_spell(soup)

            if(spell != None):
                self.spell_dict[spell.name] = spell

ws = GDnDWebScraper()

#get all cantrips from master spell list
raw_html = ws.simple_get('http://gdnd.wikidot.com/spells')
soup = BeautifulSoup(raw_html, 'html.parser')
spell_contents = soup.findAll('div', attrs = {'id':'page-content'})
cantrip_links = spell_contents[0].contents[11].contents[0].contents[1]
cantrips = []
for c in cantrip_links.find_all('a', href = True):
    cantrips.append('http://gdnd.wikidot.com'+ c['href'])

ws.add_spells_to_dict(cantrips)
print()

for key, spell in ws.spell_dict.items():
    print(spell.to_discord_string())

#print(spell_contents[0].contents[11].contents[0].contents[1].contents[1])
print("\n Done")
