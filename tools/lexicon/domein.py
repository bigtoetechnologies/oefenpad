#!/usr/bin/env python3
"""Classify tools/lexicon/woorden.tsv by semantic domain.

Writes tools/lexicon/woorden-domein.tsv:
    nl<TAB>domein<TAB>en
one row per input row, same order, `nl` byte-identical.

The domain axis is a second classification, independent of the 24 product
themes in `woorden-thema.tsv`. The themes are *situations* — a supermarket, a
doctor's appointment — and they leave 7,421 of 10,000 words in `algemeen`,
which is a bucket, not a category. The domain axis is the *semantic field*:
what kind of thing the word names, whatever the situation.

This file replaces the earlier method of slicing the list into six files and
having an agent read them. That method was not reproducible and the labels it
produced were close to random (`atoom` -> Names, `zullen` -> Names, `zus` ->
Food & drink, `zweden` -> Body & health). The tell was the distribution: every
label landed near 1/30 of the list, which is what a scatter produces, not a
classifier. The slices were deleted; this script is the only source.

Pipeline, first match wins:

   0. structural: pos function -> Function words; pos name or theme naam -> Names
   1. curated overrides (OVERRIDES) for words the rules get wrong
   2. gloss/lemma keyword table (RULES), most specific domain first
   3. Dutch suffix table (SUFFIX_RULES) for compounds the gloss misses
   4. game seed from `herkomst` (GAME_SEED) — a word in the dinosaurs game is
      an animal even if no keyword fired
   5. theme seed from `woorden-thema.tsv` (THEME_SEED)
   6. fallback: Abstract & general

Rules 0, 1 and 2 also encode the two invariants the old files broke: a
`pos=function` word is always `Function words` and a proper name is always
`Names`. Those are applied structurally, so they cannot drift.

Deterministic: no randomness, no network, local Python only. The 100-row hand
check is printed under a fixed seed, so it is the same sample forever.
"""

import os
import random
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
WOORDEN = os.path.join(HERE, "woorden.tsv")
POS = os.path.join(HERE, "woorden-woordsoort.tsv")
THEMA = os.path.join(HERE, "woorden-thema.tsv")
OUT = os.path.join(HERE, "woorden-domein.tsv")

SAMPLE_SEED = 20261117

# ---------------------------------------------------------------------------
# The taxonomy. Mirrors DOMAINS in bouw-viewer.py; the viewer refuses the file
# if a label is outside this set.
# ---------------------------------------------------------------------------

DOMAINS = [
    "People & relations", "Body & health", "Food & drink",
    "Clothing & appearance", "House & home", "Work & jobs",
    "Money & trade", "Transport & travel", "Nature & weather", "Animals",
    "Plants & farming", "Places & geography", "Time", "Quantity & measure",
    "Movement & position", "Thought & knowledge", "Communication & language",
    "Emotion & feeling", "Character & behaviour", "Society & politics",
    "Law & conflict", "War & military", "Education & learning",
    "Technology & tools", "Arts & media", "Sport & games",
    "Religion & belief", "Abstract & general", "Function words", "Names",
]
ALLOWED = set(DOMAINS)
ABSTRACT = "Abstract & general"

# ---------------------------------------------------------------------------
# Curated overrides. Only for words where the keyword table demonstrably
# misfires. Keyed by the `nl` lemma, lowercase.
# ---------------------------------------------------------------------------

OVERRIDES = {
    # gloss ambiguity: "court" beats "dish" for gerecht
    "gerecht": "Law & conflict",
    "bank": "Money & trade",
    "hof": "Society & politics",
    "sinaasappel": "Food & drink",
    "sediment": "Nature & weather",
    "hogeschool": "Education & learning",
    "zwaard": "War & military",
    "speer": "War & military",
    "schaal": "Quantity & measure",
    "schaduw": "Nature & weather",
    "schade": "Money & trade",
    "stem": "Communication & language",
    "stemming": "Emotion & feeling",
    "stemmen": "Society & politics",
    "stelling": "Thought & knowledge",
    "samenleven": "People & relations",
    "terugreis": "Transport & travel",
    "verblijfsvergunning": "Society & politics",
    "verschuiving": "Movement & position",
    "waterland": "Nature & weather",
    "aanbidden": "Religion & belief",
    "alinea": "Communication & language",
    "belastinggeld": "Money & trade",
    "beveiliger": "Work & jobs",
    "skelet": "Body & health",
    "veranda": "House & home",
    "zeespiegel": "Nature & weather",
    "zuurstof": "Nature & weather",
    "zwaartekracht": "Nature & weather",
    "mythe": "Religion & belief",
    "mythologie": "Religion & belief",
    "zwartgat": "Nature & weather",
    "zwarteweduwe": "Animals",
    "stekmug": "Animals",
    "gebruik": "Abstract & general",
    "zaak": "Abstract & general",
    "geval": "Abstract & general",
    "aard": "Character & behaviour",
    "neuken": "People & relations",
    "respectievelijk": "Abstract & general",
    "stal": "Plants & farming",
    "register": "Arts & media",
    "opzet": "Thought & knowledge",
    "zending": "Transport & travel",
    "receptie": "House & home",
    "schoonzoon": "People & relations",
    "schoondochter": "People & relations",
    "schoonvader": "People & relations",
    "schoonmoeder": "People & relations",
    "vn": "Society & politics",
    # polysemous or abstract-sense words the keyword table reads literally
    "zeggenschap": "Society & politics",
    "oever": "Nature & weather",
    "niveau": "Quantity & measure",
    "dagen": "Time",
    "pickel": "Sport & games",
    "hok": "House & home",
    "verlof": "Work & jobs",
    "vakblad": "Work & jobs",
    "contra-expertise": "Law & conflict",
    "gedegen": "Abstract & general",
    "portefeuille": "Money & trade",
    "vermoeidheid": "Body & health",
    "sportief": "Sport & games",
    "onttrekken (zich)": "Money & trade",
    "manipuleren": "Character & behaviour",
    # audit-round-2 collisions the keyword table cannot resolve
    "rechercheur": "Law & conflict",
    "aanduiding": "Communication & language",
    "gelijkvloers": "Movement & position",
    "bewerkstelligen": "Abstract & general",
    "opstarten": "Technology & tools",
    "jonker": "People & relations",
    "omwille": "Function words",
    "opleiden": "Education & learning",
    "alom": "Movement & position",
    "aangeven": "Communication & language",
    "aanbrengen": "Movement & position",
    "overhandigen": "Movement & position",
    "linkerhand": "Body & health",
    "rechterhand": "Body & health",
    "hand": "Body & health",
    "langzamerhand": "Time",
    "naderhand": "Time",
    # third audit round: English homographs and compound leakage
    "hittegolf": "Nature & weather",
    "diplomatie": "Society & politics",
    "gemeen": "Character & behaviour",
    "rondom": "Movement & position",
    "tip": "Communication & language",
    "interesse": "Emotion & feeling",
    "interesseren": "Emotion & feeling",
    "veruit": "Quantity & measure",
    "overlaten": "Abstract & general",
    "doorzoeken": "Thought & knowledge",
    "inleveren": "Abstract & general",
    "bekleden": "Work & jobs",
    "diepzeetrog": "Nature & weather",
    "hoogtepunt": "Abstract & general",
    "voorzitter": "Work & jobs",
    "voorbeeld": "Abstract & general",
    "warenhuis": "Money & trade",
    "stroomgebied": "Places & geography",
    "opgroeien": "People & relations",
    "bijvoorbeeld": "Function words",
    # the game banks seed the domain by game, which mislabels a few ordinary
    # words: luifel is an awning over a door, not a cinema artefact. Its gloss
    # keeps the game's sense ("marquee") because that is how `spel:movies` uses it.
    "luifel": "House & home",
}

# The coursebook additions of 2026-11: the keyword table read these literally
# (`head of department` became Body & health, `main course` Education).
OVERRIDES.update({
    "afdelingshoofd": "Work & jobs",
    "bijwerking": "Body & health",
    "beterschap": "Body & health",
    "goedkomen": "Abstract & general",
    "klamboe": "House & home",
    "loonschaal": "Work & jobs",
    "medestander": "People & relations",
    "moedertaalspreker": "Communication & language",
    "olielamp": "House & home",
    "onderuitgaan": "Movement & position",
    "pieken": "Abstract & general",
    "schuren": "House & home",
    "spellen": "Sport & games",
    "stratenmaker": "Work & jobs",
    "uitwisselingsprogramma": "Education & learning",
    "videogesprek": "Communication & language",
    "gehaktbal": "Food & drink",
    "hoofdgerecht": "Food & drink",
    "kledingzaak": "Clothing & appearance",
    "dagschotel": "Food & drink",
    "mosselen": "Food & drink",
    "paella": "Food & drink",
    "peterselie": "Food & drink",
    "rucola": "Food & drink",
    "zalf": "Body & health",
    "zandplaat": "Places & geography",
    "rapper": "Arts & media",
    "ranglijst": "Sport & games",
    "relativering": "Abstract & general",
    "notulen": "Work & jobs",
    "tube": "Body & health",
    "thermometer": "Body & health",
    "zwoel": "Nature & weather",
    "zoem": "Animals",
    "zoemen": "Animals",
    "snurken": "Body & health",
    "uitputten": "Body & health",
    "verdacht": "Law & conflict",
    "zorgzaam": "Character & behaviour",
    "yogadocent": "Work & jobs",
    "volleybalteam": "Sport & games",
    "glazenwasser": "Work & jobs",
    "lantaarnpaal": "Places & geography",
    "kruiwagen": "Plants & farming",
})

