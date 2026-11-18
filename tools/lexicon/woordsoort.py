#!/usr/bin/env python3
"""Tag every row of woorden.tsv with a part of speech.

Deterministic: rules over the Dutch form and the English gloss, then a curated
override table for the cases the rules get wrong. Writes
woorden-woordsoort.tsv with the same nl values in the same order as the input.

    python3 tools/lexicon/woordsoort.py              # write the tsv
    python3 tools/lexicon/woordsoort.py --dump X     # every row + its reason
    python3 tools/lexicon/woordsoort.py --sample [--seed N]   # the 100-row sample

Labels: noun verb adj adv function interjection name phrase

The lists below are split into two groups:

  * curated lexicons -- VERBS, NOUN_EN, ADJ_EN, ADV_LEXICON, FUNCTION,
    INTERJECTIONS, NAMES -- read by the tagger in that order of confidence;
  * morphology and gloss-shape rules, applied after the lists and before the
    noun default.

Uppercase in `nl` is a signal: the source kept the capitals of a few hundred
entries (`Nederland`, `Poolse`), and a capital that is not a sentence start is a
proper noun, which the game lists and the glosses cannot always tell us.
"""

import csv
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "woorden.tsv")
OUT = os.path.join(HERE, "woorden-woordsoort.tsv")

# --------------------------------------------------------------------------
# Overrides. Key = the exact `nl` value from woorden.tsv.
# --------------------------------------------------------------------------

OVERRIDES = {
    # the source gloss is a paraphrase of a noun (`ontspanning | to start`,
    # `ontslag | to escape`), or the lemma is mistyped (`opbengst`, `misburik`)
    "opengaan": "verb",
    "opbengst": "noun",
    "misburik": "verb",
    "alpien": "adj",
    # ---- closed-class pairs the source splits with a comma ----
    "een, één": "function",
    "hem, ’m": "function",
    "het, ’t": "function",
    "jij, je": "function",
    "wijs, we": "function",
    "wij, we": "function",
    "zij, ze": "function",
    "mij, me": "function",
    "mijn, m’n": "function",
    "mijzelf, mezelf": "function",
    "zijn, z’n": "function",
    "gij, ge": "function",
    "ons": "function",            # a) us b) our
    "zo\u2019n": "function",          # the appendix spells it with a curly apostrophe
    # ---- multiword ----
    "alstublieft alsjeblieft": "interjection",
    "enzovoort, enz": "adv",
    "et cetera, etc": "adv",
    "gedroogde pruim": "noun",
    "vrije worp": "noun",
    "gebruikmaken van": "phrase",
    "verenigen (zich)": "verb",
    "vereningen (zich)": "verb",  # a typo for `verenigen (zich)`, glossed `club`
    "wagen (zich)": "verb",
    "afspelen (zich)": "verb",
    "kost, kosten (noun)": "noun",
    # ---- the gloss is the verb, the lemma is the noun ----
    "ontspanning": "noun",
    "opblazen": "noun",           # gloss: construction
    "opbrengen": "noun",          # gloss: proceeds
    "veroordelen": "noun",        # gloss: conviction
    "uitkeren": "verb",           # gloss is wrong; `uitkering` is the noun
    "opbrengen (verb)": "verb",
    "vermogen (verb)": "verb",
    "kosten (verb)": "verb",
    "ebben": "noun",              # gloss: ebony; `eb` is also a noun
    "vervellen": "verb",          # gloss: molt (noun) but the lemma is the verb
    "kring": "noun",
    "uiting": "noun",
    "vereniging": "noun",
    "ontvangen": "noun",          # gloss: reception -- the source means the noun
    "opbengst": "noun",           # typo of `opbrengst`; the gloss says `to store`
    "ontvangst": "noun",
    "ontvangen (verb)": "verb",
    # ---- likely nouns, glosses that mislead the -en rules ----
    "promoveren": "verb",
    "praten": "verb",
    "hoeven": "verb",
    "weten": "verb",
    "moeten": "verb",
    "kunnen": "verb",
    "zullen": "verb",
    "willen": "verb",
    "mogen": "verb",
    "komen": "verb",
    "geven": "verb",
    "bukken": "verb",
    "lonken": "verb",
    "kripen": "noun",             # gloss: circle; `krijt`-type noun not a verb here
    # ---- adverbs and particles the gloss hides ----
    "niet": "adv",
    "geen": "function",
    "nauwelijks": "adv",
    "vaak": "adv",
    "heel": "adv",
    "nog": "adv",
    "wel": "adv",
    "eens": "adv",
    "al": "adv",
    "aanzien": "noun",            # gloss: respect
    # ---- game-list glosses that describe the word instead of naming it ----
    "limoen": "noun",
    "oostzee": "name",
    "amon": "name",               # Amun, the Egyptian god
    "aanslag": "noun",            # gloss `attack`; the source means the tax bill
    "wanneer": "function",        # gloss `when`
    "naakt": "adj",               # gloss `nude, naked`
    "draak": "noun",              # the mythology list's `dragon` is an animal
    "tegenstander": "noun",
    "oma": "noun",                # `grandma`; the game lists also call it a place
    # ---- game-list glosses that describe the word instead of naming it ----
    "brand": "noun",              # `fire`; the beer brand is not the lemma
    "mekaar": "function",         # `each other` is a reciprocal pronoun
    "he": "interjection",
    "ja": "interjection",
    "pest": "noun",
    "rap": "adj",
    "zijde": "noun",
    # ---- gloss traps: the gloss is a verb or an adverb the lemma is not ----
    "telefoonnummer": "noun",          # gloss `to phone`
    "opbouw": "noun",                 # gloss `to construct`; `opbouwen` is the verb
    "ontslag": "noun",                # gloss `to escape`; `ontslaan` is the verb
    "misburik": "verb",               # typo of `misbruiken`; gloss `to abuse`
    "ernaar": "adv",                 # `to it, at it`: a pronominal adverb, not a verb
    "hieraan": "adv",
    "naartoe": "adv",
    "daarnaast": "adv",
    "tuurlijk": "interjection",
    "jee": "interjection",            # `oh dear, oh no`; the -ee is not -en
    "tier": "noun",                   # `-ier` spelling of `tijger`
    "gaaf": "adj",                    # a) intact b) great
    "vuil": "adj",                    # `dirt`; the adjective is the usual word
    "dankzij": "function",            # a preposition
    "lang": "adj",                    # `long, tall`
    "kil": "adj",                     # `chilly`
    "lager": "adj",                   # `lower`
    "vast": "adj",                    # `fixed`
    "gedurende": "function",
    "geleden": "adv",                 # `ago`; a postposed adverb
    "min": "function",                # `minus`; the -in ending is not a word
    "nagenoeg": "adv",
    "alsof": "function",               # a conjunction
    "vanachter": "function",          # a preposition
    "evenmin": "adv",
    "verliefd": "adj",
    "hip": "adj",                      # `fancy`
    "lunair": "adj",
    # ---- reflexives: pronouns, however the capital sets fail to catch them ----
    "zelf": "function",
    "ikzelf": "function",
    "hijzelf": "function",
    "jijzelf": "function",
    "wijzelf": "function",
    "zijzelf": "function",
    "julliezelf": "function",
    "zichzelf": "function",
    # ---- more gloss traps: a verb gloss on a noun lemma, a noun gloss on a
    # verb lemma, a partitive for a quantity ----
    "ontslaan": "verb",             # gloss `resignation, dismissal`; the noun is `ontslag`
    "sieraden": "noun",            # `jewelry`; a plural-only noun, not an infinitive
    "driekwart": "function",       # a quantity, not a noun
    "anatomie": "noun",
    # ---- an adjective gloss the lemma's shape explains better than the gloss ----
    "ijzer": "noun",                 # `iron`; a consonant and `-en` is a plural
    "kermis": "noun",                # `fair`; the -is is not an ending
    "lusten": "verb",                # `to like`; elsewhere in the list the lemma is the verb
    "voilà": "interjection",
    "hartstikke": "adv",              # `terribly`; an intensifier
    "minstens": "adv",               # `at least`
    "morgenavond": "adv",
    "onterecht": "adj",
    "dicht": "adj",                   # `closed`
    "handig": "adj",                  # `handy`
    "enthousiast": "adj",
    # ---- adverbs the noun path takes for want of a lexicon entry ----
    "kwijt": "adj",                  # `lost`; a predicative adjective
    "buitengewoon": "adj",
    "tegenwoordig": "adj",          # `nowadays`; also the adjective `present-day`
    "eenzijdig": "adj",
    "luidruchtig": "adj",
    "ongewoon": "adj",
    "zeldzaam": "adj",
    "vorig": "adj",
    "binnenkort": "adv",
    "vandoor": "adv",               # `off, away`
}

