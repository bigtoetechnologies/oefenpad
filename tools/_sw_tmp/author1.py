# -*- coding: utf-8 -*-
CL = []
CD = []
def C(c, frame, nl, en): CL.append((c, frame, nl, en))
def K(i, scene, must, avoid, contrast, split, nl, en, perfect, alt): CD.append((i, scene, must, avoid, contrast, split, nl, en, perfect, alt))

C('lamp', "one adult in plain clothes stands whole-figure, side view, beside a plain table lamp on a plain table, a hand on the lamp base, same distance from the viewer, a plain wall behind. Only whether the lamp shines, with rays round the shade, or is dark changes.",
  "Ik doe de lamp aan en later doe ik hem weer uit.", "I switch the lamp on and later I switch it off again.")
K('aandoen', "One drawing, one panel. An adult stands beside a plain table lamp on a table with one finger on the switch at the lamp base, and the lamp shines: five bold straight rays leave the shade and the shade has a bright inner outline. The adult looks at the lamp.",
  "bold rays leaving the shade beside a finger on the switch.",
  "the same lamp with no rays (uitdoen); an adult lighting a candle with a match (aansteken); a window with sun rays and no lamp (not the action); a ceiling bulb with nobody near it (not the action).",
  "Pair with uitdoen. The only difference is the lamp: rays round the shade here, no rays there.",
  "doe ... aan", "Ik doe de lamp aan.", "I switch on the lamp.", "heeft aangedaan",
  "Een volwassene houdt een vinger op de schakelaar van een tafellamp en uit de kap komen stralen.")
K('uitdoen', "One drawing, one panel. An adult stands beside the same plain table lamp with one finger on the switch at the lamp base, and the lamp is dark: no rays, a plain shade with an empty outline. The adult looks at the lamp. The room and table are unchanged.",
  "a plain unlit shade with no rays beside a finger on the switch.",
  "the same lamp with rays (aandoen); a lamp knocked over on the table (omvallen); an adult blowing out a candle (uitblazen); a lamp with a cloth thrown over it (not the action).",
  "Pair with aandoen. The only difference is the lamp: no rays at all here, bold rays there.",
  "doe ... uit", "Ik doe de lamp uit.", "I switch off the lamp.", "heeft uitgedaan",
  "Een volwassene houdt een vinger op de schakelaar van een tafellamp en de kap is leeg en vlak.")

C('radio', "one adult in plain clothes stands whole-figure, front view, beside a small plain radio on a shelf at shoulder height, one hand on a round knob, same distance from the viewer, a plain wall behind. Only whether sound lines and notes leave the radio changes.",
  "Ik zet de radio aan en later zet ik hem weer uit.", "I turn the radio on and later I turn it off again.")
K('aanzetten', "One drawing, one panel. An adult stands beside a small radio on a shelf with one hand turning the round knob, and from the radio come three bold curved sound lines and two small music notes. The adult smiles slightly and looks at the radio.",
  "curved sound lines and notes from the radio beside a hand on the knob.",
  "the same radio with no lines (uitzetten); an adult with a hand cupped to an ear (not the card); an adult singing with a speech bubble (not the card); a radio lying on its side (not the action).",
  "Pair with uitzetten. The only difference is the radio: sound lines and notes here, none there.",
  "zet ... aan", "Ik zet de radio aan.", "I turn on the radio.", "heeft aangezet",
  "Een volwassene draait aan een knop van een radio en er komen golvende lijnen en noten uit.")
K('uitzetten', "One drawing, one panel. An adult stands beside the same small radio on a shelf with one hand on the round knob, and the radio is silent: no sound lines, no notes, the speaker plain. The adult looks at the radio with a neutral face.",
  "a plain radio with no sound lines beside a hand on the knob.",
  "the same radio with sound lines and notes (aanzetten); an adult unplugging a cable from the wall (loskoppelen); an adult with fingers in both ears (not the action); a radio on a high shelf out of reach (not the action).",
  "Pair with aanzetten. The only difference is the radio: no lines or notes here, three lines and two notes there.",
  "zet ... uit", "Ik zet de radio uit.", "I turn off the radio.", "heeft uitgezet",
  "Een volwassene houdt een hand op de knop van een radio en de radio is stil.")

C('deur', "one plain wooden door in a plain wall, seen from the front at the same distance, whole door and frame visible, a flat floor line below, a round handle and a small keyhole on the right side, one adult standing beside the frame. Only the door position and the key change.",
  "Ik doe de deur open, doe hem weer dicht en sluit hem daarna af.", "I open the door, close it again and then lock it.")
