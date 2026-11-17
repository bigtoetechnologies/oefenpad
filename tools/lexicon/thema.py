#!/usr/bin/env python3
"""Classify tools/lexicon/woorden.tsv by product theme and priority.

Writes tools/lexicon/woorden-thema.tsv:
    nl<TAB>thema<TAB>thema_ook<TAB>prioriteit<TAB>en
one row per input row, same order, `nl` byte-identical.

Themes are the 24 in Docs/product.md §12 (11 base + 13 candidates, with
Het lichaam), plus three buckets the product's worlds do not hold:
`algemeen`, `naam`, `plaats`.

Pipeline, first match wins:
  0. structural: pos function -> algemeen
  1. curated lemma overrides (OVERRIDES), including `thema_ook`
  2. gloss-equality overrides (EN_ONLY)
  3. seed from herkomst for game-only words (no bijlage8 in herkomst)
  4. curated `algemeen` gloss list (abstract verbs/adjectives)
  5. gloss keyword table, first world that matches
  6. weak seed from herkomst (the word is also in the appendix)
  7. fallback: name -> naam, else algemeen

Priority never defaults from the theme: `algemeen` is the B1 core the product
exists to teach, so a verb/adjective there is normally `kern`. `laag` is
reserved for encyclopaedic one-offs and names with no everyday use.

The 100-row hand-check sample is printed to stdout under a fixed seed.
Deterministic: no randomness, no network, local Python only.
"""

import csv
import os
import random
import re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = os.path.join(HERE, "woorden.tsv")
POS = os.path.join(HERE, "woorden-woordsoort.tsv")
OUT = os.path.join(HERE, "woorden-thema.tsv")

# Fixed seed for the 100-row hand check, so the sample is reproducible forever.
SAMPLE_SEED = 20261116

# ---------------------------------------------------------------------------
# The taxonomy: Docs/product.md §12, plus the three non-product buckets.
# ---------------------------------------------------------------------------

WORLD_THEMES = [
    # 11 base themes
    "Boodschappen", "Mensen", "Wonen", "Werk", "Gezondheid", "Het lichaam",
    "Kinderen en school", "Gemeente en post", "Reizen", "De weg", "Afspraken",
    # 13 candidates
    "Eten en drinken", "Kleding", "Bank en geld", "Telefoon en internet",
    "Buurt", "Sport en vrije tijd", "Solliciteren", "Nood en politie",
    "Zorg voor iemand anders", "Bellen", "Klachten", "Mening geven",
    "Formulieren",
]
BUCKETS = ["algemeen", "naam", "plaats"]
THEMES = WORLD_THEMES + BUCKETS
PRIOS = ["kern", "nuttig", "laag"]

# The default priority of a world, used only when nothing more specific is
# known. `algemeen` has none: priority there is decided by part of speech.
THEME_PRIO = {
    "Boodschappen": "kern",
    "Mensen": "kern",
    "Wonen": "kern",
    "Werk": "kern",
    "Gezondheid": "kern",
    "Het lichaam": "kern",
    "Kinderen en school": "kern",
    "Gemeente en post": "kern",
    "Reizen": "kern",
    "De weg": "kern",
    "Afspraken": "kern",
    "Eten en drinken": "kern",
    "Kleding": "kern",
    "Bank en geld": "kern",
    "Telefoon en internet": "kern",
    "Buurt": "kern",
    "Sport en vrije tijd": "nuttig",
    "Solliciteren": "nuttig",
    "Nood en politie": "nuttig",
    "Zorg voor iemand anders": "nuttig",
    "Bellen": "kern",
    "Klachten": "kern",
    "Mening geven": "kern",
    "Formulieren": "kern",
    "plaats": "nuttig",
    "naam": "laag",
}

# Words with no home in a world: narrow, encyclopaedic or technical vocabulary
# that sits in the product only as background. `algemeen` is not in this map;
# see priority_for() and the abstract-verb rule.
THEME_ALSO = {
    # a word that is genuinely in two worlds
    "knie": "Gezondheid",
    "rekening": "Eten en drinken;Boodschappen",  # §12's own example
    "boodschap": "Boodschappen",  # the shopping try, beside Mensen's message
    "pin": "Bank en geld",
    "pas": "Bank en geld",
    "wisselgeld": "Bank en geld",
    "Sms": "Telefoon en internet",
    "fax": "Telefoon en internet",
    "kopie": "Gemeente en post",
    "ondertekenen": "Gemeente en post",
    "noise": "Buurt",
    "overlast": "Nood en politie",
    "diefstal": "Nood en politie;Klachten",
    "excuse": "Klachten",
    "vriend": "Mensen",
    "buurman": "Buurt",
    "buurvrouw": "Buurt",
    "verhuizen": "Gemeente en post",
    "sollicitatie": "Solliciteren",
    "cv": "Solliciteren",
    "dokter": "Afspraken",
    "tandarts": "Afspraken",
    "afspraak": "Mensen",
    "bejaard": "Zorg voor iemand anders",
}

# ---------------------------------------------------------------------------
# Seed from the game word banks. A game-only word takes its category's world.
# Owner's ruling: countries are worth keeping (nuttig); cities, mountains,
# dinosaurs and mythology are not (laag).
# ---------------------------------------------------------------------------

SPEL_MAP = {
    "animals": ("algemeen", "nuttig"),
    "insects": ("algemeen", "nuttig"),
    "marine": ("algemeen", "nuttig"),
    "nature": ("algemeen", "nuttig"),
    "oceans": ("algemeen", "nuttig"),
    "flowers": ("algemeen", "nuttig"),
    "food": ("Eten en drinken", "kern"),
    "household": ("Wonen", "kern"),
    "fashion": ("Kleding", "kern"),
    "professions": ("Werk", "kern"),
    "travel": ("Reizen", "kern"),
    "sports": ("Sport en vrije tijd", "nuttig"),
    "science": ("algemeen", "nuttig"),
    "technology": ("algemeen", "nuttig"),
    "space": ("algemeen", "nuttig"),
    "music": ("algemeen", "nuttig"),
    "art": ("algemeen", "laag"),
    "literature": ("algemeen", "nuttig"),
    "movies": ("algemeen", "nuttig"),
    "history": ("algemeen", "nuttig"),
    "countries": ("naam", "nuttig"),  # naams from this bank are gemeenten
    "cities": ("naam", "laag"),
    "mountains": ("naam", "laag"),
    "mythology": ("naam", "laag"),
    "dinosaurs": ("naam", "laag"),
    # spel:reels is a picture-tile set, not a theme: no seed.
}

# Everyday vocabulary that belongs to no product world. Animals, plants,
# weather and geography are `algemeen` or `plaats` here; a word that is also in
# a product world (`money`, `water`) is decided by the keyword table first.
EVERYDAY = [
    # (thema, gloss words)
    ("algemeen", """dog cat horse cow pig sheep chicken duck goose fish whale dolphin
        shark rabbit mouse rat fox wolf bear lion tiger elephant monkey snake frog
        turtle insect bee fly mosquito ant spider butterfly beetle worm snail crab
        seal penguin owl eagle parrot pigeon swan bird animal livestock pet horse
        kater hond kat mug mier vlinder muis beer wolf vos egel kraai meeuw
        tulip flower tree tree's root leaf bush hedge grass pine oak plant seed
        beach sand stone rock hill valley river lake sea island coast shore wave
        mountain forest field wood desert dike dyke polder canal meadow marsh
        pond spring summer autumn winter season
    """),
]

# Animals and their homes/sounds. Everyday ones (`hond`, `kat`) are `kern`.
DIEREN_KERN = set("""dog cat horse cow pig sheep chicken goat duck fish bird
    mouse rabbit bee insect animals bug pet pets""".split())

# Plants, trees and their parts.
PLANTS_GLOSS = set("""flower flowers plant plants tree trees leaf leaves branch
    branches root roots seed seeds grass bush bushes hedge hedges pine oak rose
    tulip tulips palm cactus blossom bloom petal stem stems moss fern orchid
    lily daisy violet carnation bamboo birch beech maple willow poplar shrub
    bark trunk vegetation flora weeds weed""".split())
PLANTS_KERN = set("flower flowers plant plants tree trees leaf leaves grass"
                  .split())

# Place and geography common nouns: the `plaats` bucket. Never a name.
PLAATS_GLOSS = set("""coast coasts shore border borders boundary region regions
    area areas district districts province provinces village villages town
    towns city cities country countries countryside landscape terrain valley
    valleys hill hills mountain mountains river rivers lake lakes sea ocean
    island islands dike dyke polder canal meadow desert forest forests jungle
    swamp marsh cave caves cliff cliffs dune dunes peninsula plain plains bay
    bays gulf equator hemisphere glacier volcano crater reef highland lowland
    plateau geography location place places""".split())
