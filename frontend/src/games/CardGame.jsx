import React ,{ useState, useEffect } from 'react'
import cardData from '../components/data/cards'
const shuffleArray = (array) => [...array].sort(() => Math.random() - 0.5);

const CardGame = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [selectedOption, setSelectedOption] = useState('');
  const [gameOver, setGameOver] = useState(false);
  const [options, setOptions] = useState([]);

  const currentCard = cardData[currentIndex];

  useEffect(() => {
    const generateOptions = () => {
      const others = cardData
        .filter((card) => card.answer !== currentCard.answer)
        .map((card) => card.answer);
      const shuffled = shuffleArray(others).slice(0, 3);
      return shuffleArray([currentCard.answer, ...shuffled]);
    };

    setOptions(generateOptions());
  }, [currentIndex, currentCard.answer]);

  const handleAnswerClick = (option) => {
    if (showAnswer) return;
    setSelectedOption(option);
    setShowAnswer(true);
    if (option === currentCard.answer) {
      setScore((prev) => prev + 1);
    }
  };

  const handleNext = () => {
    const nextIndex = currentIndex + 1;
    if (nextIndex < cardData.length) {
      setCurrentIndex(nextIndex);
      setShowAnswer(false);
      setSelectedOption('');
    } else {
      setGameOver(true);
    }
  };

  // Enhanced UI Styles
  const gradientBg = "bg-gradient-to-tr from-cyan-200 via-purple-100 to-pink-200";
  const cardShadow = "shadow-2xl";
  const accentText = "text-purple-700";
  const optionBase = "p-3 rounded-xl border text-left transition-all text-md font-semibold";
  const optionCorrect = "bg-green-100 border-green-400 text-green-800 font-bold";
  const optionWrong = "bg-red-100 border-red-400 text-red-800";
  const optionNeutral = "bg-gray-100 border-gray-300";
  const optionActive = "bg-blue-200 hover:bg-blue-300 border-blue-400";
  const buttonBase = "mt-6 px-8 py-3 bg-gradient-to-tr from-purple-600 to-pink-500 text-white rounded-xl shadow-lg hover:scale-105 hover:from-purple-700 hover:to-pink-600 transition-transform duration-200 font-bold";

  // Wrap everything in the main gradient background
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
              setSelectedOption('');
            }}
          >
            Play Again
          </button>
        </div>
      ) : (
        <div className={`max-w-xl w-full mx-auto p-8 ${cardShadow} rounded-2xl text-center bg-white/70`}>
          <div className="relative">
            <img
              src={currentCard.imgSrc}
              alt="figure"
              className="w-52 h-52 mx-auto rounded-full object-cover mb-5 border-4 border-purple-400 shadow-lg transition-transform duration-300 hover:scale-105"
            />
            <span className="absolute top-4 left-4 bg-white/80 text-purple-600 px-4 py-1 rounded-xl font-bold text-lg shadow-md">
            Question {currentIndex + 1} / {cardData.length}
            </span>
          </div>
          <p className={`text-xl font-medium mb-8 ${accentText} drop-shadow-lg`}>{currentCard.description}</p>
          <div className="grid grid-cols-1 gap-4 mb-4">
            {options.map((option, idx) => {
              let optionStyle = optionBase;
              if (showAnswer) {
                if (option === currentCard.answer) optionStyle += ` ${optionCorrect}`;
                else if (option === selectedOption) optionStyle += ` ${optionWrong}`;
                else optionStyle += ` ${optionNeutral}`;
              } else {
                optionStyle += ` ${optionActive}`;
              }
              return (
                <button
                  key={idx}
                  className={optionStyle}
                  onClick={() => handleAnswerClick(option)}
                  disabled={showAnswer}
                  style={{ cursor: showAnswer ? 'default' : 'pointer' }}
                >
                  <span className="ml-2">{option}</span>
                </button>
              );
            })}
          </div>
          {showAnswer && (
            <button
              className={buttonBase}
              onClick={handleNext}
            >
              {currentIndex === cardData.length - 1 ? "Finish" : "Next"}
            </button>
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