# --------------------------------------------------------------------------
# Curated closed classes
# --------------------------------------------------------------------------

FUNCTION = set("""
aan achter af als alvorens behalve bij binnen boven buiten circa dan dat de
degene die diegene dit doch door doordat echter en er geen gij haar hij hen het
hun ik in indien jij jou jouw jullie maar mee men met mij mijn mits na naar
naast nadat naargelang naarmate noch of om onder op onze over per plus qua
sedert sinds te tegen tegenover tenzij terwijl tot totdat tussen u uit van
vanaf vanuit versus via volgens voor voorbij want wegens welke welk wie wiens
zodat zoals zonder zo'n deze gene zulke elk elke enig enkele ieder iedere
alle allebei andere anderen elkander elkaar m'n z'n 't 'm 'k je ze me we ge
uw zich zichzelf uzelf mijzelf jezelf hemzelf haarzelf onszelf julliezelf
namens opdat tijdens evenals overheen gedurende van zodra terwijl alhoewel
angezien opdat ofschoon tenware ingeval naarmate
""".split())
# `af`, `mee`, `nu` are adverbs this list also holds (see ADVERB); `toen` is a
# conjunction in `toen ...` but an adverb as a time word, which is how the list
# glosses it (`then`), so it stays out of FUNCTION too.
FUNCTION -= {"af", "mee", "nu", "toen"}

# spelled-out numbers and ordinals: `vijfenveertig`, `driehonderd`, `zevende`
# spelled-out numbers and ordinals: `vijfenveertig`, `driehonderd`, `zevende`
NUMBER_UNIT = ("een|twee|drie|vier|vijf|zes|zeven|acht|negen|der|veer|tach|"
               "twin")
NUMBER_WORD = re.compile(
    r"^("
    r"(" + NUMBER_UNIT + r")?(tien|tig|honderd|duizend)"
    r"|(" + NUMBER_UNIT + r")?en(" + NUMBER_UNIT + r")?(tig|tien)"
    r"|miljoen|miljard"
    r")$")
ORDINAL_WORD = re.compile(
    r"^(eerste|tweede|derde|vierde|vijfde|zesde|zevende|achtste|negende|"
    r"tiende|elfde|twaalfde)$")

# `drieëntwintig`, `tweeëntwintig`: the diaeresis breaks NUMBER_WORD, so the
# numeral test and the `-ig` adjective test both read the folded spelling
DIACRITICS = str.maketrans({"ë": "e", "é": "e", "è": "e", "ê": "e",
                            "ï": "i", "ó": "o", "ö": "o", "á": "a",
                            "à": "a", "ú": "u", "ü": "u", "ç": "c"})


def is_numeral(lower):
    return (lower in NUMERALS or bool(NUMBER_WORD.match(lower))
            or bool(ORDINAL_WORD.match(lower))
            or bool(NUMBER_WORD.match(lower.translate(DIACRITICS))))


DEMONSTRATIVES = set("""
datzelfde dergelijke zulk zodanig sommige bepaalde hierdie hetzelfde dezelfde
datgene gene gindse
""".split())

NUMERALS = set("""
een één twee drie vier vijf zes zeven acht negen tien elf twaalf dertien
veertien vijftien zestien zeventien achttien negentien twintig dertig veertig
vijftig zestig zeventig tachtig negentig honderd duizend miljoen miljard
biljoen nul half anderhalf kwart dozijn driehonderd vijfduizend drieduizend
twaalfhonderd honderden duizenden honderdduizend tienduizend
""".split())
for _t in ("tien", "tig", "honderd"):
    for _p in ("twee", "drie", "vier", "vijf", "zes", "zeven", "acht", "negen"):
        NUMERALS.add(_p + _t)

YES_NO = set("yes no yeah nope".split())

INTERJECTIONS = set("""
ach ah aha amai au bah boe brr foei goh ha haha hallo hee hmmm hoera hoi hola
hoor hup jemig jo joch joh jongens komaan nou och oei oh oké ola ooh pff pfieuw
poe poeh proost sorry tjee tsjonge tjonge tja verdikkeme verdomme wauw welja
welnee welaan zeg hé hè hm hmm enfin allee
""".split())

# adverbs that are not pronominal
ADVERB = set("""
af al anders allicht almaar alsnog altijd alvast amper andersom daar dadelijk
achteren doorheen omheen nadien voren zelden
daarnet daarstraks desalniettemin desnoods desondanks destijds thans toen
doorgaans dus eerder eerst eigenlijk elders erg even eventjes gauw gisteren
gisterenavond grotendeels haast hier hierna hieronder inmiddels integendeel
intussen langzamerhand later liefst louter mee mede meteen meer nabij
natuurlijk nee net nooit nogal nu ooit onderwijl ondertussen onderweg onlangs
opnieuw overigens overmorgen samen sindsdien soms sowieso spoedig straks te
thuis toch toentertijd tussendoor verder volop vooraf vooraan voorheen
voorlopig vandaag vanavond vanmorgen vanmiddag vannacht vanochtend vast veelal
verre veruit vlot vooruit vroeger waarschijnlijk weleens weinig weliswaar
zowaar zozeer bovendien beneden achterna achteraf achteraan achterin achterop
achteruit dichtbij ginds ginder overal ergens nergens heen niet niets jawel
nimmer immer nimmermeer voorts genoeg dusdanig weer alweer daarentegen ondanks
toe ook zelfs slechts alleen enkel uitsluitend links rechts bovenop bovenin
onderin middenin immanent inzake gedurende dusver bijgevolg daarentegen
bijvoorbeeld nogmaals nauwelijks nog wel eens heel bijna half zo zeer nogal
eens even vrij tamelijk behoorlijk redelijk nogal gauw dadelijk dikwijls vaak
momenteel reeds terug tevoren uitermate uiterst vandaan vanzelf vervolgens
volstrekt vooral voorgoed voorop voortaan vooraleer vrijwel wederom weeral
wekelijks zodoende zowat zowel zeven zeer tegemoet terzijde opzij overeind
omhoog omlaag omstreeks omtrent ongeacht ongetwijfeld ongeveer nochtans nader
liever meestal minder minst meerder meest steeds steevast stilaan trouwens
tevens hardop halverwege ineens opeens oftewel ofwel ofschoon vermits vandaar
vanop zover toch tenminste kortom elders indertijd enigszins hoger heter
hoeverre middels voorwaarts achterwaarts zijwaarts opwaarts neerwaarts
zolang zoverre hoegenaamd omzeggens inderdaad alleszins dienaangaande
""".split())