# ---------------------------------------------------------------------------
# Keyword rules. (domain, allowed pos or None, regex over "nl en").
# Order is significance: the first match wins, so narrow or unambiguous
# vocabulary comes before broad vocabulary. E.g. "sword" must reach War before
# any general weapon or object rule; "court" must reach Law before Sport.
# ---------------------------------------------------------------------------

ABSTRACT_OR_NONE = None
NOUN = {"noun"}
VERB = {"verb"}
ADJ = {"adj"}

RULES = [
    # --- War & military -----------------------------------------------------
    ("War & military", None,
     r"\b(war|warfare|army|soldier|sergeant|lieutenant|colonel|regiment|"
     r"battalion|infantry|cavalry|artillery|centurion|legion|mercenary|"
     r"weapon|firearm|rifle|pistol|revolver|cannon|artillery|sword|sabre|blade|"
     r"dagger|spear|lance|axe|bow and arrow|shield|armour|armor|"
     r"bomb|grenade|missile|torpedo|minefield|tank|warship|submarine|"
     r"battle|combat|siege|trench|invasion|to invade|conquest|"
     r"victory|defeat|truce|ceasefire|armistice|peace treaty|"
     r"military|navy|air force|fortress|fort|barracks|ammunition|bullet|"
     r"allies|ally|alliance|enemy|prisoner of war|veteran|conscription|"
     r"to shoot down|shoot down|to surrender|to occupy|occupation|resistance|guerrilla|"
     r"air raid|bombing|front line|casualty|war crime)\b"),

    # --- Religion & belief --------------------------------------------------
    ("Religion & belief", None,
     r"\b(religion|religious|faith|belief|to believe in|god|goddess|"
     r"deity|divine|holy|sacred|church|chapel|cathedral|mosque|temple|"
     r"synagogue|monastery|convent|priest|pastor|vicar|clergy|clergyman|"
     r"chaplain|deacon|preacher|reverend|rabbi|imam|"
     r"monk|nun|bishop|pope|saint|angel|demon|devil|satan|heaven|hell|"
     r"paradise|purgatory|soul|spirit|spiritual|prayer|to pray|"
     r"worship|to worship|ritual|sacrifice|pilgrimage|bible|gospel|"
     r"koran|quran|torah|psalm|hymn|sermon|baptism|communion|"
     r"sin|sinful|forgiveness|resurrection|afterlife|reincarnation|"
     r"myth|mythology|mythical|legend|deity|cult|sect|occult|"
     r"magic|magical|witch|wizard|sorcerer|spell|curse|amulet|"
     r"supernatural|miracle|prophet|prophecy|atheist|christian|"
     r"catholic|protestant|muslim|jewish|buddhist|hindu|"
     r"islam|islamic|christianity|christian|judaism|buddhism|hinduism)\b"),

    # --- Sport & games ------------------------------------------------------
    ("Sport & games", None,
     r"\b(sport|sports|athletics|athlete|game|match|tournament|"
     r"championship|champion|world title|trophy|medal|podium|referee|umpire|"
     r"coach|trainer|team|player|opponent|score|goal|penalty|"
     r"football|soccer|tennis|hockey|volleyball|basketball|handball|"
     r"baseball|cricket|golf|rugby|cycling|swimming|running|jogging|"
     r"skating|skiing|snowboarding|surfing|rowing|sailing|boxing|"
     r"wrestling|judo|karate|fencing|gymnastics|equestrian|"
     r"chess|draughts|checkers|puzzle|dice|board game|card game|"
     r"stadium|arena|track|pitch|tennis court|ring|race|racing|marathon|"
     r"olympic|olympics|league|cup|final|semi-final|qualifier|"
     r"to win|to lose|victory|defeat|draw|stadium|skate|skates|"
     r"sporty|sportive|athletic|"
     r"bicycle race|prize|record|training|to train|sports club|"
     r"goalkeeper|striker|midfielder|bat|racket|ball)\b"),

    # --- Education & learning ----------------------------------------------
    ("Education & learning", None,
     r"\b(education|educational|school|pupil|student|teacher|professor|"
     r"lecturer|headmaster|principal|classroom|lesson|course|curriculum|"
     r"exam|examination|test|grade|mark|diploma|certificate|degree|"
     r"homework|assignment|essay|thesis|dissertation|lecture|seminar|"
     r"tutorial|study|to study|to learn|to teach|training|apprenticeship|"
     r"university|college|academy|institute|faculty|"
     r"library|librarian|textbook|dictionary|encyclopaedia|encyclopedia|"
     r"kindergarten|nursery|primary school|secondary school|"
     r"secondary education|higher education|vocational|vocational school|"
     r"scholarship|to graduate|graduation|pupil|professor|"
     r"class|schoolbag|blackboard|chalk|homework|school subject|"
     r"mathematics|arithmetic|grammar|spelling|vocabulary)\b"),

    # --- Law & conflict -----------------------------------------------------
    ("Law & conflict", None,
     r"\b(law|laws|legal|illegal|legislation|justice|court|tribunal|"
     r"judge|jury|lawyer|attorney|solicitor|prosecutor|defence lawyer|"
     r"trial|verdict|sentence|appeal|evidence|witness|suspect|"
     r"crime|criminal|offence|offense|theft|robbery|burglary|fraud|"
     r"murder|manslaughter|assault|kidnapping|smuggling|vandalism|"
     r"police|policeman|police officer|detective|prison|jail|cell|"
     r"guard|arrest|to arrest|to detain|detention|custody|bail|"
     r"punishment|penalty|fine|to fine|guilt|guilty|innocent|"
     r"contract|agreement|clause|signature|to sue|lawsuit|claim|"
     r"damages|compensation|copyright|patent|rights|human rights|"
     r"rule|regulation|bylaw|statute|constitution|to forbid|forbidden|"
     r"prohibited|permission|licence|license|permit|"
     r"complaint|to complain|court case|conflict|dispute|quarrel|"
     r"to quarrel|revenge|retaliation|vendetta|threat|to threaten|blackmail|corruption|"
     r"corrupt|bribe|bribery|discrimination|to discriminate)\b"),

    # --- Technology & tools -------------------------------------------------
    ("Technology & tools", None,
     r"\b(technology|technological|technical|technique|machine|machinery|"
     r"engine|motor|computer|laptop|desktop|tablet|smartphone|"
     r"software|hardware|program|programme|application|app|"
     r"internet|website|server|network|database|algorithm|code|"
     r"email|e-mail|password|login|download|upload|data|digital|"
     r"coding|programming|to code|source code|"
     r"robot|robot|drone|sensor|scanner|printer|fax|modem|router|"
     r"cable|battery|charger|plug|socket|switch|button|remote control|"
     r"tool|tools|hammer|screwdriver|wrench|spanner|drill|saw|"
     r"nail|screw|bolt|nut|hinge|lever|pulley|gear|valve|pipe|"
     r"pump|generator|turbine|boiler|radiator|air conditioning|"
     r"machine|device|apparatus|gadget|instrument|equipment|"
     r"to repair|repair|maintenance|to install|installation|"
     r"factory|industrial|industry|engineering|engineer|"
     r"rope|cable|wire|string|thread|"
     r"steam engine|electricity|electric|electronic|electronics|"
     r"telephone|phone|mobile phone|smartphone|television|radio|"
     r"camera|camcorder|headphones|speaker|microphone|"
     r"nuclear|reactor|laser|radar|satellite|GPS)\b"),

    # --- Transport & travel ------------------------------------------------
    ("Transport & travel", None,
     r"\b(transport|transportation|traffic|vehicle|car|automobile|"
     r"lorry|truck|bus|coach|tram|metro|subway|train|railway|"
     r"railroad|station|platform|airport|airplane|aeroplane|plane|"
     r"aircraft|flight|helicopter|boat|ship|vessel|ferry|yacht|"
     r"canoe|kayak|barge|sailing ship|cruise|bicycle|bike|motorbike|"
     r"motorcycle|scooter|taxi|cab|driver|passenger|pilot|crew|"
     r"captain|sailor|ticket|fare|journey|trip|voyage|travel|"
     r"to travel|tourist|tourism|holiday|vacation|hotel|hostel|"
     r"camping|campsite|luggage|baggage|suitcase|backpack|"
     r"passport|visa|border|route|itinerary|destination|"
     r"highway|motorway|road|street|avenue|lane|junction|"
     r"roundabout|traffic light|bridge|tunnel|car park|parking|"
     r"petrol|petrol station|fuel|diesel|to drive|driving licence|"
     r"seat belt|speed limit|traffic jam|congestion|"
     r"to depart|departure|to arrive|arrival|delay|transfer|"
     r"to fly|to sail|to cycle|to ride|commuter|"
     r"shipping|freight|cargo|load|shipment|harbour|harbor|port|dock|quay)\b"),

    # --- Clothing & appearance ---------------------------------------------
    ("Clothing & appearance", None,
     r"\b(clothing|clothes|garment|fashion|fashionable|outfit|uniform|"
     r"shirt|blouse|t-shirt|sweater|jumper|cardigan|jacket|coat|"
     r"raincoat|trousers|pants|jeans|shorts|skirt|dress|gown|suit|"
     r"waistcoat|vest|underwear|bra|sock|socks|stocking|tights|"
     r"shoe|shoes|boot|boots|sandal|slipper|sneaker|trainer|"
     r"hat|cap|beret|helmet|scarf|glove|gloves|mitten|belt|tie|"
     r"necktie|bow tie|button|zip|zipper|buckle|pocket|collar|sleeve|"
     r"fabric|textile|cloth|wool|woollen|cotton|silk|linen|leather|"
     r"nylon|polyester|velvet|lace|embroidery|seam|hem|patch|"
     r"to sew|sewing|needle|thread|pin|tailor|seamstress|"
     r"to wear|to dress|to undress|to try on|naked|nude|barefoot|"
     r"hairstyle|haircut|beard|moustache|moustache|make-up|"
     r"cosmetics|perfume|jewellery|jewelry|necklace|bracelet|"
     r"earring|ring|brooch|watch|glasses|sunglasses|contact lens|"
     r"tattoo|piercing|appearance|good-looking|ugly|elegant|"
     r"smart|scruffy|trendy|style|to dress up|costume)\b"),

    # --- Animals ------------------------------------------------------------
    ("Animals", None,
     r"\b(animal|animal species|mammal|bird|fish|reptile|amphibian|"
     r"insect|bug|beetle|butterfly|moth|dragonfly|stonefly|spider|"
     r"scorpion|snail|slug|worm|bee|wasp|ant|termite|mosquito|"
     r"fly|flea|tick|mite|crustacean|crab|lobster|shrimp|prawn|"
     r"scampi|squid|octopus|jellyfish|starfish|shellfish|oyster|"
     r"mussel|clam|mollusc|mollusk|"
     r"dog|puppy|cat|kitten|horse|pony|donkey|mule|cow|cattle|bull|"
     r"ox|pig|hog|sheep|ram|lamb|goat|chicken|hen|rooster|cock|"
     r"duck|goose|swan|turkey|pigeon|dove|rabbit|hare|mouse|mice|rat|"
     r"hamster|guinea pig|squirrel|hedgehog|bat|mole|beaver|otter|"
     r"seal|walrus|whale|dolphin|porpoise|shark|ray|eel|salmon|trout|"
     r"cod|herring|haddock|tuna|sardine|anchovy|bass|carp|pike|"
     r"perch|sole|plaice|flounder|halibut|mackerel|swordfish|"
     r"wolf|fox|bear|deer|stag|elk|moose|reindeer|boar|badger|"
     r"lynx|panther|leopard|tiger|lion|cheetah|jaguar|elephant|"
     r"rhinoceros|rhino|hippopotamus|hippo|giraffe|zebra|camel|"
     r"llama|monkey|ape|chimpanzee|gorilla|orangutan|baboon|"
     r"kangaroo|koala|panda|sloth|armadillo|anteater|"
     r"lizard|gecko|iguana|chameleon|crocodile|alligator|turtle|"
     r"tortoise|frog|toad|salamander|newt|snake|python|cobra|viper|"
     r"dinosaur|dinosaur species|sauropod|stegosaur|pachycephalosaur|"
     r"tyrannosaurus|triceratops|velociraptor|pterosaur|plesiosaur|"
     r"ibex|chamois|antelope|gazelle|buffalo|bison|yak|"
     r"ostrich|penguin|parrot|owl|eagle|hawk|falcon|vulture|"
     r"crow|raven|magpie|sparrow|finch|lark|nightingale|robin|"
     r"swallow|swift|crane|heron|stork|seagull|gull|pelican|"
     r"flamingo|peacock|pheasant|partridge|quail|woodpecker|"
     r"cormorant|kingfisher|buzzard|kestrel|"
     r"gannet|seabird|songbird|waterfowl|wader|"
     r"pet|livestock|zoo|aquarium|nest|birdcage|cage|kennel|"
     r"feather|fur|paw|claw|beak|fang|horn|tail|mane|wool|"
     r"to bark|to purr|to bite|to sting|to breed|to hatch|"
     r"animal species|wildlife|fauna)\b"),

    # --- Plants & farming ---------------------------------------------------
    ("Plants & farming", None,
     r"\b(plant|plants|flora|flower|flowers|tree|trees|bush|shrub|"
     r"grass|lawn|moss|fern|algae|seaweed|weed|herb|vegetation|"
     r"leaf|leaves|branch|twig|trunk|bark|root|roots|seed|seeds|"
     r"bulb|sprout|shoot|stem|stalk|pollen|nectar|petal|blossom|"
     r"bloom|to bloom|to grow|growth|to plant|to sow|to harvest|"
     r"harvest|crop|crops|grain|wheat|barley|oats|rye|maize|corn|"
     r"rice|straw|hay|silage|fertiliser|fertilizer|manure|pesticide|"
     r"farm|farmer|farming|agriculture|agricultural|arable|"
     r"field|meadow|pasture|orchard|vineyard|greenhouse|"
     r"barn|stable|shed|tractor|plough|plow|irrigation|"
     r"to cultivate|cultivation|horticulture|gardening|gardener|"
     r"garden|vegetable garden|allotment|"
     r"tulip|rose|daffodil|sunflower|lily|orchid|daisy|violet|"
     r"poppy|lavender|jasmine|hyacinth|crocus|geranium|"
     r"ash|yew|larch|alder|poplar|cedar|cypress|"
     r"oak|pine|birch|beech|willow|maple|elm|fir|spruce|"
     r"palm|bamboo|cactus|ivy|clover|thistle|nettle|reed|"
     r"conifer|deciduous|evergreen|timber|lumber|wood|firewood|"
     r"cereal|legume|pulse|tuber|herb|spice plant)\b"),

    # --- Food & drink -------------------------------------------------------
    ("Food & drink", None,
     r"\b(food|drink|beverage|meal|dish|cuisine|recipe|menu|"
     r"breakfast|lunch|dinner|supper|snack|dessert|starter|main course|"
     r"to eat|to drink|to cook|cook|cooking|chef|cook|kitchen|"
     r"bakery|butcher|greengrocer|market|supermarket|groceries|"
     r"bread|loaf|roll|bun|toast|pastry|cake|pie|biscuit|cookie|"
     r"pancake|pudding|ice cream|chocolate|sweets|candy|sugar|"
     r"honey|jam|syrup|salt|pepper|spice|herb|sauce|gravy|"
     r"oil|vinegar|mustard|mayonnaise|ketchup|soup|stew|"
     r"cheese|butter|margarine|yoghurt|yogurt|cream|milk|"
     r"egg|eggs|omelette|meat|beef|pork|veal|lamb|chicken|"
     r"ham|bacon|sausage|mince|steak|fish|seafood|"
     r"potato|potatoes|chip|chips|rice|pasta|noodle|spaghetti|"
     r"macaroni|flour|dough|batter|yeast|"
     r"vegetable|fruit|apple|pear|banana|orange|lemon|lime|"
     r"grape|peach|apricot|plum|cherry|strawberry|raspberry|"
     r"blueberry|melon|watermelon|pineapple|kiwi|mango|"
     r"tomato|cucumber|lettuce|cabbage|carrot|onion|garlic|"
     r"leek|celery|spinach|broccoli|cauliflower|pumpkin|"
     r"courgette|aubergine|eggplant|pea|bean|lentil|"
     r"mushroom|nut|peanut|almond|walnut|hazelnut|"
     r"coffee|tea|juice|lemonade|water|beer|wine|spirits|"
     r"whisky|vodka|gin|rum|champagne|cider|soda|"
     r"glass|cup|mug|plate|bowl|saucer|cutlery|knife|fork|spoon|"
     r"napkin|tablecloth|tray|pan|saucepan|frying pan|pot|kettle|"
     r"oven|stove|microwave|fridge|freezer|dishwasher|"
     r"hunger|hungry|thirst|thirsty|appetite|taste|tasty|delicious|"
     r"to taste|to bake|to fry|to boil|to roast|to grill|"
     r"vegetarian|vegan|diet|allergy|allergic|"
     r"restaurant|cafe|cafeteria|canteen|fast food|takeaway|"
     r"waiter|waitress|bill|tip|portion|ingredient)\b"),

    # --- Body & health ------------------------------------------------------
    ("Body & health", None,
     r"\b(body|human body|anatomy|head|skull|brain|face|forehead|"
     r"eye|eyes|eyebrow|eyelash|ear|ears|nose|mouth|lip|lips|"
     r"tongue|tooth|teeth|gum|chin|cheek|jaw|neck|throat|"
     r"shoulder|arm|arms|elbow|wrist|finger|fingers|"
     r"thumb|nail|chest|breast|back|spine|waist|hip|belly|"
     r"stomach|abdomen|intestine|gut|liver|kidney|lung|lungs|"
     r"heart|blood|vein|artery|muscle|bone|bones|skeleton|skull|"
     r"skin|flesh|nerve|cell|hormone|gene|dna|chromosome|"
     r"leg|legs|thigh|knee|shin|calf|ankle|foot|feet|toe|toes|"
     r"heel|paw|tail|hair|beard|"
     r"health|healthy|unhealthy|illness|disease|sickness|sick|ill|"
     r"pain|to hurt|injury|wound|scar|bruise|burn|bleeding|"
     r"fever|temperature|cough|cold|flu|influenza|virus|bacteria|"
     r"infection|inflammation|allergy|cancer|diabetes|asthma|"
     r"heart attack|stroke|epilepsy|depression|dementia|"
     r"disability|disabled|handicap|handicapped|blind|deaf|mute|paralysed|"
     r"doctor|physician|gp|general practitioner|nurse|surgeon|"
     r"dentist|midwife|specialist|hospital|clinic|ward|"
     r"surgery|operation|treatment|therapy|therapist|"
     r"medicine|medication|drug|pill|tablet|vaccine|vaccination|"
     r"injection|bandage|plaster|crutch|wheelchair|"
     r"appointment|waiting list|"
     r"to breathe|breathing|respiration|pulse|blood pressure|"
     r"to heal|to recover|recovery|cure|"
     r"pregnant|pregnancy|birth|to give birth|baby|"
     r"hygiene|hygienic|to wash|shampoo|soap|toothbrush|"
     r"to shave|razor|deodorant|sanitary|toilet|"
     r"unconscious|conscious|dizzy|nausea|vomit|to vomit|"
     r"pandemic|epidemic|immune|immunity|"
     r"poison|poisoning|poisonous|overdose|dose|"
     r"tired|fatigue|tiredness|weariness|wearied|exhausted|insomnia|to sleep|sleep|dream|"
     r"to die|death|dead|mortality|autopsy|organ|donor)\b"),

    # --- House & home -------------------------------------------------------
    ("House & home", None,
     r"\b(house|home|residence|dwelling|flat|apartment|studio|"
     r"room|bedroom|bathroom|kitchen|living room|living space|sitting room|"
     r"townhouse|town house|mansion|manor|trellis|"
     r"dining room|hall|hallway|corridor|attic|loft|basement|"
     r"cellar|garage|shed|garden|balcony|terrace|porch|"
     r"door|doorway|window|skylight|wall|floor|ceiling|roof|"
     r"stairs|staircase|step|elevator|lift|chimney|fireplace|"
     r"furniture|table|chair|stool|bench|sofa|couch|armchair|"
     r"bed|mattress|pillow|blanket|duvet|sheet|wardrobe|"
     r"cupboard|closet|cabinet|drawer|shelf|bookcase|"
     r"desk|mirror|lamp|light|bulb|candle|curtain|blind|"
     r"carpet|rug|mat|tile|parquet|wallpaper|paint|"
     r"tap|sink|basin|bath|bathtub|shower|drain|pipe|"
     r"toilet|lavatory|loo|bin|rubbish|garbage|trash|"
     r"broom|brush|mop|bucket|vacuum cleaner|dustpan|"
     r"washing machine|dryer|iron|ironing board|"
     r"key|lock|latch|handle|hinge|bolt|doorbell|"
     r"household|housekeeping|chore|to clean|cleaning|"
     r"to tidy|tidy|messy|untidy|cosy|spacious|"
     r"rent|rental|tenant|landlord|mortgage|neighbour|neighbor|"
     r"neighbourhood|neighborhood|street|square|"
     r"residential|housing|accommodation|to move house|"
     r"building|panel|insulation|to decorate|decoration|"
     r"furnished|unfurnished|utility|heating|central heating|"
     r"electricity|gas|water supply|wifi|broadband)\b"),

    # --- Work & jobs --------------------------------------------------------
    ("Work & jobs", None,
     r"\b(work|job|employment|unemployment|profession|occupation|"
     r"career|employer|employee|worker|staff|personnel|colleague|"
     r"boss|manager|director|supervisor|foreman|apprentice|"
     r"intern|internship|trainee|volunteer|freelancer|self-employed|"
     r"salary|wage|income|payroll|pension|retirement|to retire|"
     r"office|workplace|factory|workshop|warehouse|site|"
     r"shift|overtime|holiday pay|contract|permanent|temporary|"
     r"to apply|application|job interview|interview|cv|resume|"
     r"vacancy|vacant|recruitment|to recruit|to hire|to fire|"
     r"dismissal|redundancy|strike|trade union|union|"
     r"profession|craft|trade|skill|skilled|unskilled|"
     r"mechanic|electrician|plumber|carpenter|joiner|painter|"
     r"bricklayer|welder|mason|roofer|glazier|"
     r"engineer|architect|surveyor|technician|programmer|"
     r"accountant|bookkeeper|auditor|banker|economist|"
     r"chemist|physicist|biologist|geologist|astronomer|"
     r"lawyer|judge|notary|journalist|editor|writer|translator|"
     r"interpreter|designer|photographer|artist|musician|"
     r"actor|actress|director|producer|chef|cook|baker|butcher|"
     r"farmer|gardener|florist|hairdresser|barber|"
     r"shop assistant|sales assistant|salesman|saleswoman|"
     r"cashier|receptionist|secretary|assistant|clerk|"
     r"guard|security guard|cleaner|porter|driver|pilot|"
     r"sailor|soldier|police officer|firefighter|nurse|"
     r"teacher|professor|lecturer|trainer|coach|"
     r"manager|consultant|advisor|adviser|agent|broker|"
     r"civil servant|official|politician|diplomat|"
     r"to work|working hours|working conditions|"
     r"business|company|firm|enterprise|corporation|"
     r"entrepreneur|start-up|branch|department|"
     r"task|duty|responsibility|deadline|meeting|"
     r"project|assignment|report|to manage|management)\b"),

    # --- Money & trade ------------------------------------------------------
    ("Money & trade", None,
     r"\b(money|cash|currency|coin|note|banknote|bank|account|"
     r"savings|to save|deposit|withdrawal|to withdraw|transfer|"
     r"payment|to pay|payer|payee|price|cost|expense|fee|charge|"
     r"bill|invoice|receipt|refund|discount|offer|bargain|"
     r"cheap|expensive|costly|affordable|free of charge|"
     r"profit|loss|revenue|turnover|budget|debt|loan|credit|"
     r"mortgage|interest|instalment|installment|"
     r"insurance|premium|insurance policy|claim|"
     r"tax|taxes|vat|duty|levy|subsidy|fine|"
     r"invest|investment|investor|share|shares|stock|stock market|"
     r"exchange rate|inflation|deflation|recession|economy|"
     r"economic|financial|finance|fiscal|monetary|"
     r"trade|commerce|commercial|market|marketplace|"
     r"to buy|to sell|purchase|sale|sales|retail|wholesale|"
     r"supplier|supply|demand|customer|client|consumer|"
     r"shareholder|stakeholder|shop|store|shopkeeper|merchant|trader|dealer|"
     r"auction|bid|bidding|contract|transaction|"
     r"lottery|gambling|to gamble|bet|casino|"
     r"rich|wealthy|wealth|poor|poverty|debt|bankrupt|"
     r"treasure|fortune|inheritance|to inherit|donation|to donate|"
     r"salary|wage|bonus|commission|allowance|benefit|"
     r"pension|grant|fund|funding|sponsor|sponsorship|"
     r"euro|dollar|pound|cent|price tag|value|worth|"
     r"wallet|purse|briefcase|chequebook|checkbook|"
     r"to compensate|compensation|subscription|yield|"
     r"to borrow|to lend|borrower|lender|savings account|"
     r"damage|compensation|loss|claim)\b"),

    # --- Arts & media -------------------------------------------------------
    ("Arts & media", None,
     r"\b(art|arts|artist|painting|drawing|sketch|sculpture|statue|"
     r"gallery|museum|exhibition|exhibit|masterpiece|portrait|"
     r"landscape|still life|canvas|easel|palette|brush|"
     r"music|musical|musician|song|singer|band|orchestra|choir|"
     r"composer|conductor|instrument|piano|guitar|violin|cello|"
     r"flute|trumpet|drum|drums|saxophone|clarinet|harp|organ|"
     r"melody|tune|rhythm|harmony|note|scale|concert|opera|"
     r"ballet|dance|dancer|theatre|theater|play|actor|"
     r"actress|drama|comedy|tragedy|performance|to perform|"
     r"audience|applause|curtain|script|rehearsal|"
     r"film|movie|cinema|screen|director|producer|scene|"
     r"documentary|animation|cartoon|series|episode|"
     r"television|tv|programme|program|channel|broadcast|"
     r"radio|podcast|studio|audio|video|"
     r"book|novel|story|short story|poem|poetry|poet|"
     r"literature|literary|writer|author|chapter|paragraph|"
     r"character|plot|narration|narrator|genre|satire|"
     r"newspaper|magazine|journal|article|column|review|"
     r"lyre|lute|banjo|accordion|harmonica|"
     r"headline|press|media|journalism|journalist|"
     r"publisher|publishing|edition|translation|"
     r"photography|photograph|photo|camera|film camera|"
     r"architecture|architect|design|poster|illustration|"
     r"cartoon|comic|graffiti|sculptor|muse|mosaic|"
     r"festival|circus|magic show|entertainment|opening act|index)"),

    # --- Communication & language -------------------------------------------
    ("Communication & language", None,
     r"\b(language|linguistic|word|words|vocabulary|sentence|phrase|"
     r"paragraph|text|message|letter|email|note|memo|"
     r"speech|talk|conversation|dialogue|discussion|debate|"
     r"to speak|to talk|to say|to tell|to ask|to answer|answer|"
     r"question|reply|response|to reply|to respond|"
     r"to write|writing|to read|reading|to listen|listening|"
     r"to translate|translation|translator|interpreter|"
     r"pronunciation|accent|dialect|grammar|spelling|"
     r"meaning|to mean|definition|synonym|antonym|"
     r"announcement|to announce|statement|to state|"
     r"rumour|rumor|gossip|news|report|to report|"
     r"interview|to interview|press conference|"
     r"telephone|phone call|to call|call|to ring|"
     r"letter|post|postal|postman|mail|envelope|stamp|address|"
     r"form|form filling|to fill in|application form|"
     r"to complain|complaint|complaints procedure|"
     r"to curse|curse|swear word|insult|to insult|"
     r"to discuss|discussion|meeting|appointment|to agree|agreement|"
     r"to disagree|disagreement|negotiation|to negotiate|"
     r"argument|to argue|opinion|point of view|view|"
     r"to explain|explanation|to describe|description|"
     r"to inform|information|to notify|notification|"
     r"to indicate|indication|to insist|to point out|"
     r"to warn|warning|advice|to advise|to recommend|recommendation|"
     r"to persuade|persuasion|"
     r"to promise|promise|to apologise|apologise|apologize|apology|"
     r"to thank|thanks|greeting|to greet|farewell|"
     r"to invite|invitation|to introduce|introduction|"
     r"conversation|chat|to chat|small talk|"
     r"sign|signature|sign language|symbol|code|"
     r"chapter|title|heading|summary|to summarise|"
     r"command|request|order|instruction|"
     r"joke|humour|humor|irony|sarcasm|"
     r"whisper|to whisper|to shout|shout|silence|silent)\b"),

    # --- Emotion & feeling --------------------------------------------------
    ("Emotion & feeling", None,
     r"\b(emotion|emotional|feeling|feelings|to feel|mood|"
     r"love|to love|beloved|affection|romance|romantic|"
     r"hate|hatred|to hate|anger|angry|rage|fury|furious|"
     r"fear|afraid|scared|frightened|terror|panic|anxiety|anxious|"
     r"worry|worried|stress|stressed|tension|nervous|nerves|"
     r"happy|happiness|joy|joyful|pleasure|delight|delighted|"
     r"sad|sadness|sorrow|grief|to grieve|mourning|"
     r"disappointment|disappointed|frustration|frustrated|"
     r"shame|ashamed|embarrassment|embarrassed|guilt|guilty|"
     r"pride|proud|jealousy|jealous|envy|envious|"
     r"surprise|surprised|astonishment|astonished|shock|shocked|"
     r"hope|to hope|hopeful|hopeless|despair|desperate|"
     r"comfort|to comfort|to reassure|reassurance|"
     r"calm|to calm down|relaxed|to relax|relaxation|peaceful|"
     r"loneliness|lonely|loneliness|boredom|bored|"
     r"gratitude|grateful|thankful|sympathy|sympathetic|"
     r"empathy|compassion|pity|contempt|disgust|disgusting|"
     r"trust|to trust|distrust|suspicion|suspicious|"
     r"courage|courageous|confidence|confident|insecure|"
     r"to laugh|laughter|to cry|crying|tears|to smile|smile|"
     r"to sigh|sigh|to tremble|trembling|to blush|blush|"
     r"nostalgia|nostalgic|longing|to long for|"
     r"desire|to desire|passion|passionate|"
     r"disappointment|regret|to regret|remorse|"
     r"bored|excitement|excited|enthusiasm|enthusiastic|"
     r"irritation|irritated|annoyance|annoyed|to annoy|"
     r"to be ashamed|ashamed|to care|to care about)\b"),

    # --- Character & behaviour ---------------------------------------------
    ("Character & behaviour", None,
     r"\b(character|personality|behaviour|behavior|behavioural|"
     r"attitude|mentality|temperament|nature|disposition|"
     r"habit|custom|manner|manners|etiquette|"
     r"honest|honesty|dishonest|integrity|sincere|sincerity|"
     r"kind|kindness|friendly|friendliness|cruel|cruelty|"
     r"rude|rudeness|polite|politeness|impolite|respect|respectful|"
     r"disrespectful|arrogant|arrogance|humble|humility|"
     r"modest|modesty|generous|generosity|greedy|greed|"
     r"selfish|selfishness|mature|immature|responsible|irresponsible|"
     r"reliable|reliability|unreliable|trustworthy|"
     r"brave|bravery|courage|coward|cowardly|timid|shy|shyness|"
     r"lazy|laziness|diligent|hard-working|industrious|"
     r"stubborn|stubbornness|flexible|rigid|adaptable|"
     r"patient|patience|impatient|tolerant|tolerance|intolerant|"
     r"gentle|gentleness|violent|violence|aggressive|aggression|"
     r"calm|quiet|talkative|outgoing|introverted|extroverted|"
     r"cheerful|optimistic|optimism|pessimistic|pessimism|"
     r"serious|humorous|funny|silly|stupid|clever|smart|intelligent|"
     r"wise|wisdom|foolish|fool|naive|naivety|cynical|cynicism|"
     r"eccentric|weird|strange|normal|ordinary|special|unique|"
     r"ambitious|ambition|motivated|motivation|determined|willpower|resolve|determination|perseverance|persistence|"
     r"stubborn|spontaneous|disciplined|discipline|"
     r"to behave|to misbehave|to apologise|to forgive|forgiveness|"
     r"to help|helpful|to support|supportive|"
     r"to encourage|encouragement|to criticise|criticism|"
     r"to praise|praise|to blame|blame|to accuse|accusation|"
     r"to lie|lie|liar|to cheat|cheating|cheat|"
     r"to steal|theft|to betray|betrayal|betrayal|"
     r"to respect|to obey|obedience|disobedient|"
     r"to share|sharing|to cooperate|cooperation|"
     r"to compete|competition|competitive|"
     r"scandal|scandalous|shameful|disgraceful|"
     r"intimidation|to intimidate|bullying|to bully|"
     r"reputation|prestige|status|dignity|"
     r"role model|influence|to influence)\b"),

    # --- Society & politics -------------------------------------------------
    ("Society & politics", None,
     r"\b(society|social|societal|community|public|citizen|citizenship|"
     r"population|inhabitant|resident|immigrant|migrant|refugee|"
     r"asylum|integration|to integrate|multicultural|diversity|"
     r"politics|political|politician|policy|government|governance|"
     r"state|nation|country|republic|monarchy|kingdom|"
     r"democracy|democratic|dictatorship|dictator|regime|"
     r"election|to elect|voter|vote|to vote|ballot|referendum|"
     r"parliament|congress|senate|chamber|seat|coalition|"
     r"party|political party|opposition|majority|minority|"
     r"minister|ministry|secretary of state|cabinet|"
     r"president|prime minister|mayor|alderman|council|"
     r"municipality|local authority|municipal|civil servant|"
     r"official|bureaucracy|bureaucratic|administration|"
     r"policy|reform|to reform|legislation|"
     r"protest|to protest|demonstration|to demonstrate|strike|"
     r"union|trade union|movement|activist|activism|"
     r"campaign|to campaign|lobby|lobbying|"
     r"ideology|ideological|left-wing|right-wing|liberal|"
     r"conservative|socialist|socialism|communist|communism|"
     r"capitalism|capitalist|nationalism|nationalist|"
     r"freedom|liberty|equality|justice|solidarity|"
     r"rights|civil rights|human rights|duty|obligation|"
     r"constitution|law|rule of law|"
     r"tax|taxation|welfare|social security|benefit|"
     r"healthcare|health care|education system|housing|"
     r"census|statistics|poll|survey|public opinion|"
     r"media|press|public debate|"
     r"municipality|town hall|citizen service|registration|"
     r"to register|registration|permit|residence permit|"
     r"form|forms|formality|paperwork|bureaucracy|"
     r"post office|postal service|parcel|"
     r"neighbourhood|neighborhood|community centre|"
     r"volunteer|volunteering|charity|ngo|"
     r"globalisation|globalization|global|international|"
     r"society|class|social class|elite|middle class|working class)\b"),

    # --- People & relations -------------------------------------------------
    ("People & relations", None,
     r"\b(people|person|human|human being|individual|"
     r"man|woman|boy|girl|child|children|baby|infant|toddler|"
     r"adult|teenager|adolescent|youth|elderly|senior|old person|"
     r"family|relative|relation|household|parent|parents|"
     r"mother|father|mom|dad|mum|son|daughter|brother|sister|"
     r"sibling|grandmother|grandfather|grandparents|grandson|"
     r"granddaughter|grandchild|uncle|aunt|nephew|niece|cousin|"
     r"husband|wife|spouse|partner|boyfriend|girlfriend|"
     r"fiance|fiancee|lover|ex|widow|widower|orphan|"
     r"marriage|to marry|married|wedding|bride|groom|"
     r"divorce|to divorce|separation|to separate|"
     r"friendship|friend|best friend|acquaintance|companion|"
     r"neighbour|neighbor|colleague|roommate|flatmate|"
     r"relationship|to date|dating|couple|pair|"
     r"generation|ancestor|descendant|heir|"
     r"birth|to be born|childhood|youth|adulthood|old age|"
     r"to raise|upbringing|to adopt|adoption|foster|"
     r"guardian|godparent|twin|only child|"
     r"sex|gender|male|female|masculine|feminine|"
     r"group|team|membership|member|club|association|"
     r"community|society|acquaintance|contact|"
     r"to meet|meeting|encounter|to visit|visitor|guest|"
     r"host|hostess|party|celebration|to celebrate|"
     r"funeral|to mourn|condolence|congratulations|"
     r"orphan|loneliness|to live together|to live together as partners|"
     r"rescuer|saviour|savior|"
     r"comrade|mate|buddy|"
     r"boy|girl|friend|mate|buddy)\b"),

    # --- Places & geography -------------------------------------------------
    ("Places & geography", None,
     r"\b(place|location|site|spot|area|region|district|zone|"
     r"city|town|village|hamlet|municipality|capital|"
     r"country|nation|state|territory|province|county|"
     r"continent|subcontinent|island|isle|peninsula|cape|"
     r"coast|coastline|shore|beach|dune|harbour|harbor|port|"
     r"bay|gulf|strait|channel|estuary|delta|"
     r"border|boundary|frontier|frontier|"
     r"square|plaza|park|garden|playground|market square|"
     r"street|road|lane|avenue|alley|boulevard|"
     r"neighbourhood|neighborhood|suburb|outskirts|centre|center|"
     r"downtown|city centre|old town|"
     r"map|atlas|globe|compass|geography|geographical|"
     r"geographic|topography|topographical|"
     r"latitude|longitude|equator|pole|hemisphere|"
     r"region|regional|local|locality|"
     r"address|postcode|zip code|destination|"
     r"to locate|location|situated|to situate|"
     r"countryside|rural|urban|metropolitan|"
     r"landmark|monument|ruin|ruins|excavation|archaeology|"
     r"tumulus|burial mound|grave mound|"
     r"archaeological|heritage|world heritage|"
     r"border crossing|checkpoint|"
     r"earth|world|planet|globe|geography|"
     r"north|south|east|west)"),

    # --- Nature & weather ---------------------------------------------------
    ("Nature & weather", None,
     r"\b(nature|natural|environment|environmental|ecosystem|"
     r"ecology|ecological|climate|climatic|weather|"
     r"rain|to rain|rainy|rainfall|shower|drizzle|storm|stormy|"
     r"thunder|lightning|wind|windy|gale|hurricane|tornado|"
     r"snow|to snow|snowy|snowfall|hail|sleet|frost|frozen|"
     r"ice|icy|glacier|iceberg|avalanche|"
     r"sun|sunny|sunshine|sunlight|moon|moonlight|star|stars|"
     r"starlight|sky|cloud|cloudy|fog|foggy|mist|misty|"
     r"heat|heatwave|drought|flood|to flood|earthquake|"
     r"volcano|volcanic|eruption|tsunami|landslide|"
     r"air|atmosphere|oxygen|nitrogen|carbon dioxide|"
     r"water|sea|ocean|marine|wave|tide|current|"
     r"river|stream|brook|creek|lake|pond|pool|waterfall|"
     r"spring|well|reservoir|canal|marsh|swamp|bog|"
     r"mountain|hill|peak|summit|ridge|slope|valley|gorge|"
     r"canyon|cliff|rock|stone|boulder|sand|soil|earth|mud|"
     r"forest|wood|woodland|jungle|rainforest|desert|"
     r"steppe|savanna|savannah|tundra|polar|arctic|antarctic|"
     r"planet|planetary|solar system|galaxy|universe|cosmos|"
     r"cosmic|comet|asteroid|meteor|meteorite|nebula|"
     r"star|black hole|gravity|orbit|space|astronomy|"
     r"astronomical|astral|telescope|constellation|"
     r"horizon|dawn|dusk|sunrise|sunset|twilight|"
     r"season|seasons|spring|summer|autumn|fall|winter|"
     r"temperature|degree|celsius|fahrenheit|humidity|"
     r"pressure|air pressure|forecast|weather forecast|"
     r"pollution|polluted|to pollute|waste|"
     r"recycling|to recycle|sustainable|sustainability|"
     r"energy|solar energy|wind energy|fossil fuel|"
     r"emission|greenhouse effect|global warming|"
     r"nature reserve|national park|wildlife|"
     r"sand|gravel|clay|mineral|ore|coal|oil|gas|"
     r"zinc|copper|iron|lead|tin|nickel|aluminium|aluminum|mercury|"
     r"crater|erosion|sediment|steep|invariably)\b"),

    # --- Time ---------------------------------------------------------------
    ("Time", None,
     r"\b(time|times|moment|instant|second|minute|hour|day|week|"
     r"month|year|decade|century|millennium|era|epoch|period|"
     r"date|deadline|schedule|timetable|agenda|calendar|"
     r"morning|afternoon|evening|night|midnight|noon|"
     r"dawn|dusk|sunrise|sunset|today|tonight|tomorrow|yesterday|"
     r"now|then|soon|later|early|late|already|yet|still|"
     r"always|never|sometimes|often|usually|rarely|seldom|"
     r"frequently|occasionally|constantly|continuously|"
     r"immediately|suddenly|eventually|finally|at last|"
     r"before|after|during|while|since|until|till|"
     r"past|present|future|recent|recently|current|currently|"
     r"future|past|history|historical|historic|prehistoric|"
     r"ancient|medieval|modern|contemporary|"
     r"season|spring|summer|autumn|winter|"
     r"holiday|vacation|weekend|weekday|working day|"
     r"anniversary|birthday|festival|celebration|party|"
     r"duration|interval|pause|break|delay|wait|waiting time|"
     r"to wait|to last|to take time|temporary|permanent|"
     r"annual|annually|monthly|weekly|daily|hourly|"
     r"punctual|punctuality|on time|late|too late|"
     r"beginning|start|end|ending|middle|"
     r"timer|clock|watch|alarm clock|stopwatch|"
     r"appointment|appointments|diary|"
     r"to plan|planning|plan|schedule|to schedule)\b"),

    # --- Quantity & measure -------------------------------------------------
    ("Quantity & measure", None,
     r"\b(quantity|amount|number|figure|total|sum|count|"
     r"half|quarter|third|fraction|percentage|percent|"
     r"dozen|pair|couple|piece|part|portion|share|"
     r"trio|quartet|quintet|"
     r"metre|meter|centimetre|centimeter|millimetre|kilometre|"
     r"kilometer|mile|inch|foot|feet|yard|"
     r"gram|kilogram|kilo|milligram|ton|tonne|"
     r"litre|liter|millilitre|gallon|pint|"
     r"square metre|cubic metre|hectare|acre|"
     r"degree|celsius|fahrenheit|kelvin|"
     r"weight|mass|length|width|height|depth|thickness|"
     r"breadth|distance|area|volume|capacity|size|speed|"
     r"to measure|measurement|measure|scale|balance|"
     r"ruler|tape measure|thermometer|barometer|"
     r"many|much|more|most|few|fewer|least|little|less|"
     r"all|every|each|both|either|neither|none|some|any|"
     r"several|various|numerous|plenty|enough|sufficient|"
     r"insufficient|too much|too many|too little|"
     r"increase|to increase|decrease|to decrease|"
     r"rise|to rise|fall|to fall|growth|to grow|"
     r"decline|to decline|reduction|to reduce|"
     r"double|triple|to double|"
     r"average|median|maximum|minimum|"
     r"hundred|thousand|million|billion|trillion|"
     r"approximate|approximately|about|roughly|exactly|"
     r"scarce|abundant|plentiful|rare|common|"
     r"majority|minority|proportion|ratio|rate|"
     r"estimate|to estimate|estimation|stijging|daling|"
     r"rise|increase|amount|quantity)\b"),

    # --- Movement & position ------------------------------------------------
    ("Movement & position", None,
     r"\b(movement|motion|to move|to go|to come|to walk|to run|"
     r"to jump|to leap|to hop|to climb|to descend|to ascend|"
     r"to fall|to drop|to rise|to stand|to sit|to lie|to kneel|"
     r"to bend|to stretch|to turn|to rotate|to spin|to roll|"
     r"to push|to pull|to drag|to carry|to lift|to lower|"
     r"to throw|to catch|to hold|to put|to place|to set|"
     r"to lay|to insert|to remove|to take out|to bring|"
     r"to send|to receive|to follow|to lead|to guide|"
     r"to enter|to leave|to exit|to arrive|to depart|"
     r"to approach|to retreat|to escape|to flee|to chase|"
     r"to pass|to cross|to overtake|to meet|to join|"
     r"to open|to close|to shut|to lock|to unlock|"
     r"to connect|to disconnect|to attach|to detach|"
     r"to tie|to untie|to fasten|to loosen|"
     r"direction|position|location|place|spot|"
     r"above|below|under|underneath|over|on top of|"
     r"in front of|behind|beside|next to|near|close to|far|"
     r"left|right|straight|forward|backward|backwards|"
     r"up|down|upwards|downwards|inside|outside|within|"
     r"between|among|amongst|around|across|along|through|"
     r"towards|toward|away|apart|together|"
     r"top|bottom|side|edge|corner|centre|center|middle|"
     r"surface|base|foundation|layer|level|"
     r"vertical|horizontal|diagonal|parallel|"
     r"to separate|separation|to divide|division|"
     r"to gather|to collect|to assemble|to scatter|"
     r"to flow|to pour|to spill|to drip|to leak|"
     r"to swing|to shake|to wave|to nod|to point|"
     r"distance|proximity|nearby|adjacent|opposite|"
     r"to touch|touch|to stop|"
     r"to travel|to move house|to move|movement)\b"),

    # --- Thought & knowledge ------------------------------------------------
    ("Thought & knowledge", None,
     r"\b(thought|thinking|to think|idea|notion|concept|"
     r"knowledge|to know|known|unknown|"
     r"to understand|understanding|comprehension|"
     r"to believe|belief|to doubt|doubt|doubtful|"
     r"reason|reasoning|logic|logical|rational|irrational|"
     r"argument|to conclude|conclusion|premise|"
     r"theory|theoretical|hypothesis|assumption|to assume|"
     r"science|scientific|scientist|research|researcher|"
     r"to research|experiment|experimental|laboratory|"
     r"analysis|to analyse|analyze|to analyse|"
     r"method|methodology|approach|technique|"
     r"evidence|proof|to prove|to disprove|"
     r"fact|facts|data|information|to inform|"
     r"memory|to remember|to forget|forgetful|"
     r"mind|mental|intelligence|intelligent|"
     r"attention|to concentrate|concentration|"
     r"imagination|to imagine|imaginary|fantasy|"
     r"to dream|dream|dreams|nightmare|"
     r"consciousness|conscious|awareness|aware|unaware|"
     r"perception|to perceive|to notice|noticeable|"
     r"to learn|learning|to study|study|"
     r"to discover|discovery|to invent|invention|inventor|"
     r"to solve|solution|problem|question|issue|"
     r"to decide|decision|choice|to choose|"
     r"to consider|consideration|to judge|judgement|judgment|"
     r"to compare|comparison|to distinguish|distinction|"
     r"to classify|classification|category|class|"
     r"principle|rule|rule of thumb|law|"
     r"view|opinion|perspective|point of view|"
     r"philosophy|philosophical|philosopher|"
     r"psychology|psychological|sociology|sociological|"
     r"mathematics|mathematical|physics|chemistry|biology|"
     r"geology|astronomy|genetics|anatomy|"
     r"scheme|plan|scenario|model|framework|structure|"
     r"to estimate|to calculate|calculation|"
     r"to measure|estimate|"
     r"to explore|exploration|to investigate|investigation|"
     r"curiosity|curious|to wonder|wonder|"
     r"to realise|realize|realisation|realization|"
     r"insight|intuition|intuitive|to intuit|"
     r"to memorise|memorize|to recite|"
     r"to test|testing|to check|to verify|verification|"
     r"to doubt|sceptical|skeptical|scepticism|"
     r"to reason|to deduce|deduction|to infer|inference|"
     r"to focus|focus|to pay attention|"
     r"magnetic|magnetism|gravity|atom|molecule|electron|"
     r"to explore|to examine|examination|to inspect|inspection)\b"),
]