PLAATS_KERN = set("""place places area areas country countries border borders
    village villages town city location coast region district province
    landscape countryside mountain river sea""".split())

# Weather, sky and the natural world: no world of their own, but everyday.
WEER_KERN = set("""nature weather rain snow wind storm cloud sky sun sunshine
    frost ice thunder lightning fog heat cold warmth season spring summer
    autumn winter""".split())

# Time, number and colour words have no world of their own; they are `kern`
# and land in `algemeen` with the abstract core.
CORE_EXTRA = {
    "human": "kern", "humans": "kern", "world": "kern", "space": "kern",
    "earth": "kern", "environment": "kern", "surroundings": "kern",
    "colour": "nuttig", "colour's": "nuttig", "red": "kern", "blue": "kern",
    "green": "kern", "yellow": "kern", "black": "kern", "white": "kern",
    "brown": "kern", "grey": "kern", "gray": "kern", "purple": "nuttig",
    "pink": "nuttig",
    "monday": "kern", "tuesday": "kern", "wednesday": "kern", "thursday": "kern",
    "friday": "kern", "saturday": "kern", "sunday": "kern",
    "january": "kern", "february": "kern", "march": "kern", "april": "kern",
    "may": "kern", "june": "kern", "july": "kern", "august": "kern",
    "september": "kern", "october": "kern", "november": "kern",
    "december": "kern",
    "hour": "kern", "hours": "kern", "minute": "kern", "minutes": "kern",
    "second": "kern", "seconds": "kern", "day": "kern", "days": "kern",
    "week": "kern", "weeks": "kern", "month": "kern", "months": "kern",
    "year": "kern", "years": "kern", "today": "kern", "yesterday": "kern",
    "tomorrow": "kern", "morning": "kern", "afternoon": "kern",
    "evening": "kern", "night": "kern", "number": "kern", "numbers": "kern",
    "three": "kern", "four": "kern", "five": "kern", "six": "kern",
    "seven": "kern", "eight": "kern", "nine": "kern", "ten": "kern",
    "hundred": "kern", "thousand": "kern", "first": "kern", "second": "kern",
    "last": "kern", "plastic": "nuttig", "metal": "nuttig", "metals": "nuttig",
    "cathedral": "nuttig", "gladiator": "laag",
    "tablet": "nuttig", "dirt": "kern", "square": "nuttig", "circle": "nuttig",
}

# ---------------------------------------------------------------------------
# Gloss keyword table: theme -> list of whole words (or short phrases, written
# with underscores... no: with spaces, matched as substrings bounded by word
# edges). First world in this order that matches wins.
# ---------------------------------------------------------------------------

KEYWORDS = [
    ("Boodschappen", r"""
        supermarket groceries grocery grocery store market
        butcher bakery basket trolley price prices cheap expensive pay paying
        till cashier change change receipt receipt bill discount sale
        packet pack bag money euro
        supermarkets stores shopper
    """),
    ("Eten en drinken", r"""
        shop shops food meal meals eat eats ate eaten eating drink drinks drank drunk
        breakfast lunch dinner supper snack snackbar bread cheese butter jam
        honey meat beef pork chicken chicken's fish egg eggs milk cream
        yoghurt sugar salt pepper spice spices sauce soup salad rice pasta
        potato potatoes vegetable vegetables fruit apple apple's orange
        oranges banana bananas pear pears grape grapes lemon lemons strawberry
        strawberries cherry cherries pie cake cakes biscuit biscuits cookie
        chocolate sweets candy coffee tea beer wine juice water lemonade cola
        bottle bottle's cup cups plate plate's bowl spoon fork knife kitchen
        recipe cook cooks cooking baked fried roasted boiled hunger hungry
        thirst thirsty taste tastes delicious tasty bite sandwich ham sausage
        onion onion's garlic mushroom mushrooms bean beans nut nuts olive oil
        vinegar chips fries pancake pancakes restaurant cafes cafe menu waiter
        waitress tip vanille pizza hut pita markt bazaar
    """),
    ("Wonen", r"""
        house house's home home's room rooms living bedroom kitchen bathroom
        toilet hall corridor attic cellar basement floor floors wall walls
        roof roof's window windows door doors doorbell key keys lock lock's
        furniture table tables chair chairs bed beds sofa couch cupboard closet
        bed bag bed linen bedclothes bedsheets sheet sheets duvet pillowcase
        wardrobe drawer drawers shelf shelves pillow blanket blanket's carpet
        carpet's curtain curtains lamp lamps light bulb mirror tap faucet sink
        bath shower heater radiator garage garden yard fence stair stairs
        staircase lift elevator rent rents tenant landlord mortgage cleaning
        clean soap brush broom vacuum bin rubbish trash bucket towel towels
        electricity heating gas dish dishes pot pan pans kettle fridge
        refrigerator freezer oven stove cooker microwave washing flat flats
        apartment apartments studio villa castle construct construction
        repair repairs leak leaking ceiling ceiling's doorstep gate gates
        klus klussen boor spijker plugs stekker stroom
    """),
    ("Kleding", r"""
        cloth clothes clothing wear wears wearing wore worn dress dresses
        shirt shirts blouse skirt trousers pants jeans jacket coats coat
        raincoat sweater jumper cardigan socks sock shoe shoes boots hat hats
        cap caps scarf gloves glove belt ties tie buttons button pocket
        pockets sleeve sleeves collar size sizes gingham trendy uniform
        necklace ring rings earring bracelet purse handbag handbag's
        wallet umbrella fabric cotton wool silk leather sew needle knitting
        tights pyjamas underwear bra hanger vicuna
    """),
    ("Werk", r"""
        work works worked working job jobs profession career employer
        employers employee employees boss manager managers office staff
        colleague colleagues wage wages shop assistant farmer builder plumber
        electrician painter baker butcher mechanic mechanics salesperson
        secretary accountant engineer lawyer judge judges crew team worker
        workers labour trade craft skill shift overtime workmate workplace
        factory factories truck driver loader
    """),
    ("Solliciteren", r"""
        apply applies applied application applications interview interviews
        vacancy vacancies cv motivation cover letter sacked fired fired
        promotion internship sollicitation
    """),
    ("Bank en geld", r"""
        money money's bank accounts account banknote payment payments
        price prices cost costs cheap expensive rich poor wealth debt debts
        loan loans credit borrow lends owe owes invoice invoices receipt
        profit loss losses invest invests investment budget cashier savings
        save spends spent income tax taxes insurance bill bills finance
        financial cheaper cheapest discount discounts value worth bonus salary
        pocket euro cent cents coin coins
    """),
    ("Telefoon en internet", r"""
        internet website sites phone phones mobile telephone email emails
        software program programs battery batteries invention inventions invent
        invented discovery data digital network networks wire wires cable cables
        screen keyboard download upload modem printer laptop telecom sim
        wifi bluetooth broadband provider subscription contract
    """),
    ("Gezondheid", r"""
        ill illness sick sickness disease disease's pain painful ache hurt
        injury wound scar fever cough flu headache medicine medicines pill
        pills tablet drugs drug pharmacy hospital doctor doctors nurse dentist
        surgeon patient therapy treatment cure heal healthy health breathing
        breathe breath blind deaf lame disability disabled wheelchair
        operation surgery plaster stitches ambulance emergency prescription
        appointment
    """),
    ("Het lichaam", r"""
        head face eye eyes ear ears nose mouth tooth teeth lip lips tongue
        neck throat chin cheek cheeks forehead hair skin blood heart heart's
        lung lungs stomach belly liver kidney kidneys brain bone bones muscle
        muscles nerve vein finger fingers thumb fingertip toe toes hip hips
        arm arms elbow wrist shoulder shoulders chest breast back back's leg
        legs knee ankle foot feet body flesh sweat tear tears beard moustache
        bald skinny
    """),
    ("Mensen", r"""
        man men woman women boy boys girl girls child children kid kids baby
        babies person persons people human humans family families father
        fathers mother mothers dad mum mom parent parents son sons daughter
        daughters brother brothers sister sisters grandpa grandma grandfather
        grandmother uncle uncle aunt aunts cousin cousins nephew niece husband
        husbands wife wives partner partners married marriage marriages
        wedding weddings divorced divorce friend friends friendship adult
        adults elderly youth teenager teenagers relative relatives guests
        guest stranger strangers couples couple male female lady queen king
        prince princess dame widow orphan Dutchman visitor guest's neighbours
        neighbour neighbour's hug birthday
    """),
    ("Kinderen en school", r"""
        school schools pupil pupils student students teacher teachers lesson
        lessons class classes course courses study studies studied learn
        learns learned learnt university universities college college
        education degree degrees diploma diploma homework explain explains
        explanation explanations meaning means example examples conversation
        conversations pronounce pronunciation exercise exercises practise
        practice talk talks talking listening reading writing writes write
        wrote written essay essays knowledge subject subjects exam exams test
        tests dictionary dictionaries crèche playground juf meester
    """),
    ("Gemeente en post", r"""
        government governments municipality municipal council permit permits
        form forms envelope envelopes passport passports identity id citizen
        citizens registration registered licence licence municipality
        stamp letterbox mailbox postcode envelope signing signature
        declaration official office offices
    """),
    ("Formulieren", r"""
        form formula fill filling signature signing declaration
        signed undersign initials
    """),
    ("Reizen", r"""      
        road roads street street's highway highways lane pavement sidewalk
        crossroad crossroads junction junctions traffic jam car cars bus buses
        tram trams train trains metro subway taxi taxis bike bikes bicycle
        motorbike scooter lorry truck trucks van vans boat boats ship ships
        ferry plane planes aeroplane airplane flight flights airport airports
        station stations platform platforms passenger passengers seat seats
        ticket tickets fare journey journeys trip trips travel
        traveller traveler tourist tourists luggage suitcase suitcases
        backpack visa visas crossing arrive arrives arrived arrival depart
        departure leave leaves leaving drive drives driven ride rides ridden
        flew flown sail sails harbour harbor port ports bridge bridges tunnel
        tunnels delay delays wheel wheels tyre tyre's brake brakes parking
        parked driving licence travelling tourism safari holiday holidays
        vacation holidays abroad kaartje kaartjes
    """),
    ("De weg", r"""
        map map's route routes direction directions straight
        towards nearby opposite corner corners sign signs crossroads
        traffic-light roundabout avenue
    """),
    ("Afspraken", r"""
        appointment appointments meet meets arranged arrange cancel cancel
        postponed date agenda deadline invitation
    """),
    ("Buurt", r"""
        neighbourhood neighbour neighbours neighbour's street hallway shared
        noise nuisance overlast block doorbell
        fence garden street
    """),
    ("Sport en vrije tijd", r"""
        sport sports play plays played playing game games match matches team
        teams ball balls score scores goal goals player players trainer
        trainers coach coaches competition championship championships league
        leagues running run runs ran swim swims swimming cycle cycling
        football soccer tennis golf hockey boxing boxen wrestle wrestling
        skiing ski skate skating hobby hobbies leisure entertainment party
        parties festival festivals club clubs membership memberships gym
        fitness tournament champion champions trophy fan fans supporter
        supporters cheer dances dance dancing yoga cards chess toy toys
        activity
    """),
    ("Nood en politie", r"""
        police crime crimes criminal criminals prison prisons punishment
        court courts law laws legal illegal justice judge judges election
        elections vote voted politics politician minister ministers president
        mayor parliament democracy war wars army armies soldier soldiers
        peace enemy enemies weapon weapons theft stolen steal thief rob
        robbery fire firefighter emergency alarm accident crash ambulance 112
        report reported arrest arrested
    """),
    ("Klachten", r"""
        complaint complaints complain broken refund exchange warranty faulty
        return returns repair repairs escalate manager service guarantee
    """),
    ("Mening geven", r"""
        opinion opinions agree agrees disagree disagree, think thinks
        believes belief reason reasons discuss discussion argument claim
        claims argue suggest suggestion position stand position protest
    """),
    ("Zorg voor iemand anders", r"""
        care cares caring elderly handicapped handicap dependant dependent
        """
    ),
    ("Bellen", r"""
        call calls calling phone phone's telephone ring rings rang call back
        voicemail mobile dial operator
    """),
    ("Mensen", r"""
        feeling feelings emotion emotions happy happiness glad joy sad sadness
        unhappy angry anger afraid fear fears scared worried worry worries
        anxious nervous stress stressed calm relaxed bored boring love loves
        loved loving like likes liked hate hates hated hope hopes hoped wish
        wishes wished proud shy brave kind friendly honest polite rude lazy
        patient impatient funny fun serious surprised surprise surprises
        jealous lonely alone tired tiredness mood moods character characters
        personality attitude sorry laugh laughs laughed smile smiles smiled
        laughing cry cries cried crying curious courage trust distrust
        disappointed disappointment grateful ashamed guilty shame shy
        confidence hospitable
    """),
]