K('opendoen', "One drawing, one panel. An adult stands beside the door frame holding the round handle with the door swung wide open towards the viewer, so the dark doorway and the thickness of the door are visible. No key is in the keyhole. The adult looks into the doorway.",
  "a door swung wide with a dark gap beside the adult's hand on the handle.",
  "the same door flat shut (dichtdoen); the same door shut with a key turned in the lock (afsluiten); a door open only a crack (not the card); a window opened wide (not the card).",
  "Pair with dichtdoen and afsluiten. The only difference is the door: swung wide here, flat in its frame there.",
  "doe ... open", "Ik doe de deur open.", "I open the door.", "heeft opengedaan",
  "Een volwassene staat naast een deur die wijd naar binnen staat en kijkt in het donkere deurgat.")
K('dichtdoen', "One drawing, one panel. An adult stands beside the door frame with one hand flat on the door and the door sitting flat in its frame with no gap showing; the round handle is level and the keyhole is empty. A short motion line shows the door has just swung.",
  "the door flat in its frame with no gap and a motion line.",
  "the same door swung wide (opendoen); the same door with a key turned in the keyhole (afsluiten); an adult slamming the door with a cartoon burst (not the card); a closed window (not the card).",
  "Pair with opendoen and afsluiten. The only difference is the door: flat shut with no key here, wide open there.",
  "doe ... dicht", "Ik doe de deur dicht.", "I close the door.", "heeft dichtgedaan",
  "Een volwassene legt een hand op een deur die vlak in de sponning zit en er is geen kier.")
K('afsluiten', "One drawing, one panel. An adult stands beside the shut door and turns a plain key in the lock with one hand, the key clearly sticking out of the keyhole, the fingers round the key, and the door sitting flat in its frame. A small turning arrow curves round the key.",
  "a key turning in the keyhole of a shut door.",
  "the same door shut with no key (dichtdoen); the same door open with a key in the lock (opendoen); an adult holding keys in a pocket (not the action); a padlock on a gate (not the card).",
  "Pair with opendoen and dichtdoen. The only difference is the key: turning in the keyhole here, no key anywhere there.",
  "sluit ... af", "Ik sluit de deur af.", "I lock the door.", "heeft afgesloten",
  "Een volwassene draait een sleutel in een deur die vlak in de sponning zit.")

C('koffer', "one adult in plain clothes stands whole-figure, side view, beside a plain open suitcase lying on a bed, a few simple shirts and trousers nearby, same distance from the viewer, a plain wall behind. Only whether the clothes go into the case or come out of it changes.",
  "Ik pak mijn koffer in en na de reis pak ik hem weer uit.", "I pack my suitcase and after the trip I unpack it again.")
K('inpakken', "One drawing, one panel. An adult stands at a bed laying a folded shirt into an open suitcase; half the clothes are already inside the case and two more folded piles still lie on the bed. The adult's hands and the shirt are above the case, a small arrow pointing down into it.",
  "a folded shirt going down into a half-full open suitcase.",
  "the same suitcase being emptied onto the bed (uitpakken); an adult carrying a closed suitcase to a door (meenemen); a suitcase with a folded umbrella next to it (not the card); an adult folding a shirt on the bed with no suitcase (not the card).",
  "Pair with uitpakken. The only difference is the direction: clothes going into the case here, coming out of it there.",
  "pak ... in", "Ik pak mijn koffer in.", "I pack my suitcase.", "heeft ingepakt",
  "Een volwassene legt een gevouwen overhemd in een open koffer op een bed.")
K('uitpakken', "One drawing, one panel. An adult stands at a bed lifting a folded shirt out of the same open suitcase; most clothes already lie in small piles on the bed and the case is nearly empty. The adult's hands and the shirt are above the bed, a small arrow pointing up out of the case.",
  "a shirt lifted out of a nearly empty open suitcase.",
  "the same suitcase being filled (inpakken); an adult opening a wrapped present (not the card); an adult hanging clothes on a rail (not the card); a shut suitcase on the floor (not the action).",
  "Pair with inpakken. The only difference is the direction: clothes coming out of the case here, going into it there.",
  "pak ... uit", "Ik pak mijn koffer uit.", "I unpack my suitcase.", "heeft uitgepakt",
  "Een volwassene haalt een gevouwen overhemd uit een bijna lege koffer en legt het op het bed.")

C('bus', "one plain city bus seen side-on at a plain stop with a single bench, doors open at the middle, a flat kerb line, same distance from the viewer, one adult in plain clothes near the doors. Only whether the adult faces the doors stepping in or turns their back to them stepping out changes.",
  "Ik stap bij de halte in en bij het station stap ik uit.", "I get on at the stop and I get off at the station.")
K('instappen', "One drawing, one panel. A plain bus stands side-on at a stop with its middle doors open, and one adult has one foot on the bus step and the other still on the kerb, chest to the open doors and body leaning in, a small arrow pointing into the bus.",
  "one foot on the bus step, chest to the open doors.",
  "an adult stepping off the bus onto the kerb (uitstappen); an adult waiting on the bench (not the action); an adult driving the bus (not the card); an adult running behind a bus (not the card).",
  "Pair with uitstappen. The only difference is the direction: stepping up into the bus here, down onto the kerb there.",
  "stap ... in", "Ik stap bij de halte in.", "I get on at the stop.", "is ingestapt",
  "Een volwassene zet een voet op de trede van een bus met open deuren en leunt naar binnen.")