# ---------------------------------------------------------------------------
# Dutch suffix rules. Compounds the gloss does not reveal, e.g. a gloss of
# "ibex" for `steenbok` is caught by the keyword table, but `-vogel` and
# `-boom` compounds are not. These are high-precision and run after RULES.
# ---------------------------------------------------------------------------

SUFFIX_RULES = [
    ("Animals", r"(vis|vogel|vlinder|kever|spin|slang|hond|kat|paard|"
                r"koe|schaap|geit|kip|muis|rat|beer|wolf|vos|haas|"
                r"hert|aap|olifant|leeuw|tijger|dier|mier|wesp|"
                r"mug|libel|kreeft|krab|schildpad|dolfijn|walvis|haai|"
                r"struis|papegaai|arend|uil|valk|raaf|kraai|meeuw|"
                r"zwaan|eend|gans|duif|fazant|ekster|specht)$"),
    ("Plants & farming", r"(boom|bloem|plant|gras|varen|struik|"
                         r"heester|kruid|zaad|vrucht|"
                         r"tarwe|gerst|haver|rogge|mais|rijst|"
                         r"landbouw|weide|tuin)$"),
    ("Transport & travel", r"(schip|boot|trein|fiets|vliegtuig|"
                           r"wagen|bus|tram|metro|haven|luchthaven|"
                           r"station|snelweg|vaartuig)$"),
    ("House & home", r"(huis|kamer|deur|raam|muur|vloer|dak|tafel|"
                     r"stoel|kast|bed|lamp|keuken|badkamer|slaapkamer|"
                     r"woonkamer|zolder|kelder|tuinhek|meubel)"),
    ("Body & health", r"(ziekte|kwaal|ontsteking|pijn|wond|"
                      r"kanker|koorts|spier|zenuw|lever|hart|"
                      r"maag|keel|gezondheid|genees)$"),
    ("Clothing & appearance", r"(kleding|kleren|jas|broek|jurk|"
                              r"hemd|blouse|trui|schoen|laars|hoed|"
                              r"sjaal|handschoen|riem|knoop|"
                              r"stof|wol|katoen|zijde|"
                              r"kapsel|baard|snor|sieraad)$"),
    ("Money & trade", r"(geld|prijs|kosten|belasting|bank|rekening|"
                      r"lening|schuld|verzekering|winst|verlies|"
                      r"korting|markt|inkomen|loon|salaris|"
                      r"budget|betaal|factuur|huur|hypotheek)$"),
    ("Arts & media", r"(kunst|muziek|lied|film|toneel|dans|"
                     r"schilderij|beeld|roman|gedicht|verhaal|"
                     r"krant|tijdschrift|boek|bibliotheek|"
                     r"televisie|radio|theater|concert|museum)"),
    ("Technology & tools", r"(machine|apparaat|computer|telefoon|"
                           r"internet|software|techniek|motor|"
                           r"gereedschap|hamer|schroef|batterij|"
                           r"kabel|stekker|schakelaar|printer|"
                           r"scanner|robot|sensor|netwerk|server)"),
    ("Sport & games", r"(sport|wedstrijd|speler|team|bal|doel|"
                      r"stadion|kampioen|toernooi|trainer|"
                      r"scheidsrechter|schaats|voetbal|tennis|"
                      r"hockey|zwem|wielren|hardloop|schaak)"),
    ("Work & jobs", r"(beroep|baan|werk|kantoor|fabriek|"
                    r"werknemer|werkgever|collega|chef|bakker|"
                    r"leidinggevende|stage|sollicit|ontslag|"
                    r"vakbond|pensioen|loopbaan)$"),
    ("Education & learning", r"(school|opleiding|onderwijs|studie|"
                             r"student|leraar|docent|les|examen|"
                             r"diploma|universiteit|hogeschool|"
                             r"cursus|klas|lokaal|huiswerk)"),
    ("Time", r"(dag|week|maand|jaar|eeuw|minuut|seconde|"
              r"tijd|ochtend|avond|nacht|zomer|winter|lente|"
              r"herfst|weekend|vakantie|seizoen|periode|moment)$"),
]