KEYWORD_LIST = [(t, [p for p in block.split() if p]) for t, block in KEYWORDS]

# Abstract glosses that borrow a world's word. Checked before the keyword table.
ABSTRACT_GLOSS = set("""
    form forms shape board figure branch scale flight play drop fall pass
    stand train bank note count run deal change return lead matter issue form
    order light house store field yard camp share interest sale course test
    subject practice ring tie land lot line point case right left back top
    bottom mark seat guard watch rule
""".split())
# Number words: a function word, but the first months need them.
NUMBERS = set("""one two three four five six seven eight nine ten eleven twelve
    thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty
    thirty forty fifty sixty seventy eighty ninety hundred thousand million
    billion zero nought a an
    first second third fourth fifth sixth seventh eighth ninth tenth
    eleventh twelfth""".split())

def is_number(en_low, raw=""):
    """`twenty-four`, `a hundred and one`, `1 000` are all numbers.

    Hyphens split into parts, so a compound like `twenty-four` is a number even
    though the whole string never equals a NUMBERS entry. `raw` is the gloss
    before norm_gloss() stripped the `a)`/`b)` markers: `1) the 2) it` is a
    numbered gloss, not a number.
    """
    if re.search(r"\d\)", raw or en_low):
        return False
    if any(ch.isdigit() for ch in en_low):
        return True
    parts = [p for p in re.split(r"[-\s]+", en_low) if p and p != "and"]
    return bool(parts) and all(p in NUMBERS for p in parts)

# Abstract words that are also the everyday thing: these keep their world.
CONCRETE_GLOSS = set("back top point line house head form board".split())
EVERYDAY_LIST = [(t, set(block.split())) for t, block in EVERYDAY]

# ---------------------------------------------------------------------------
# Overrides, keyed by lemma (`@nl:`) or gloss (`@en:`). Value is
# (thema, prioriteit); optional `thema_ook` follows in THEME_ALSO.
# ---------------------------------------------------------------------------

OVERRIDES = {
    # proper-noun sweep: countries stay (nuttig), the rest is `laag`
    "@nl:nederland": ("naam", "nuttig"),
    "@nl:nederlands": ("naam", "kern"),  # the language, met on day one
}


