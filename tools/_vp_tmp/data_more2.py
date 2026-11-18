"""B1 batch added by the 15 Nov 2026 verb-preposition audit, second run.

Schema per group:
  page, band, stem, action (single|cluster|append|convert), preps, noot,
  chunks[{chunk, gloss, cards[{id, scene, must, avoid, note, nl, en,
                              builds[2], q, answer, alt}]}]

Every card here is a proposal: no art yet, so no data-verdict and no counts
beyond the honest ones the page derives from the example total.
"""

GROUPS = [
# ---------------------------------------------------------------- B1
{
 "page": "b1.html", "band": "b1", "stem": "slagen", "action": "convert",
 "preps": ["voor", "in"], "noot": "slagen voor names the test you pass; slagen in names the task you manage.", "chunks": [{
  "chunk": "slagen in", "gloss": "to succeed in",
  "cards": [{
   "id": "slagen-in-het-examen",
   "scene": "a woman stands at a small table with both hands on a stiff window that has jammed halfway. The right hand pushes the frame up, the left hand steadies the sill, teeth set and one foot braced back on the floor. A potted plant sits on the sill, a full watering can stands beside her chair and a calendar hangs on the wall. The hands forcing the stuck frame up are the clearest mark.",
   "must": "managing a tricky job by hand.",
   "avoid": "a leap with a rolled certificate (slagen voor het examen); a party with balloons; a person sitting back with a cup; a closed door still shut (mislukken).",
   "note": "The idiom is er ... in slagen (om te): the er holds the place of the task and in names it. Slagen voor het examen in the section beside this one is passing a test; slagen in is getting a job done, and it is often used with the er pattern.",
   "nl": "Zij slaagt erin het raam open te krijgen.",
   "en": "She succeeds in getting the window open.",
   "builds": ["Zij slaagt erin het raam open te krijgen", "Hij slaagt erin het raam open te krijgen"],
   "q": "Duwt de vrouw met haar handen tegen het raam?", "answer": "Ja",
   "alt": "Een vrouw duwt met beide handen een klem zittend raam omhoog, tanden op elkaar en een voet naar achteren; op de vensterbank staat een plant en naast haar stoel een gieter."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "spreken", "action": "cluster",
 "preps": ["met", "over"], "noot": "met names the person, over names the subject; praten met and praten over are the everyday twin of both.", "chunks": [{
  "chunk": "spreken met", "gloss": "to speak with",
  "cards": [{
   "id": "spreken-met-de-buurvrouw",
   "scene": "an older woman stands at her front gate with one hand resting on the gate post, head turned up to the neighbour who leans over the low hedge towards her. The neighbour holds a broom in one hand and lifts the other in greeting; a bicycle leans by the gate and a cat sits on the step behind her. The two faces turned to each other across the hedge are the clearest mark.",
   "must": "two neighbours talking together.",
   "avoid": "one person addressing a row of seated listeners (spreken over); a handshake at a first meeting (kennismaken met); two people arguing; a phone at the ear.",
   "note": "met names the person spoken to, and both sides talk. The everyday twin is praten met; spreken met is the same shape in a more formal register, and it is the verb to pick when the meeting is arranged rather than casual.",
   "nl": "Zij spreekt met de buurvrouw bij het hek.",
   "en": "She speaks with the neighbour at the gate.",
   "builds": ["Zij spreekt met de buurvrouw bij het hek", "Hij spreekt met de buurman bij het hek"],
   "q": "Staan de twee mensen bij een hek?", "answer": "Ja",
   "alt": "Een oudere vrouw staat bij haar tuinhek met een hand op de paal en kijkt naar de buur die over de lage heg naar haar toe leunt, een bezem in de ene hand."
  }]
 },
 {
  "chunk": "spreken over", "gloss": "to speak about",
  "cards": [{
   "id": "spreken-over-de-verhuizing",
   "scene": "a man stands at the head of a small table in a plain room, one hand flat on the table and the other raised open as he addresses three people seated facing him. All three look up at him. On the table lie an open cardboard box with a folded blanket over the edge and a roll of tape, and a large house shape is drawn in chalk on the board behind him. The chalk house behind the seated row is the clearest mark.",
   "must": "one speaker raising a subject for a group.",
   "avoid": "two people facing each other (spreken met); a packed moving van in the street (verhuizen naar); a crowd with blank placards (protesteren tegen de plannen); a list of addresses on the board.",
   "note": "over names the subject that is spoken about, not the listener. The everyday twin is praten over; spreken over is its formal counterpart, and it often stands with a noun where praten over would take a verb.",
   "nl": "Hij spreekt over de verhuizing met zijn buren.",
   "en": "He speaks about the move with his neighbours.",
   "builds": ["Hij spreekt over de verhuizing met zijn buren", "Zij spreekt over de verhuizing met haar buren"],
   "q": "Kijken de mensen op tafel naar de spreker?", "answer": "Ja",
   "alt": "Een man staat aan het hoofd van een kleine tafel met een platte hand op het blad en een open hand omhoog, en spreekt drie mensen aan die aan de tafel zitten; achter hem staat een huis in krijt op het bord."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "informeren", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "informeren naar", "gloss": "to ask about",
  "cards": [{
   "id": "informeren-naar-de-openingstijden",
   "scene": "a man stands at a shop counter with his free hand held up flat against a question on his face, leaning slightly forward. The shop assistant behind the counter turns a page of a thick booklet with one hand and points at a line with the other. A large blank clock is painted on the shop window and a trolley stands behind the man. The assistant turning the booklet while the man waits is the clearest mark.",
   "must": "asking what the times or details are.",
   "avoid": "a full trolley at the till (betalen); a nurse at a desk with a form (een afspraak maken); one person speaking to a group; a shop closed with the shutter down.",
   "note": "naar names the information being asked for, not the person being asked. Informeren is the formal verb; vragen naar is the everyday one with the same naars, and both take the thing asked about.",
   "nl": "Hij informeert naar de openingstijden van de winkel.",
   "en": "He asks about the shop's opening hours.",
   "builds": ["Hij informeert naar de openingstijden van de winkel", "Zij informeert naar de openingstijden van de winkel"],
   "q": "Staat de man bij de balie van de winkel?", "answer": "Ja",
   "alt": "Een man staat met een open hand bij de toonbank van een winkel en kijkt vragend; de verkoper achter de balie slaat een dik boekje open en wijst een regel aan."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "recht hebben", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "recht hebben op", "gloss": "to be entitled to",
  "cards": [{
   "id": "recht-hebben-op-een-vergoeding",
   "scene": "a man sits at a desk with a letter held in one hand and a folded banknote resting on the desk beside a pen and a mug. He points a finger at one line on the page with his other hand and his shoulders are squared. A second, unopened envelope lies by the mug. The banknote on the desk under his finger is the clearest mark.",
   "must": "being owed money because of a rule or a loss.",
   "avoid": "a person counting coins into a purse (betalen aan); a handshake and a shop bag (krijgen van); a letter being torn up in anger; a person at a cash machine.",
   "note": "op names the thing one is owed. Recht is a noun, so hebben carries the tense; the partner frame without the noun is geen recht hebben op, and it is the same op.",
   "nl": "Hij heeft recht op een vergoeding voor de vertraging.",
   "en": "He is entitled to compensation for the delay.",
   "builds": ["Hij heeft recht op een vergoeding voor de vertraging", "Wij hebben recht op een vergoeding voor de vertraging"],
   "q": "Ligt er geld op het bureau?", "answer": "Ja",
   "alt": "Een man zit aan een bureau met een brief in de ene hand en wijst met de vinger naar een regel; naast hem liggen een pen, een mok en een opgevouwen bankbiljet."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "protesteren", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "protesteren tegen", "gloss": "to protest against",
  "cards": [{
   "id": "protesteren-tegen-de-plannen",
   "scene": "four people stand in a row on a pavement facing a tall construction fence, each holding up a blank placard on a stick. The nearest one has the mouth open in a shout and one fist forward at chest height. Behind the fence stands a half-built building with two cranes. Three passers-by walk past without stopping. The row of blank signs raised at the fence is the clearest mark.",
   "must": "a group openly opposing a building plan.",
   "avoid": "lettering or symbols on the placards; a calm two-person discussion (praten over); a queue at a counter; a party with balloons.",
   "note": "tegen names the thing being opposed; it is the opposite pole of voor in protesteren voor. The same verb takes both, and only the preposition shows which side the group is on.",
   "nl": "De buurt protesteert tegen de plannen voor een nieuwe weg.",
   "en": "The neighbourhood protests against the plans for a new road.",
   "builds": ["De buurt protesteert tegen de plannen voor een nieuwe weg", "De inwoners protesteren tegen de plannen voor een nieuwe weg"],
   "q": "Houdt iedereen een bord omhoog?", "answer": "Ja",
   "alt": "Vier mensen staan in een rij op de stoep tegenover een hoge bouwschutting met blanco borden aan stokken; de voorste roept met een gebalde vuist, achter de schutting staan twee kranen."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "overtuigen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "overtuigen van", "gloss": "to convince of",
  "cards": [{
   "id": "overtuigen-van-het-gelijk",
   "scene": "two people sit at opposite sides of a small table, each with a sheet of paper in front and a pen in one hand. The one on the left leans forward with both palms open over the table, pointing a finger at one line on the right person's sheet. That person sits back with an arm folded across the chest, mouth pulled to one side. A mug stands between them. The finger on the other sheet and the open palms are the clearest mark.",
   "must": "one person pressing another towards agreement.",
   "avoid": "two people shouting with jagged bubbles (ruzie maken met); a judge with a hammer; a handshake (akkoord gaan met); a sign with words.",
   "note": "van names the point one is convinced about, not the person convinced: je overtuigt iemand van iets. Iemand overtuigen om te is the other shape, used for getting someone to do something.",
   "nl": "Hij overtuigt de buurman van zijn gelijk.",
   "en": "He convinces the neighbour that he is right.",
   "builds": ["Hij overtuigt de buurman van zijn gelijk", "Zij overtuigt de buurvrouw van haar gelijk"],
   "q": "Leunt de persoon links naar de ander toe?", "answer": "Ja",
   "alt": "Twee mensen zitten tegenover elkaar aan een kleine tafel met een vel papier en een pen; de linker leunt voorover met open handpalmen en wijst naar een regel op het papier van de rechter, die achterover zit met een arm over de borst."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "spijt hebben", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "spijt hebben van", "gloss": "to regret",
  "cards": [{
   "id": "spijt-hebben-van-de-keuze",
   "scene": "a woman sits on a sofa with an open letter in her lap, one hand pressed flat to her forehead and eyes on the floor. On the low table before her lies a torn sheet and a mug gone cold; a second, framed picture stands face down behind the mug. A coat hangs over the arm of the sofa with a shop receipt curling out of the pocket. The hand flat to the forehead is the clearest mark.",
   "must": "looking back at a choice with regret.",
   "avoid": "a person jumping with a rolled certificate (slagen voor het examen); a crowd at a party; a person reading without reaction (lezen); an envelope still sealed.",
   "note": "van names the thing one regrets doing or choosing. Spijt is a noun, so hebben carries the tense; the twin shape with a verb is er spijt van hebben dat, where the van stays behind.",
   "nl": "Zij heeft spijt van haar keuze.",
   "en": "She regrets her choice.",
   "builds": ["Zij heeft spijt van haar keuze", "Hij heeft spijt van zijn keuze"],
   "q": "Zit de vrouw met een hand aan het hoofd?", "answer": "Ja",
   "alt": "Een vrouw zit op een bank met een open brief op schoot en een platte hand tegen het voorhoofd, de blik op de grond; op de lage tafel liggen een gescheurd vel en een koude mok."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "zeker zijn", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "zeker zijn van", "gloss": "to be sure of",
  "cards": [{
   "id": "zeker-zijn-van-de-uitslag",
   "scene": "a man stands at a noticeboard in a corridor with one finger held on a list of plain lines, the other hand in a fist at his side. He faces the board square on, chin up, and does not look at the two people behind him who lean to squint at the same list. A door with a blank plate stands beside the board. The finger planted on the list and the upright posture are the clearest mark.",
   "must": "knowing the result already and needing no confirmation.",
   "avoid": "a shrugged shoulder and a tilted head (twijfelen); a person asking at a counter (informeren naar); a certificate held up high; a crowd arguing.",
   "note": "van names the thing one is sure about. Zeker is an adjective, so zijn carries the tense; the twin is onzeker zijn over, where the uncertainty turns to over.",
   "nl": "Hij is zeker van de uitslag van het examen.",
   "en": "He is sure of the exam result.",
   "builds": ["Hij is zeker van de uitslag van het examen", "Zij is zeker van de uitslag van het examen"],
   "q": "Kijkt de man op het bord?", "answer": "Ja",
   "alt": "Een man staat recht voor een prikbord in de gang en houdt een vinger op een lijst met kale regels; achter hem leunen twee mensen naar voren om mee te kijken."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "gevoelig zijn", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "gevoelig zijn voor", "gloss": "to be sensitive to",
  "cards": [{
   "id": "gevoelig-zijn-voor-kritiek",
   "scene": "a woman sits at a desk with both hands gathered in her lap and her head low, shoulders drawn in. On the desk before her lies a sheet with a red line drawn under one paragraph, and a colleague at the next desk points at that line with a pencil while talking. Three other colleagues work on, looking down. The low head beside the red line is the clearest mark.",
   "must": "reacting strongly and quietly to criticism.",
   "avoid": "a crowd with blank placards (protesteren tegen de plannen); a smile and a shrug; a doctor with a stethoscope (allergisch zijn voor); a person shouting back.",
   "note": "voor names what one reacts to. Gevoelig is an adjective, so zijn carries the tense; allergisch zijn voor is the physical twin used for medicines, foods and pollen rather than words.",
   "nl": "Zij is gevoelig voor kritiek van haar collega's.",
   "en": "She is sensitive to criticism from her colleagues.",
   "builds": ["Zij is gevoelig voor kritiek van haar collega's", "Hij is gevoelig voor kritiek van zijn collega's"],
   "q": "Zit de vrouw met gebogen hoofd?", "answer": "Ja",
   "alt": "Een vrouw zit met beide handen in de schoot en het hoofd laag aan een bureau waar een vel met een rood onderstreepte regel ligt; een collega ernaast wijst met een potlood naar die regel."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "zich interesseren", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "zich interesseren voor", "gloss": "to be interested in",
  "cards": [{
   "id": "zich-interesseren-voor-de-kunst",
   "scene": "a visitor stands close to a large canvas on a museum wall, head tipped back and chin lifted, one hand resting on the low barrier rail. The canvas shows only colour and shape, no picture. A second visitor walks past the low barrier without turning. A folded museum map hangs from the first visitor's hand. The hand on the rail and the tipped-back head are the clearest mark.",
   "must": "leaning in to look properly at a work of art.",
   "avoid": "a person taking a photo of the canvas and walking off; a queue at a till; a handshake (kennismaken met); a painting with a face on it.",
   "note": "voor names the thing that draws the attention. The verb is reflexive, so the pronoun changes with the subject: ik interesseer me, hij interesseert zich. Geinteresseerd zijn in is the adjective frame and turns to in; this one keeps voor.",
   "nl": "Hij interesseert zich voor kunst.",
   "en": "He is interested in art.",
   "builds": ["Hij interesseert zich voor kunst", "Zij interesseert zich voor kunst"],
   "q": "Staat de bezoeker dicht bij het schilderij?", "answer": "Ja",
   "alt": "Een bezoeker staat dicht bij een groot schilderij in een museum met het hoofd achterover en een hand op de lage afzetting; een ander loopt langs zonder te kijken."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "studeren", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "studeren voor", "gloss": "to study for",
  "cards": [{
   "id": "studeren-voor-het-examen",
   "scene": "a learner sits hunched at a library desk with a thick open book propped against two others, one hand moving a finger down the page and the other tapping a pen on a notebook. A stack of coloured cards lies to the side and a small blank clock stands on the desk. An empty chair faces the desk and the room is otherwise still. The finger tracking a line of print is the clearest mark.",
   "must": "working through books to pass a coming test.",
   "avoid": "an exam hall with rows of desks and an invigilator (examen doen); a hand raised with two fingers counting (oefenen voor het examen); a classroom with a teacher; readable text in the book.",
   "note": "voor names the goal the study is aimed at, not the school subject. Studeren voor is the same voor as oefenen voor; studeren aan is the subject or the institution, as in studeren aan de universiteit.",
   "nl": "Zij studeert voor het examen.",
   "en": "She is studying for the exam.",
   "builds": ["Zij studeert voor het examen", "Hij studeert voor het examen"],
   "q": "Zit de persoon met een open boek?", "answer": "Ja",
   "alt": "Een cursist zit gebogen aan een tafel in de bibliotheek met een dik open boek en een vinger langs de regel; ernaast liggen kleurkaartjes en een klein klokje."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "besteden", "action": "cluster",
 "preps": ["aan"], "noot": "the object of besteden is what is spent, and aan names where it goes.", "chunks": [{
  "chunk": "aandacht besteden aan", "gloss": "to pay attention to",
  "cards": [{
   "id": "aandacht-besteden-aan-de-tuin",
   "scene": "a gardener kneels on a mat in a vegetable garden, holding a small seedling between thumb and forefinger and setting it upright in a straight row of earth. The other hand pats the soil round the base. A trowel, a coil of string and a watering can stand along the bed. The hand setting the small plant straight is the clearest mark.",
   "must": "tending one small thing with care.",
   "avoid": "a person mowing a lawn in a hurry (werken in de tuin); a hammer and a broken fence (repareren); a garden hose with nobody there; a plant in flower on a shop shelf.",
   "note": "besteden is a verb and aandacht is its object, so the tense sits on besteden: zij besteedt. Aan names what receives the care. The twin frame is aandacht voor, a noun phrase with voor instead of aan.",
   "nl": "Zij besteedt veel aandacht aan de tuin.",
   "en": "She pays a lot of attention to the garden.",
   "builds": ["Zij besteedt veel aandacht aan de tuin", "Hij besteedt veel aandacht aan de tuin"],
   "q": "Zet de persoon een klein plantje in de grond?", "answer": "Ja",
   "alt": "Een tuinier zit op een mat in de groentetuin en zet een klein plantje recht in een rij omgespitte aarde; langs het bed staan een schepje, een bol touw en een gieter."
  }]
 },
 {
  "chunk": "tijd besteden aan", "gloss": "to spend time on",
  "cards": [{
   "id": "tijd-besteden-aan-de-kinderen",
   "scene": "an adult sits on the floor with both knees drawn up, holding two small hands that pull at a picture book open on the rug between them. Two children sit close, one on each side, leaning in towards the page. A model train and a cup of cold tea lie aside on the floor. The book held open between the three heads is the clearest mark.",
   "must": "giving one's time to other people.",
   "avoid": "a person alone at a laptop (werken aan de computer); children at a table while the adult is on a phone; a pile of banknotes (geld besteden aan); a crowded playground with the adult elsewhere.",
   "note": "tijd is the object spent and aan names who gets it. Besteden is separable, so it drifts in the past tense: zij besteedde er tijd aan.",
   "nl": "Hij besteedt veel tijd aan de kinderen.",
   "en": "He spends a lot of time on the children.",
   "builds": ["Hij besteedt veel tijd aan de kinderen", "Zij besteedt veel tijd aan de kinderen"],
   "q": "Zitten de kinderen bij het boek?", "answer": "Ja",
   "alt": "Een volwassene zit met opgetrokken knieen op de vloer en houdt twee kleine handen vast bij een open prentenboek; aan beide kanten leunen twee kinderen naar de bladzijde toe."
  }]
 },
 {
  "chunk": "besteden aan", "gloss": "to spend on",
  "cards": [{
   "id": "besteden-aan-het-huis",
   "scene": "a man stands on a stepladder with a paint roller in one hand and a small tin balanced on the top step beside him. The roller is pressed to a half-painted wall, the line between the old colour and the new one running down beside him. A pile of folded banknotes lies on the drop cloth on the floor with a receipt on top. The roller at the half-painted wall is the clearest mark.",
   "must": "spending money on the home.",
   "avoid": "a person at a till paying for food (betalen); a full shopping bag; a bank with a window; a finished room with no work in progress.",
   "note": "besteden takes a thing as its object: money, time or attention, and aan names where it goes. Geld besteden aan is the money frame; the same verb covers tijd en aandacht, which is why this section sits beside them.",
   "nl": "Wij besteden dit jaar veel geld aan het huis.",
   "en": "This year we spend a lot of money on the house.",
   "builds": ["Wij besteden dit jaar veel geld aan het huis", "Zij besteden dit jaar veel geld aan het huis"],
   "q": "Is de muur nog niet afgeschilderd?", "answer": "Ja",
   "alt": "Een man staat op een trap met een verfroller in de ene hand en een blik op de bovenste trede; de muur is half geschilderd en op het schildersdoek ligt een stapel bankbiljetten met een bon erop."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "achterlaten", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "achterlaten in", "gloss": "to leave behind in",
  "cards": [{
   "id": "achterlaten-in-de-trein",
   "scene": "a person stands on a platform looking back at a train that is pulling away, one hand lifted to the face. Through the window of the train one seat is empty and a folded umbrella of the same colour as the basket in the person's other hand lies on it. A departing sign stands on a post and a barrier arm is down. The umbrella left on the seat behind the moving window is the clearest mark.",
   "must": "leaving something accidentally in a vehicle.",
   "avoid": "a person walking off with the bag in hand (vergeten mee te nemen); a lost-property counter (informeren naar); a bag on a platform seat; a train standing still at the platform.",
   "note": "in names the place the thing stays behind. Achterlaten is separable, so achter moves to the end of the clause: zij laat haar tas in de trein achter.",
   "nl": "Zij laat haar paraplu in de trein achter.",
   "en": "She leaves her umbrella behind on the train.",
   "builds": ["Zij laat haar paraplu in de trein achter", "Hij laat zijn paraplu in de trein achter"],
   "q": "Rijdt de trein weg van het perron?", "answer": "Ja",
   "alt": "Iemand staat op het perron met een hand bij het gezicht en kijkt een wegrijdende trein na; achter het raam blijft een paraplu op een lege stoel liggen."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "bedekken", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "bedekken met", "gloss": "to cover with",
  "cards": [{
   "id": "bedekken-met-een-deken",
   "scene": "a person leans over a sleeping child on a sofa and spreads a folded blanket with both hands so that it settles over the child's legs and shoulders. The child's shoes stand on the floor and a lamp glows on a table beside the sofa. One corner of the blanket still hangs from the person's right hand. The blanket laid over the child is the clearest mark.",
   "must": "putting a cloth over someone or something.",
   "avoid": "a person wrapped up in a blanket for themselves (zich inpakken); a duvet pulled over a bed being made (opmaken); a person holding a blanket but not laying it; a suitcase being packed (inpakken).",
   "note": "met names the thing used to cover. Dutch keeps the part being covered as the direct object and the cloth after met, the reverse of the English order, so the met phrase can move to the front for emphasis.",
   "nl": "Zij bedekt het kind met een deken.",
   "en": "She covers the child with a blanket.",
   "builds": ["Zij bedekt het kind met een deken", "Hij bedekt het kind met een deken"],
   "q": "Legt de persoon de deken over het kind?", "answer": "Ja",
   "alt": "Iemand buigt zich over een slapend kind op de bank en spreidt met beide handen een opgevouwen deken over de benen en de schouders; naast de bank staat een schoenenpaar en brandt een lamp."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "bedoelen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "bedoelen met", "gloss": "to mean by",
  "cards": [{
   "id": "bedoelen-met-dat-woord",
   "scene": "a learner sits at a desk with one finger pressed on a line in an open book and a puzzled face turned to the teacher beside them. The teacher circles a simple picture of a tree on a notepad with a pencil and taps it twice. A dictionary lies shut under the book. The pencil circling the small picture is the clearest mark.",
   "must": "asking what a particular word is meant to point at.",
   "avoid": "a person reading alone without a question on the face (lezen); a dictionary being flipped through; a sign with words on it; a shouted argument (ruzie maken met).",
   "note": "met names the word itself, and the thing meant follows as the object without a preposition: wat bedoel je met dat woord? Bedoelen is about intention; betekenen is about what a word stands for, and that verb takes no met.",
   "nl": "Wat bedoelt de docent met dat woord?",
   "en": "What does the teacher mean by that word?",
   "builds": ["Wat bedoelt de docent met dat woord", "Wat bedoelt de cursist met dat woord"],
   "q": "Wijst de docent naar een plaatje op het notitieblok?", "answer": "Ja",
   "alt": "Een cursist zit aan een tafel met een vinger op een regel in een open boek en kijkt vragend naar de docent ernaast, die met een potlood een simpele boom op een blocnote omcirkelt."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "begrijpen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "begrijpen van", "gloss": "to understand about",
  "cards": [{
   "id": "begrijpen-van-de-uitleg",
   "scene": "a man sits at a table with a sheet of paper in front of him and both hands on his head, staring at a column of scribbled workings. Beside him a second person points a pencil at one line and nods, mouth open in explanation. Crumpled sheets lie on the floor around the chair and a clock stands on the table. The crumpled sheets on the floor are the clearest mark.",
   "must": "failing to follow an explanation.",
   "avoid": "a person smiling and nodding (snappen); a full rubbish bin with nothing on the table; a teacher at a board with a class (lesgeven); words on the paper.",
   "note": "van names the part or the thing one does or does not understand. Dutch often pairs it with veel or weinig: veel begrijpen van, weinig begrijpen van. The bare verb takes the thing as its object; van is what marks a share of it.",
   "nl": "Hij begrijpt weinig van de uitleg.",
   "en": "He understands little of the explanation.",
   "builds": ["Hij begrijpt weinig van de uitleg", "Zij begrijpt weinig van de uitleg"],
   "q": "Zit er een tweede persoon naast de man?", "answer": "Ja",
   "alt": "Een man zit aan tafel met beide handen aan het hoofd en kijkt naar een vel met krabbels; naast hem wijst iemand met een potlood een regel aan, terwijl er proppen papier op de vloer liggen."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "dreigen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "dreigen met", "gloss": "to threaten with",
  "cards": [{
   "id": "dreigen-met-ontslag",
   "scene": "a manager stands behind a desk pointing a finger at the door, jaw set and brows down. Opposite the desk a worker sits with clenched hands on the chair arms, face pale and eyes on the manager. On the desk lie a closed folder and a blank sheet turned face down. The finger pointed at the door is the clearest mark.",
   "must": "warning someone that something bad will follow.",
   "avoid": "a handshake (akkoord gaan met); a group with blank placards (protesteren tegen de plannen); a worker packing a box with nobody else present; a shrug (twijfelen).",
   "note": "met names the bad thing held up as the consequence. Dreigen takes met and a noun; with a whole clause Dutch prefers dat: hij dreigt ermee dat hij opstapt.",
   "nl": "De baas dreigt met ontslag.",
   "en": "The boss threatens dismissal.",
   "builds": ["De baas dreigt met ontslag", "De directeur dreigt met ontslag"],
   "q": "Wijst de baas naar de deur?", "answer": "Ja",
   "alt": "Een baas staat achter een bureau en wijst met de vinger naar de deur, terwijl een medewerker tegenover hem met gebalde vuisten op de stoelleuning zit en naar hem kijkt."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "het hebben", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "het hebben over", "gloss": "to be talking about",
  "cards": [{
   "id": "het-hebben-over-het-weer",
   "scene": "two people sit at a kitchen table facing each other with cups in front, one leaning back with a hand behind the head and the other resting both elbows on the table. Each has a blank speech bubble above the head, and the two bubbles hold the same sun behind a striped cloud. A radio stands on the sill behind them. The matching sun and cloud in both bubbles are the clearest mark.",
   "must": "two people in a talk whose subject is shared.",
   "avoid": "one person lecturing a group (spreken over de verhuizing); a handshake (akkoord gaan met); a weather chart with numbers on a wall; a storm blowing through the kitchen window.",
   "note": "het hebben over puts the subject after over, and het is fixed: it is the same het whatever the speaker. Without het the phrase becomes hebben over, which is not Dutch; the everyday twin is praten over.",
   "nl": "Zij hebben het over het weer.",
   "en": "They are talking about the weather.",
   "builds": ["Zij hebben het over het weer", "Wij hebben het over het weer"],
   "q": "Staat er in beide tekstballonnen een zon achter een wolk?", "answer": "Ja",
   "alt": "Twee mensen zitten tegenover elkaar aan een keukentafel met koppen koffie; boven elk hoofd hangt een tekstballon met dezelfde zon achter een gestreepte wolk."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "een hekel hebben", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "een hekel hebben aan", "gloss": "to hate",
  "cards": [{
   "id": "een-hekel-hebben-aan-hardlopen",
   "scene": "a runner stands bent over with hands on the knees on a park path, chest heaving, mouth open, a hand towel hanging limp from one hand. Running shoes sit tied at the feet, a water bottle stands on the kerb and a second runner jogs past with an easy face. The bent-over runner beside the passing one is the clearest mark.",
   "must": "an activity the person cannot stand.",
   "avoid": "a runner crossing a finish line with a ribbon (winnen van); a head shaking over a plate of food (vies vinden); two people with jagged bubbles (ruzie maken met); a jogger going happily uphill.",
   "note": "aan names the thing disliked. The frame keeps the indefinite een, so the dislike counts as a thing the person carries, not a property of the sport. Without een the phrase is not Dutch; the bare object, ik haat hardlopen, is the blunter verb.",
   "nl": "Hij heeft een hekel aan hardlopen.",
   "en": "He hates running.",
   "builds": ["Hij heeft een hekel aan hardlopen", "Zij heeft een hekel aan hardlopen"],
   "q": "Staat de hardloper gebogen met de handen op de knieen?", "answer": "Ja",
   "alt": "Een hardloper staat gebogen met de handen op de knieen op een pad in het park, buiten adem met een handdoek in een hand, terwijl een ander rustig voorbij jogt."
  }]
 }]
},
]
