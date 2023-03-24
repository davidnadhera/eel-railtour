class HranaTrasy:
    def __init__(self, odjezd, prijezd, premie_c, premie_k, premie_p, premie_d, premie_u, presun=None, hrana=None, spanek=None):
        self.hrana = hrana
        self.presun = presun
        self.spanek = spanek
        self.odjezd = odjezd
        self.prijezd = prijezd
        self.premie_c = premie_c
        self.premie_k = premie_k
        self.premie_p = premie_p
        self.premie_d = premie_d
        self.premie_u = premie_u

    def to_dict(self):
        return {
            'hrana': self.hrana.id,
            'presun_od': self.presun.od_id,
            'presun_do': self.presun.do_id,
            'spanek': self.spanek,
            'premie_c': self.premie_c,
            'premie_d': self.premie_d,
            'premie_k': self.premie_k,
            'premie_p': self.premie_p,
            'premie_u': self.premie_u,
            'odjezd': self.odjezd,
            'prijezd': self.prijezd
        }

    def vypis_spoje(self):
        if self.spanek:
            print(f'Spánek od {self.odjezd} do {self.prijezd}')
        elif self.presun:
            print(self.presun)
        else:
            for spoj in self.hrana.spoje:
                if spoj.presun:
                    print(spoj.presun)
                else:
                    print(spoj.spoj)