OVERRIDES.update({
    "@nl:aantal": ("algemeen", "kern"),
    "@nl:nummer": ("algemeen", "kern"),
    "@nl:cijfer": ("algemeen", "kern"),
    "@nl:grootte": ("algemeen", "kern"),
    "@nl:rechterhand": ("Het lichaam", "kern"),
    "@nl:regelrecht": ("algemeen", "kern"),
    "@nl:toepassing": ("algemeen", "kern"),
    "@nl:geheimschrift": ("algemeen", "nuttig"),
    "@nl:formule": ("algemeen", "nuttig"),
    "@nl:portaal": ("Telefoon en internet", "nuttig"),
    "@nl:periscoop": ("algemeen", "laag"),
    "@nl:garnaal": ("algemeen", "nuttig"),
    "@nl:schrappen": ("algemeen", "kern"),
    "@nl:terugkeren": ("algemeen", "kern"),
    "@nl:vzw": ("Zorg voor iemand anders", "nuttig"),
    "@nl:inrichten": ("Wonen", "kern"),
    "@nl:inbouwen": ("Wonen", "kern"),
    "@nl:onderwerpen": ("algemeen", "kern"),
    "@nl:opvangen": ("Zorg voor iemand anders", "nuttig"),
    "@nl:engel": ("algemeen", "nuttig"),
    "@nl:hopelijk": ("algemeen", "kern"),
    "@nl:verandering": ("algemeen", "kern"),
    "@nl:toenmalig": ("algemeen", "kern"),
    "@nl:zeshonderd": ("algemeen", "kern"),
    "@nl:premier": ("Gemeente en post", "kern"),
    "@nl:staatssecretaris": ("Gemeente en post", "nuttig"),
    "@nl:senator": ("Gemeente en post", "nuttig"),
    "@nl:socialistisch": ("algemeen", "nuttig"),
    "@nl:staking": ("Nood en politie", "nuttig"),
    "@nl:afstuderen": ("Kinderen en school", "kern"),
    "@nl:photograaf": ("algemeen", "kern"),
    "@nl:fotograaf": ("algemeen", "kern"),
    "@nl:zorg": ("Zorg voor iemand anders", "kern"),
    # first world-coverage pass: gloss keywords that land a word in a world it
    # is not in, plus everyday words no world table caught
    "@nl:ligging": ("plaats", "kern"),
    "@nl:landschap": ("plaats", "nuttig"),
    "@nl:aanklacht": ("Nood en politie", "nuttig"),
    "@nl:aanvragen": ("Gemeente en post", "kern"),
    "@nl:aanvraag": ("Gemeente en post", "kern"),
    "@nl:terugblikken": ("algemeen", "nuttig"),
    "@nl:terugkeer": ("algemeen", "kern"),
    "@nl:mentor": ("Kinderen en school", "kern"),
    "@nl:sergeant": ("Nood en politie", "nuttig"),
    "@nl:samurai": ("naam", "laag"),
    "@nl:samoerai": ("naam", "laag"),
    "@nl:mouw": ("Kleding", "kern"),
    "@nl:opsteken": ("algemeen", "kern"),
    "@nl:baan": ("Werk", "kern"),
    "@nl:links": ("De weg", "kern"),
    "@nl:rechts": ("De weg", "kern"),
    "@nl:recht": ("algemeen", "kern"),
    "@nl:recht (noun)": ("Gemeente en post", "kern"),
    "@nl:recht (adj)": ("algemeen", "kern"),
    "@nl:terug naar": ("De weg", "kern"),
    "@nl:door": ("De weg", "kern"),
    "@nl:langs": ("De weg", "kern"),
    "@nl:kader": ("algemeen", "nuttig"),
    "@nl:respecteren": ("algemeen", "kern"),
    "@nl:respeteren": ("algemeen", "nuttig"),
    "@nl:tegendeel": ("Mening geven", "nuttig"),
    "@nl:burgemeester": ("Gemeente en post", "kern"),
    "@nl:parlementslid": ("Nood en politie", "nuttig"),
    "@nl:rechercheur": ("Nood en politie", "nuttig"),
    "@nl:arrestatie": ("Nood en politie", "kern"),
    "@nl:koers": ("algemeen", "nuttig"),
    "@nl:regie": ("algemeen", "nuttig"),
    "@nl:vormen": ("algemeen", "kern"),
    "@nl:verzorgen": ("Zorg voor iemand anders", "nuttig"),
    "@nl:verzorging": ("Zorg voor iemand anders", "nuttig"),
    "@nl:reus": ("algemeen", "nuttig"),
    "@nl:dickens": ("naam", "laag"),
    "@nl:abrupt": ("algemeen", "kern"),
    "@nl:ruil": ("Klachten", "kern"),
    "@nl:student": ("Kinderen en school", "kern"),
    "@nl:bestaand": ("Telefoon en internet", "nuttig"),
    "@nl:kiezer": ("Nood en politie", "nuttig"),
    "@nl:rijke": ("Bank en geld", "nuttig"),
    "@nl:wijk": ("Buurt", "kern"),
    "@nl:pauze": ("Kinderen en school", "kern"),
    "@nl:acht": ("algemeen", "kern"),
    "@nl:achttien": ("algemeen", "kern"),
    "@nl:derde": ("algemeen", "kern"),
    "@nl:dertien": ("algemeen", "kern"),
    "@nl:dertig": ("algemeen", "kern"),
    "@nl:drie": ("algemeen", "kern"),
    "@nl:duizend": ("algemeen", "kern"),
    "@nl:een": ("algemeen", "kern"),
    "@nl:eerste": ("algemeen", "kern"),
    "@nl:elf": ("algemeen", "kern"),
    "@nl:honderd": ("algemeen", "kern"),
    "@nl:miljoen": ("algemeen", "kern"),
    "@nl:negen": ("algemeen", "kern"),
    "@nl:negentien": ("algemeen", "kern"),
    "@nl:negentig": ("algemeen", "kern"),
    "@nl:tachtig": ("algemeen", "kern"),
    "@nl:tien": ("algemeen", "kern"),
    "@nl:twaalf": ("algemeen", "kern"),
    "@nl:twee": ("algemeen", "kern"),
    "@nl:tweede": ("algemeen", "kern"),
    "@nl:twintig": ("algemeen", "kern"),
    "@nl:veertien": ("algemeen", "kern"),
    "@nl:veertig": ("algemeen", "kern"),
    "@nl:vier": ("algemeen", "kern"),
    "@nl:vierde": ("algemeen", "kern"),
    "@nl:vijf": ("algemeen", "kern"),
    "@nl:vijfde": ("algemeen", "kern"),
    "@nl:vijftien": ("algemeen", "kern"),
    "@nl:vijftig": ("algemeen", "kern"),
    "@nl:zes": ("algemeen", "kern"),
    "@nl:zestien": ("algemeen", "kern"),
    "@nl:zestig": ("algemeen", "kern"),
    "@nl:zeven": ("algemeen", "kern"),
    "@nl:zeventien": ("algemeen", "kern"),
    "@nl:zeventig": ("algemeen", "kern"),
    "@nl:plat": ("algemeen", "kern"),
    "@nl:klauw": ("algemeen", "nuttig"),
    "@nl:snuisterij": ("Kleding", "nuttig"),
    "@nl:filter": ("Wonen", "kern"),
    "@nl:melding": ("Nood en politie", "kern"),
    "@nl:inlichting": ("algemeen", "kern"),
    "@nl:teken": ("De weg", "kern"),
    "@nl:nuchter": ("algemeen", "kern"),
    "@nl:plaatsvinden": ("algemeen", "kern"),
    "@nl:voltrekken": ("algemeen", "kern"),
    "@nl:nerveus": ("Mensen", "kern"),
    "@nl:model": ("algemeen", "kern"),
    "@nl:instelling": ("algemeen", "kern"),
    "@nl:merkwaardig": ("algemeen", "kern"),
    "@nl:ernstig": ("algemeen", "kern"),
    "@nl:houding": ("algemeen", "kern"),
    "@nl:kreet": ("algemeen", "nuttig"),
    "@nl:geschikt": ("algemeen", "kern"),
    "@nl:politiek (adj)": ("Nood en politie", "nuttig"),
    "@nl:politie": ("Nood en politie", "kern"),
    "@nl:fractie": ("Gemeente en post", "nuttig"),
    "@nl:lijsttrekker": ("Nood en politie", "nuttig"),
    "@nl:aanhanger": ("algemeen", "kern"),
    "@nl:aanloop": ("algemeen", "nuttig"),
    "@nl:aanrijden": ("algemeen", "kern"),
    "@nl:doelstelling": ("algemeen", "kern"),
    "@nl:overeenkomen": ("algemeen", "kern"),
    "@nl:concurrentie": ("Werk", "kern"),
    "@nl:conditie": ("Sport en vrije tijd", "nuttig"),
    "@nl:begeleiden": ("algemeen", "kern"),
    "@nl:evenwicht": ("algemeen", "kern"),
    "@nl:gewichtheffen": ("Sport en vrije tijd", "nuttig"),
    "@nl:medaille": ("Sport en vrije tijd", "nuttig"),
    "@nl:rugzak": ("Reizen", "kern"),
    "@nl:koffie": ("Eten en drinken", "kern"),
    "@nl:kop": ("Eten en drinken", "kern"),
    "@nl:kopje": ("Eten en drinken", "kern"),
    "@nl:gegevens": ("Gemeente en post", "kern"),
    "@nl:telefoonnummer": ("Bellen", "kern"),
    "@nl:digitale": ("Telefoon en internet", "kern"),
    "@nl:digtaal": ("Telefoon en internet", "kern"),
    "@nl:computer": ("Telefoon en internet", "kern"),
    "@nl:online": ("Telefoon en internet", "kern"),
    "@nl:toegang": ("Telefoon en internet", "kern"),
    "@nl:wachtwoord": ("Telefoon en internet", "kern"),
    "@nl:app": ("Telefoon en internet", "kern"),
    "@nl:applicatie": ("Telefoon en internet", "kern"),
    "@nl:e-mail": ("Telefoon en internet", "kern"),
    "@nl:mail": ("Telefoon en internet", "kern"),
    "@nl:mailen": ("Telefoon en internet", "kern"),
    "@nl:bericht": ("Telefoon en internet", "kern"),
    "@nl:verduidelijken": ("algemeen", "kern"),
    "@nl:spijt": ("Mensen", "kern"),
    "@nl:geboorte": ("Mensen", "kern"),
    "@nl:kerel": ("Mensen", "kern"),
    "@nl:kleuter": ("Kinderen en school", "kern"),
    "@nl:crèche": ("Kinderen en school", "kern"),
    "@nl:creche": ("Kinderen en school", "kern"),
    "@nl:oppas": ("Kinderen en school", "kern"),
    "@nl:failliet": ("Bank en geld", "kern"),
    "@nl:vergoeding": ("Bank en geld", "kern"),
    "@nl:risico": ("Bank en geld", "kern"),
    "@nl:kapitaal": ("Bank en geld", "kern"),
    "@nl:overschot": ("Bank en geld", "nuttig"),
    "@nl:overval": ("Nood en politie", "kern"),
    "@nl:moordenaar": ("Nood en politie", "kern"),
    "@nl:verdenking": ("Nood en politie", "kern"),
    "@nl:wraak": ("Nood en politie", "nuttig"),
    "@nl:parkeren": ("Reizen", "kern"),
    "@nl:parkeerplaats": ("Reizen", "kern"),
    "@nl:parkeergarage": ("Reizen", "kern"),
    "@nl:kaartje": ("Reizen", "kern"),
    # `spel:art` drags these to laag, but their everyday sense is not art.
    "@nl:bron": ("algemeen", "kern"),
    "@nl:lijst": ("algemeen", "kern"),
    "@nl:opdracht": ("algemeen", "kern"),
    "@nl:modern": ("algemeen", "kern"),
    "@nl:installatie": ("algemeen", "nuttig"),
    "@nl:koper": ("algemeen", "kern"),
    "@nl:abstract": ("algemeen", "kern"),
    "@nl:horizon": ("algemeen", "nuttig"),
    # Real homes the gloss tables missed.
    "@nl:park": ("plaats", "kern"),
    "@nl:schuur": ("Wonen", "kern"),
    "@nl:rommel": ("Wonen", "kern"),
    "@nl:bedienen": ("Eten en drinken", "kern"),
    "@nl:pint": ("Eten en drinken", "kern"),
    "@nl:breedband": ("Telefoon en internet", "kern"),
    "@nl:aansluiting": ("Telefoon en internet", "kern"),
    "@nl:dader": ("Nood en politie", "kern"),
    "@nl:berucht": ("Nood en politie", "nuttig"),
    "@nl:ramp": ("Nood en politie", "kern"),
    "@nl:botsing": ("De weg", "kern"),
    "@nl:duiker": ("Sport en vrije tijd", "nuttig"),
    "@nl:puber": ("Kinderen en school", "kern"),
    # A play bank's name seed is not a name: `klimgordel` is a harness.
    "@nl:klimgordel": ("algemeen", "nuttig"),
    "@nl:keteldal": ("plaats", "laag"),
    # Art/cinema banks: a crew credit is not worth a picture, a style word is not.
    "@nl:aftiteling": ("algemeen", "laag"),
    "@nl:retrospectief": ("algemeen", "laag"),
    # English glosses that read as a different Dutch sense.
    "@nl:verzetten": ("algemeen", "kern"),  # to move (an appointment is afspraak)
    "@nl:uitstel": ("algemeen", "kern"),  # delay, not a travel delay only
    "@nl:loop (noun)": ("algemeen", "kern"),  # course of a river, not a school course
    "@nl:mule": ("algemeen", "nuttig"),  # a mule, not footwear
    "@nl:klipper": ("algemeen", "nuttig"),  # clipper ship
    "@nl:damast": ("algemeen", "nuttig"),  # damask, not a garment
    "@nl:wellington": ("naam", "laag"),
    # Common nouns inside a name-heavy play bank: never `naam`.
    "@nl:zadel": ("algemeen", "nuttig"),  # saddle
    "@nl:kling": ("algemeen", "nuttig"),  # blade
    "@nl:toendra": ("plaats", "nuttig"),  # tundra, geography
    # pos `name` upstream, but these are common nouns.
    "@nl:atlas": ("Kinderen en school", "nuttig"),
    "@nl:boekrol": ("algemeen", "laag"),
    "@nl:held": ("algemeen", "kern"),
    "@nl:nimf": ("algemeen", "laag"),
    "@nl:relikwie": ("algemeen", "laag"),
    "@nl:sfinx": ("algemeen", "laag"),
    "@nl:samoerai": ("algemeen", "laag"),  # a noun, not a name
    # A1 core that carries a name bank's seed (`spel:mountains`), so the weak
    # seed made it `laag`: `certain` is not encyclopaedic.
    "@nl:zeker": ("algemeen", "kern"),
    "@nl:jong": ("algemeen", "kern"),  # a dinosaur bank's `young`, but A1 core
    # B1 words carrying an art or mountain bank seed.
    "@nl:gouden": ("algemeen", "kern"),  # golden, not the art-bank sense
    "@nl:perspectief": ("algemeen", "kern"),
    "@nl:portret": ("algemeen", "nuttig"),
    "@nl:trekken": ("algemeen", "kern"),
    "@nl:tolkien": ("naam", "laag"),  # a fiction author: not for teaching
    # Body and animal words a dinosaur bank carries as `laag`.
    "@nl:kaak": ("Het lichaam", "kern"),
    "@nl:schedel": ("Het lichaam", "kern"),
    "@nl:klauw": ("algemeen", "kern"),
    "@nl:hoorn": ("Het lichaam", "kern"),  # horn; also the phone receiver
    "@nl:staart": ("algemeen", "kern"),
    "@nl:stekel": ("algemeen", "nuttig"),
    "@nl:nest": ("algemeen", "kern"),
    "@nl:kudde": ("algemeen", "nuttig"),
    "@nl:roedel": ("algemeen", "nuttig"),
    "@nl:roofdier": ("algemeen", "nuttig"),
    "@nl:vleeseter": ("algemeen", "nuttig"),
    "@nl:planteneter": ("algemeen", "nuttig"),
    "@nl:alleseter": ("algemeen", "nuttig"),
    "@nl:mammoet": ("algemeen", "nuttig"),
    # Everyday verbs/nouns a nature bank carries as `laag`.
    "@nl:graven": ("algemeen", "kern"),
    "@nl:opgraven": ("algemeen", "kern"),
    "@nl:jagen": ("algemeen", "kern"),
    "@nl:klimmen": ("algemeen", "kern"),
    "@nl:zilver": ("algemeen", "nuttig"),
    "@nl:uitgestorven": ("algemeen", "nuttig"),
    "@nl:versteend": ("algemeen", "nuttig"),
    "@nl:halte": ("Reizen", "kern"),
    "@nl:spoor": ("Reizen", "kern"),
    "@nl:spoorweg": ("Reizen", "kern"),
    "@nl:ov": ("Reizen", "kern"),
    "@nl:abonnement": ("Reizen", "kern"),
    "@nl:schutting": ("Wonen", "kern"),
    "@nl:behang": ("Wonen", "kern"),
    "@nl:behangen": ("Wonen", "kern"),
    "@nl:behanger": ("Werk", "nuttig"),
    "@nl:tegels": ("Wonen", "kern"),
    "@nl:vloeren": ("Wonen", "kern"),
    "@nl:kwast": ("Wonen", "nuttig"),
    "@nl:spons": ("Wonen", "kern"),
    "@nl:stof": ("Wonen", "kern"),
    "@nl:afwassen": ("Wonen", "kern"),
    "@nl:afwas": ("Wonen", "kern"),
    "@nl:afwasborstel": ("Wonen", "kern"),
    "@nl:stofzuigen": ("Wonen", "kern"),
    "@nl:stofzuiger": ("Wonen", "kern"),
    "@nl:dweil": ("Wonen", "kern"),
    "@nl:dweilen": ("Wonen", "kern"),
    "@nl:afstoffen": ("Wonen", "kern"),
    "@nl:strijken": ("Wonen", "kern"),
    "@nl:strijkijzer": ("Wonen", "kern"),
    "@nl:stomerij": ("Kleding", "nuttig"),
    "@nl:wasmiddel": ("Wonen", "kern"),
    "@nl:wasmachine": ("Wonen", "kern"),
    "@nl:panty": ("Kleding", "nuttig"),
    "@nl:pittig": ("Eten en drinken", "nuttig"),
    "@nl:verf": ("Wonen", "kern"),
    "@nl:wethouder": ("Gemeente en post", "kern"),
    "@nl:eclips": ("algemeen", "nuttig"),
    "@nl:pulsar": ("algemeen", "laag"),
    "@nl:penseel": ("algemeen", "nuttig"),
    "@nl:kunstenaar": ("algemeen", "nuttig"),
    "@nl:museum": ("algemeen", "nuttig"),
    "@nl:galerie": ("algemeen", "nuttig"),
    "@nl:schilderij": ("algemeen", "nuttig"),
    "@nl:tentoonstelling": ("algemeen", "nuttig"),
    "@nl:theater": ("algemeen", "nuttig"),
    "@nl:bioscoop": ("algemeen", "nuttig"),
    "@nl:film": ("algemeen", "nuttig"),
    "@nl:muziek": ("algemeen", "nuttig"),
    "@nl:concert": ("algemeen", "nuttig"),
    "@nl:boek": ("algemeen", "kern"),
    "@nl:krant": ("algemeen", "kern"),
    "@nl:marmer": ("algemeen", "nuttig"),
    "@nl:verhaal": ("algemeen", "kern"),
    "@nl:dagboek": ("algemeen", "nuttig"),
    "@nl:hallo": ("algemeen", "kern"),
    "@nl:gehandicapt": ("Zorg voor iemand anders", "nuttig"),
    "@nl:pan": ("Eten en drinken", "kern"),
    "@nl:verdwijnpunt": ("algemeen", "laag"),
    "@nl:dinges": ("algemeen", "nuttig"),
    "@nl:afspraak": ("Afspraken", "kern"),
    "@nl:afspraken": ("Afspraken", "kern"),
    "@nl:afspreken": ("Afspraken", "kern"),
    "@nl:afzeggen": ("Afspraken", "kern"),
    "@nl:annuleren": ("Afspraken", "kern"),
    "@nl:uitnodiging": ("Afspraken", "kern"),
    "@nl:uitnodigen": ("Afspraken", "kern"),
    "@nl:agenda": ("Afspraken", "kern"),
    "@nl:bel": ("Bellen", "kern"),
    "@nl:bellen": ("Bellen", "kern"),
    "@nl:opbellen": ("Bellen", "kern"),
    "@nl:terugbellen": ("Bellen", "kern"),
    "@nl:telefoon": ("Telefoon en internet", "kern"),
    "@nl:mobiel": ("Telefoon en internet", "kern"),
    "@nl:klacht": ("Klachten", "kern"),
    "@nl:klagen": ("Klachten", "kern"),
    "@nl:klachten": ("Klachten", "kern"),
    "@nl:terugbrengen": ("Klachten", "kern"),
    "@nl:stuk": ("Klachten", "kern"),
    "@nl:buurt": ("Buurt", "kern"),
    "@nl:overlast": ("Buurt", "kern"),
    "@nl:geluidsoverlast": ("Buurt", "kern"),
    "@nl:hinder": ("Buurt", "kern"),
    "@nl:portiek": ("Buurt", "kern"),
    "@nl:galerij": ("Buurt", "kern"),
    "@nl:demonstreren": ("Mening geven", "nuttig"),
    "@nl:achteren": ("De weg", "kern"),
    "@nl:kapot": ("Klachten", "kern"),
    "@nl:meer": ("algemeen", "kern"),
    "@nl:letter": ("algemeen", "kern"),
})