MONTHS = set("""
januari februari maart april mei juni juli augustus september oktober november
december
""".split())

# prepositions that close pronominal adverbs -- the bases of Dutch, never full
# prepositions: `door + op` is not a pronominal adverb
PRONOUN_BASES = set("""
af bij binnen boven buiten door heen in langs mee met na onder op over toe
uit van voor weg zonder tussen tegen langs om langs uit
""".split())

# --------------------------------------------------------------------------
# Curated lexicons (keyed lowercase)
# --------------------------------------------------------------------------

# English noun glosses that are also English adjectives; when the lemma's shape
# is a noun (a plural `-en` with a consonant stem), this set decides
NOUN_ADJ_GLOSS = set("""
iron fair stone copper coral opal legion bush alpine marine
""".split())

# ordinary adverbs with no pronominal or suffix clue
ADV_LEXICON = set("""
graag vanwaar telkens vooralsnog
""".split())

# English glosses that are adverbs or function words, for the `-en` noun rule
ADV_EN = set("""
ago always almost already also around away back before behind below besides
better down enough even ever far fast forward forward further hardly here
home instead just later less maybe more much never often only out over again
perhaps quite rather really seldom since soon still then there therefore
together twice up very well yet
""".split())
PRONOUN_EN = set("""
everyone everybody everything someone somebody something anyone anybody
anything nobody nothing none each both all other others
""".split())

# nouns that the -en rule would otherwise take for infinitives
NOUN_EN = set("""
gen seizoen teen schoen bijeen omheen achteren veren voorshands
bekken bluescreen discuswerpen elektricien griffioen hyaden leisteen linnen
pauken puntogen sardien speerwerpen stippen token
""".split())
NOUN_EN.add("algen")

# adjectives the -en and gloss rules cannot see
ADJ_EN = set("""
afgelopen bescheiden dronken eigen geboren gespannen gemeen omstreden
ontevreden open overdreven ontspannen tevreden verlegen verscheiden versleten
volwassen bont brons bronzen gouden gulden houten ijzeren koperen metalen
stenen wollen verwant verheugd vermoeid verslaafd vergeefs verdomd welkom zuur
zwart wakker waard zat volkomen zogeheten Hollands Vlaams Waals Pools Spaans
Turks Zweeds Deens Noors Fins IJslands Portugees Grieks Italiaans Frans Duits
Engels Russisch Chinees Japans Arabisch Marokkaans Afrikaans Amerikaans
Europees Nederlands Romeins middeleeuws parlementair revolutionair
universitair literair financieel elektrisch subalpien uitgestorven alpien
""".split())

# verbs with no `to` gloss
VERBS = set("""
aandoen aanspreken achterhalen afdoen afleiden afrekenen afronden afvallen
afzetten afzien bederven bedienen belasten beleggen bevallen bijkomen dagen
demonstreren doorlopen doortrekken heersen inhouden inleveren innemen
intrekken lenen maken misbruiken nalaten opblazen opbrengen opgeven ophalen
opheffen opknappen opkomen optrekken opvangen opvoeren overblijven overgeven
pikken prijzen prikkelen scheppen schokken sneuvelen staken steken trappen
uithalen uitlaten uitlopen uitmaken uitpakken uitrusten uitsteken uitzetten
verbinden verbouwen verkiezen vermogen vervolgen voordoen voorkomen vorderen
telefoneren uitdragen inschrijven rondlopen nadenken lassen duren landen
drukken vrijen breken kraken aaien rijmen wenken stichten wensen overnemen
opnemen opstaan afstaan voorstellen voorzien ontstaan achterlaten mislopen
wekken strekken bedoelen reizen peilen luiden kweken lozen toppen paren
verhalen vrezen keren wachten zoenen varen sturen voelen rollen regelen
draaien melden wenden opgaan toespreken uitroepen oproepen bijeenroepen
hangen jagen rotten braden rukken trekken schrikken wassen bakken blazen
liggen zitten lopen geven nemen komen doen gaan staan zien lezen eten drinken
slapen zullen moeten kunnen willen mogen weten hoeven zeggen vragen spelen
""".split())

# names the game lists and glosses miss
NAMES = set("""
nederland belgië belgie duitsland frankrijk spanje italië italie portugal
duitsland oostenrijk zwitserland griekenland rusland polen jemen litouwen
noorwegen zweden denemarken ierland schotland engeland wales finland ijsland
oekraïne oekraine hongarije roemenië roemenie bulgarije kroatië kroatie
servië servie marokko turkije egypte egypte israël israel china japan india
indonesië indonesie suriname amerika canada australië australie mexico
brazilië brazilie argentië argentinie colombia peru cambodja
amsterdam rotterdam den-haag 's-gravenhage utrecht eindhoven groningen tilburg
almere breda nijmegen apeldoorn haarlem arnhem enschede amersfoort zwolle
maastricht leiden dordrecht delft alkmaar leeuwarden
londen parijs berlijn rome madrid brussel antwerpen gent brugge luxemburg
wenen kopenhagen stockholm oslo helsinki moskou praag boedapest warschau
lissabon madrid athene brussel kaapstad cairo istanbul teheran beiroet
tokio new-york chicago los-angeles sydney melbourne
romeins napoleon tolkien shakespeare
""".split())

# spellings with capitals that are names, matched case-insensitively
NAME_SPELLINGS = set("""
nederland belgië duitsland frankrijk spanje italië portugal oostenrijk
zwitserland griekenland rusland polen jemen litouwen noorwegen zweden
denemarken ierland schotland engeland finland ijsland hongarije roemenië
bulgarije kroatië servië marokko turkije egypte israël china japan india
indonesië suriname amerika canada australië mexico brazilië argentië
colombia peru cambodja amsterdam rotterdam utrecht eindhoven groningen
tilburg almere breda nijmegen apeldoorn haarlem arnhem enschede amersfoort
zwolle maastricht leiden dordrecht delft alkmaar leeuwarden londen parijs
berlijn rome madrid brussel antwerpen gent brugge luxemburg wenen kopenhagen
stockholm oslo helsinki moskou praag boedapest warschau lissabon athene
kaapstad cairo istanbul teheran beiroet tokio napoleon tolkien shakespeare
jezus christus allah god mozes abraham mohammed
""".split())

# places the game lists give without a capital
PLACES_EXTRA = set("""
andes himalaya everest kilimanjaro matterhorn montblanc denali citlaltepetl
aconcagua fuji vinson olympus atlantis avalon camelot tartarus asgard valhalla
midgard yggdrasil ragnarok elysium nijl rijn maas schelde donau theems
apenninen karpaten pyreneeen alpen
""".split())
# words that are in the country and city lists but are ordinary Dutch words too,
# so their place reading only applies when something else says "place"
COUNTRY_CONFUSABLE = set("""
pool polen guinea niger chad chile mali congo jordan cuba turkije vlaanderen
oma overig filippijnen malediven
""".split())
CITY_CONFUSABLE = set("""
oma bors overig
""".split())
# country and city names whose lowercase `-en` lemma reads as an infinitive
# (`polen | poland`); only consulted in the game place lists
COUNTRY_EN = set("""
polen jemen
""".split())
CITY_EN = set("""
wenen
""".split())
# countries whose lowercase lemma arrives via a game list and has no capital
COUNTRY_PLACE_EN = COUNTRY_EN | {"filippijnen", "malediven", "alpen"}
MOUNTAINS = {"alpen"}
# creatures, props and places in the mythology list that are common nouns, not
# the proper name of a god or hero: `fee | fairy` is a noun, `zeus` is a name
MYTH_COMMON = set("""
betoveraar centaur cycloop draak druide dwerg fee feniks griffioen halfgod
heksenmeester kling magier minotaurus mysticus orakel reus rune sater sirene
sjamaan talisman titaan totem tovenaar vloek voorspeller voorspelling ziener
atlantis avalon camelot eden elysium olympus shangrila tartarus asgard valhalla
zegen
""".split())
# writers in the literature list
AUTHORS = set("""
dickens hemingway hugo orwell verne tolstoj tolstoy dostojewski poe kafka
""".split())
# planets and spacecraft in the space list
SPACE_NAMES = set("""
mars venus jupiter uranus neptunus saturnus mercurius pluto hubble kepler
doppler andromeda pleiaden""".split())
# writers of the literature list who gave their name to something else
AUTHORS_BEYOND = set("""
austen borges beckett camus dante goethe sartre wilde zola cervantes
""".split())

