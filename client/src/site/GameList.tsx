import { Link } from 'react-router-dom';
import { GameShell } from './GameShell';

interface GameEntry {
  route: string;
  name: string;
  about: string;
  kind: string;
}

const GAMES: GameEntry[] = [
  {
    route: '/hangman',
    name: 'Galgje',
    about: 'Raad het woord, letter voor letter.',
    kind: 'Spelling',
  },
  {
    route: '/wordsearch',
    name: 'Woordzoeker',
    about: 'Zoek de woorden in het raster.',
    kind: 'Spelling',
  },
  {
    route: '/memory',
    name: 'Geheugen',
    about: 'Zoek de paren: één woord, één plaatje.',
    kind: 'Woorden',
  },
  {
    route: '/matching',
    name: 'Koppelen',
    about: 'Koppel elk woord aan het juiste plaatje.',
    kind: 'Woorden',
  },
  {
    route: '/prepositions',
    name: 'Voorzetselpaden',
    about: 'Zelfde werkwoord, ander voorzetsel: kijk naar de situatie.',
    kind: 'Betekenis',
  },
  {
    route: '/storymachine',
    name: 'Verhaalmachine',
    about: 'Draai de rollen, vertel het verhaal hardop.',
    kind: 'Spreken',
  },
  {
    route: '/verbs',
    name: 'Werkwoorden',
    about: 'Eén beeld per werkwoord. Kies het juiste beeld.',
    kind: 'Betekenis',
  },
  {
    route: '/separable',
    name: 'Scheidbare werkwoorden',
    about: 'Opbellen, aandoen, meenemen: zie hoe ze splitsen en wat ze betekenen.',
    kind: 'Betekenis',
  },
];

/** The SPA's own index, for anyone who lands on /spelen/ directly. */
export function GameList() {
  return (
    <GameShell game="index" title="Spelen">
      <main className="app-container">
        <div className="spellen-list">
          {GAMES.map((game) => (
            <Link key={game.route} to={game.route}>
              <div>
                <div className="spellen-naam">{game.name}</div>
                <div className="spellen-om">{game.about}</div>
              </div>
              <div className="spellen-et">{game.kind}</div>
            </Link>
          ))}
        </div>
      </main>
    </GameShell>
  );
}