# words whose gloss keyword lands them in a world they are not in
OVERRIDES.update({
    "@nl:dienst": ("algemeen", "kern"),
    "@nl:dienstverlening": ("algemeen", "kern"),
    "@nl:aanleiding": ("algemeen", "kern"),
    "@nl:hof": ("algemeen", "nuttig"),
    "@nl:tribune": ("Sport en vrije tijd", "nuttig"),
    "@nl:opstaan": ("algemeen", "kern"),
    "@nl:uitsteken": ("algemeen", "nuttig"),
    "@nl:invallen": ("algemeen", "nuttig"),
    "@nl:vorderen": ("algemeen", "kern"),
    "@nl:troep": ("algemeen", "nuttig"),
    "@nl:tank": ("Reizen", "nuttig"),
    "@nl:stem": ("algemeen", "kern"),
    "@nl:stemming": ("algemeen", "kern"),
    "@nl:stemmen": ("algemeen", "kern"),
    "@nl:rapport": ("algemeen", "kern"),
    "@nl:verslag": ("algemeen", "kern"),
    "@nl:reportage": ("algemeen", "nuttig"),
    "@nl:melden": ("Nood en politie", "nuttig"),
    "@nl:positie": ("algemeen", "kern"),
    "@nl:reden": ("algemeen", "kern"),
    "@nl:bedenken": ("algemeen", "kern"),
    "@nl:nadenken": ("algemeen", "kern"),
    "@nl:menen": ("Mening geven", "kern"),
    "@nl:opeisen": ("algemeen", "nuttig"),
    "@nl:bereid": ("algemeen", "kern"),
    "@nl:afwezigheid": ("algemeen", "kern"),
    "@nl:ontslag": ("Werk", "kern"),
    "@nl:schriftelijk": ("Formulieren", "kern"),
    "@nl:onderhands": ("algemeen", "kern"),
    "@nl:geheim": ("algemeen", "kern"),
    "@nl:macht": ("algemeen", "kern"),
    "@nl:schuld": ("Bank en geld", "kern"),
    "@nl:stadium": ("algemeen", "kern"),
    "@nl:reactie": ("algemeen", "kern"),
    "@nl:ruimte": ("algemeen", "kern"),
    "@nl:schorsing": ("Werk", "nuttig"),
    "@nl:overzicht": ("algemeen", "kern"),
    "@nl:debat": ("Mening geven", "nuttig"),
    "@nl:mening": ("Mening geven", "kern"),
    "@nl:partij": ("Nood en politie", "nuttig"),
    "@nl:partijen": ("Nood en politie", "nuttig"),
    "@nl:verdrag": ("Nood en politie", "nuttig"),
    "@nl:wetgeving": ("Nood en politie", "nuttig"),
    "@nl:bezwaar": ("Klachten", "kern"),
    "@nl:bezwaarschrift": ("Formulieren", "kern"),
    "@nl:oordeel": ("Mening geven", "kern"),
    "@nl:gelijk": ("Mening geven", "kern"),
    "@nl:uitdrukking": ("algemeen", "nuttig"),
    "@nl:bijval": ("Mening geven", "nuttig"),
    "@nl:tegenspraak": ("Mening geven", "nuttig"),
    "@nl:stemming maken": ("algemeen", "nuttig"),
    "@nl:verklaring": ("Formulieren", "kern"),
    "@nl:aangifte": ("Nood en politie", "kern"),
    "@nl:aangeven": ("Formulieren", "kern"),
    "@nl:inleveren": ("Formulieren", "kern"),
    "@nl:leveren": ("algemeen", "kern"),
    "@nl:aanleveren": ("Formulieren", "kern"),
    "@nl:opsturen": ("Gemeente en post", "kern"),
    "@nl:versturen": ("Gemeente en post", "kern"),
    "@nl:zenden": ("Gemeente en post", "nuttig"),
    "@nl:post": ("Gemeente en post", "kern"),
    "@nl:postkantoor": ("Gemeente en post", "kern"),
    "@nl:brief": ("Gemeente en post", "kern"),
    "@nl:pakket": ("Gemeente en post", "kern"),
    "@nl:zegel": ("Gemeente en post", "kern"),
    "@nl:adres": ("Gemeente en post", "kern"),
    "@nl:woonplaats": ("Gemeente en post", "kern"),
    "@nl:geboortedatum": ("Formulieren", "kern"),
    "@nl:handtekening": ("Formulieren", "kern"),
    "@nl:ondertekenen": ("Formulieren", "kern"),
    "@nl:digid": ("Gemeente en post", "kern"),
    "@nl:paspoort": ("Gemeente en post", "kern"),
    "@nl:identiteitsbewijs": ("Gemeente en post", "kern"),
    "@nl:rijk": ("Bank en geld", "kern"),
    "@nl:arm": ("Bank en geld", "kern"),
    "@nl:arm (adj)": ("Bank en geld", "kern"),
    "@nl:bank": ("Bank en geld", "kern"),
    "@nl:rekening": ("Bank en geld", "kern"),
    "@nl:boodschap": ("Mensen", "kern"),  # message; the shopping try is Boodschappen
    "@nl:pinnen": ("Bank en geld", "kern"),
    "@nl:geldautomaat": ("Bank en geld", "kern"),
    "@nl:betalen": ("Bank en geld", "kern"),
    "@nl:kosten": ("Bank en geld", "kern"),
    "@nl:prijs": ("Boodschappen", "kern"),
    "@nl:goedkoop": ("Boodschappen", "kern"),
    "@nl:winkel": ("Boodschappen", "kern"),
    "@nl:supermarkt": ("Boodschappen", "kern"),
    "@nl:boodschappen": ("Boodschappen", "kern"),
    "@nl:wagen": ("Reizen", "nuttig"),
    "@nl:etage": ("Wonen", "kern"),
    "@nl:huur": ("Wonen", "kern"),
    "@nl:huurtoeslag": ("Bank en geld", "kern"),
    "@nl:zorgtoeslag": ("Bank en geld", "kern"),
    "@nl:toeslag": ("Bank en geld", "kern"),
    "@nl:uitkering": ("Bank en geld", "kern"),
    "@nl:belasting": ("Bank en geld", "kern"),
    "@nl:verzekering": ("Bank en geld", "kern"),
    "@nl:hypotheek": ("Bank en geld", "kern"),
    "@nl:loon": ("Werk", "kern"),
    "@nl:salaris": ("Werk", "kern"),
    "@nl:advocaat": ("Nood en politie", "nuttig"),
    "@nl:adviseur": ("Werk", "kern"),
    "@nl:ontslagbrief": ("Werk", "kern"),
    "@nl:contract": ("Werk", "kern"),
    "@nl:baas": ("Werk", "kern"),
    "@nl:chef": ("Werk", "kern"),
    "@nl:collega": ("Werk", "kern"),
    "@nl:kantoor": ("Werk", "kern"),
    "@nl:bijbaan": ("Werk", "kern"),
    "@nl:bijbaantje": ("Werk", "kern"),
    "@nl:opleiding": ("Kinderen en school", "kern"),
    "@nl:opleiden": ("Kinderen en school", "kern"),
    "@nl:school": ("Kinderen en school", "kern"),
    "@nl:leraar": ("Kinderen en school", "kern"),
    "@nl:lerares": ("Kinderen en school", "kern"),
    "@nl:juf": ("Kinderen en school", "kern"),
    "@nl:meester": ("Kinderen en school", "kern"),
    "@nl:kind": ("Mensen", "kern"),
    "@nl:kinderen": ("Mensen", "kern"),
    "@nl:ouders": ("Mensen", "kern"),
    "@nl:moeder": ("Mensen", "kern"),
    "@nl:vader": ("Mensen", "kern"),
    "@nl:zuster": ("Mensen", "kern"),
    "@nl:broer": ("Mensen", "kern"),
    "@nl:oma": ("Mensen", "kern"),
    "@nl:opa": ("Mensen", "kern"),
    "@nl:verjaardag": ("Mensen", "kern"),
    "@nl:feest": ("Sport en vrije tijd", "kern"),
    "@nl:ziekenhuis": ("Gezondheid", "kern"),
    "@nl:huisarts": ("Gezondheid", "kern"),
    "@nl:apotheek": ("Gezondheid", "kern"),
    "@nl:medicijn": ("Gezondheid", "kern"),
    "@nl:ziekte": ("Gezondheid", "kern"),
    "@nl:ziek": ("Gezondheid", "kern"),
    "@nl:pijn": ("Gezondheid", "kern"),
})