# ---------------------------------------------------------------------------
# Game seed. `herkomst` records which game a word was harvested for. Games
# that are semantically homogeneous give a reliable default when no keyword
# fired. Mixed games (oceans, history, science, reels) are deliberately weak
# and are listed after the homogeneous ones.
# ---------------------------------------------------------------------------

GAME_SEED_ORDER = [
    ("spel:dinosaurs", "Animals"),
    ("spel:insects", "Animals"),
    ("spel:animals", "Animals"),
    ("spel:marine", "Animals"),
    ("spel:flowers", "Plants & farming"),
    ("spel:food", "Food & drink"),
    ("spel:countries", "Places & geography"),
    ("spel:cities", "Places & geography"),
    ("spel:mythology", "Religion & belief"),
    ("spel:fashion", "Clothing & appearance"),
    ("spel:sports", "Sport & games"),
    ("spel:professions", "Work & jobs"),
    ("spel:household", "House & home"),
    ("spel:technology", "Technology & tools"),
    ("spel:music", "Arts & media"),
    ("spel:art", "Arts & media"),
    ("spel:movies", "Arts & media"),
    ("spel:literature", "Arts & media"),
    ("spel:travel", "Transport & travel"),
    ("spel:nature", "Nature & weather"),
    ("spel:mountains", "Nature & weather"),
    ("spel:space", "Nature & weather"),
    # mixed games, last resort
    ("spel:oceans", "Nature & weather"),
    ("spel:history", "Society & politics"),
    ("spel:science", "Thought & knowledge"),
]