# a capitalised -s/-e lemma whose gloss is a bare place name is the derived
# adjective (`Antwerps | Antwerp`), unless it names a place itself (`Almere`)
PLACE_DERIVED = set("""
rotterdam amsterdam antwerpen brussel utrecht leiden delft haarlem breda
arnhem groningen nijmegen maastricht tilburg eindhoven zwolle tilburg leuven
gent brugge luik holland vlaanderen west-vlaanderen oudenaarde
""".split())
NAME_SUFFIX_PLAIN = re.compile(r"(man|vrouw|aar|ers|ling|iet)$")
NAME_SUFFIX = re.compile(r"(man|vrouw|aar|ers|isch|er|ling|iet|é|ees|eester)$")
INHABITANTS = set("""
nederlander vlaming fransman duitser brit engelsman amerikaan chinees japanner
belg italiaan spanjaard portegees portuges rus pool pools turk deen zweed noor
fins griek ier schot fransman jood joodse europese afrikaanse aziatische
""".split())

# place / person names in the game lists
GAME_PROPER_EXTRA = set("""
tolkien shakespeare napoleon
""".split())

# game words that are ordinary Dutch words despite the category
GAME_COMMON = set("""
jemen polen den wenen alpen lagen kussen eden citroen limoen meloen pompoen
katoen garen barnsteen kalksteen zandsteen vuursteen puimsteen schoorsteen
vuurtoren jachthaven gootsteen bladgroen blauweregen sneeuwregen pioen
malediven filippijnen school been hand handschoen hemel beken teen schoen
keuken haven varken kampioen geweten gebeden leven bevelen gebroken
""".split())
# English nouns that a game-list gloss supplies for an -en lemma
GAME_EN_NOUN = set("""
ascension attic auction availability baby backgammon bakery bamboo bargain
bark barley barn basket battle bean beech beer birch blood blossom board boat
bone boot border bosom bottle brain branch bread breast breath broth brother
brussels bucket bulb bun bush butter button cabbage cactus calcium calendar
camera cannon canvas carbon carrot cartridge cassette castle cattle ceiling
cellar chain chalk chamber champion chance charcoal chest chicken chimney
china chocolate chord chorus cider circle closet coal cocoa coffin colour
column commission community condition confession connection consequence
constellation continent convention conversation copper corner council counter
country course cousin crane creation cricket crime crystal culture curtain
cushion cycle
""".split())
# endings of English verb glosses that a lowercase game word uses for a verb
VERB_GLOSS_ENDINGS = re.compile(r"(ate|ize|ise|ify|en|fy|e|y|s|h|k|p|t|b|d|g|l|m|n|r|v|w)$")
# lemma endings that are nouns, never infinitives: `verwijderd` is a participle
# used as an adjective in this list, `nominalisatie` a noun
NON_VERB_LEMMA_ENDING = re.compile(r"(d|t|de|te|atie|itie|ing|heid|iteit|schap|isme|ist|teur|ment|sis)$")
# -en verbs with an inseparable prefix (`be-, ge-, ont-, ver-, her-, er-`) are
# verbs up to a few hundred; a `ver-`/`ge-` word that does not match is a noun
STRONG_VERB_PREFIX = ("be", "ont", "her", "er")
# a game word that is also a known verb is a verb, whatever its gloss says
# (`snijden | cut`, `plakken | slice` are both nouns there, the list is lemmas)
VERBS_GAME = set("""
snijden plakken drukken slaan vallen zetten pakken krijgen weten bellen
""".split())

MULTIWORD_SEA = set("""
adriatische zee atlantische oceaan caraibische zee egeische zee kaspische zee
middellandse zee pacifische oceaan oostzee noordzee rode zee zwarte zee
""".split())

MULTIWORD_RIVER = set("""
rijn maas schelde amazone donau theems ijssel niagara mississippi fuji
""".split())

# --------------------------------------------------------------------------
# Morphology
# --------------------------------------------------------------------------

STRONG_NOUN_SUFFIX = (
    "heid", "ing", "atie", "itie", "ment", "schap", "teit", "isme", "ist", "eur",
    "age", "iteiten", "iteit", "logie", "grafie", "tuur", "erie", "nis", "dom",
)
# the `-baar` endings, which are also the plural of a `-aar` noun (`gebaar` is
# not `ge` + `baar`)
ADJ_SUFFIX_STRONG = ("lijk", "baar", "vol", "loos", "isch", "ief", "erig",
                     "achtig", "zaam", "aal")
# the strong adjective suffixes; `-ig`/`-end` are weak because `redding`,
# `duisternis`-type nouns end in the same letters
ADJ_SUFFIX_STRONG = ("lijk", "baar", "vol", "loos", "isch", "ief", "erig",
                     "achtig", "zaam", "aal")
# every adjective suffix, weak ones included
ADJ_SUFFIX = ADJ_SUFFIX_STRONG + ("ig", "end")
ADJ_GLOSS_SUFFIX = ("ent", "ant", "ive", "ful", "less", "ous", "able", "ible",
                    "ic", "al", "y", "ish")
# adjective-only Dutch endings: a lemma ending in one of these, with a gloss that
# plenty of adjectives also carry, is an adjective rather than the noun it looks
# like (`schriftelijk | written`, `vrijwillig | voluntary`)
# adjective endings with one-letter nouns behind them: `slordig`, `nuttig`
WEAK_ADJ_SUFFIX = ("ig", "ig", "vuldig", "achtig", "erig", "loos", "vol", "baar")
ADJ_GLOSS_SUFFIX_BLOCK = ("lijk", "ig", "baar", "vol", "loos", "isch", "ief",
                          "erig", "achtig", "zaam", "aal", "end")
ADV_SUFFIX = ("waarts", "halve", "gewijze", "weg", "langs")
# an English gloss that is an adjective by its own ending
ADJ_EN_ENDING = re.compile(r"(ous|ful|less|ive|able|ible)$")
# `-aal` and `-ief` end more Dutch adjectives than any other pair of endings, but
# the lists also hold a few dozen nouns of the same shape; these are the ones
# whose gloss is the noun, or that are too short for the ending to be a suffix
AAL_IEF_NOUNS = set("""
admiraal archeef archief brief dief garnaal generaal hieroglief initiatief
journaal kaal kanaal kapitaal kathedraal koraal kwartaal maal materiaal metaal
mineraal moraal motief opaal paal perspectief portaal sandaal schaal schandaal
signaal sjaal staal straal taal tarief verhaal zaal bidsgarnaal eischaal
luchtkanaal weegschaal madelief oeraal hadaal litoraal
""".split())
# `-maal` is also the adverb ending (`allemaal`, `tweemaal`), which wins over
# `-aal`: `eenmaal` is `once`, not the `-aal` adjective it looks like.
AAL_ADVERBS = set("""
allemaal ditmaal driemaal eenmaal helemaal tweemaal
""".split())
# `-end` words whose ending is not a present-participle suffix
END_NOUNS = set("""
eend ochtend vriend weekend trend avond
""".split())
# `-en` words that are adverbs, checked before the bare `-en` noun rules
EN_ADVERB_PRE = set("""
achteren doorheen omheen nadien voren zelden
""".split())
# a lemma with a Dutch adjective ending that is a noun all the same
NOUN_LEMMA_BLOCK = ("ier", "eer", "foon", "graaf", "beer", "tiek", "kaart",
                    "jaar", "zaal", "daal", "baan", "maan", "haan")