EN_ONLY = {
    "post": ("Gemeente en post", "kern"),
    "bank": ("Bank en geld", "kern"),
    "course": ("Kinderen en school", "kern"),
    "date": ("algemeen", "kern"),
    "test": ("Kinderen en school", "kern"),
    "art": ("Sport en vrije tijd", "nuttig"),
    "letter": ("algemeen", "kern"),
    "nummer": ("algemeen", "kern"),
    "number": ("algemeen", "kern"),
}

# Abstract verbs, adjectives and adverbs that must land in `algemeen` rather
# than a world whose keyword they happen to hit. Matching is on the exact
# lowercased gloss.
FALLBACK_GLOSS = {
    "to take", "to put", "to get", "to give", "to go", "to come", "to make",
    "to keep", "to let", "to set", "to turn", "to look", "to see", "to pass",
    "to move", "to run", "to show", "to leave", "to fall", "to find", "to call",
    "to order", "to catch", "to blow", "to bring", "to stay", "to drop",
    "to cover", "to design", "to mind", "to sound", "to push", "to lead",
    "to stick", "to stand", "to walk", "to release", "to send", "to strike",
    "to provide", "to share", "to pull", "to dress", "to build", "to reason",
    "to touch", "to sense", "to request", "to perform", "to do", "to finish",
    "to happen", "to arrange", "to lose", "to shed", "to separate", "to fear",
    "to answer", "to chat", "to serve", "to understand", "to need", "to help",
    "to occupy", "to prevent", "to ring", "to prepare", "to view", "to decide",
    "to save", "to spend", "to enter", "to regret", "to doubt", "to claim",
    "to visit", "to swear", "to meet", "to add", "to remain", "to drink",
    "to correct", "to protest", "to continue", "to extend", "to carry",
    "to overtake", "to scale", "to lift", "to cut", "to hold", "to hand",
    "to hand in", "to search", "to know", "to remind", "to show", "to work",
    "to matter", "to count", "to mean", "to apply", "to offer", "to accept",
    "to achieve", "to achieve", "to count", "to measure",
}

