import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import p1 from '../assets/p1.jpg';
import p2 from '../assets/p2.jpg';
import p3 from '../assets/p3.jpg';
import p4 from '../assets/p4.jpg';
import p5 from '../assets/p5.jpg';
import p6 from '../assets/p6.avif';

const categories = [
  { id: 1, name: 'Political System', image: p1 },
  { id: 2, name: 'Political History', image: p6 },
  { id: 3, name: 'Law', image: p2 },
  { id: 4, name: 'Legal Awareness', image: p5 },
  { id: 5, name: 'Rights', image: p4 },
  { id: 6, name: 'Constitution', image: p3 },
];

const gameRouteMap = {
  "Quiz": "quiz",
  "Sorting Order": "Sorting",
  "CardGame": "Card",
  "Scenario Play": "Scenario",
  "Crossword": "crossword",
}
const gameTypes = Object.keys(gameRouteMap);

const Categories = () => {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const navigate = useNavigate();
  const handleClick = (categoryName) => {
    setSelectedCategory(categoryName);
  };

  const handleClosePopup = () => {
    setSelectedCategory(null);
  };
    const handleGameSelect = (gameName) => {
    const route = gameRouteMap[gameName];
    if (route) {
      navigate(`/game/${route}`);
    }
  };
  return (
    <div className="p-6 bg-gradient-to-br from-blue-100 via-blue-300 to-blue-500 min-h-screen relative">
      <h2 className="text-3xl font-bold mb-10 text-center italic">Explore Categories</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {categories.map((category) => (
          <button
            key={category.id}
            onClick={() => handleClick(category.name)}
            className="rounded-xl overflow-hidden shadow-md hover:shadow-xl transition duration-300 focus:outline-none hover:scale-105"
          >
            <img
              src={category.image}
              alt={category.name}
              className="w-full h-48 object-cover"
            />
            <div className="text-center p-4">
              <h3 className="text-lg font-semibold bg-blue-500 text-white p-2 rounded-2xl">
                {category.name}
              </h3>
            </div>
          </button>
        ))}
      </div>

      {selectedCategory && (
        <div className="absolute top-50 left-1/2 transform -translate-x-1/2 bg-gradient-to-br from-blue-100 via-blue-200 to-blue-300 border-4 border-white rounded-2xl shadow-2xl p-6 w-[700px] h-[400px] z-30 animate-fade-in">
          <h2 className="text-xl font-extrabold text-center mb-5 text-purple-800 drop-shadow">
            🎮 Games for <span className="text-pink-700">{selectedCategory}</span>
          </h2>

          <div className="flex flex-col gap-3 items-center">
            {gameTypes.map((game, index) => (
              <button
                key={index}
                onClick={() => handleGameSelect(game)}
                className="w-full bg-gradient-to-r from-indigo-400 via-purple-500 to-pink-400 text-white py-2 rounded-xl shadow-md hover:scale-105 transition-transform duration-200 text-sm font-semibold"
              >
                {game}
              </button>
            ))}
          </div>

          <div className="text-center mt-5">
            <button
              onClick={handleClosePopup}
              className="text-sm text-purple-700 hover:underline font-medium"
            >
              Close ❌
            </button>
          </div>
        </div>
      )}

    </div>
  );
};

export default Categories;
