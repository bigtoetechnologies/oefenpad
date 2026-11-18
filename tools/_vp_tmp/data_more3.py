"""Batches added by the 15 Nov 2026 verb-preposition audit, part three (B1).

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
 "page": "b1.html", "band": "b1", "stem": "herkennen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "herkennen aan", "gloss": "to recognise by",
  "cards": [{
   "id": "herkennen-aan-de-stem",
   "scene": "a woman stands at a kitchen sink with her back to the open doorway, a plate in one soapy hand. Through the doorway behind her a second woman stands in the hall speaking, mouth open. The woman at the sink has turned her head suddenly over her shoulder towards the door, not yet looking at it. A tea towel hangs on the oven handle and a radio sits silent on the counter. The head turned over the shoulder is the clearest mark.",
   "must": "recognising someone by a feature, without seeing the face.",
   "avoid": "seeing the face and embracing (kennismaken met); two people shaking hands; a phone held to the ear (horen van); a dog with its nose down (speuren naar).",
   "note": "aan names the feature that gives the person away, a voice, a walk, a smell. kennismaken met is meeting someone for the first time; herkennen aan is knowing who it is before you see them.",
   "nl": "Ik herken de buurvrouw aan haar stem.",
   "en": "I recognise the neighbour by her voice.",
   "builds": ["Ik herken de buurvrouw aan haar stem", "Wij herkennen de buurvrouw aan haar stem"],
   "q": "Kijkt de vrouw naar de deur?", "answer": "Ja",
   "alt": "Een vrouw staat bij de gootsteen met de rug naar de deuropening en draait haar hoofd om over haar schouder, terwijl in de gang iemand staat te praten; een theedoek hangt aan de oven en de radio staat stil."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "horen van", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "horen van", "gloss": "to hear of",
  "cards": [{
   "id": "horen-van-het-nieuws",
   "scene": "two people stand close together in a shop doorway, the one on the left speaking with a raised open hand and the mouth open, the one on the right with the eyebrows lifted and a flat hand pressed to the chest. A closed umbrella leans against the wall beside them and no phone is in the frame. The lifted eyebrows and the hand on the chest are the clearest mark.",
   "must": "being told news by another person.",
   "avoid": "a phone held at the ear (bellen met); a newspaper read in both hands; a television on a wall; belonging to a group (horen bij).", 
   "note": "van names the person or place the news comes from. horen bij is belonging, horen van is being told something you did not know.",
   "nl": "Ik hoor net van mijn zus dat ze komt.",
   "en": "I have just heard from my sister that she is coming.",
   "builds": ["Wij horen van de docent dat het examen is verplaatst", "Zij hoort van de docent dat het examen is verplaatst"],
   "q": "Zijn de twee mensen aan het praten?", "answer": "Ja",
   "alt": "Twee mensen staan dicht bij elkaar in een winkeldeur; de een praat met een opgeheven open hand, de ander trekt de wenkbrauwen op en houdt een vlakke hand op de borst; een dichte paraplu leunt tegen de muur."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "leiden", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "leiden tot", "gloss": "to lead to",
  "cards": [{
   "id": "leiden-tot-een-oplossing",
   "scene": "two people sit facing each other at a small table, a sheet of paper between them covered in plain lines and two arrows, one hand of each person pointing at the same spot. A pencil lies in the middle, and a crumpled ball of earlier paper sits on the floor. On both faces the mouth has opened into a smile. The two hands pointing at the same spot are the clearest mark.",
   "must": "one thing producing a result after thought or pressure.",
   "avoid": "a person pointing the way down a street (leiden naar); a guide walking ahead; an argument; a door that opens by itself.",
   "note": "tot names the result that follows. leiden naar is the physical route to a place; leiden tot is a cause that ends in an outcome.",
   "nl": "Overleg tussen buren leidt tot een oplossing.",
   "en": "Consultation between neighbours leads to a solution.",
   "builds": ["Overleg tussen buren leidt tot een oplossing", "Rustig praten tussen buren leidt tot een oplossing"],
   "q": "Kijken de twee mensen naar hetzelfde punt?", "answer": "Ja",
   "alt": "Twee mensen zitten tegenover elkaar aan een tafeltje met een vel papier vol lijnen en twee pijlen; beide handen wijzen naar dezelfde plek en er ligt een prop papier op de grond."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "lenen", "action": "cluster",
 "preps": ["van", "aan"], "noot": "van takes, aan gives", "chunks": [
  {
  "chunk": "lenen van", "gloss": "to borrow from",
  "cards": [{
   "id": "lenen-van-de-buurman",
   "scene": "a person stands on a doorstep holding a drill in one hand towards their own chest, the wire looped around the arm; with the other hand they grip the open door. Inside the doorway the neighbour smiles and lets go of the drill. The drill travelling towards the person on the step is the clearest mark.",
   "must": "receiving an object to use and give back.",
   "avoid": "handing the drill out (lenen aan); the neighbour carrying it away; money changing hands (betalen); a shop counter (huren).",
   "note": "van names the person the thing comes from and stays with the borrower. The twin is lenen aan on this page, the same verb giving the same drill away.",
   "nl": "Ik leen de boor van de buurman.",
   "en": "I borrow the drill from the neighbour.",
   "builds": ["Ik leen de boor van de buurman", "Wij lenen de boor van de buurman"],
   "q": "Geeft de buurman de boor weg?", "answer": "Ja",
   "alt": "Iemand staat op een stoep met een boormachine in de hand naar de eigen borst en houdt met de andere hand de deur vast; in de deuropening laat de buurman de boor los en lacht."
  }]
 }, {
  "chunk": "lenen aan", "gloss": "to lend to",
  "cards": [{
   "id": "lenen-aan-een-vriend",
   "scene": "a person holds out a bicycle with both hands on the handlebars towards a friend standing on the pavement, one foot already on the pedal. The friend reaches for the bars with a wide smile and a helmet slung on the arm. A second bicycle is locked to the rack behind them. The bars passing from the two hands to the friend are the clearest mark.",
   "must": "letting someone else use a thing for a while.",
   "avoid": "getting the bicycle back (lenen van); a bike locked and left alone; a shop buying and selling (verkopen aan); a repair stand.",
   "note": "aan names the person who receives the thing and expects to give it back. The twin is lenen van on this page, where the same verb takes the thing towards the speaker.",
   "nl": "Zij leent haar fiets aan een vriend.",
   "en": "She lends her bike to a friend.",
   "builds": ["Zij leent haar fiets aan een vriend", "Hij leent zijn fiets aan een vriend"],
   "q": "Blijft de fiets bij de vriend?", "answer": "Ja",
   "alt": "Iemand houdt met beide handen een fiets aan het stuur naar een vriend op de stoep, die er al een voet op de trapper heeft en lachend de stang vastpakt; achter hen staat een tweede fiets op slot."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "lijden", "action": "convert",
 "preps": ["aan", "van"], "noot": "aan an illness, van hardship or a condition", "chunks": [
  {
  "chunk": "lijden van", "gloss": "to suffer from",
  "cards": [{
   "id": "lijden-van-de-hitte",
   "scene": "a person sits slumped on the bottom step of a stairwell with a folded newspaper used as a fan in one hand, the other hand pulling at a damp shirt collar. The window above is wide open with the sun full on the glass, and a full bottle of water stands untouched on the floor. The fan in motion and the wet collar are the clearest mark.",
   "must": "suffering from a condition around a person, not a disease.",
   "avoid": "a person in bed with a pill strip (lijden aan); lifting a heavy box (dragen aan); a broken arm in a sling; an empty plate with a rumbling stomach (honger hebben).", 
   "note": "van names the condition the person is under, heat, cold, hunger, drought. lijden aan on this page covers an illness that keeps coming back; lijden van is for hardship and conditions of body or weather.",
   "nl": "De oude mevrouw lijdt van de hitte.",
   "en": "The old lady is suffering from the heat.",
   "builds": ["De oude mevrouw lijdt van de hitte", "De oude man lijdt van de hitte"],
   "q": "Staat er water op de grond?", "answer": "Ja",
   "alt": "Iemand zit onderaan een trap met een opgevouwen krant als waaier in de ene hand en trekt met de andere aan een vochtige kraag; boven staat het raam open en op de grond staat een volle fles water."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "overlaten", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "overlaten aan", "gloss": "to leave to",
  "cards": [{
   "id": "overlaten-aan-de-ouders",
   "scene": "a man stands at a doorway with one hand on the door handle and the other open, palm up, towards a child who is already hanging on a woman's sleeve at the table. The woman looks up from a plate and nods. A school bag lies ready on a chair and the man's own coat stays on the hook behind him. The open palm towards the woman and child is the clearest mark.",
   "must": "handing a decision or a task to someone else.",
   "avoid": "carrying the child out oneself (meenemen); two people arguing over the child; a stranger pointing the way; a handover of money (betalen aan).",
   "note": "aan names the person who takes over the responsibility. overlaten keeps its own party passive, which is why the scene shows a hand open and empty, not holding.",
   "nl": "Hij laat de opvoeding van zijn zoon aan zijn ex-vrouw over.",
   "en": "He leaves his son's upbringing to his ex-wife.",
   "builds": ["Hij laat de opvoeding van zijn zoon aan zijn ex-vrouw over", "Zij laat de opvoeding van haar dochter aan haar ex-man over"],
   "q": "Blijft de man bij de deur staan?", "answer": "Ja",
   "alt": "Een man staat bij de deur met een hand aan de klink en de andere open naar het kind, dat al aan de mouw van een vrouw aan tafel hangt; op een stoel staat een schooltas klaar."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "van plan zijn", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "van plan zijn om te", "gloss": "to intend to",
  "cards": [{
   "id": "van-plan-zijn-om-te-verhuizen",
   "scene": "a person stands in a barely furnished room with three cardboard boxes stacked beside them, one open and stopped in the act of folding a jumper onto the top. The other hand holds a roll of tape. The old sofa is bare and a lamp stands on the floor without a table. The open box with folded clothes is the clearest mark.",
   "must": "an intention to do something, which has not started yet.",
   "avoid": "a moving van at the kerb with the job under way (weggaan); a rented room already furnished; a person signing a contract; a suitcase packed for a trip (vertrekken naar).",
   "note": "zijn is the carrier: zijn van plan zijn om te + whole verb. Without om te a bare infinitive or a noun follows, and om te keeps the intention fixed on the action itself.",
   "nl": "Wij zijn van plan om in mei te verhuizen.",
   "en": "We intend to move house in May.",
   "builds": ["Wij zijn van plan om in mei te verhuizen", "Ik ben van plan om in mei te verhuizen"],
   "q": "Staan de verhuisdozen in de kamer?", "answer": "Ja",
   "alt": "Iemand staat in een bijna lege kamer met drie dozen, waarvan er een openstaat en de hand een trui erin vouwt; de bank is kaal en een lamp staat op de vloer."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "schrijven", "action": "convert", "preps": ["aan", "over"],
 "noot": None, "chunks": [{
  "chunk": "schrijven over", "gloss": "to write about",
  "cards": [{
   "id": "schrijven-over-de-reis",
   "scene": "a person sits at a kitchen table with a pen in one hand and a small notebook open beside a larger sheet filled with plain lines. Beside the sheet lies an open train ticket with no words, a postcard showing a drawn mountain, and a cold cup of tea. The pen resting on the sheet next to the mountain picture is the clearest mark.",
   "must": "writing on a topic, with the subject matter shown beside the page.",
   "avoid": "a letter in an envelope going to one person (schrijven aan); typing on a laptop; a form with boxes (invullen); a book being read (lezen over).",
   "note": "over names the subject the text is about. schrijven aan on this page is writing to a person or working on a text as an object; schrijven over is the topic inside it.",
   "nl": "Zij schrijft over haar reis door Nederland.",
   "en": "She writes about her trip through the Netherlands.",
   "builds": ["Zij schrijft over haar reis door Nederland", "Hij schrijft over zijn reis door Nederland"],
   "q": "Ligt er een kaart met een berg ernaast?", "answer": "Ja",
   "alt": "Iemand zit aan de keukentafel met een pen in de hand, een schrift naast een vel vol lijnen; ernaast liggen een kaartje met een getekende berg en een koud kopje thee."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "stelen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "stelen van", "gloss": "to steal from",
  "cards": [{
   "id": "stelen-van-de-bakker",
   "scene": "a person half turns away from a bakery counter with one hand diving a bread roll into an open coat pocket, eyes fixed on the doorway. Behind the counter the baker has both hands full with a tray and looks the other way. A glass display case stands between them with more rolls inside. The roll entering the pocket is the clearest mark.",
   "must": "taking what belongs to someone without paying or asking.",
   "avoid": "the baker handing over bread and taking money (kopen bij); a delivery crate being carried to the door; a child taking its own snack at home; a wallet found on the ground (vinden).",
   "note": "van names the person or shop the thing is taken from. The roll goes out of sight into the pocket rather than into a basket, which is the difference from buying.",
   "nl": "Hij steelt een broodje van de bakker.",
   "en": "He steals a roll from the baker.",
   "builds": ["Hij steelt een broodje van de bakker", "Zij steelt een broodje van de bakker"],
   "q": "Kijkt de bakker naar de persoon?", "answer": "Nee",
   "alt": "Iemand draait zich half weg van de toonbank en stopt met een hand een broodje in de open zak van de jas, de ogen op de deur; de bakker kijkt de andere kant op met een dienblad in de handen."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "vastmaken", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "vastmaken aan", "gloss": "to attach to",
  "cards": [{
   "id": "vastmaken-aan-de-paal",
   "scene": "a person crouches on the pavement with a rope in both hands, looping it twice around a wooden post and pulling it taut. The other end of the rope runs to the handlebars of a bicycle standing beside the post. A padlock lies open on the ground by the knee. The rope looped around the post is the clearest mark.",
   "must": "securing one thing to another so it stays there.",
   "avoid": "untying a knot (losmaken); a bike already locked and the person walking off (vastzitten aan); hanging a coat on a hook; a nail being hammered into a wall.",
   "note": "aan names the thing the object is fixed onto. The action is the fixing; vastzitten aan is the state after it, which is the contrast on this page.",
   "nl": "Zij maakt de fiets met een touw vast aan de paal.",
   "en": "She attaches the bike to the post with a rope.",
   "builds": ["Zij maakt de fiets met een touw vast aan de paal", "Hij maakt de fiets met een touw vast aan de paal"],
   "q": "Is het touw al om de paal?", "answer": "Ja",
   "alt": "Iemand hurkt op de stoep en trekt een touw twee keer om een houten paal, terwijl het andere eind naar het stuur van een fiets loopt; naast de knie ligt een open slot."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "vastzitten", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "vastzitten aan", "gloss": "to be stuck to",
  "cards": [{
   "id": "vastzitten-aan-de-grond",
   "scene": "a tree lies across a garden path with its trunk sunk deep into wet earth, roots torn up and a heavy stone pressed into the bark. Two people lean with both hands on the trunk and push, feet braced, faces strained; the trunk does not move an inch. A spade stands stuck upright in the soil beside the roots. The trunk sunk in the soil while both people push is the clearest mark.",
   "must": "something fixed in place so that it cannot be moved.",
   "avoid": "a person tying a rope round a post (vastmaken aan); a free trunk rolling away; a nail being hammered; a person standing and holding a spade idly.",
   "note": "aan names what the object is held by. Nothing is being done to the tree here, so the scene shows hands pushing and no hands tying: the state is what counts, against vastmaken aan on this page.",
   "nl": "De omgevallen boom zit nog aan de grond vast.",
   "en": "The fallen tree is still stuck to the ground.",
   "builds": ["De omgevallen boom zit nog aan de grond vast", "De omgevallen takken zitten nog aan de grond vast"],
   "q": "Duwen de mensen tegen de stam?", "answer": "Ja",
   "alt": "Een boom ligt over een tuinpad met de stam diep in de natte aarde en een zware steen in de schors; twee mensen duwen met beide handen tegen de stam en de boom beweegt niet."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "vechten", "action": "convert",
 "preps": ["tegen", "met", "voor", "om"], "noot": "tegen a thing, met a person, voor a cause, om a prize", "chunks": [
  {
  "chunk": "vechten met", "gloss": "to fight with",
  "cards": [{
   "id": "vechten-met-de-broer",
   "scene": "two young men stand chest to chest on a living room floor, each gripping the other's forearms with both hands, heads leaned in and teeth clenched. A knocked-over chair lies between their feet and a cushion is on the floor. A third person in the doorway raises both hands to part them. The four locked arms are the clearest mark.",
   "must": "two people in a scuffle with each other.",
   "avoid": "one person against tiredness or a storm (vechten tegen); a trophy held up (vechten om); a placard at a protest march (vechten voor); injuries or weapons of any kind.",
   "note": "met names an opponent of the same size, a person. vechten tegen on this page is a struggle against something bigger, sleep, illness, wind; the two are a pair and must not share a scene.",
   "nl": "De twee broers vechten met elkaar om de afstandsbediening.",
   "en": "The two brothers are fighting each other over the remote control.",
   "builds": ["De twee broers vechten met elkaar om de afstandsbediening", "De twee zussen vechten met elkaar om de afstandsbediening"],
   "q": "Staan er twee mensen tegenover elkaar?", "answer": "Ja",
   "alt": "Twee jonge mannen staan tegenover elkaar op de vloer en pakken elkaars onderarmen vast, de hoofden naar voren; tussen hun voeten ligt een omgevallen stoel en een kussen, en iemand in de deuropening steekt de handen op."
  }]
 }, {
  "chunk": "vechten voor", "gloss": "to fight for",
  "cards": [{
   "id": "vechten-voor-de-vrijheid",
   "scene": "a row of people stand close together at the foot of stone steps, a blank placard held high on two sticks above their heads. One person in front grips the sticks with both hands and lifts the chin; the others hold hands in a line behind. A crowd of the same placards fills the road further back. The blank placard lifted high on two sticks is the clearest mark.",
   "must": "a group standing up together for a cause, without weapons.",
   "avoid": "two people grappling (vechten met); a single person and a trophy (vechten om); a soldier in uniform; written words on the placard.",
   "note": "voor names the cause, a thing wanted, not a person. Unlike vechten met, the people here face the same way, towards a goal, not towards each other.",
   "nl": "De mensen vechten voor hun vrijheid.",
   "en": "The people are fighting for their freedom.",
   "builds": ["De mensen vechten voor hun vrijheid", "De studenten vechten voor hun vrijheid"],
   "q": "Staan de mensen naast elkaar?", "answer": "Ja",
   "alt": "Een rij mensen staat dicht op elkaar onderaan een stenen trap met een leeg bord hoog op twee stokken; een van hen houdt de stokken vast en heft de kin op, de anderen houden elkaars hand vast."
  }]
 }, {
  "chunk": "vechten om", "gloss": "to fight over",
  "cards": [{
   "id": "vechten-om-het-laatste-stuk",
   "scene": "two people reach across a table towards the last slice of cake on a plate, one hand arriving from the left and one from the right, fingers almost touching. One leans forward with a elbow planted on the edge and a grin, the other pulls the plate by its rim towards themselves. An empty tray and a knife with crumbs stand on the side. The two hands meeting over the last slice are the clearest mark.",
   "must": "two people competing for one thing both want.",
   "avoid": "a trophy held up in a stadium (vechten om de beker); two people gripping each other's arms (vechten met); a person eating alone; a full cake nobody touches.",
   "note": "om names the prize both sides want and only one can have. The confusable twin is vechten voor, which is a cause rather than something you can carry off, and vechten om de beker, a sporting final.",
   "nl": "De kinderen vechten om het laatste stuk taart.",
   "en": "The children are fighting over the last piece of cake.",
   "builds": ["De kinderen vechten om het laatste stuk taart", "De broers vechten om het laatste stuk taart"],
   "q": "Staat er nog een stuk taart op het bord?", "answer": "Ja",
   "alt": "Twee mensen reiken over tafel naar het laatste stuk taart, een hand van links en een van rechts; een van hen leunt voorover met een elleboog op de tafel en de ander trekt het bord aan de rand naar zich toe."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "veranderen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "veranderen in", "gloss": "to turn into",
  "cards": [{
   "id": "veranderen-in-een-vlinder",
   "scene": "a green caterpillar clings to a twig with its front segments already a smooth dark shape and a pair of wings half unfolded from the back, still crumpled and wet. The empty shell hangs on the twig below it with a split down the side. A leaf beside it is half eaten and the morning light falls across the wings. The split shell under the half-open wings is the clearest mark.",
   "must": "one thing becoming another thing, visibly in between.",
   "avoid": "a whole butterfly on a flower, no caterpillar; a person in a costume with sewn wings; a picture frame on the wall; two separate insects.",
   "note": "in names what the thing becomes. The in-between state is what makes the picture teach the verb, because the frame holds both the old and the new form at once.",
   "nl": "De rups verandert in een vlinder.",
   "en": "The caterpillar turns into a butterfly.",
   "builds": ["De rups verandert in een vlinder", "De rupsen veranderen in vlinders"],
   "q": "Zit er nog een rups aan de tak?", "answer": "Ja",
   "alt": "Een groene rups zit aan een takje met al een donker, glad lichaam en twee half uitgevouwen vleugels die nog vochtig zijn; onder hem hangt de lege pop met een scheur erin."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "zich verbazen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "zich verbazen over", "gloss": "to be amazed at",
  "cards": [{
   "id": "zich-verbazen-over-de-prijs",
   "scene": "a shopper stands in an aisle holding up a pair of socks with a small blank card clipped to the hem, the card turned towards the face; the eyebrows are raised high and the mouth is open in a round O. The other hand points at the same card and the trolley beside them is still empty. The raised eyebrows over the lifted card are the clearest mark.",
   "must": "surprise at a fact, shown on the face while looking at it.",
   "avoid": "anger with a fist on the counter (zich ergeren aan); a queue and a tapping foot; a bargain being carried off happily (blij zijn met); a closed wallet.",
   "note": "over names the fact that causes the surprise. The verb is reflexive: zich verbazen over, with zich agreeing with the person, mij verbaas ik, haar verbaast het.",
   "nl": "Zij verbaast zich over de hoge prijs.",
   "en": "She is amazed at the high price.",
   "builds": ["Zij verbaast zich over de hoge prijs", "Hij verbaast zich over de hoge prijs"],
   "q": "Heeft de persoon al boodschappen in de kar?", "answer": "Nee",
   "alt": "Een klant staat in een gangpad met een paar sokken omhoog en een leeg kaartje aan de zoom, naar het gezicht gekeerd; de wenkbrauwen zijn hoog en de mond staat open, de andere hand wijst naar het kaartje en de kar is leeg."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "verdwijnen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "verdwijnen uit", "gloss": "to disappear from",
  "cards": [{
   "id": "verdwijnen-uit-de-kamer",
   "scene": "an empty bedroom with the wardrobe doors hanging open on bare hangers and the bed stripped to a bare mattress. One suitcase stands in the doorway, half out of the frame, a hand visible on its handle. The window is shut and the curtain still. The stripped bed and the suitcase half out of the door are the clearest mark.",
   "must": "a thing leaving a place it used to be, with the place left empty.",
   "avoid": "a person walking towards a door still inside the room; a magician with a hat; an empty room nobody has used; a wallet found under a table.",
   "note": "uit names the place the thing was before and no longer is. The place itself has to be visible and bare, otherwise the picture only says empty.",
   "nl": "De schilderijen verdwijnen uit het museum.",
   "en": "The paintings are disappearing from the museum.",
   "builds": ["De schilderijen verdwijnen uit het museum", "Het schilderij verdwijnt uit het museum"],
   "q": "Staat er nog een koffer in de deuropening?", "answer": "Ja",
   "alt": "Een lege slaapkamer met open kastdeuren vol lege hangers en een bed met alleen een matras; in de deuropening staat een koffer half buiten beeld met een hand aan het hengsel."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "verwachten", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "verwachten van", "gloss": "to expect of",
  "cards": [{
   "id": "verwachten-van-de-leerlingen",
   "scene": "a teacher stands at the front of a classroom with one hand open above a pile of exercise books on the desk and the other arm raised towards the class. Every student sits upright with a book open on the table and a pen in the hand. A clock on the wall is close to the hour and the teacher's eyes are on the class, not on the books. The teacher's raised arm towards the seated class is the clearest mark.",
   "must": "a standard one person expects another to meet.",
   "avoid": "two people greeting each other by the hand (kennismaken met); a parent with a gift (geven aan); an empty room; a student asleep on the desk.",
   "note": "van names the person the expectation is aimed at, the one who has to deliver. verwachten is used with a noun or an object clause: wat verwacht de leraar van hen.",
   "nl": "De leraar verwacht veel van de leerlingen.",
   "en": "The teacher expects a lot of the pupils.",
   "builds": ["De leraar verwacht veel van de leerlingen", "De lerares verwacht veel van de leerlingen"],
   "q": "Zitten de leerlingen rechtop met een boek?", "answer": "Ja",
   "alt": "Een leraar staat voor de klas met een open hand boven een stapel schriften en de andere arm geheven naar de leerlingen, die rechtop met een open boek aan tafel zitten; de klok is bijna op het uur."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "winnen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "winnen van", "gloss": "to beat (a person or team)",
  "cards": [{
   "id": "winnen-van-de-kampioen",
   "scene": "two chess players sit across a board, one leaning back with both arms crossed and a small smile, the other sitting forward with the head in one hand, knocking over a piece with the other. The board is nearly bare and the clock beside it shows the flag dropped on one side. A water glass and a folded scoresheet stand to one side, blank. The dropped clock flag beside the leaning-back player is the clearest mark.",
   "must": "one player getting the better of another.",
   "avoid": "an empty stadium (spelen tegen); a trophy lifted by one person (vechten om de beker); a coin toss; two people shaking hands before the start.",
   "note": "van names the loser, the one who is beaten. The same verb without van takes the prize: de beker winnen; with van it takes the opponent.",
   "nl": "Zij winnen van de kampioen.",
   "en": "They beat the champion.",
   "builds": ["Zij winnen van de kampioen", "Wij winnen van de kampioen"],
   "q": "Is een van de twee spelers achterover gaan zitten?", "answer": "Ja",
   "alt": "Twee schakers zitten tegenover elkaar aan een bijna leeg bord; de een leunt achterover met gekruiste armen en de ander zit voorover met het hoofd in een hand naast een klok met een gevallen vlaggetje."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "gooien", "action": "cluster",
 "preps": ["naar", "tegen"], "noot": "naar a living receiver, tegen a hard surface", "chunks": [
  {
  "chunk": "gooien naar", "gloss": "to throw to",
  "cards": [{
   "id": "gooien-naar-de-hond",
   "scene": "a person in the park swings one arm forward, a ball just leaving the hand in mid-air, the body twisted and one foot lifted. A dog runs towards the ball with its front paws off the grass and its mouth open. A bench and a leashed lead lie on the ground behind. The ball in mid-air between the hand and the dog is the clearest mark.",
   "must": "throwing something towards a living thing that catches it.",
   "avoid": "the ball bouncing off a wall (gooien tegen); a bin with rubbish (weggooien); a person placing a ball on the ground (leggen); two people with a rake.",
   "note": "naar names a receiver who can catch and give the ball back. Its twin here is gooien tegen, where the surface faces the throw but does nothing with it.",
   "nl": "Hij gooit de bal naar de hond.",
   "en": "He throws the ball to the dog.",
   "builds": ["Hij gooit de bal naar de hond", "Zij gooit de bal naar de hond"],
   "q": "Rent de hond achter de bal aan?", "answer": "Ja",
   "alt": "Iemand zwaait in het park een arm naar voren en een bal hangt net uit de hand in de lucht; een hond rent met de voorpoten van de grond naar de bal, en achter hen liggen een bank en een riem."
  }]
 }, {
  "chunk": "gooien tegen", "gloss": "to throw against",
  "cards": [{
   "id": "gooien-tegen-de-muur",
   "scene": "a person stands in a side alley facing a bare brick wall with one arm still following through after the throw. A ball is flattened on the wall, caught mid-contact, and a second ball lies on the ground below. The person faces the wall squarely with nothing between them but the ball. The ball pressed against the brick in mid-bounce is the clearest mark.",
   "must": "throwing something at a hard surface, with no catcher.",
   "avoid": "a ball in the air towards a dog (gooien naar); a bin; a person catching a ball in two hands; a window that has broken.",
   "note": "tegen names the hard surface the object strikes. Its twin here is gooien naar, where something living receives the throw; here the wall gives the ball back.",
   "nl": "Het kind gooit de bal tegen de muur.",
   "en": "The child throws the ball against the wall.",
   "builds": ["Het kind gooit de bal tegen de muur", "Het kind gooit de ballen tegen de muur"],
   "q": "Staat er een muur voor de persoon?", "answer": "Ja",
   "alt": "Iemand staat in een steeg tegenover een kale bakstenen muur met een arm nog in de zwaai; een bal is plat tegen de muur te zien en eronder op de grond ligt een tweede bal."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "vermenigvuldigen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "vermenigvuldigen met", "gloss": "to multiply by",
  "cards": [{
   "id": "vermenigvuldigen-met-zes",
   "scene": "a person sits at a table with a pencil in one hand, pointing with the other at a sheet of paper on which four tallies are drawn in a row and a second row is being added below them. A set of six identical wooden blocks lies beside the sheet. A calculator is turned face down. The six blocks laid out beside the four tallies is the clearest mark.",
   "must": "a number being repeated a set number of times.",
   "avoid": "two numbers being added (optellen bij); a subtraction with a crossed-out line (aftrekken van); a pie being divided at a table (delen door); a dictionary open at a word.",
   "note": "met names the factor the number is repeated by. The pattern is number + vermenigvuldigen met + factor; in the passive met becomes door: vier wordt met zes vermenigvuldigd.",
   "nl": "Vermenigvuldig vier met zes.",
   "en": "Multiply four by six.",
   "builds": ["Zij vermenigvuldigt vier met zes", "Hij vermenigvuldigt vier met zes"],
   "q": "Liggen er blokken naast het papier?", "answer": "Ja",
   "alt": "Iemand zit aan tafel met een potlood in de ene hand en wijst met de andere naar een vel papier met vier streepjes waaronder een tweede rij komt; naast het vel liggen zes blokjes en de rekenmachine ligt ondersteboven."
  }]
 }]
},
]