def is_adj_suffix(lower, suffixes):
    """The suffix test, with the `-baar` trap: `gebaar | gesture` is a plural
    noun whose gloss is not an adjective."""
    for s in suffixes:
        if lower.endswith(s):
            if s == "baar" and lower.endswith("gebaar"):
                return False
            return True
    return False

# --------------------------------------------------------------------------
# Glosses
# --------------------------------------------------------------------------

# adjectives frequent in this file's glosses
ADJ_GLOSS = set("""
abstract absolute absurd active actual afraid aggressive alone ancient angry
anonymous anxious apparent artistic attentive authentic automatic available
aware bad basic beautiful best better big bitter bizarre blank blind blond blue
bold boring brave brief bright broad brown busy calm careful central certain
cheap chemical chief chic civil classical clean clear clever close cloudy cold
comfortable commercial common complete complex concrete confident conscious
consistent constant continuous cool correct creative criminal critical cruel
curious current cute daily dangerous dark dead deaf dear decent deep definite
dependent desperate different difficult digital direct dirty distant distinct
diverse double dry dual dull dumb eager early easy economic effective efficient
electric electronic elegant emotional empty endless enormous entire equal
essential eternal exact excellent exceptional exotic expensive extra extreme
fair faithful false famous fantastic far fast fatal favourite federal female
fertile few fierce final fine firm fit flat flexible fluent foolish foreign
formal former fortunate fragile free frequent fresh friendly frozen full funny
furious future general gentle genuine giant glad global gloomy golden good
gradual grateful great greedy green grey gross guilty handsome happy hard harsh
healthy heavy helpful hidden high hollow honest horrible hostile hot huge human
humble hungry ideal ill immediate immature immune important impossible
impressive incredible independent individual industrial infamous infinite
informal innocent intense interesting internal international invisible iron
ironic jealous joint jolly joyful junior just keen kind large last late lazy
legal legendary liberal light likely limited liquid little lively local lonely
long loose loud lovely low loyal lucky mad magical major male manual marine
mature mean medical medium mental middle mild military minimal minor miserable
mixed mobile modest modern moral mutual mysterious naked narrow nasty national
native natural naughty neat negative nervous neutral new next nice noble normal
northern notable novel numerous obvious odd official old only open opposite
optimistic ordinary organic original other outstanding overall pale parallel
particular passive past patient peaceful peculiar perfect permanent personal
physical pink plain pleasant polite poor popular positive possible potential
powerful practical precious precise pregnant present pretty previous primary
prime private probable professional profound prominent proper proud public
pure quick quiet radical random rapid rare raw ready real reasonable recent red
regular relevant reliable religious remote responsible rich right ripe risky
romantic rough round royal rude rural sacred sad safe same satisfactory scarce
scared secret secure selective senior sensible sensitive separate serious
severe shallow sharp shy sick significant silent silly silver simple sincere
single slight slim slow small smart smooth social soft solid sorry sour
southern special specific spectacular spiritual splendid stable steady steep
sticky stiff straight strange strict strong structural stupid subtle sudden
sufficient suitable superior sure surprised suspicious sweet swift tall
technical temporary tender tense terrible thick thin third thorough tight tiny
tired tolerant total tough toxic tragic tremendous tropical true typical ugly
ultimate unable uncertain unequal unhappy uniform unique universal unknown
unusual upper upset urban urgent usual vacant vague valid various vast vertical
violent virtual visible vital vivid warm weak wealthy weird western wet white
whole wide wild willing wise wonderful wooden worried worse wrong yellow young
old-time several each whole french german english dutch spanish polish turkish
swedish greek italian portuguese russian chinese japanese arabic african
european american belgian danish norwegian finnish icelandic moroccan
spicy salty tasty windy sunny rainy muddy dusty sandy leafy
""".split())

# English adjectives the list glosses words with but never glosses anything else
# with, so the vote cannot see them (`slordig | untidy, sloppy`)
ADJ_PARTICIPLE = set("""
surprised confused disappointed satisfied annoyed frightened
delighted exhausted embarrassed bored ashamed pleased
unfair handy closed enthusiastic correct next
""".split())

# English `-y` adjectives whose only lemma in the list is a `-t`/`-d` word
ADJ_Y_GLOSS = set("""
untidy sloppy stuffy leaky elderly crenellated
explicit evident educated prepared civilized known bare ready concerned fascinating
bloot bloot
""".split())

# single-word glosses that are nouns *and* English adjectives, where the Dutch
# lemma is normally the noun: `materiaal | material`, `individu | individual`.
# The adjective is differently shaped (`individueel`, `nationaal`), so the plain
# adjective suffixes run before this set; the weak suffix rules run after it.
NOUN_GLOSS_ADJ_TOO = set("""
animal material mineral musical individual musical native marine oval ideal
orange spiritual
""".split())

# single-word glosses that are adjectives only: `definitief | final`. They are
# never the noun, whatever the lemma's ending looks like.
ADJ_GLOSS_ONLY = set("""
regular stable final general formal typical medical national natural central
local mutual digital personal professional classical concrete
""".split())

# Gloss keys that end in -en but are not verbs, so an -en lemma gets no free
# pass from them.
NON_VERB_GLOSS_ENDINGS = ("n", "ion", "ment", "ness", "ty", "ce", "ing", "er",
                          "th", "ck", "el", "r", "l", "e", "s", "m", "d")
# gloss endings that mark a noun (`darkness`, `meeting`, `monarchy`)
NOUN_GLOSS_ENDINGS = ("ness", "tion", "sion", "ment", "ity", "ance", "ence",
                      "ship", "hood", "dom", "ism", "ist", "ing", "er", "or",
                      "ary", "ery", "logy", "graphy", "ics", "ure", "age", "um",
                      "on", "a", "o", "ce", "th", "archy", "cracy", "scope",
                      "phone", "graph", "meter", "tion", "tor", "ment")
# ... but these noun glosses are spelled just like an English adjective, so the
# weak `-y`/`-al` adjective rule must not reach them
NOUN_GLOSS_STEMS = set("""
medal trial topic tent scarf incident marriage language hall beam accident ad
advent assembly burglary library diary gallery bakery delivery melody comedy
secretary salary penalty victory strategy policy economy company agency energy
history memory mystery theory category factory bakery jewellery relative native
representative executive negative objective initiative relative detective
""".split())
# the `-y` and `-al` endings are shared with nouns, so they are only adjectives
# with a known stem behind them (listed in ADJ_GLOSS ending so)
# endings a Dutch adjective can have, for the gloss-driven adjective rule
LEMMA_ADJ_ENDING = ("ig", "lijk", "baar", "vol", "loos", "isch", "ief", "aal",
                    "erig", "achtig", "zaam", "end", "ies", "e", "ief")
WEAK_ADJ_ENDINGS = ("ent", "ant", "ive", "ful", "less", "ous", "able", "ible",
                    "ish", "ic")

# English noun glosses whose Dutch lemma is a noun whatever its ending
# (`kunstmatig`-type words are safe; `-ig` words with these glosses are not)