# ---------------------------------------------------------------------------
# Priority rules
# ---------------------------------------------------------------------------

# A lemma in these worlds is `laag` whatever the seed said is overridden above;
# an encyclopaedic one-off inside a world is caught here by gloss.
ENCYCLOPAEDIC_GLOSS = {
    "dinosaur", "dinosaur's", "god", "goddess", "temple", "myth", "legend",
    "statue", "monument", "asteroid", "meteorite", "galaxy", "theorem",
    "dynasty", "emperor", "knight", "sword", "castle", "cathedral", "folklore",
}

ABSTRACT_SUFFIX = re.compile(
    r"(heid|igheid|baarheid|zaamheid|theid|iteit|atie|ing|ment|isme|schap|"
    r"teit|iteit)$"
)


def gloss_tokens(en):
    g = en.lower()
    g = re.sub(r"\d+\s+van\s+\d+", " ", g)
    g = g.replace("/", " / ").replace("(", " ( ").replace(")", " ) ")
    g = re.sub(r"[^a-zà-öø-ÿ ]", " ", g)
    return g, g.split()


def keyword_hit(pats, gl, toks):
    for p in pats:
        if " " in p:
            if re.search(r"(?<![a-z])" + p + r"(?![a-z])", gl):
                return True
        elif p in toks:
            return True
    return False


def load_knm():
    """Hand-checked theme and priority for the KNM vocabulary.

    The KNM words are filed by the TaalCompleet word list's own eight society
    themes, which are the right evidence for a word like `kwijtschelding` or
    `verloskundige` and are not recoverable from a gloss keyword table. The
    table applies only to rows whose `herkomst` is `knm`, so it cannot disturb
    the appendix and games rows that the overrides above were tuned on.
    """
    path = os.path.join(HERE, "knm-thema.tsv")
    table = {}
    if not os.path.exists(path):
        return table
    for r in csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"):
        table[r["nl"].strip().lower()] = (r["thema"], r["prioriteit"])
    return table


KNM_THEMA = load_knm()


def load():
    words = list(csv.DictReader(open(WORDS, encoding="utf-8"), delimiter="\t"))
    pos = list(csv.DictReader(open(POS, encoding="utf-8"), delimiter="\t"))
    assert len(words) == len(pos), "row count differs"
    for w, p in zip(words, pos):
        assert w["nl"] == p["nl"], "nl differs at %r" % (w["nl"],)
        w["pos"] = p["pos"]
    return words


def seeds(herkomst):
    cats = [h.split(":", 1)[1] for h in herkomst.split(";") if h.startswith("spel:")]
    return [SPEL_MAP[c] for c in cats if c in SPEL_MAP]


def priority_for(thema, pos, en=""):
    """Priority of a word that reached `algemeen` without a world.

    `algemeen` is the B1 core the product teaches: a verb, noun or adjective
    there is `kern`. Adverbs, interjections and the like are `nuttig`.
    """
    if pos in ("verb", "adj", "noun", None):
        return "kern"
    return "nuttig"