THEME_SEED = {
    "Wonen": "House & home",
    "Mensen": "People & relations",
    "Eten en drinken": "Food & drink",
    "Reizen": "Transport & travel",
    "Werk": "Work & jobs",
    "Sport en vrije tijd": "Sport & games",
    "Kleding": "Clothing & appearance",
    "Kinderen en school": "Education & learning",
    "Het lichaam": "Body & health",
    "Nood en politie": "Law & conflict",
    "Gezondheid": "Body & health",
    "Bank en geld": "Money & trade",
    "Gemeente en post": "Society & politics",
    "Telefoon en internet": "Technology & tools",
    "Boodschappen": "Food & drink",
    "Mening geven": "Communication & language",
    "De weg": "Movement & position",
    "Zorg voor iemand anders": "Body & health",
    "Formulieren": "Society & politics",
    "Klachten": "Communication & language",
    "Solliciteren": "Work & jobs",
    "Buurt": "Places & geography",
    "Bellen": "Communication & language",
    "Afspraken": "Time",
    "plaats": "Places & geography",
}

# ---------------------------------------------------------------------------

def compile_rule(pattern):
    """Every rule is `\\b(alternatives)`; force the closing word boundary.

    Without it a prefix alternative matches inside a longer word:
    `programme` fires on `programmeren`, `character` on `characteristic`.
    Normalising here means an individual rule cannot forget it.
    """
    pattern = re.sub(r"\\b$", "", pattern.strip())
    if not pattern.endswith(")"):
        raise ValueError("rule does not end in a group: %r" % pattern[-40:])
    return re.compile(pattern[:-1] + r")\b", re.IGNORECASE)


