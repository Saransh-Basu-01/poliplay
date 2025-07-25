import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home'
import Leaderboard from './leaderboard/leaderboard'
import Categories from './games/categories'
import Timeline from './Resources/Timeline'
import Quiz from './games/Quiz'
import Crossword from './games/Crossword'
import Match from './games/Match'
import Scenario from './games/Scenarioplay'
import Sorting from './games/sorting'
const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/game">
          <Route index element={<Categories />} />
          <Route path="quiz" element={<Quiz />} />
          <Route path="crossword" element={<Crossword />} />
          <Route path="Match" element={<Match />} />
          <Route path="Scenario" element={<Scenario />} />
          <Route path="Sorting" element={<Sorting />} />
        </Route>
        <Route path="/resources" element={<Timeline />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
      </Routes>
    </Router>
  )
}

export default App