# words that are both adjective and adverb in Dutch
ADJ_ADV = set("""
hoelang hoever hoe lang allang eerder zoveel hoeveel zomin nauwelijks dikwijls
tenslotte allerlei enerzijds anderzijds zogezegd mekaar
""".split())
# adverb glosses, for a compound whose gloss is exactly one of these
ADV_GLOSS = set("""
ahead alarm along aloud already also always anyway apart around aside away
back backwards beforehand behind below besides between both by down downstairs
early easily else enough even ever everywhere far fast forward free further
hard hardly here home how however immediately instead just late later less
long maybe meanwhile more most mostly nearly never nevertheless next no not
now often once only otherwise out outside over past perhaps probably quite
rather really recently right seldom since slowly soon still suddenly then
there therefore though thus today together tomorrow tonight too twice under
underground upstairs up usually very well when where while why yet
""".split())
# time compounds made from a day word or a time unit
DAY_OR_TIME = ("maandag", "dinsdag", "woensdag", "donderdag", "vrijdag",
               "zaterdag", "zondag", "gister", "morgen", "vanmorgen", "half",
               "jaar", "dag", "week", "nacht", "avond", "niet", "onder")

# Gloss first words that mark a noun gloss despite no article
NOUN_GLOSS = set("""
one ones people person man people thing things kind sort type way part piece
""".split())

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

FREQ_TAIL = re.compile(r"\s+\d+\s+van\s+148$")
READING = re.compile(r"^\s*(?:[a-c]\)|\d\))\s*")


def first_gloss(en):
    """The first reading of an `a) ... b) ...` or `1) ... 2) ...` gloss."""
    g = FREQ_TAIL.sub("", en.strip())
    g = READING.sub("", g)
    g = re.split(r"\s+[a-c]\)\s+|\s+\d\)\s+", g)[0]
    return g.strip()


def gloss_key(en):
    return first_gloss(en).strip().lower()


def gloss_head(en):
    """The first comma reading of a gloss: `surprised, amazed` -> `surprised`."""
    return re.split(r"[,/;]", gloss_key(en))[0].strip()


def gloss_is_verb(en):
    return gloss_key(en).startswith("to ")


def gloss_verb_tail(en):
    """The object of a `to ...` gloss: `to put on` -> `put on`."""
    k = gloss_key(en)
    return k[3:].strip() if k.startswith("to ") else ""


def gloss_is_adj_shape(en):
    """A gloss that reads as a bare English adjective: `modest`, `happy, glad`,
    `large-scale`. Noun glosses (`darkness`, `meeting`) are the ones the -en
    adjective rule must not claim."""
    k = gloss_key(en)
    if not k or k.startswith("to "):
        return False
    if k in ADJ_GLOSS or k.split()[0] in ADJ_GLOSS:
        return True
    first = re.split(r"[,/;]", k)[0].strip()
    if not re.fullmatch(r"[a-z][a-z'\- ]*", first) or len(first.split()) > 2:
        return False
    return not first.endswith(NOUN_GLOSS_ENDINGS)


def is_pronominal_adverb(lower):
    m = re.match(r"^(daar|hier|waar|ergens|nergens|overal|er)(.+)$", lower)
    if not m:
        return False
    return m.group(2) in PRONOUN_BASES


def has_capital(nl):
    w = nl.strip()
    return bool(w[:1].isupper()) and not w.startswith("'s ")