RULES = [(domain, pos, compile_rule(pat)) for domain, pos, pat in RULES]

SUFFIX_RULES = [(d, re.compile(r"(%s)$" % pat, re.IGNORECASE))
                for d, pat in SUFFIX_RULES]


def read_tsv(path):
    with open(path, encoding="utf-8") as fh:
        rows = [line.rstrip("\n").split("\t") for line in fh if line.strip()]
    return rows[0], rows[1:]


# Numerals are tagged `function` by woordsoort.py, but they are learnable
# quantity vocabulary, not grammar glue. They are the one exception to the
# `pos=function -> Function words` invariant.
NUMERAL = re.compile(
    r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|"
    r"hundred|thousand|million|billion|trillion|"
    r"first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|"
    r"half|quarter|third|dozen|zero|nought|naught)\b", re.IGNORECASE)


def classify(word, gloss, pos, thema, herkomst):
    nl = word.lower()
    # The appendix carries page markers like "118 van 148" glued into the
    # gloss. Strip them before matching: "van" is also a Transport keyword.
    gloss = re.sub(r"\b\d+\s+van\s+\d+\b", " ", gloss)
    text = word + " " + gloss

    # 0. structural invariants
    if pos == "function":
        return "Quantity & measure" if NUMERAL.search(gloss) else "Function words"
    if pos == "name" or thema == "naam":
        return "Names"
    if pos == "interjection":
        return "Communication & language"

    # 1. curated overrides
    if nl in OVERRIDES:
        return OVERRIDES[nl]

    # 2. keyword table
    for domain, pos_ok, rx in RULES:
        if pos_ok is not None and pos not in pos_ok:
            continue
        if rx.search(text):
            return domain

    # 3. Dutch suffix table
    for domain, rx in SUFFIX_RULES:
        if rx.search(nl):
            return domain

    # 4. game seed
    tags = herkomst.split(";")
    for tag, domain in GAME_SEED_ORDER:
        if tag in tags:
            return domain

    # 5. theme seed
    if thema in THEME_SEED:
        return THEME_SEED[thema]

    # 6. fallback
    return ABSTRACT