K('uitstappen', "One drawing, one panel. The same plain bus stands side-on at the stop with its middle doors open, and one adult has one foot on the kerb and the other still on the bus step, back to the open doors and body leaning out, a small arrow pointing out of the bus.",
  "one foot on the kerb, back to the open doors.",
  "an adult stepping up into the bus (instappen); an adult waving at a bus driving off (not the card); an adult sitting inside the bus (not the action); an adult climbing out of a car (not the card).",
  "Pair with instappen. The only difference is the direction: stepping down onto the kerb here, up into the bus there.",
  "stap ... uit", "Ik stap bij het station uit.", "I get off at the station.", "is uitgestapt",
  "Een volwassene zet een voet op de stoeprand en heeft de rug naar de open deuren van een bus.")

C('telefoon', "one adult in plain clothes sits whole-figure, side view, at a plain table with an old-style desk phone on it, a plain wall behind, same distance from the viewer. Only whether the handset is at the ear or back on the cradle changes.",
  "Ik bel mijn vader op en daarna hang ik op.", "I phone my father and then I hang up.")
K('opbellen', "One drawing, one panel. An adult sits at a table holding the handset of a desk phone against one ear, the other hand on the buttons, mouth slightly open as if speaking, and a thin curl of cable running from the handset to the phone on the table.",
  "a handset held against the ear with the cable running to the phone.",
  "the handset sitting on the cradle with nobody holding it (ophangen); an adult typing on a laptop (not the card); an adult speaking through a megaphone (not the card); an adult texting with both thumbs on a small phone (not the action).",
  "Pair with ophangen. The only difference is the handset: at the ear here, down on its cradle there.",
  "bel ... op", "Ik bel mijn vader op.", "I phone my father.", "heeft opgebeld",
  "Een volwassene aan een tafel houdt een hoorn tegen het oor en drukt met de andere hand op de toetsen.")
K('ophangen', "One drawing, one panel. An adult sits at the same table and lowers the handset of the desk phone onto its cradle with one hand, the handset a few centimetres above the cradle, the cable hanging in a loop, the adult's mouth closed.",
  "a handset a hand's width above its cradle with the cable looped.",
  "the handset held against the ear (opbellen); a coat hung on a wall hook (not this sense); a picture frame hung on a nail (not this sense); an adult putting the phone in a pocket (not the card).",
  "Pair with opbellen. The only difference is the handset: lowered towards the cradle here, held to the ear there.",
  "hang ... op", "Na het gesprek hang ik op.", "After the call I hang up.", "heeft opgehangen",
  "Een volwassene laat de hoorn van een telefoon op de houder zakken en de mond blijft dicht.")

C('station', "one plain railway platform seen from the side with a single plain train carriage on the track beside it, a flat platform edge, same distance from the viewer, one adult with a small suitcase standing still on the platform. Only whether the train's nose enters at the right edge or its tail leaves at the left edge changes.",
  "De trein komt aan en na vijf minuten rijdt hij weer weg.", "The train arrives and after five minutes it drives off again.")
K('aankomen', "One drawing, one panel. A plain train carriage enters from the right edge of the picture, its nose and front door already beside the platform and the rest still off the page, a small arrow pointing left; on the platform an adult with a small suitcase faces the train's nose.",
  "a train nose entering at the right edge with the adult facing it.",
  "the train's tail leaving at the left edge (wegrijden); an adult walking along the platform (not the card); a bus at a stop (not the card); an adult stepping off the train (uitstappen).",
  "Pair with wegrijden. The only difference is the train: its nose entering at the right edge here, its tail leaving at the left edge there.",
  "komt ... aan", "De trein komt om tien uur aan.", "The train arrives at ten o'clock.", "is aangekomen",
  "Een trein stopt bij het perron en een volwassene met een koffer staat met het gezicht naar de voorkant van de trein.")
K('wegrijden', "One drawing, one panel. The same plain train carriage leaves at the left edge of the picture, only its tail end still beside the platform and the front already off the page, a small arrow pointing left; the adult with a small suitcase stands behind it on the platform, hands down.",
  "a train tail leaving at the left edge with the adult behind it.",
  "the train's nose entering at the right edge (aankomen); an adult stepping off the train (uitstappen); a car pulling out of a drive (not the card); a bus at a stop with its doors open (instappen).",
  "Pair with aankomen. The only difference is the train: its tail leaving at the left edge here, its nose entering at the right edge there.",
  "rijdt ... weg", "De trein rijdt om elf uur weg.", "The train drives off at eleven o'clock.", "is weggereden",
  "Een trein verlaat het station en alleen de achterkant staat nog naast het perron, met een volwassene erachter.")
