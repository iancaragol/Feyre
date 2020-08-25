class Character():
    def __init__(self, user_id, character_name, character_id, pp, gp, ep, sp, cp, init_mod = None, selected = False):
        self.user_id = user_id
        self.character_name = character_name[:32] + '...' if len(character_name) > 32 else character_name
        self.character_id = character_id
        self.pp = pp
        self.gp = gp
        self.ep = ep
        self.sp = sp
        self.cp = cp
        self.init_mod = init_mod
        self.selected = selected

    async def coalesce(self):
        total_pp = 0
        total_gp = 0
        total_ep = 0
        total_sp = 0
        total_cp = self.pp*1000 + self.gp*100 + self.ep*50 + self.sp*10 + self.cp
        
        if total_cp > 0:
            s, c = divmod(total_cp, 10)
            total_sp += s
            total_cp = c
        
        if total_sp > 0:
            e, s = divmod(total_sp, 5)
            total_ep += e
            total_sp = s
        
        if total_ep > 0:
            g, e = divmod(total_ep, 2)
            total_gp += g
            total_ep = e
        
        if total_gp > 0:
            p, g = divmod(total_gp, 10)
            total_pp += p
            total_gp = g

        self.pp = total_pp
        self.gp = total_gp
        self.ep = total_ep
        self.sp = total_sp
        self.cp = total_cp