def place_priority(toks, en_low):
    """`algemeen` fallback for the natural world and geography."""
    if set(toks) & PLAATS_GLOSS:
        return "plaats", ("kern" if set(toks) & PLAATS_KERN else "nuttig")
    if set(toks) & PLAATS_KERN and len(toks) <= 2:
        return "plaats", "kern"
    if set(toks) & WEER_KERN:
        return "algemeen", "kern"
    if set(toks) & PLANTS_GLOSS:
        return "algemeen", ("kern" if set(toks) & PLANTS_KERN else "nuttig")
    if set(toks) & DIEREN_KERN:
        return "algemeen", "kern"
    return "algemeen", priority_for("algemeen", None)


def classify(w, stats):
    nl, en, pos = w["nl"], w["en"], w["pos"]
    herkomst = w["herkomst"]
    en_low = norm_gloss(en)

    if pos == "function":
        if is_number(en_low, en):
            stats["function_number"] += 1
            return ("algemeen", "kern")
        stats["function"] += 1
        return ("algemeen", "nuttig")

    key = "@nl:" + nl
    if key in OVERRIDES:
        stats["override"] += 1
        return OVERRIDES[key]
    if en_low in EN_ONLY:
        stats["override"] += 1
        return EN_ONLY[en_low]

    # KNM rows carry their own hand-checked theme (see load_knm).
    if herkomst == "knm":
        hit = KNM_THEMA.get(nl.strip().lower())
        if hit:
            stats["knm"] += 1
            return hit

    if pos == "name":
        # Countries are worth keeping (owner's ruling): `nuttig`. Cities,
        # mountains, gods and dinosaurs are not: `laag`.
        stats["name"] += 1
        s = seeds(herkomst)
        if s and s[0][0] == "naam":
            return s[0]
        return ("naam", "nuttig")

    s = seeds(herkomst)
    has_bijlage = "bijlage8" in herkomst.split(";")
    game_only = bool(s) and not has_bijlage and pos != "name"

    if game_only:
        theme, prio = s[0]
        if theme == "naam" and pos != "name":
            # A common noun from a name-heavy bank (a mountain, a dinosaur that
            # is not itself a name) never buckets as a name: it goes to its
            # sense below, or to `algemeen`.
            stats["name_bucket_common"] += 1
        else:
            stats["seed_only"] += 1
            return (theme, prio)

    if en_low in FALLBACK_GLOSS:
        stats["fallback_gloss"] += 1
        return place_priority(en_low.split(), en_low)

    gl, toks = gloss_tokens(en)

    # A gloss word that reads like a world but names an abstract idea is off:
    # `vorm` is not a formulier, `tak` is not a branch office, `oever` is not a
    # bank. Skip the keyword table when every gloss word is abstract.
    if toks and set(toks) <= ABSTRACT_GLOSS - CONCRETE_GLOSS:
        stats["abstract_gloss"] += 1
        return place_priority(toks, en_low)

    for theme, words in EVERYDAY_LIST:
        if set(toks) & words:
            stats["everyday"] += 1
            return place_priority(toks, en_low)

    if toks and len(toks) <= 2:
        for t in toks:
            if t in CORE_EXTRA:
                stats["core_extra"] += 1
                return ("algemeen", CORE_EXTRA[t])

    for theme, pats in KEYWORD_LIST:
        if pos == "verb" and theme in {"Bellen", "De weg", "Afspraken",
                                       "Klachten", "Buurt", "Kleding"}:
            continue  # these worlds are driven by nouns; a verb there is off
        if keyword_hit(pats, gl, toks):
            stats["keyword"] += 1
            if toks and set(toks) & ENCYCLOPAEDIC_GLOSS:
                return (theme, "laag")
            return (theme, THEME_PRIO.get(theme, priority_for(theme, pos)))

    if s:
        stats["seed_weak"] += 1
        if s[0][0] == "naam":
            # A name bank's seed on a common noun (`zeker`, `gletsjer`) is not
            # a name: keep the word out of `naam` and take the bank's priority,
            # which for mountains/dinosaurs/mythology is `laag`.
            return ("algemeen", s[0][1])
        return s[0]

    prio = place_priority(toks, en_low)
    stats["fallback_" + pos] += 1
    return prio


def norm_gloss(en):
    """Lowercase gloss with the numbering and case markers taken off.

    `a) to settle the bill b) to judge (on)` -> `to settle the bill to judge on`
    `May 72 van 148` -> `may`  -- but `kick-off`, `(well-)known` keep their
    sense, so only the markers are removed.
    """
    g = en.lower()
    g = re.sub(r"\b\d+\s+van\s+\d+", " ", g)
    g = re.sub(r"\b[a-z]\)\s*", " ", g)
    g = g.replace("(", " ").replace(")", " ")
    g = re.sub(r"\s+", " ", g).strip(" ,.;")
    return g


def secondary(thema, nl, en):
    """thema_ook: only where the product genuinely puts the word in two worlds."""
    ook = THEME_ALSO.get(nl)
    if not ook:
        return ""
    parts = [p for p in ook.split(";") if p and p != thema]
    return ";".join(parts)


def check_tables():
    """Every table that is a dict literal must have no shadowed key.

    A duplicated OVERRIDES key is invisible: the last one wins and the earlier
    one is dead. That bit twice during authoring, so it is asserted here.
    """
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    for name in ("OVERRIDES", "EN_ONLY", "THEME_ALSO", "SPEL_MAP"):
        start = src.index(name + " = {")
        end = src.index("\n}", start)
        keys = re.findall(r'^\s*"([^"]+)":', src[start:end], re.M)
        dupes = {k for k in keys if keys.count(k) > 1}
        assert not dupes, "duplicate %s keys: %s" % (name, sorted(dupes))


def main():
    check_tables()
    words = load()
    stats = Counter()
    rows = []
    for w in words:
        thema, prio = classify(w, stats)
        # `kern` is the teaching core, so a word that only entered from the
        # frequency extension cannot be it: the appendix already holds the
        # 5,000 most frequent lemmas, and these are what lies beyond. Without
        # this the bucket collapses, because every `algemeen` noun, verb and
        # adjective reaches `kern` whatever its frequency. A KNM row is exempt:
        # its priority is hand-checked against the inburgering word list, which
        # is better evidence than frequency.
        if prio == "kern" and w["herkomst"] == "kaikki":
            prio = "nuttig"
            stats["cap_beyond_5000"] += 1
        assert thema in THEMES, "bad theme %r" % (thema,)
        assert prio in PRIOS, "bad priority %r" % (prio,)
        rows.append((w["nl"], thema, secondary(thema, w["nl"], w["en"]), prio, w["en"]))

    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        fh.write("nl\tthema\tthema_ook\tprioriteit\ten\n")
        for nl, thema, ook, prio, en in rows:
            assert "\t" not in nl and "\t" not in en
            fh.write("%s\t%s\t%s\t%s\t%s\n" % (nl, thema, ook, prio, en))

    print("rows written:", len(rows))
    print("\nper thema:")
    for t, n in Counter(r[1] for r in rows).most_common():
        print("  %-26s %5d  %5.1f%%" % (t, n, 100.0 * n / len(rows)))
    print("\nper prioriteit:")
    for p, n in Counter(r[3] for r in rows).most_common():
        print("  %-8s %5d  %5.1f%%" % (p, n, 100.0 * n / len(rows)))
    print("\nthema_ook filled:", sum(1 for r in rows if r[2]))
    print("\npipeline:")
    for k, n in sorted(stats.items()):
        print("  %-30s %5d" % (k, n))

    rng = random.Random(SAMPLE_SEED)
    by_theme = defaultdict(list)
    for i, r in enumerate(rows):
        by_theme[r[1]].append(i)
    sample = []
    for t in sorted(by_theme):
        sample.extend(rng.sample(by_theme[t], min(3, len(by_theme[t]))))
    sample = sample[:78]  # never overdraw; the rest is uniform from the file
    taken = set(sample)
    rest = [i for i in range(len(rows)) if i not in taken]
    sample.extend(rng.sample(rest, 100 - len(sample)))
    sample = sorted(sample)[:100]
    print("\nsample (seed %d):\n" % SAMPLE_SEED)
    print("row\tnl\tthema\tthema_ook\tprioriteit\ten\tpos\therkomst")
    for i in sample:
        w = words[i]
        print("%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            i + 2, w["nl"], rows[i][1], rows[i][2], rows[i][3], w["en"],
            w["pos"], w["herkomst"]))
    print("\nsample rows: %d" % len(sample))


if __name__ == "__main__":
    main()
