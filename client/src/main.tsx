import { createRoot } from 'react-dom/client';
import { App } from './App';

import './styles/base.css';
import './styles/games/hangman.css';
import './styles/games/memory.css';
import './styles/games/matching.css';
import './styles/games/wordsearch.css';
import './styles/games/storymachine.css';
import './styles/games/prepositions.css';
import './styles/games/verbs.css';

const root = document.getElementById('root');
if (!root) throw new Error('Missing #root');

createRoot(root).render(<App />);
