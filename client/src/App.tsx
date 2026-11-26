import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { GameList } from './site/GameList';
import { HangmanGame } from './games/hangman/HangmanGame';
import { MemoryGame } from './games/memory/MemoryGame';
import { MatchingGame } from './games/matching/MatchingGame';
import { WordSearchGame } from './games/wordsearch/WordSearchGame';
import { StoryMachineGame } from './games/storymachine/StoryMachineGame';
import { PrepositionsGame } from './games/prepositions/PrepositionsGame';
import { VerbGame } from './games/verbs/VerbGame';
import { SeparableGame } from './games/separable/SeparableGame';

export function App() {
  return (
    <BrowserRouter basename="/spelen">
      <Routes>
        <Route path="/" element={<GameList />} />
        <Route path="/hangman" element={<HangmanGame />} />
        <Route path="/memory" element={<MemoryGame />} />
        <Route path="/matching" element={<MatchingGame />} />
        <Route path="/wordsearch" element={<WordSearchGame />} />
        <Route path="/storymachine" element={<StoryMachineGame />} />
        <Route path="/prepositions" element={<PrepositionsGame />} />
        <Route path="/verbs" element={<VerbGame />} />
        <Route path="/separable" element={<SeparableGame />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
