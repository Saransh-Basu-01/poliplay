import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import ApiService from '../services/Api';

import sortingData from '../components/data/Sorting';
import ScenarioData from '../components/data/Scenario'; 

import p1 from '../assets/p1.jpg';
import p2 from '../assets/p2.jpg';
import p3 from '../assets/p3.jpg';
import p4 from '../assets/p4.jpg';
import p5 from '../assets/p5.jpg';
import p6 from '../assets/p6.avif';

const images = [p3, p2, p5, p6, p1, p4];

const gameRouteMap = {
  Quiz: 'quiz',
  'Sorting Order': 'Sorting',
  CardGame: 'Card',
  'Scenario Play': 'Scenario',
};
const gameTypes = Object.keys(gameRouteMap);

const Categories = () => {
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    ApiService.fetchCategories()
      .then((data) => {
        // Assume data is an array: [{id, name, ...}]
        setCategories(
          data.map((cat, idx) => ({
            ...cat,
            image: images[idx % images.length] // Assign images in order
          }))
        );
        setLoading(false);
      })
      .catch((err) => {
        setError('Failed to load categories');
        setLoading(false);
      });
  }, []);

  const handleClick = (categoryName) => {
    setSelectedCategory(categoryName);
  };

  const handleClosePopup = () => {
    setSelectedCategory(null);
  };

const handleGameSelect = (gameName) => {
  const route = gameRouteMap[gameName];
  let state = { category: selectedCategory };
  if (route === "Sorting" && sortingData[selectedCategory]) {
    state = { ...state, ...sortingData[selectedCategory] };
  }
  if (route === "Scenario") {
    const categoryScenarios = ScenarioData.filter(item => item.category === selectedCategory);
    if (categoryScenarios.length > 0) {
      state = {
        category: selectedCategory,
        questions: categoryScenarios[0].questions
      };
    }
  }
  if (route) {
    navigate(`/game/${route}`, { state });
  }
};

if (loading) {
  return <div className="flex items-center justify-center min-h-screen">Loading categories...</div>;
}
  if (error) {
    return <div className="flex items-center justify-center min-h-screen text-red-500">{error}</div>;
  }

  return (
    <div className="p-6 bg-gradient-to-br from-blue-100 via-blue-300 to-blue-500 min-h-screen relative ">
      <h2 className="text-3xl font-bold mt-5 text-center italic">Explore Categories</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-24 mt-10 w-6xl container mx-auto">
        {categories.map((category) => (
          <button
            key={category.id}
            onClick={() => handleClick(category.name)}
            className="rounded-xl overflow-hidden shadow-md hover:shadow-xl transition duration-300 focus:outline-none hover:scale-105"
          >
            <img
              src={category.image}
              alt={category.name}
              className="w-full h-76  object-cover"
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
        <div className="absolute top-50 left-1/2 transform -translate-x-1/2 bg-gradient-to-br from-blue-100 via-blue-200 to-blue-300 border-4 border-white rounded-2xl shadow-2xl p-6 w-[600px] h-[500px] z-30 animate-fade-in flex flex-col justify-center items-center">
          <h2 className="text-5xl font-extrabold text-center mb-5 text-purple-800 drop-shadow">
            🎮 Games for <span className="text-pink-700">{selectedCategory}</span>
          </h2>
          <div className="flex flex-col gap-3 items-cente w-84">
            {gameTypes.map((game, index) => (
              <button
                key={index}
                onClick={() => handleGameSelect(game)}
                className="w-full bg-gradient-to-r from-indigo-400 via-purple-500 to-pink-400 text-white py-2 rounded-xl shadow-md hover:scale-105 transition-transform duration-200 text-md font-semibold"
              >
                {game}
              </button>
            ))}
          </div>
          <div className="text-center mt-5">
            <button
              onClick={handleClosePopup}
              className="text-xl text-red-700 hover:underline font-medium "
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