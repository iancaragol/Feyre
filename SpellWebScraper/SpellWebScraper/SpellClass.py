class SpellClass():
    def __init__(self, name = None, type = None, casting_time = None, range = None, target = None, 
                 components = None, duration = None, saving_throw = None, 
                 concentration = None, description = None, higher_levels = None):

        self.name = name
        self.type = type
        self.casting_time = casting_time
        self.range = range
        self.target = target
        self.components = components
        self.duration = duration
        self.saving_throw = saving_throw
        self.concentration = concentration
        self.description = description
        self.higher_levels = higher_levels

    def to_discord_string(self):
        to_Str = f'''***{self.name}***
*{self.type}*
**Casting Time: **{self.casting_time}
**Range: **{self.range}
**Target: **{self.target}
**Components: **{self.components}
**Duration: **{self.duration}
**Saving Throw: **{self.saving_throw}
**Concentration: **{self.concentration}
{self.description}'''

        return to_Str