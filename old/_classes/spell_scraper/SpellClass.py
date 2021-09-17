class SpellClass():
    def __init__(self, name = None, level = None, casting_time = None,
                 range = None, 
                 components = None, duration = None, school = None, saving_throw = None, 
                 description = None):

        self.name = name
        self.level = level
        self.casting_time = casting_time
        self.range = range
        self.components = components
        self.duration = duration
        self.school = school
        self.saving_throw = saving_throw
        self.description = description

    def to_discord_string(self):
        to_Str = f'''***{self.name}***
**Level: **{self.level}
**Casting Time: **{self.casting_time}
**Range: **{self.range}
**Components: **{self.components}
**Duration: **{self.duration}
**School: **{self.school}
**Attack/Save: **{self.saving_throw}

{self.description}'''

        to_Str = to_Str.encode('ascii', 'ignore')

        return to_Str