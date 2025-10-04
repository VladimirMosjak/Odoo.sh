from odoo import models, fields, api
from datetime import date

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Firma & stav
    x_validni_kontakt = fields.Boolean(string='Validní kontakt')
    x_pravni_stav = fields.Selection([
        ('aktivni', 'Aktivní'),
        ('insolvence', 'Insolvence'),
        ('likvidace', 'Likvidace'),
    ], string='Právní stav')
    x_platce_dph = fields.Boolean(string='Plátce DPH')
    x_pocet_zamestnancu = fields.Selection([
        ('0_1', '0–1'), ('2_9', '2–9'), ('10_49', '10–49'),
        ('50_249', '50–249'), ('250_plus', '250+'),
    ], string='Počet zaměstnanců')
    x_datum_vzniku = fields.Date(string='Datum vzniku společnosti')
    x_datum_zapisu_or = fields.Date(string='Datum zápisu do OR')
    x_rok_zalozeni = fields.Integer(string='Rok založení', compute='_compute_rok_zalozeni', store=True)

    # Web
    x_web_existuje = fields.Boolean(string='Web existuje')
    x_kvalita_webu = fields.Selection([
        ('nema', 'Nemá'), ('slaby', 'Slabý'), ('prumerny', 'Průměrný'),
        ('dobry', 'Dobrý'), ('vyborny', 'Výborný'),
    ], string='Kvalita webu')

    # Jednatel
    x_jednatel_name = fields.Char(string='Jednatel/CEO')
    x_phone_ceo = fields.Char(string='Telefon (jednatel)')
    x_email_ceo = fields.Char(string='E-mail (jednatel)')
    x_datum_narozeni = fields.Date(string='Datum narození')
    x_vek = fields.Integer(string='Věk', compute='_compute_vek', store=True)
    x_vek_kategorie = fields.Selection([
        ('u25', 'Do 25'), ('26_35', '26–35'),
        ('36_50', '36–50'), ('51_plus', '51+'),
    ], string='Věková kategorie')
    x_statni_prislusnost = fields.Many2one('res.country', string='Státní příslušnost')

    # Ostatní
    x_datova_schranka = fields.Char(string='Datová schránka')
    x_zdroj_kontaktu = fields.Selection([
        ('firmy', 'Firmy.cz'), ('ares', 'ARES'), ('merk', 'MERK'),
        ('web', 'Web'), ('doporuceni', 'Doporučení'),
        ('vlastni', 'Vlastní výzkum'), ('jine', 'Jiné'),
    ], string='Zdroj kontaktu')
    x_odkaz_inzerat = fields.Char(string='Odkaz na inzerát')
    x_pravni_forma = fields.Selection([
        ('sro', 'Společnost s ručením omezeným'),
        ('as', 'Akciová společnost'),
        ('vos', 'Veřejná obchodní společnost'),
        ('ks', 'Komanditní společnost'),
        ('druzstvo', 'Družstvo'),
        ('socialni_druzstvo', 'Sociální družstvo'),
        ('svj', 'Společenství vlastníků jednotek'),
        ('statni_podnik', 'Státní podnik'),
        ('ustav', 'Ústav'),
        ('spolek', 'Spolek'),
        ('pobocny_spolek', 'Pobočný spolek'),
        ('nadace', 'Nadace'),
        ('nadacni_fond', 'Nadační fond'),
        ('cirkev', 'Církevní právnická osoba'),
        ('ops', 'Obecně prospěšná společnost'),
        ('prisp_organizace', 'Příspěvková organizace'),
        ('org_slozka_statu', 'Organizační složka státu'),
        ('uzemni_samosprava', 'Územní samosprávný celek'),
        ('vvi', 'Veřejná výzkumná instituce'),
        ('vvs', 'Veřejná vysoká škola'),
        ('politicka_subjekt', 'Politická strana nebo hnutí'),
        ('odstepny_zavod', 'Odštěpný závod zahraniční osoby'),
        ('evropska_spolecnost', 'Evropská společnost'),
        ('ehzs', 'Evropské hospodářské zájmové sdružení'),
        ('evropske_druzstvo', 'Evropské družstvo'),
        ('fop', 'Fyzická osoba podnikající'),
    ], string='Právní forma')

    @api.depends('x_datum_vzniku')
    def _compute_rok_zalozeni(self):
        for rec in self:
            rec.x_rok_zalozeni = rec.x_datum_vzniku.year if rec.x_datum_vzniku else 0

    @api.depends('x_datum_narozeni')
    def _compute_vek(self):
        for rec in self:
            if rec.x_datum_narozeni:
                t = date.today(); b = rec.x_datum_narozeni
                rec.x_vek = t.year - b.year - ((t.month, t.day) < (b.month, b.day))
            else:
                rec.x_vek = 0
