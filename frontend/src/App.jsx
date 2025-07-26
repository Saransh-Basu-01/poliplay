import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home'
import Leaderboard from './leaderboard/leaderboard'
import Categories from './games/categories'
import Timeline from './Resources/Timeline'
import Documentation from './Resources/Documentation';
import Chatbot from './Resources/Chatbot';
import Quiz from './games/Quiz'
import Scenario from './games/Scenarioplay'
import Sorting from './games/Sorting'
import CardGame from './games/CardGame';
import Resources from './Resources/Resources';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/game">
          <Route index element={<Categories />} />
          <Route path="quiz" element={<Quiz />} />
          <Route path="Card" element={<CardGame />} />
          <Route path="Scenario" element={<Scenario />} />
          <Route path="Sorting" element={<Sorting />} />
        </Route>
        <Route path="/resources" element={<Resources />} />
        <Route path="/resources/timeline" element={<Timeline />} />
        <Route path="/resources/documentation" element={<Documentation />} />
        <Route path="/resources/chatbot" element={<Chatbot />} />
      </Routes>
    </Router>
  );
};

export default App;
