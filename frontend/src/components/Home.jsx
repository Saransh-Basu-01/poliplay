import React from 'react';
import { Link } from 'react-router-dom';
import Poliplay from '../assets/Poliplay.png';

const Home = () => {
  return (
    <div
      className="min-h-screen w-full bg-cover bg-center bg-no-repeat flex items-center justify-center"
      style={{ backgroundImage: `url(${Poliplay})` }}
    >
      <div className="flex flex-col space-y-1 justify-center items-center">
        <Link to="/game" className="pixel-button">
          Game
        </Link>
        <Link to="/resources" className="pixel-button">
          Resources
        </Link>
        <Link to="/leaderboard" className="pixel-button">
          Leaderboard
        </Link>
      </div>
    </div>
  );
};

export default Home;