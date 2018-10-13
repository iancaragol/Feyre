import random

class BookOfTor():
    def __init__(self):
        #If you are wondering why these are typed so poorly it is so discord will like the formatting
        self.horoscopeDict = {1:'''
                        **Arcano the Mage**
      The path of magical tasks and arcane accomplishment. Arcano represents a road of wonder, mysteries, and arcane challenges. He blesses his kindred with magical aptitude in the hopes that they will be better prepared to combat or work with forces beyond the logics of physics and reality.

**Birthright:** +1 to all spell DCs
**Horoscope Skills:**
          -Craft (Magic Items)
          -Knowledge (Arcana)
          -Knowledge (Planes)
          -Linguistics
          -Spellcraft
          -Use Magic Device''', 
                      2:'''**Kraka the Warrior**
    Kraka is the strong arm in your future, either there to help force the path you choose through physical challenges, or to help you beat down the opposition from trying times. He represents a life full of physical obstructions, tough opposition, and even glorious passion.

**Birthright:** +1 on Attack Rolls
**Horoscope Skills:**
   -Climb
   -Craft All
   -Know (Local)
   -Know (Nobles)
   -Intimidate
   -Swim''',
                      3:'''**Vicet the Knave**
    A road of trickery, manipulation, choices, devices, and fun excitement await those who are born in the baseur of Vicet. Vicet foretells a path that requires social adaption, tests quick wits, and hides many adventurous secrets in store for his children.

**Birthright:** +1 on Reflex rolls
**Horoscope Skills:**
   -Acrobatics
   -Bluff
   -Diplomacy
   -Disable Device
   -Disguise
   -Escape Artist
   -Stealth''', 
                      4:'''**Levoi the Warlock**
   For those born to Levoi, life is a cascade of duality, and a path that is represented as two opposing forces which must be balanced to both progress and stay in positive light. Those who fall under Levoi’s baseur find their choices to be detrimental in the shaping of balance between opposition, and will also be faced with things that require compensation, compromise, and equal attention in order to function.

**Birthright:** +1 on Damage Rolls
**Horoscope Skills:**
   -Climb
   -Intimidate
   -Ride
   -Spellcraft
   -Swim
   -Use Magic Device''',
   5:'''**Horos the Guardian**
    Horos is the staunch birth baseur that stands to represent its children’s forecomming days of both reliance, and the reliance of others placed on themselves. Their life’s path is foretold to be riddled with loyalty, social groups, allies, united opposition, and the need for collaboration to protect the valued.

**Birthright:** +1 inherit bonus to AC
**Horoscope Skills:**
   -Craft (All)
   -Diplomacy
   -Intimidate
   -Sense Motive
   -Profession (All)''',
  6:'''**Claiva the Healer**
   The healer is a baseur who lays out a path that nurtures her children, and provides cures to issues that would otherwise seem irreparable. Those under her jurisdiction find their lives to be more subtle on a personal level than the others, even if mass issues exist which seem to affect all. All things that are, and are to come, may be resolved with action backed by care and intent.

**Birthright:** +1 point when using positive energy, healing, and heal checks
**Horoscope Skills:**
   -Appraise
   -Craft
   -Know (Religion)
   -Heal
   -Survival''', 
                      7:'''**Yameo the Survivor**
    He is the remainder, the ambitious, the tenacious, and the unyielding. Yameo is the baseur of lives full of trials both good and bad, that will forever both test and fortify his children’s resolve and force of will. Those who fail will spiral beneath the waves of Tor, and those who hold out will live to become only the most weathered and wise beings of immoveable force, despite even the harshest of conditions.

**Birthright:** +5 on rolls to stabilize
**Horoscope Skills:**
   -Acrobatics
   -Escape Artist
   -Fly
   -Handle Animal
   -Know (Nature)
   -Ride
   -Survival''',
                     8:'''**Hilferd the Savant**
    The future in store for a child of Hilferd involves the mysteries of the universe, intricate puzzles of intellect, and situations the require advanced intrigue and talent to solve. Hilferd is the sign of the secret, the forbidden, and the exclusive which hides within the very inner workings of Tor. His children face these anomalies in life, and can even find logical motives behind encounters in their personal lives.

**Birthright:** Skill Focus as a Bonus Feat
**Horoscope Skills:**
   -Craft (All)
   -Know (All)
   -Perform (All)
   -Profession (All)''', 
   9:'''**Gordant the Rationer**
   Lord of the many when there is few, Gordant shows forth a path in which careful management and playing the right cards at the right time can take his children the farthest in life. Those born in Gordant’s baseur face a daily allotment of measurement, and careful calculations when making decisions.

**Birthright:** 150% Standard Carry Weight
**Horoscope Skills:**
   -Appraise
   -Craft (All)
   -Diplomacy
   -Perception
   -Sense Motive''',
  10: '''**Voyeus the Voyager**
   Voyeus is the path of paths and the birthsign that foretells a life adventure, exploration, and new discoveries that can shape his children’s future. Whether an emotional journey, or physical trek, those born in the baseur of Voyeus find themselves on the go, and their life forever changing.

**Birthright:** +5 feet to base movement speed
**Horoscope Skills:**
   -Climb
   -Fly
   -Know (Dungeon)
   -Know (Geography)
   -Know (Planes)
   -Perception
   -Ride
   -Swim'''
                    }
        self.zodiacDict = {
            1:'''**Aedon of the Panoviraptor**
+1 Dex
+1 Cha
+1 Reflex''',
2:'''**Aedon of the Cauteropse**
+1 Str
+1 Int
+1 Fortitude''', 3:'''**Aedon of the Admortum**
+1 Str
+1 Wis
+1 Will''',
4:'''**Aedon of the Dunkle**
+1 Str
+1 Wis
+1 Reflex''',
5:'''**Aedon of the Varrien**
+1 Con
+1 Wis
+1 Fortitude''',
6:'''**Aedon of the Scythin**
+1 Dex
+1 Int
+1 Reflex''',
7:'''**Aedon of the Raokai**
+1 Str
+1 Cha
+1 Fortitude''',
8: '''**Aedon of the Sheek**
+1 Dex
+1 Int
+1 Fortitude
''',
9:'''**Aedon of the Phaedon**
+1 Con
+1 Int
+1 Will''',
10:'''**Aedon of the Stygian**
+1 Con
+1 Cha
+1 Reflex''',
11:'''**Aedon of the Guildian**
+1 Con
+1 Cha
+1 Will''',
12:'''**Aedon of the Quava**
+1 Dex
+1 Wis
+1 Wil'''}

        self.classDict = {
            1: "Selenite", 2: "Blackguard", 3:"Zealot", 4:"Blehhing",5:"Conniver",6:"Clandestinian",7:"Knight",8:"Gourmet",9:"Seraph",10:"Catalyst",
            11:"Anathemist",12:"Mistral",13:"Synergist",14:"Wayward",15:"Maven",16:"Lumenite",17: "Syntheticist",18:"Attunist",19:"Euphorist",20:"Caller"
                }

        self.raceDict = {
            1: "Raevian", 2:"Coenai", 3:"Raigo", 4:"Qhajiratta", 5:"Khibian", 6:"Thargoth", 7:"Thrixen", 8:"Jytselten", 9:"Juema",
           10:"Gargan", 11:"Euphasian", 12:"Voiren", 13:"Phon", 14:"Scovian", 15:"Averyn", 16:"Pegalian", 17:"Tael", 18:"Vurthean", 19:"Nebilian",
           20:"Tryptan", 21:"Nazkin", 22:"Gunthian", 23:"Galovian", 24:"Fleman"
                }
        
    def horo(self):
        roll = random.randint(1, 10)
        return str(self.horoscopeDict[roll])

    def zodiac(self):
        roll = random.randint(1, 12)
        return str(self.zodiacDict[roll])

    def ranchar(self):
        cclass = self.classDict[random.randint(1, 20)]
        race = self.raceDict[random.randint(1, 24)]
        return str(f"You should play a {race} {cclass}!")

    def styles(self):
        styleString = '''**Minimalist**
Simple, clean, effective. There is no need for excessive displays.
 
**Tactical**
Coordinated and well thought-out. One domino will eliminate the rest if they are positioned correctly.
 
**Lucky**
Coincidental and humorous. Nobody knows how you've lasted this long.
 
**Brutal**
Blood and gore. Never before has your party seen a bandit wear his spleen as a Clamding mask.
 
**Dirty**
Cheap and far from honorable, but ensures your victory. There are no rules in war.
 
**Practical**
Killing is a means to an end, so why not do what's tried and true. It only makes sense.'''
        return styleString