def why(word, gloss, pos, thema, herkomst):
    """Print every rule that fires for one word, in pipeline order."""
    nl = word.lower()
    clean = re.sub(r"\b\d+\s+van\s+\d+\b", " ", gloss)
    text = word + " " + clean
    print("word:   %s" % word)
    print("gloss:  %s" % gloss)
    print("pos:    %s   thema: %s   herkomst: %s" % (pos, thema, herkomst))
    print("result: %s" % classify(word, gloss, pos, thema, herkomst))
    if pos == "function":
        if NUMERAL.search(gloss):
            print("rule:   structural pos=function, numeral -> Quantity & measure")
        else:
            print("rule:   structural pos=function")
        return
    if pos == "name" or thema == "naam":
        print("rule:   structural pos=name/thema=naam")
        return
    if pos == "interjection":
        print("rule:   structural pos=interjection")
        return
    if nl in OVERRIDES:
        print("rule:   OVERRIDES -> %s" % OVERRIDES[nl])
        return
    for domain, pos_ok, rx in RULES:
        if pos_ok is not None and pos not in pos_ok:
            continue
        m = rx.search(text)
        if m:
            print("rule:   RULES %s matched %r" % (domain, m.group(0)))
            return
    for domain, rx in SUFFIX_RULES:
        m = rx.search(nl)
        if m:
            print("rule:   SUFFIX %s matched %r" % (domain, m.group(0)))
            return
    for tag, domain in GAME_SEED_ORDER:
        if tag in herkomst.split(";"):
            print("rule:   GAME_SEED %s -> %s" % (tag, domain))
            return
    if thema in THEME_SEED:
        print("rule:   THEME_SEED %s -> %s" % (thema, THEME_SEED[thema]))
        return
    print("rule:   fallback -> %s" % ABSTRACT)


