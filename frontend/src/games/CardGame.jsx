import React, { useState } from 'react';
import cardData from '../components/data/cards';

const CardGame = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [gameOver, setGameOver] = useState(false);
  const [isCorrect, setIsCorrect] = useState(null);

  const currentCard = cardData[currentIndex];

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (showAnswer) return;
    const answerNormalized = inputValue.trim().toLowerCase();
    const correctNormalized = currentCard.answer.trim().toLowerCase();
    const result = answerNormalized === correctNormalized;
    setIsCorrect(result);
    setShowAnswer(true);
    if (result) {
      setScore((prev) => prev + 1);
    }
  };

  const handleNext = () => {
    if (currentIndex + 1 < cardData.length) {
      setCurrentIndex(currentIndex + 1);
      setShowAnswer(false);
      setInputValue('');
      setIsCorrect(null);
    } else {
      setGameOver(true);
    }
  };

  // Styles
  const gradientBg = "bg-gradient-to-tr from-cyan-200 via-purple-100 to-pink-200";
  const cardShadow = "shadow-2xl";
  const accentText = "text-purple-700";
  const buttonBase = "mt-6 px-8 py-3 bg-gradient-to-tr from-purple-600 to-pink-500 text-white rounded-xl shadow-lg hover:scale-105 hover:from-purple-700 hover:to-pink-600 transition-transform duration-200 font-bold";
  const inputBase = "w-full px-4 py-2 border-2 border-purple-300 rounded-xl text-lg focus:outline-none focus:border-purple-500 transition mb-4";
  const feedbackText = isCorrect === null ? "" : isCorrect ? "Correct! 🎉" : `Wrong! The correct answer was "${currentCard.answer}"`;

  return (
    <div className={`${gradientBg} min-h-screen w-full flex items-center justify-center`}>
      {gameOver ? (
        <div className={`flex flex-col items-center justify-center min-h-[60vh] rounded-2xl ${cardShadow} p-10 bg-gradient-to-br from-blue-100 via-blue-200 to-blue-300 sm:p-8`}>
          <h2 className="text-4xl font-extrabold text-green-700 mb-2">🎉 Game Over!</h2>
          <p className="text-2xl mt-4 mb-6 font-semibold text-gray-700">
            Your Score: <span className="text-pink-600">{score}</span> / {cardData.length}
          </p>
          <button
            className={buttonBase}
            onClick={() => {
              setCurrentIndex(0);
              setScore(0);
              setGameOver(false);
              setShowAnswer(false);
              setInputValue('');
              setIsCorrect(null);
            }}
          >
            Play Again
          </button>
        </div>
      ) : (
        <div className={`max-w-xl w-full mx-auto p-8 ${cardShadow} rounded-2xl text-center bg-white/70`}>
          <span className="block text-xl font-bold mb-6 text-purple-800 drop-shadow-lg">
            Write the name:
          </span>
          <div className="relative mb-4 flex flex-col items-center">
            <img
              src={currentCard.imgSrc}
              alt="figure"
              className="w-[340px] h-[220px] object-cover rounded-xl border-4 border-purple-400 shadow-lg mb-5"
            />
          </div>
          <p className={`text-lg font-medium mb-8 ${accentText} drop-shadow-lg`}>{currentCard.description}</p>
          
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              className={inputBase}
              value={inputValue}
              onChange={handleInputChange}
              placeholder="Type the name here..."
              disabled={showAnswer}
              autoFocus
            />
            {!showAnswer && (
              <button type="submit" className={buttonBase}>
                Submit
              </button>
            )}
          </form>
          {showAnswer && (
            <>
              <div className={`mt-4 text-xl font-bold ${isCorrect ? "text-green-700" : "text-red-700"}`}>
                {feedbackText}
              </div>
              <button className={buttonBase} onClick={handleNext}>
                {currentIndex === cardData.length - 1 ? "Finish" : "Next"}
              </button>
            </>
          )}
          <div className="mt-5 flex items-center justify-center gap-2 text-lg">
            <span className="text-gray-600 font-semibold">Score:</span>
            <span className="font-bold text-pink-600 text-xl drop-shadow-md">{score}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default CardGame;