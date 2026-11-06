    /* =================================================================
       Koppelen — Oefenpad
       ================================================================= */

    const I18N = window.I18N || { lang: 'en', t: function () { return null; }, register: function () {} };
    const WORDS = window.OEFENPAD_WORDS || {};
    // Word images (../wordimages.js): keyed by uppercase English word.
    // Only words present in this manifest can be used in the game.
    const IMAGES = window.OEFENPAD_WORD_IMAGES || {};

    const TEXTS = {
        'page-title':    { en: 'Koppelen — Oefenpad', nl: 'Koppelen — Oefenpad', uk: 'З\'єднай — Oefenpad' },
        'splash-title':  { en: 'Koppelen', nl: 'Koppelen', uk: 'З\'єднай' },
        'app-title':     { en: 'Koppelen', nl: 'Koppelen', uk: 'З\'єднай' },
        'settings-title':{ en: '⚙️ Settings', nl: '⚙️ Instellingen', uk: '⚙️ Налаштування' },
        'sound-effects': { en: '🔊 Sound Effects', nl: '🔊 Geluidseffecten', uk: '🔊 Звукові ефекти' },
        'show-labels':   { en: '🏷️ Show word labels on pictures', nl: '🏷️ Toon woorden bij plaatjes', uk: '🏷️ Показувати слова на малюнках' },
        'close':         { en: 'Close', nl: 'Sluiten', uk: 'Закрити' },
        'pairs-4':       { en: '4 Pairs', nl: '4 paren', uk: '4 пари' },
        'pairs-6':       { en: '6 Pairs', nl: '6 paren', uk: '6 пар' },
        'pairs-8':       { en: '8 Pairs', nl: '8 paren', uk: '8 пар' },
        'pairs-10':      { en: '10 Pairs', nl: '10 paren', uk: '10 пар' },
        'pairs-12':      { en: '12 Pairs', nl: '12 paren', uk: '12 пар' },
        'pairs-left':    { en: '🔗 Left: {n}', nl: '🔗 Over: {n}', uk: '🔗 Залишилось: {n}' },
        'moves-label':   { en: 'Moves', nl: 'Zetten', uk: 'Ходи' },
        'time-label':    { en: '⏱ Time:', nl: '⏱ Tijd:', uk: '⏱ Час:' },
        'hint':          { en: 'Flip one card from each side and match each word with its picture.', nl: 'Draai één kaart van elke kant om en koppel elk woord aan het juiste plaatje.', uk: 'Переверни по одній картці з кожного боку та з\'єднай слово з малюнком.' },
        'cat-title':     { en: 'Choose a Category', nl: 'Kies een categorie', uk: 'Оберіть категорію' },
        'cat-subtitle':  { en: 'Select a theme for your matching game:', nl: 'Kies een thema voor je matchspel:', uk: 'Виберіть тему для гри:' },
        'random-cat':    { en: 'Random Category', nl: 'Willekeurige categorie', uk: 'Випадкова категорія' },
        'btn-new':       { en: '🎲 New Game', nl: '🎲 Nieuw spel', uk: '🎲 Нова гра' },
        'cele-title':    { en: 'All Matched!', nl: 'Alles gekoppeld!', uk: 'Усе з\'єднано!' },
        'cele-msg':      { en: 'Great job! You matched every word to its picture.', nl: 'Goed gedaan! Je hebt elk woord aan het juiste plaatje gekoppeld.', uk: 'Чудова робота! Ти з\'єднав кожне слово з малюнком.' },
        'btn-close':     { en: '✕ Close', nl: '✕ Sluiten', uk: '✕ Закрити' },
        'confirm-new-title': { en: 'Start a New Game?', nl: 'Nieuw spel starten?', uk: 'Почати нову гру?' },
        'confirm-new-msg':   { en: 'This will start a new game. Your current progress will be lost.', nl: 'Dit start een nieuw spel. Je huidige voortgang gaat verloren.', uk: 'Це почне нову гру. Поточний прогрес буде втрачено.' },
        'confirm-ok':        { en: 'Start New Game', nl: 'Nieuw spel starten', uk: 'Почати нову гру' },
        'cancel':        { en: 'Cancel', nl: 'Annuleren', uk: 'Скасувати' },
        'version':       { en: 'Version 0.2.0', nl: 'Versie 0.2.0', uk: 'Версія 0.2.0' }
    };
    I18N.register('koppelen', TEXTS);

    function T(key, vars) { return I18N.t(key, vars) || (TEXTS[key] ? TEXTS[key].en : key); }
    function wordsLang() { return (I18N.lang === 'en' || I18N.lang === 'en-us') ? 'en' : I18N.lang; }
    function catLabel(cat) { return cat.label[I18N.lang] || cat.label.en; }

    // ---- Legacy emoji map — superseded by OEFENPAD_WORD_IMAGES (word images).
    //      Kept only as reference; the game now uses images exclusively. ----
    const WORD_EMOJI = {
        animals: {
            'BEAR':'🐻','WOLF':'🐺','DEER':'🦌','FOX':'🦊','HARE':'🐰','LYNX':'🐈','OTTER':'🦦','BADGER':'🦡',
            'ADDER':'🐍','SALMON':'🐟','ROBIN':'🐦','EAGLE':'🦅','RAVEN':'🐦‍⬛','SEAL':'🦭','WHALE':'🐋',
            'SQUIRREL':'🐿️','HEDGEHOG':'🦔','DOLPHIN':'🐬','PUFFIN':'🐧','OYSTER':'🦪',
            'RACCOON':'🦝','HAMSTER':'🐹','RABBIT':'🐇','LIZARD':'🦎','IBEX':'🐐','BEAVER':'🦫','PANTHER':'🐆',
            'BUFFALO':'🐃','BABOON':'🐒','GORILLA':'🦍','CHIMP':'🐵','ORANG':'🦧','KOALA':'🐨','WALLABY':'🦘',
            'DINGO':'🐕','PEACOCK':'🦚','FLAMINGO':'🦩','MACAW':'🦜','TOAD':'🐸','WILD BOAR':'🐗'
        },
        nature: {
            'FOREST':'🌲','OAK':'🌳','MAPLE':'🍁','FERN':'🌿','CLOVER':'🍀','GLACIER':'🧊','VOLCANO':'🌋',
            'BAMBOO':'🎍','TYPHOON':'🌀','FLOOD':'🌊','BLIZZARD':'❄️','TORNADO':'🌪️','PEBBLE':'🪨',
            'SUNRISE':'🌅','SUNSET':'🌇','RAINBOW':'🌈','MIST':'🌫️','DEW':'💧'
        },
        science: {
            'ATOM':'⚛️','GENE':'🧬','WAVE':'🌊','LENS':'🔍','LASER':'🔦','HELIUM':'🎈','COMET':'☄️',
            'MAGNET':'🧲','BACTERIA':'🦠','FUNGUS':'🍄','CRYSTAL':'💎','FOSSIL':'🦴','REPTILE':'🦎',
            'INSECT':'🐜','VOLT':'⚡','SILVER':'🥈','GOLD':'🥇','TELESCOPE':'🔭','MICROSCOPE':'🔬',
            'EXPERIMENT':'🧪','GRAPH':'📊'
        },
        travel: {
            'HOTEL':'🏨','BEACH':'🏖️','CRUISE':'🚢','SAFARI':'🦁','HARBOR':'⚓','CABIN':'🛖','PASSPORT':'🛂',
            'LUGGAGE':'🧳','BACKPACK':'🎒','COMPASS':'🧭','GLOBE':'🌍','MAP':'🗺️','TICKET':'🎫','CAMERA':'📷',
            'TENT':'⛺','ISLAND':'🏝️','JUNGLE':'🌴','DESERT':'🏜️','BRIDGE':'🌉','AIRPORT':'🛫','STATION':'🚉',
            'FERRY':'⛴️','GONDOLA':'🚠','KAYAK':'🛶','HIGHWAY':'🛣️'
        },
        countries: {
            'FRANCE':'🇫🇷','SPAIN':'🇪🇸','ITALY':'🇮🇹','GREECE':'🇬🇷','NORWAY':'🇳🇴','SWEDEN':'🇸🇪','POLAND':'🇵🇱','AUSTRIA':'🇦🇹','HUNGARY':'🇭🇺','SERBIA':'🇷🇸',
            'BRAZIL':'🇧🇷','CANADA':'🇨🇦','MEXICO':'🇲🇽','CHILE':'🇨🇱','JAPAN':'🇯🇵','INDIA':'🇮🇳','KENYA':'🇰🇪','EGYPT':'🇪🇬','GHANA':'🇬🇭','MALTA':'🇲🇹',
            'PORTUGAL':'🇵🇹','BELGIUM':'🇧🇪','DENMARK':'🇩🇰','FINLAND':'🇫🇮','ICELAND':'🇮🇸','IRELAND':'🇮🇪','CROATIA':'🇭🇷','ROMANIA':'🇷🇴','BULGARIA':'🇧🇬','ESTONIA':'🇪🇪',
            'ARGENTINA':'🇦🇷','COLOMBIA':'🇨🇴','PERU':'🇵🇪','BOLIVIA':'🇧🇴','URUGUAY':'🇺🇾','MOROCCO':'🇲🇦','TUNISIA':'🇹🇳','ALGERIA':'🇩🇿','NIGERIA':'🇳🇬','ANGOLA':'🇦🇴',
            'VIETNAM':'🇻🇳','THAILAND':'🇹🇭','MYANMAR':'🇲🇲','MALAYSIA':'🇲🇾','INDONESIA':'🇮🇩','PHILIPPINES':'🇵🇭','PAKISTAN':'🇵🇰','TURKEY':'🇹🇷','UKRAINE':'🇺🇦','GEORGIA':'🇬🇪',
            'LATVIA':'🇱🇻','SLOVAKIA':'🇸🇰','SLOVENIA':'🇸🇮','ALBANIA':'🇦🇱','ARMENIA':'🇦🇲','MOLDOVA':'🇲🇩','LITHUANIA':'🇱🇹','MONTENEGRO':'🇲🇪','LUXEMBOURG':'🇱🇺','NETHERLANDS':'🇳🇱',
            'ECUADOR':'🇪🇨','PARAGUAY':'🇵🇾','HONDURAS':'🇭🇳','GUATEMALA':'🇬🇹','NICARAGUA':'🇳🇮','PANAMA':'🇵🇦','JAMAICA':'🇯🇲','BAHAMAS':'🇧🇸','BARBADOS':'🇧🇧','GRENADA':'🇬🇩',
            'SENEGAL':'🇸🇳','UGANDA':'🇺🇬','RWANDA':'🇷🇼','MALAWI':'🇲🇼','ZAMBIA':'🇿🇲','NAMIBIA':'🇳🇦','BOTSWANA':'🇧🇼','LESOTHO':'🇱🇸','SWAZILAND':'🇸🇿','ZIMBABWE':'🇿🇼'
        },
        food: {
            'BREAD':'🍞','CHEESE':'🧀','APPLE':'🍎','GRAPE':'🍇','LEMON':'🍋','PEACH':'🍑','MANGO':'🥭','OLIVE':'🫒','ONION':'🧅','GARLIC':'🧄',
            'PASTA':'🍝','PIZZA':'🍕','SUSHI':'🍣','CURRY':'🍛','STEAK':'🥩','BACON':'🥓','HONEY':'🍯','BUTTER':'🧈','COFFEE':'☕','COCOA':'🍫',
            'JUICE':'🧃','WATER':'💧','SODA':'🥤','MILK':'🥛','ALMOND':'🌰','PEANUT':'🥜','BERRY':'🫐','CHERRY':'🍒','NOODLE':'🍜','TACO':'🌮',
            'BAGEL':'🥯','WAFFLE':'🧇','MUFFIN':'🧁','COOKIE':'🍪','CARAMEL':'🍬','SALAD':'🥗','SOUP':'🍲','FRY':'🍟','CARROT':'🥕','POTATO':'🥔',
            'TOMATO':'🍅','PEPPER':'🫑','PEA':'🫛','BEAN':'🫘','PINEAPPLE':'🍍','COCONUT':'🥥','BANANA':'🍌','ORANGE':'🍊','MELON':'🍈','KIWI':'🥝',
            'GINGER':'🫚','BURGER':'🍔','SANDWICH':'🥪','OMELET':'🍳','PANCAKE':'🥞','DOUGHNUT':'🍩','PUDDING':'🍮','TART':'🥧'
        },
        sports: {
            'SOCCER':'⚽','TENNIS':'🎾','RUGBY':'🏉','CRICKET':'🏏','HOCKEY':'🏑','BOXING':'🥊','GOLF':'⛳','JUDO':'🥋','RACING':'🏎️','SKIING':'⛷️',
            'ROWING':'🚣','DIVING':'🤿','FENCING':'🤺','ARCHERY':'🏹','CYCLING':'🚴','SAILING':'⛵','SURFING':'🏄','CLIMBING':'🧗','MEDAL':'🏅','TROPHY':'🏆',
            'STADIUM':'🏟️','POOL':'🏊','GOAL':'🥅','JOCKEY':'🏇','WRESTLING':'🤼','WEIGHTLIFTING':'🏋️','GYMNASTICS':'🤸','ATHLETICS':'🏃','BASKETBALL':'🏀',
            'BASEBALL':'⚾','VOLLEYBALL':'🏐','HANDBALL':'🤾','LACROSSE':'🥍','BADMINTON':'🏸','BOWLING':'🎳','PADDLE':'🏓','HELMET':'⛑️','GOGGLES':'🥽',
            'PARACHUTE':'🪂','SKATE':'⛸️'
        },
        music: {
            'PIANO':'🎹','VIOLIN':'🎻','GUITAR':'🎸','FLUTE':'🪈','DRUM':'🥁','HORN':'📯','BALLET':'🩰','JAZZ':'🎷','MICROPHONE':'🎤','TRUMPET':'🎺',
            'BANJO':'🪕','ACCORDION':'🪗','DISCO':'🪩','NOTE':'🎵','SPEAKER':'🔊','HEADPHONE':'🎧','RECORD':'💿'
        },
        movies: {
            'ACTOR':'🎭','CAMERA':'🎥','CINEMA':'🎬','WESTERN':'🤠','HORROR':'👻','ROMANCE':'💕','HERO':'🦸','POPCORN':'🍿','TICKET':'🎫',
            'PROJECTOR':'📽️','SCIENCE FICTION':'🛸','MAKEUP':'💄','PYROTECHNICS':'🎆'
        },
        literature: {
            'NOVEL':'📖','LIBRARY':'📚','PEN':'🖊️','QUILL':'🪶','LETTER':'✉️','NOTEBOOK':'📓','PAGE':'📄','DICTIONARY':'📕'
        },
        history: {
            'CASTLE':'🏰','TEMPLE':'🛕','CROWN':'👑','SWORD':'🗡️','SHIELD':'🛡️','BATTLE':'⚔️','SCROLL':'📜','STONE':'🪨'
        },
        space: {
            'STAR':'⭐','MOON':'🌙','EARTH':'🌍','SATURN':'🪐','COMET':'☄️','GALAXY':'🌌','ROCKET':'🚀','SATELLITE':'🛰️','TELESCOPE':'🔭',
            'ASTRONAUT':'🧑‍🚀','ECLIPSE':'🌑','BLACK HOLE':'🕳️','ARIES':'♈','TAURUS':'♉','GEMINI':'♊','CANCER':'♋','LEO':'♌','VIRGO':'♍','LIBRA':'♎',
            'SCORPIO':'♏','SAGITTARIUS':'♐','CAPRICORN':'♑','AQUARIUS':'♒','PISCES':'♓'
        },
        oceans: {
            'CORAL':'🪸','WAVE':'🌊','BEACH':'🏖️','ANCHOR':'⚓','PIRATE':'🏴‍☠️','FERRY':'⛴️','DOLPHIN':'🐬','WHALE':'🐋','SHARK':'🦈','OCTOPUS':'🐙',
            'JELLYFISH':'🪼','LOBSTER':'🦞','CRAB':'🦀','SHRIMP':'🦐','SQUID':'🦑','DIVER':'🤿','FISHERMAN':'🎣'
        },
        mountains: {
            'GLACIER':'🧊','FUJI':'🗻','HIKING':'🥾','CLIMBING':'🧗','CAMPING':'🏕️','RUCKSACK':'🎒','EAGLE':'🦅','IBEX':'🐐','ICE AXE':'🪓','ROPE':'🪢',
            'CONIFER':'🌲','DECIDUOUS':'🌳'
        },
        technology: {
            'COMPUTER':'💻','PRINTER':'🖨️','MONITOR':'🖥️','KEYBOARD':'⌨️','MOUSE':'🖱️','CLOUD':'☁️','MOBILE':'📱','ROBOT':'🤖','BATTERY':'🔋',
            'ANTENNA':'📡','SATELLITE':'🛰️','PASSWORD':'🔑','WEARABLE':'⌚'
        },
        art: {
            'BRUSH':'🖌️','PALETTE':'🎨','GALLERY':'🖼️','SKETCH':'✏️','LANDSCAPE':'🏞️','CERAMIC':'🏺','SCULPTOR':'🗿','YELLOW':'🟡','ORANGE':'🟠',
            'PURPLE':'🟣','EMERALD':'🟢','SAPPHIRE':'🔷'
        },
        fashion: {
            'DRESS':'👗','BLOUSE':'👚','JACKET':'🧥','SCARF':'🧣','GLOVE':'🧤','BOOT':'🥾','SHOE':'👟','WOOL':'🧶','DENIM':'👖','NEEDLE':'🪡',
            'THREAD':'🧵','TIARA':'👑','VEST':'🦺','KIMONO':'👘','HEEL':'👠','SLIPPER':'🥿','HANDBAG':'👜','WALLET':'👛','UMBRELLA':'☂️','SUNGLASSES':'🕶️',
            'WATCH':'⌚','RING':'💍'
        },
        mythology: {
            'THOR':'🔨','DRAGON':'🐉','PHOENIX':'🐦‍🔥','PEGASUS':'🦄','SCROLL':'📜','HERO':'🦸','ELF':'🧝','FAIRY':'🧚','SIREN':'🧜','POSEIDON':'🔱',
            'FENRIR':'🐺','WIZARD':'🧙'
        },
        professions: {
            'DOCTOR':'🩺','PILOT':'👨‍✈️','CHEF':'👨‍🍳','FARMER':'👨‍🌾','MINER':'⛏️','CARPENTER':'🪚','PLUMBER':'🔧','ARTIST':'🎨','ACTOR':'🎭',
            'WRITER':'✍️','DANCER':'💃','SINGER':'🎤','CLOWN':'🤡','JUGGLER':'🤹','MAGICIAN':'🎩','SCIENTIST':'🔬','CHEMIST':'🧪','ASTRONOMER':'🔭',
            'INVENTOR':'💡','DENTIST':'🦷','ARCHITECT':'📐'
        },
        dinosaurs: {
            'TREX':'🦖','BRACHIOSAURUS':'🦕','FOSSIL':'🦴','TOOTH':'🦷','SKULL':'💀','NEST':'🪺','EGG':'🥚','HATCHLING':'🐣','MEGALODON':'🦈',
            'MAMMOTH':'🦣','DIG':'⛏️'
        },
        flowers: {
            'ROSE':'🌹','DAISY':'🌼','TULIP':'🌷','LOTUS':'🪷','LEAF':'🍃','BLOSSOM':'🌸','SUNFLOWER':'🌻','BOUQUET':'💐','HIBISCUS':'🌺',
            'SEED':'🌱','SUCCULENT':'🪴','CACTUS':'🌵'
        },
        marine: {
            'SHARK':'🦈','WHALE':'🐋','DOLPHIN':'🐬','SEAL':'🦭','OTTER':'🦦','TURTLE':'🐢','TUNA':'🐟','OCTOPUS':'🐙','SQUID':'🦑','JELLYFISH':'🪼',
            'LOBSTER':'🦞','CRAB':'🦀','OYSTER':'🦪','CORAL':'🪸','SPONGE':'🧽','PENGUIN':'🐧','NAUTILUS':'🐚'
        },
        insects: {
            'ANT':'🐜','BEE':'🐝','FLY':'🪰','BEETLE':'🪲','LADYBUG':'🐞','CRICKET':'🦗','BUTTERFLY':'🦋','CATERPILLAR':'🐛','SPIDER':'🕷️',
            'SCORPION':'🦂','WEB':'🕸️','HONEY':'🍯','MOSQUITO':'🦟'
        },
        household: {
            'CHAIR':'🪑','SOFA':'🛋️','BED':'🛏️','MIRROR':'🪞','CLOCK':'🕰️','WINDOW':'🪟','BASKET':'🧺','LANTERN':'🏮','CANDLE':'🕯️','VASE':'🏺',
            'PLATE':'🍽️','BOWL':'🥣','MUG':'☕','HAMMER':'🔨','LADDER':'🪜','BUCKET':'🪣','BROOM':'🧹','WRENCH':'🔧','LOCK':'🔒','KEY':'🔑',
            'OUTLET':'🔌','FAUCET':'🚰','SHOWER':'🚿','BATHTUB':'🛁','TOILET':'🚽','CUTLERY':'🍴','SKILLET':'🍳'
        }
    };

    const PAIR_OPTIONS = [4, 6, 8, 10, 12];
    const MIN_PAIRS = 4;
    const MAX_WORD_LEN = 12;

    // ---- State ----
    let state = {
        category: 'animals',
        pairs: 6,
        pairsData: [],       // chosen pairs: {id, word, emoji}
        matched: {},         // id -> true
        firstCard: null,     // currently flipped card element
        lock: false,
        moves: 0,
        seconds: 0,
        status: 'playing'
    };
    let timerInterval = null;
    let timerStarted = false;
    let settings = { soundEffects: true, showLabels: false };
    let stats = { gamesWon: 0, bestTime: null };

    // ---------- Utilities ----------
    // Shared helpers live in src/shared/common.js
    function shuffle(arr) { return OEFENPAD.shuffle(arr); }

    function fmtTime(seconds) { return OEFENPAD.fmtTime(seconds); }

    // ---------- Pair building ----------
    function mappedPairsFor(categoryKey) {
        const cat = WORDS[categoryKey];
        if (!cat || !cat.words) return [];
        const lang = wordsLang();
        const seenImg = {};
        const seenWord = {};
        const pairs = [];
        for (let i = 0; i < cat.words.length; i++) {
            const entry = cat.words[i];
            if (!entry.en || !entry[lang]) continue;
            const img = IMAGES[entry.en];
            if (!img) continue;
            const word = entry[lang];
            if (!word || word.length > MAX_WORD_LEN) continue;
            if (seenImg[img]) continue;
            if (seenWord[word]) continue;
            seenImg[img] = true;
            seenWord[word] = true;
            pairs.push({ id: i, word: word, img: img });
        }
        return pairs;
    }

    function playableCategories() {
        return Object.keys(WORDS).filter(function (key) {
            return mappedPairsFor(key).length >= MIN_PAIRS;
        });
    }

    // ---------- Game flow ----------
    function startGame() {
        stopTimer();
        timerStarted = false;
        const cat = WORDS[state.category];
        if (!cat) state.category = 'animals';

        const available = mappedPairsFor(state.category);
        const count = Math.min(state.pairs, available.length);
        const chosen = shuffle(available).slice(0, count);

        state.pairsData = chosen;
        state.matched = {};
        state.firstCard = null;
        state.lock = false;
        state.moves = 0;
        state.seconds = 0;
        state.status = 'playing';
        resetPop();

        renderPanels();
        renderStatus();
        updatePairButtons();
        closeCelebration();
    }

    function newGame() { startGame(); }

    // ---------- Rendering ----------
    function renderPanels() {
        const wordsPanel = document.getElementById('wordsPanel');
        const picsPanel = document.getElementById('picsPanel');
        wordsPanel.innerHTML = '';
        picsPanel.innerHTML = '';

        const wordOrder = shuffle(state.pairsData.map(function (p) { return p.id; }));
        const picOrder = shuffle(state.pairsData.map(function (p) { return p.id; }));

        // Grid columns per panel: capped at 3 so cards stay large.
        // Extra pairs flow into more rows and the page grows vertically
        // instead of shrinking the cards.
        const cols = Math.min(3, Math.max(2, Math.ceil(state.pairsData.length / 2)));
        wordsPanel.style.gridTemplateColumns = 'repeat(' + cols + ', 1fr)';
        picsPanel.style.gridTemplateColumns = 'repeat(' + cols + ', 1fr)';

        wordOrder.forEach(function (id) {
            const p = state.pairsData.find(function (x) { return x.id === id; });
            const btn = document.createElement('button');
            btn.className = 'match-card';
            btn.dataset.id = id;
            btn.dataset.side = 'word';
            btn.innerHTML =
                '<div class="card-inner">' +
                    '<div class="card-back"></div>' +
                    '<div class="card-face' + (p.word.length > 9 ? ' small-text' : '') +
                        '" aria-hidden="true">' + p.word + '</div>' +
                '</div>';
            labelCard(btn);
            btn.addEventListener('click', function () { flipCard(btn); });
            wordsPanel.appendChild(btn);
        });

        picOrder.forEach(function (id) {
            const p = state.pairsData.find(function (x) { return x.id === id; });
            const btn = document.createElement('button');
            btn.className = 'match-card';
            btn.dataset.id = id;
            btn.dataset.side = 'pic';
            btn.innerHTML =
                '<div class="card-inner">' +
                    '<div class="card-back"></div>' +
                    '<div class="card-face" aria-hidden="true"><img src="../../assets/wordimages/' + p.img + '" alt=""></div>' +
                '</div>';
            labelCard(btn);
            btn.addEventListener('click', function () { flipCard(btn); });
            picsPanel.appendChild(btn);
        });
    }

    function renderStatus() {
        const cat = WORDS[state.category];
        document.getElementById('categoryEmoji').textContent = cat ? cat.icon : '';
        document.getElementById('categoryName').textContent = cat ? catLabel(cat) : '';
        const left = state.pairsData.length - Object.keys(state.matched).length;
        document.getElementById('pairsLeft').textContent = T('pairs-left', { n: left });
        document.getElementById('movesCount').textContent = '🎯 ' + state.moves;
        document.getElementById('timerDisplay').textContent = '⏱ ' + fmtTime(state.seconds);
        document.querySelectorAll('.diff-btn').forEach(function (btn) {
            btn.classList.toggle('active', Number(btn.dataset.pairs) === state.pairs);
        });
    }

    function updatePairButtons() {
        const available = mappedPairsFor(state.category).length;
        document.querySelectorAll('.diff-btn').forEach(function (btn) {
            btn.disabled = Number(btn.dataset.pairs) > available;
        });
    }

    // ---------- Flip & match logic (memory style) ----------
    // ---------- Card zoom ----------
    let popActive = false;
    let popOnDone = null;
    let popHoldTimer = null;
    let popOutTimer = null;

    function pairForBtn(btn) {
        return state.pairsData.find(function (p) { return p.id == btn.dataset.id; });
    }

    function A11Y(key, vars, fallback) {
        const s = I18N.t(key, vars);
        return s === null ? fallback : s;
    }

    // The face sits in the DOM from the start, only rotated out of view, so it
    // stays aria-hidden until flipped — otherwise a screen reader just reads
    // every answer off the board.
    function labelCard(btn) {
        const all = Array.prototype.slice.call(
            btn.parentNode ? btn.parentNode.children : [btn]);
        const i = Math.max(0, all.indexOf(btn)) + 1;
        const faceUp = btn.classList.contains('flipped');
        const faceEl = btn.querySelector('.card-face');
        if (faceEl) faceEl.setAttribute('aria-hidden', faceUp ? 'false' : 'true');

        if (!faceUp) {
            btn.setAttribute('aria-label',
                A11Y('a11y-card-down', { i: i }, 'Card ' + i + ', face down'));
            return;
        }
        const p = pairForBtn(btn);
        const what = p ? p.word : '';
        const matched = p && state.matched[p.id];
        const key = matched ? 'a11y-card-matched' : 'a11y-card-up';
        btn.setAttribute('aria-label',
            A11Y(key, { i: i, what: what },
                 'Card ' + i + ', ' + what + (matched ? ', matched' : '')));
    }

    function relabelCards() {
        document.querySelectorAll('.match-card').forEach(labelCard);
    }

    function fillZoomCard(card, content, isImg, word) {
        if (isImg) {
            card.className = 'zoom-card';
            card.innerHTML = '<img src="' + content + '" alt="">';
            if (word) {
                const w = document.createElement('div');
                w.className = 'zoom-word';
                w.textContent = word;
                card.appendChild(w);
            }
        } else {
            card.className = 'zoom-card zoom-text';
            card.textContent = content;
        }
    }

    function openZoom(content, isImg, word) {
        if (popActive) return;
        const card = document.getElementById('zoomCard');
        fillZoomCard(card, content, isImg, word);
        document.getElementById('zoomOverlay').classList.remove('hidden');
    }
    function closeZoom() {
        if (popActive) return;
        document.getElementById('zoomOverlay').classList.add('hidden');
    }

    function beginPopOut() {
        if (!popActive) return;
        clearTimeout(popHoldTimer);
        clearTimeout(popOutTimer);
        const card = document.getElementById('zoomCard');
        card.classList.remove('zoom-pop');
        card.classList.add('zoom-pop-out');
        popOutTimer = setTimeout(function () {
            document.getElementById('zoomOverlay').classList.add('hidden');
            card.classList.remove('zoom-pop-out');
            popActive = false;
            const cb = popOnDone;
            popOnDone = null;
            if (cb) cb();
        }, 500);
    }

    // Tear the popup down immediately, dropping any pending callback. Called
    // when a new game is dealt (the board the callback closed over is gone)
    // and at the top of autoPop, so a second pop can never leave the first
    // one's hold timer running — that timer would fire early and resolve the
    // *new* pop ahead of time.
    function resetPop() {
        clearTimeout(popHoldTimer);
        clearTimeout(popOutTimer);
        popHoldTimer = null;
        popOutTimer = null;
        popActive = false;
        popOnDone = null;
        const card = document.getElementById('zoomCard');
        if (card) card.classList.remove('zoom-pop', 'zoom-pop-out');
        const overlay = document.getElementById('zoomOverlay');
        if (overlay) overlay.classList.add('hidden');
    }

    // Esc or a click sends the popup back to normal size early.
    function dismissPop() { if (popActive) beginPopOut(); }

    // Auto pop: the just-flipped card spins up to full size, holds ~1s,
    // then spins back down to its proper size on the board.
    function autoPop(btn, onDone) {
        resetPop();
        popActive = true;
        popOnDone = onDone;
        const face = btn.querySelector('.card-face');
        const img = face ? face.querySelector('img') : null;
        const pair = pairForBtn(btn);
        const card = document.getElementById('zoomCard');
        card.className = '';
        if (img) {
            fillZoomCard(card, img.getAttribute('src'), true, settings.showLabels && pair ? pair.word : '');
        } else {
            fillZoomCard(card, face ? face.textContent.trim() : '', false);
        }
        card.classList.add('zoom-pop');
        document.getElementById('zoomOverlay').classList.remove('hidden');
        popHoldTimer = setTimeout(beginPopOut, 1400);
    }

    function flipCard(btn) {
        // Face-up cards zoom their content instead of flipping.
        if (btn.classList.contains('flipped')) {
            const face = btn.querySelector('.card-face');
            const img = face ? face.querySelector('img') : null;
            const pair = pairForBtn(btn);
            if (img) openZoom(img.getAttribute('src'), true, settings.showLabels && pair ? pair.word : '');
            else openZoom(face ? face.textContent.trim() : '', false);
            return;
        }
        if (state.lock) return;
        if (state.status !== 'playing') return;
        if (state.matched[btn.dataset.id]) return;

        // Rule: the two flipped cards must come from opposite sides.
        // Same-side second pick is rejected with a shake — no move counted.
        if (state.firstCard && btn.dataset.side === state.firstCard.dataset.side) {
            btn.classList.add('deny');
            setTimeout(function () { btn.classList.remove('deny'); }, 400);
            playWrongSound();
            return;
        }

        btn.classList.add('flipped');
        labelCard(btn);
        playFlipSound();

        if (!timerStarted) {
            timerStarted = true;
            startTimer();
        }

        if (!state.firstCard) {
            state.firstCard = btn;
            autoPop(btn);
            return;
        }

        // Second card flipped
        const firstId = state.firstCard.dataset.id;
        const secondId = btn.dataset.id;
        state.moves++;
        renderStatus();

        if (firstId === secondId) {
            // Word ↔ picture match
            state.matched[firstId] = true;
            state.firstCard.classList.add('matched');
            btn.classList.add('matched');
            relabelCards();
            state.firstCard = null;
            renderStatus();
            playCorrectSound();
            const isWin = Object.keys(state.matched).length === state.pairsData.length;
            state.lock = true;
            autoPop(btn, function () {
                state.lock = false;
                if (isWin) winGame();
            });
        } else {
            // No match — pop the card, then flip both back
            state.lock = true;
            const prev = state.firstCard;
            state.firstCard = null;
            autoPop(btn, function () {
                prev.classList.add('wrong');
                btn.classList.add('wrong');
                playWrongSound();
                setTimeout(function () {
                    prev.classList.remove('flipped', 'wrong');
                    btn.classList.remove('flipped', 'wrong');
                    relabelCards();
                    state.lock = false;
                }, 350);
            });
        }
    }

    // ---------- Win ----------
    function winGame() {
        stopTimer();
        state.status = 'won';
        stats.gamesWon++;
        if (stats.bestTime === null || state.seconds < stats.bestTime) {
            stats.bestTime = state.seconds;
        }
        saveStats();
        document.getElementById('celeMoves').textContent = state.moves;
        document.getElementById('celeTime').textContent = fmtTime(state.seconds);
        document.getElementById('celebrationOverlay').classList.remove('hidden');
        spawnConfetti();
        playFanfare();
    }

    function closeCelebration() {
        document.getElementById('celebrationOverlay').classList.add('hidden');
    }

    // ---------- Timer ----------
    function startTimer() {
        stopTimer();
        timerInterval = setInterval(function () {
            if (state.status === 'playing') {
                state.seconds++;
                document.getElementById('timerDisplay').textContent = '⏱ ' + fmtTime(state.seconds);
            }
        }, 1000);
    }
    function stopTimer() {
        if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
    }

    // ---------- Category picker ----------
    function buildCategoryGrid() {
        const grid = document.getElementById('categoryGrid');
        grid.innerHTML = '';
        const cats = playableCategories();
        if (cats.indexOf(state.category) === -1 && cats.length) state.category = cats[0];
        cats.forEach(function (key) {
            const cat = WORDS[key];
            const btn = document.createElement('button');
            btn.className = 'cat-btn';
            btn.innerHTML = '<span>' + cat.icon + '</span><span>' + catLabel(cat) + '</span>';
            btn.addEventListener('click', function () {
                closeCategoryPicker();
                const apply = function () { state.category = key; startGame(); };
                if (inProgress()) askNewGame(apply);
                else apply();
            });
            grid.appendChild(btn);
        });
        const randBtn = document.createElement('button');
        randBtn.className = 'cat-btn random-btn';
        randBtn.innerHTML = '<span>🎲</span><span>' + T('random-cat') + '</span>';
        randBtn.addEventListener('click', function () {
            const apply = function () {
                state.category = cats[Math.floor(Math.random() * cats.length)];
                startGame();
            };
            closeCategoryPicker();
            if (inProgress()) askNewGame(apply);
            else apply();
        });
        grid.appendChild(randBtn);
    }

    function openCategoryPicker() { document.getElementById('categoryOverlay').classList.remove('hidden'); }
    function closeCategoryPicker() { document.getElementById('categoryOverlay').classList.add('hidden'); }

    // ---------- Settings ----------
    function openSettings() {
        document.getElementById('settingSoundEffects').checked = settings.soundEffects;
        document.getElementById('settingShowLabels').checked = settings.showLabels;
        document.getElementById('settingsOverlay').classList.remove('hidden');
    }
    function closeSettings() { document.getElementById('settingsOverlay').classList.add('hidden'); }
    function updateSetting(key, value) {
        settings[key] = value;
        saveSettings();
    }
    function saveSettings() {
        try { localStorage.setItem('oefenpad-koppelen-settings', JSON.stringify(settings)); } catch (e) {}
    }
    function loadSettings() {
        try {
            const saved = JSON.parse(localStorage.getItem('oefenpad-koppelen-settings') || 'null');
            if (saved) settings = Object.assign(settings, saved);
        } catch (e) {}
    }
    function saveStats() {
        try { localStorage.setItem('oefenpad-koppelen-stats', JSON.stringify(stats)); } catch (e) {}
    }
    function loadStats() {
        try {
            const saved = JSON.parse(localStorage.getItem('oefenpad-koppelen-stats') || 'null');
            if (saved) stats = Object.assign(stats, saved);
        } catch (e) {}
    }

    // ---------- Audio ----------
    // Tones and the shared AudioContext live in common.js.
    function playFlipSound() { OEFENPAD.sfx.flip(settings.soundEffects); }
    function playCorrectSound() { OEFENPAD.sfx.correct(settings.soundEffects); }
    function playWrongSound() { OEFENPAD.sfx.wrong(settings.soundEffects); }
    function playFanfare() { OEFENPAD.sfx.fanfare(settings.soundEffects); }

    // ---------- Confetti ----------
    function spawnConfetti() {
        OEFENPAD.spawnConfetti({
            container: 'confettiContainer',
            colors: ['#FFB300', '#009688', '#E57373', '#64B5F6', '#81C784', '#BA68C8'],
            count: 80,
            duration: [2, 4],
            delay: [0, 0.6],
            clear: false,
            removeAfter: 4600
        });
    }

    // ---------- Splash ----------
    function hideSplash() { OEFENPAD.hideSplash('splashScreen', 600); }

    // ---------- Language change ----------
    let lastLang = I18N.lang;
    document.addEventListener('i18nchange', function () {
        buildCategoryGrid();
        renderStatus();
        if (I18N.lang === lastLang) return;
        lastLang = I18N.lang;
        if (inProgress()) askNewGame(startGame);
        else startGame();
    });

    // ---------- New-game confirmation ----------
    let pendingNewGame = null;
    function inProgress() {
        return state.status === 'playing' &&
            (state.moves > 0 || Object.keys(state.matched).length > 0 || state.firstCard !== null);
    }
    function askNewGame(cb) {
        pendingNewGame = cb;
        document.getElementById('confirmOverlay').classList.remove('hidden');
    }
    function confirmNewGame() {
        document.getElementById('confirmOverlay').classList.add('hidden');
        const cb = pendingNewGame;
        pendingNewGame = null;
        if (cb) cb();
    }
    function cancelNewGame() {
        document.getElementById('confirmOverlay').classList.add('hidden');
        pendingNewGame = null;
    }

    // ---------- Init ----------
    function init() {
        loadSettings();
        loadStats();
        buildCategoryGrid();
        document.querySelectorAll('.diff-btn').forEach(function (btn) {
            btn.addEventListener('click', function () {
                const n = Number(btn.dataset.pairs);
                if (n === state.pairs) return;
                const apply = function () { state.pairs = n; renderStatus(); startGame(); };
                if (inProgress()) askNewGame(apply);
                else apply();
            });
        });
        startGame();
        document.getElementById('zoomOverlay').addEventListener('click', function () {
            if (popActive) dismissPop(); else closeZoom();
        });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') { if (popActive) dismissPop(); else closeZoom(); }
        });
        const splash = document.getElementById('splashScreen');
        splash.addEventListener('click', hideSplash);
        setTimeout(hideSplash, 2500);
        window.addEventListener('beforeunload', function (e) {
            if (inProgress()) { e.preventDefault(); e.returnValue = ''; }
        });
    }
    init();