def main():
    header_w, words = read_tsv(WOORDEN)
    assert header_w == ["nl", "en", "niveau", "top2000", "herkomst"], header_w
    header_p, posrows = read_tsv(POS)
    assert header_p == ["nl", "pos", "en"], header_p
    header_t, themarows = read_tsv(THEMA)
    assert header_t == ["nl", "thema", "thema_ook", "prioriteit", "en"], header_t

    assert len(words) == len(posrows) == len(themarows), (
        len(words), len(posrows), len(themarows))
    for i, (w, p, t) in enumerate(zip(words, posrows, themarows), start=2):
        assert w[0] == p[0] == t[0], (i, w[0], p[0], t[0])

    if len(sys.argv) == 3 and sys.argv[1] == "--why":
        needle = sys.argv[2].lower()
        found = [(w, p, t) for w, p, t in zip(words, posrows, themarows)
                 if w[0].lower() == needle]
        if not found:
            sys.exit("not in the list: %r" % sys.argv[2])
        for w, p, t in found:
            why(w[0], w[1], p[1], t[1], w[4])
        return

    labels = []
    for w, p, t in zip(words, posrows, themarows):
        label = classify(w[0], w[1], p[1], t[1], w[4])
        assert label in ALLOWED, label
        labels.append(label)

    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        fh.write("nl\tdomein\ten\n")
        for w, label in zip(words, labels):
            fh.write("%s\t%s\t%s\n" % (w[0], label, w[1]))

    counts = Counter(labels)
    print("rows written:", len(labels))
    print("\nper domein:")
    for d in DOMAINS:
        n = counts.get(d, 0)
        print("  %-26s %5d  %5.1f%%" % (d, n, 100.0 * n / len(labels)))
    unused = [d for d in DOMAINS if not counts.get(d)]
    print("\ndomains never used:", unused)
    print("under 100 words:", [(d, counts.get(d, 0)) for d in DOMAINS
                               if counts.get(d, 0) < 100 and counts.get(d, 0)])
    print("Abstract & general: %d (%.1f%%)"
          % (counts[ABSTRACT], 100.0 * counts[ABSTRACT] / len(labels)))

    rng = random.Random(SAMPLE_SEED)
    idx = rng.sample(range(len(labels)), 100)
    print("\n100-row hand check (seed %d):" % SAMPLE_SEED)
    for i in sorted(idx):
        print("  %-24s %-44s %-22s %s"
              % (words[i][0], words[i][1][:44], posrows[i][1], labels[i]))


if __name__ == "__main__":
    main()