def load():
    with open(SRC, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


# --------------------------------------------------------------------------
# The tagger
# --------------------------------------------------------------------------


def tag(nl, en, niveau, herkomst, base=False):
    raw = nl
    w = nl.strip()
    lower = w.lower()
    herkomst = herkomst or ""

    def out(p, why=None):
        return (p, why) if not base else p

    if raw in OVERRIDES:
        return out(OVERRIDES[raw], "override")

    # ---- parenthetical hints: `druk (noun)`, `alternatief (adj)`, `meer num` ----
    m = re.search(r"[( ](adj|noun|verb|pron|adv|conj|prep|num)\)?$", w)
    if m:
        hint = m.group(1)
        return out({"adj": "adj", "noun": "noun", "verb": "verb", "adv": "adv",
                    "pron": "function", "conj": "function", "prep": "function",
                    "num": "function"}[hint], "paren " + hint)

    # ---- game-list myth, place and person names the source lowercased ----
    close_class = (lower in FUNCTION or lower in NUMERALS or lower in ADVERB
                   or lower in INTERJECTIONS or lower in EN_NONVERB)
    if " " not in w and not close_class and (
            "spel:mythology" in herkomst or lower in PLACES_EXTRA
            or "spel:literature" in herkomst and (lower in AUTHORS
                                                    or lower in AUTHORS_BEYOND)
            or "spel:space" in herkomst and lower in SPACE_NAMES
            or "spel:countries" in herkomst and lower in COUNTRY_CONFUSABLE
            or "spel:cities" in herkomst and lower in CITY_CONFUSABLE):
        if lower not in GAME_COMMON and lower not in MYTH_COMMON:
            return out("name", "game proper name")

    # ---- a capitalised lemma is a proper noun ----
    if has_capital(w) and " " not in w:
        if lower not in FUNCTION and lower not in INTERJECTIONS:
            if lower in NAME_SPELLINGS or gloss_key(en) in NAME_SPELLINGS:
                if lower not in PLACE_DERIVED and \
                        not lower.endswith(("s", "isch")) and \
                        lower not in INHABITANTS:
                    return out("name", "capital + name list")
            if lower in INHABITANTS or NAME_SUFFIX.match(w):
                return out("noun", "capital, inhabitant")
            if lower in ADJ_EN or lower.endswith(("s", "e", "isch", "ig")) or \
                    ("-" in w and gloss_key(en) != lower):
                return out("adj", "capital, derived adjective")
            if lower.isupper() and "spel:" not in herkomst:
                return out("name", "capital, acronym")
            if "spel:" in herkomst:
                return out("name", "capital, game proper")
            return out("noun", "capital, common noun")

    # ---- a source comma or parenthetical that only repeats the head word ----
    # `koek, koekje` is one noun; `hapje (klein)` is a noun with a usage note.
    # `(zich)` marks a reflexive verb (`schamen (zich)`): the marker comes off and
    # the infinitive is tagged as the verb it is. `gelijk ad` is a truncated
    # adjective and keeps the raw lemma.
    head = w
    if "(zich)" in lower:
        head = re.sub(r"\s*\(zich\)$", "", w).strip()
    elif "(" in w and not re.search(
            r"[( ](adj|noun|verb|pron|adv|conj|prep|num)\)?$", w):
        head = re.split(r"\s*[(,]", w)[0].strip()
    elif "," in w:
        head = w.split(",")[0].strip()
    elif re.search(r" (ad|num)$", w):
        head = re.sub(r" (ad|num)$", "", w)
    if head != w:
        # a second variant (`zijde, zij`) may be clipped, so only the first part
        # counts; a `,` inside it would be a list, but no lemma has one
        w = head
        lower = w.lower()

    # ---- multiword ----
    if " " in w:
        if lower.startswith(("'s ", "’s ")):
            return out("adv", "time of day")
        if "spel:" in herkomst and ("cities" in herkomst or "countries" in herkomst):
            return out("name", "multiword place")
        if lower in MULTIWORD_SEA or (lower.endswith(("zee", "oceaan")) and "spel:" in herkomst):
            return out("name", "sea")
        if lower in MULTIWORD_RIVER:
            return out("name", "river")
        if lower.replace(" ", "-") in NAME_SPELLINGS:
            return out("name", "place")
        if gloss_is_verb(en):
            return out("phrase", "multiword verb")
        return out("phrase", "multiword")

    # ---- a game list of a country or city is a name ----
    if "spel:" in herkomst and ("countries" in herkomst or "cities" in herkomst) \
            and lower not in GAME_COMMON and lower not in NAME_SPELLINGS:
        return out("name", "place")

    in_game = "spel:" in herkomst and "bijlage8" not in herkomst
    if in_game and ("countries" in herkomst or "cities" in herkomst) \
            and (lower in NAME_SPELLINGS or lower in COUNTRY_PLACE_EN):
        # `polen | poland`, `wenen | vienna`, `filippijnen | philippines`: the
        # lowercase `-en` would be read as an infinitive further down
        return out("name", "place")
    if "spel:" in herkomst and "mountains" in herkomst and lower in MOUNTAINS:
        return out("name", "mountain")
    if in_game and lower not in GAME_COMMON:
        if lower in COUNTRY_EN or lower in CITY_EN:
            return out("name", "place")
        if lower in GAME_PROPER_EXTRA or lower in NAME_SPELLINGS:
            return out("name", "proper name")
        if lower in FUNCTION or lower in NUMERALS:
            return out("function", "closed class")
        if lower in ADVERB:
            return out("adv", "adverb")
        if lower in INTERJECTIONS:
            return out("interjection", "interjection")
        if lower.endswith(STRONG_NOUN_SUFFIX) or lower in NOUN_EN:
            return out("noun", "game noun")
        if gloss_is_verb(en) and not (lower.endswith("en") and lower in NOUN_EN):
            return out("verb", "game infinitive")
        if lower.endswith("en") and lower in VERBS:
            return out("verb", "game infinitive")
        # a plural noun whose gloss is a noun or an adjective the lemma cannot be
        if lower.endswith("en") and lower not in NOUN_EN and \
                lower not in VERBS and gloss_key(en) not in ADJ_GLOSS and (
                    gloss_key(en) in NOUN_ADJ_GLOSS
                    or (re.fullmatch(r"[a-z][a-z' \-]*", gloss_key(en))
                        and not gloss_is_adj_shape(en))):
            return out("noun", "game noun")
        if gloss_is_verb(en):
            return out("verb", "game infinitive")
        if gloss_key(en) in ADJ_GLOSS or lower in ADJ_EN or is_adj_suffix(lower, ADJ_SUFFIX):
            if lower not in AAL_IEF_NOUNS:
                return out("adj", "game adjective")
            return out("noun", "aar/ief noun")
        if lower.endswith("en") and not NON_VERB_LEMMA_ENDING.match(lower):
            k = gloss_key(en)
            if (re.fullmatch(r"[a-z][a-z'\-]*( [a-z][a-z'\-]*)?", k)
                    and not k.endswith(NOUN_GLOSS_ENDINGS)
                    and k not in ADJ_GLOSS
                    and not VERB_GLOSS_ENDINGS.match(k)
                    and k not in GAME_EN_NOUN):
                return out("verb", "game infinitive")
            if lower not in EN_NONVERB or lower in VERBS_GAME:
                return out("verb", "game infinitive")
        return out("noun", "game noun")

    # ---- closed classes first: they cannot be anything else ----
    if lower in INTERJECTIONS or gloss_key(en) in YES_NO:
        return out("interjection", "interjection")
    if lower in MONTHS:
        return out("name", "month")
    if is_numeral(lower):
        return out("function", "numeral")
    if lower in DEMONSTRATIVES:
        return out("function", "determiner")
    if lower in FUNCTION:
        return out("function", "function word")
    # a weekday or `gister`/`morgen` plus a time of day is an adverb, whatever its
    # gloss calls it (`maandagavond | Monday evening`)
    if re.match(r"^(maandag|dinsdag|woensdag|donderdag|vrijdag|zaterdag|zondag|"
                r"gister|morgen)(avond|ochtend|middag|nacht)$", lower):
        return out("adv", "time of day")
    if lower in ("eergisteren", "eergisteravond", "voorgisteren"):
        return out("adv", "time of day")
    # a space plus an adverb gloss is that adverb: `gisteravond`, `halverwege`
    if lower.startswith(DAY_OR_TIME) and ADJ_GLOSS_VOTE.get(gloss_key(en), 0) < 0 \
            and gloss_key(en) in ADV_GLOSS:
        return out("adv", "time adverb")
    if lower in ADVERB or lower in ADV_LEXICON:
        return out("adv", "adverb")
    if is_pronominal_adverb(lower):
        return out("adv", "pronominal adverb")

    # ---- the `-aal`/`-ief` nouns the adjective-suffix rules would claim ----
    if lower in AAL_IEF_NOUNS:
        return out("noun", "aal/ief noun")
    if lower in AAL_ADVERBS:
        return out("adv", "aal adverb")

    # ---- adjectives the morphology cannot see ----
    if lower in ADJ_EN:
        return out("adj", "adj lexicon")

    # a word that is an adjective and an adverb at once: the adverb is the usual
    # label in this list unless the gloss is a bare adjective
    if lower in ADJ_ADV and gloss_key(en) not in ADJ_GLOSS:
        return out("adv", "adj/adv, adverb")

    # ---- strong noun suffixes ----
    if lower.endswith(STRONG_NOUN_SUFFIX):
        return out("noun", "noun suffix")

    # ---- a bare adjective, from its own gloss or from its ending ----
    if gloss_key(en) in NOUN_GLOSS_ADJ_TOO and lower not in ("muzikaal", "nationaal"):
        return out("noun", "noun gloss")
    if gloss_key(en) in ADJ_GLOSS:
        return out("adj", "adj gloss")
    # `-ig` is an adjective ending almost without exception here: `plechtig`,
    # `tijdig`. The `-tig` numerals are caught above by NUMBER_WORD, the two
    # nouns whose `-ig` sits inside a compound (`vliegtuig`, `voertuig`) are
    # not, and a few adverbs carry the same shape.
    if lower.endswith("ig") and not lower.endswith(("igheid", "igde")) \
            and lower not in ("vliegtuig", "voertuig", "vrijgevig") \
            and lower not in ADVERB and not is_numeral(lower):
        return out("adj", "adj suffix")
    if is_adj_suffix(lower, ADJ_SUFFIX_STRONG) \
            and lower not in AAL_IEF_NOUNS and lower not in AAL_ADVERBS:
        return out("adj", "adj suffix")
    if gloss_key(en) in ADJ_GLOSS_ONLY:
        return out("adj", "adj gloss")
    if lower.endswith(ADJ_GLOSS_SUFFIX_BLOCK) and len(lower) > 7 and \
            re.search(r"(lijk|ig|baar|vol|loos|isch|ief|erig|achtig|zaam|end)$", lower) and \
            ADJ_GLOSS_VOTE.get(gloss_key(en), 0) > 0:
        # `schriftelijk | written`: -lijk is only an adjective ending when the
        # gloss is not the noun the lemma also is
        return out("adj", "adj gloss from ending")
    if len(gloss_key(en).split()) == 1 and \
            gloss_key(en).endswith(WEAK_ADJ_ENDINGS) and \
            gloss_key(en) not in NOUN_GLOSS_STEMS and \
            lower.endswith(LEMMA_ADJ_ENDING):
        return out("adj", "adj gloss suffix")
    # the -ig / -end words: `-igheid` and `-endheid` are nouns, the rest is an
    # adjective unless the gloss names a noun
    if lower.endswith(("ig", "end")) and not lower.endswith(
            ("igheid", "endheid", "ends", "erig")):
        if ADJ_GLOSS_VOTE.get(gloss_key(en), 0) > 0:
            return out("adj", "adj suffix")
        if gloss_key(en) in NOUN_GLOSS_STEMS:
            return out("noun", "noun gloss stem")
    if lower.endswith(WEAK_ADJ_SUFFIX) and not lower.endswith(NOUN_GLOSS_ENDINGS):
        if gloss_key(en) in ADJ_GLOSS or ADJ_GLOSS_VOTE.get(gloss_key(en), 0) > 0:
            return out("adj", "adj suffix")
    if lower.endswith(ADV_SUFFIX):
        return out("adv", "adv suffix")
    # `-end` is the present participle and is an adjective in this list (`spannend`,
    # `opvallend`, `vervelend`); the nouns of the same shape are the ones whose
    # `-end` is not a suffix at all.
    if lower.endswith("end") and lower not in END_NOUNS \
            and not is_numeral(lower):
        return out("adj", "present participle")

    # ---- verbs ----
    if NON_VERB_LEMMA_ENDING.match(lower) and lower not in VERBS:
        return out("noun", "non verb ending")
    if lower in VERBS:
        return out("verb", "verb lexicon")
    gv = gloss_verb_tail(en)
    if gv and gv.split()[0] not in ADJ_GLOSS:
        # `to ...`, but the infinitive rule is not licensed by `-t` glosses
        if lower.endswith("en"):
            return out("verb", "to gloss")
        if not re.search(r"(s|t|e)$", lower) or lower.endswith("e"):
            return out("verb", "to gloss")
        return out("noun", "to gloss, noun shape")

    # ---- bare -en forms: the -en is an adjective ending only when the gloss
    # says adjective; `duisternis | darkness` must not become `duister` + `nis` ----
    if lower in EN_ADVERB_PRE and "spel:" not in herkomst:
        return out("adv", "adverb")
    if lower.endswith("en") and len(lower) > 3:
        if lower in NOUN_EN or lower in EN_NONVERB:
            return out("noun", "en noun lexicon")
        # a noun-shaped gloss: no English verb, adverb or pronoun could be it
        k = gloss_key(en)
        first = re.split(r"[,/;]", k)[0].strip()
        # a stem ending in a consonant and `-en` with a pure noun gloss
        # (`wapen | weapon`, `bewoner`-type plurals) is a noun
        if (first.endswith(NOUN_GLOSS_ENDINGS) or gloss_key(en) in NOUN_ADJ_GLOSS) \
                and re.search(r"[^aeiou]en$", lower.strip(" ,")):
            return out("noun", "en noun gloss")
        if (re.fullmatch(r"[a-z][a-z' \-]*", k) and not gloss_is_verb(en)
                and k not in ADJ_GLOSS and k.split()[0] not in ADJ_GLOSS
                and first not in ADV_GLOSS and first not in ADV_EN
                and first not in PRONOUN_EN
                and not first.endswith(("it", "this", "that", "there", "here",
                                        "then", "where", "ago", "elsewhere"))):
            return out("noun", "en noun gloss")
        core = lower[:-2]
        if len(lower) <= 5 and core and core[-1] not in "aeiou":
            return out("noun", "short en noun")
        if core and core[-1] in "aeo" and len(lower) <= 7:
            return out("adj", "en adjective")
        if gloss_is_adj_shape(en):
            return out("adj", "en adjective from gloss")

    # ---- the default: a noun. The `-t` ending is a supine or a past participle
    # (`verliefd | in love`), and an English noun gloss is why the lemma is here.
    # A Dutch adjective ending plus an adjective gloss is the adjective it looks
    # like (`spontaan`, `naïef`, `ambitieus`); a noun gloss keeps it a noun
    # (`salaris`, `tabel`).
    if lower.endswith(("isch", "ief", "ef", "eus", "aal")) \
            and not lower.endswith(NOUN_LEMMA_BLOCK) and gloss_is_adj_shape(en) \
            and gloss_key(en) not in NOUN_GLOSS_STEMS \
            and re.search(r"(ous|ful|less|ive|ic|al|ive|able|ible|ant|ent|ate|ish)$",
                          gloss_key(en)):
        return out("adj", "adj gloss from ending")
    if lower.endswith(("d", "t")) and not lower.endswith(("heid", "iteit", "teit")) \
            and not gloss_key(en).startswith("to "):
        h = gloss_head(en)
        last = h.split()[-1] if h.split() else ""
        if h in NOUN_ADJ_GLOSS or last in NOUN_ADJ_GLOSS:
            return out("noun", "default")
        if h in ADJ_GLOSS or h in ADJ_PARTICIPLE or h in ADJ_Y_GLOSS:
            return out("adj", "default, adj gloss")
        # `vertrouwd | familiar`, `uitgebreid | extensive`, `opgewekt | cheerful`:
        # a past participle used as an adjective, recognisable from a gloss whose
        # own ending only an adjective carries
        if h and ADJ_EN_ENDING.search(h) and h not in NOUN_GLOSS_STEMS:
            return out("adj", "default, participle")

    return out("noun", "default")


# filled in main() from the data
EN_NONVERB = set()
VERBS_ALL = set()
ADJ_GLOSS_VOTE = {}   # gloss key -> 1 when the lemmas using it are adjectives


def classify(r):
    return tag(r["nl"], r["en"], r["niveau"], r["herkomst"], base=True)


def main():
    rows = load()

    # verbs the data attests: an -en lemma with a `to ...` gloss
    global VERBS_ALL
    VERBS_ALL = {r["nl"].strip().lower() for r in rows
                 if r["nl"].strip().lower().endswith("en") and gloss_is_verb(r["en"])}
    VERBS.update(VERBS_ALL)

    # each gloss key takes its majority label over the lemmas it glosses. The
    # key is the first comma reading (`surprised, amazed` is `surprised`) so a
    # word reaches the vote whichever list it was glossed with. Two passes: the
    # `default, adj gloss` rule reads the vote, so the first pass cannot see it.
    ADJ_GLOSS_VOTE.clear()
    for _ in range(2):
        votes = {}
        for r in rows:
            pos, why = tag(r["nl"], r["en"], r["niveau"], r["herkomst"])
            if why == "override":
                continue
            key = gloss_head(r["en"])
            for k in {gloss_key(r["en"]), key}:
                c = votes.setdefault(k, {"adj": 0, "noun": 0})
                if pos in c:
                    c[pos] += 1
        for key, c in votes.items():
            ADJ_GLOSS_VOTE[key] = c["adj"] - c["noun"]

    if "--dump" in sys.argv:
        path = sys.argv[sys.argv.index("--dump") + 1]
        with open(path, "w", encoding="utf-8") as f:
            for r in rows:
                pos, why = tag(r["nl"], r["en"], r["niveau"], r["herkomst"])
                f.write(f"{pos}\t{why}\t{r['nl']}\t{r['en']}\n")
        return

    if "--sample" in sys.argv:
        seed = 20261116
        if "--seed" in sys.argv:
            seed = int(sys.argv[sys.argv.index("--seed") + 1])
        rnd = random.Random(seed)
        for i in sorted(rnd.sample(range(len(rows)), 100)):
            r = rows[i]
            pos, why = tag(r["nl"], r["en"], r["niveau"], r["herkomst"])
            print(f"{i + 1}\t{r['nl']}\t{pos}\t{why}\t{r['en']}")
        print("note: the number printed is the line number in woorden.tsv,"
              " header included; the data row is one less.", file=sys.stderr)
        return

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, delimiter="\t", lineterminator="\n")
        wr.writerow(["nl", "pos", "en"])
        for r in rows:
            wr.writerow([r["nl"], classify(r), r["en"]])


if __name__ == "__main__":
    main()
