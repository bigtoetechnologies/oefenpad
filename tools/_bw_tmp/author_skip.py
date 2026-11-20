# SKIP sets: every member is a SKIP so the whole set goes to the backlog (no card is left without its partner).
def S(i, why, exnl, exen):
    return (i, "SKIP: " + why, "-", "-", "Pair with the other members of the set.", exnl, exen, "-")
T = "Needs a clock or a calendar to show the time, and one drawing cannot show before and after."
CL = [
("dag", "Skipped set: the days relative to today.", "Gisteren was het droog, vandaag regent het en morgen schijnt de zon.", "Yesterday was dry, today it rains and tomorrow the sun shines."),
("moment", "Skipped set: now and later.", "Ik werk nu, maar ik rust straks uit.", "I am working now, but I will rest later."),
("altijd-nooit", "Skipped set: always and never.", "Hij is altijd op tijd, maar zij is nooit op tijd.", "He is always on time, but she is never on time."),
("frequentie", "Skipped set: how often.", "Ik fiets vaak, mijn broer fietst zelden en mijn zus fietst soms.", "I cycle often, my brother rarely cycles and my sister sometimes cycles."),
("al-nog", "Skipped set: already and still.", "Ik ben al klaar, maar jij bent nog bezig.", "I am already done, but you are still busy."),
("plots-geleidelijk", "Skipped set: suddenly and gradually.", "Het licht ging plotseling uit, maar de zon ging geleidelijk onder.", "The light went out suddenly, but the sun set gradually."),
("volgorde", "Skipped set: first and afterwards.", "Eerst eten wij, daarna gaan wij wandelen.", "First we eat, afterwards we go for a walk."),
("zekerheid", "Skipped set: maybe and certainly.", "Misschien komt hij, maar zij komt zeker.", "Maybe he will come, but she will certainly come."),
("opzet", "Skipped set: on purpose and by accident (drawn in Vaste uitdrukkingen).", "Hij deed het expres, maar zij deed het per ongeluk.", "He did it on purpose, but she did it by accident."),
("ontkenning", "Skipped set: affirming and negating.", "Hij komt wel, maar zij komt niet.", "He is coming, but she is not coming."),
]
CARDS = [
S("gisteren", T, "Gisteren was het koud.", "Yesterday it was cold."),
S("vandaag", T, "Vandaag werk ik thuis.", "Today I work at home."),
S("morgen", T, "Morgen ga ik naar de dokter.", "Tomorrow I am going to the doctor."),
S("nu", T, "Ik heb nu geen tijd.", "I have no time now."),
S("straks", T, "Ik bel je straks.", "I will call you later."),
S("altijd", "Frequency needs repeated events; one frozen drawing cannot show every time, and a row of identical panels is not one drawing.", "Hij drinkt altijd koffie.", "He always drinks coffee."),
S("nooit", "Never is an absence of events over time; one drawing can only show a single moment.", "Ik rook nooit.", "I never smoke."),
S("vaak", "Frequency needs repeated events; one frozen drawing cannot show how often.", "Ik ga vaak naar de markt.", "I often go to the market."),
S("zelden", "Frequency needs repeated events; one frozen drawing cannot show how rarely.", "Wij eten zelden vis.", "We rarely eat fish."),
S("soms", "Frequency needs repeated events; one frozen drawing cannot show some of the times.", "Soms neem ik de bus.", "Sometimes I take the bus."),
S("al", "Already compares a moment with an expectation; one drawing cannot show what was expected.", "Ben je al klaar?", "Are you done already?"),
S("nog", "Still compares a moment with an expectation; one drawing cannot show what was expected.", "Het regent nog.", "It is still raining."),
S("plotseling", "Suddenness is a change over time; one drawing cannot show the change.", "Plotseling ging het licht uit.", "Suddenly the light went out."),
S("geleidelijk", "Gradual change needs several stages; one drawing cannot show a process.", "Het wordt geleidelijk warmer.", "It is gradually getting warmer."),
S("eerst", "Order needs two moments; a two-panel sequence is not allowed on one card.", "Eerst bel ik mijn moeder.", "First I call my mother."),
S("daarna", "Order needs two moments; a two-panel sequence is not allowed on one card.", "Daarna ga ik naar huis.", "Afterwards I go home."),
S("misschien", "Doubt has no object to draw; a shrug or a question mark would carry it, and text is not allowed in artwork.", "Misschien regent het morgen.", "Maybe it will rain tomorrow."),
S("zeker", "Certainty has no object to draw; a nod would not separate it from agreement or yes.", "Hij komt morgen zeker.", "He is certainly coming tomorrow."),
S("expres", "duplicate of vaste-uitdrukkingen:met-opzet (the same tipped-glass contrast; Vaste uitdrukkingen draws met opzet / per ongeluk).", "Hij liet het expres vallen.", "He dropped it on purpose."),
S("per-ongeluk", "duplicate of vaste-uitdrukkingen:per-ongeluk.", "Ik heb het per ongeluk gedaan.", "I did it by accident."),
S("wel", "Affirming and negating a fact cannot be drawn without text or a crossed-out image.", "Hij komt wel.", "He is coming, really."),
S("niet", "Negation cannot be drawn without text or a crossed-out image, and a cross is not in the style.", "Ik ben niet moe.", "I am not tired."),
]

# Sets that redraw a card of another family. The rows stay in author_a*.py so the set can come
# back if the other family drops its card; author.py turns each into a SKIP with this reason.
DUP = {
    "hier": "bijvoeglijke-naamwoorden:dichtbij", "daar": "bijvoeglijke-naamwoorden:ver",
    "binnen": "voorzetselpaden:binnen-onder-de-parasol", "buiten": "voorzetselpaden:buiten-in-de-tuin",
    "samen": "bijvoeglijke-naamwoorden:gezellig", "alleen-solo": "bijvoeglijke-naamwoorden:eenzaam",
    "helemaal": "bijvoeglijke-naamwoorden:vol", "bijna": "bijvoeglijke-naamwoorden:vol",
    "beetje": "bijvoeglijke-naamwoorden:vol",
}
