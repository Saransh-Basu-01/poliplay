import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import ApiService from '../services/Api';

const CardGame = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const categoryName = location.state?.category;

  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [showAnswer, setShowAnswer] = useState(false);
  const [score, setScore] = useState(0);
  const [gameOver, setGameOver] = useState(false);

  useEffect(() => {
    if (!categoryName) {
      setError('No category selected');
      setLoading(false);
      return;
    }
    setLoading(true);
    ApiService.fetchCategoryData(categoryName)
      .then((data) => {
        if (data.questions && data.questions.length > 0) {
          setQuestions(data.questions);
        } else {
          setError('No questions found for this category');
        }
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load questions');
        setLoading(false);
      });
  }, [categoryName]);

  const currentQuestion = questions[currentIndex];

  const handleOptionSelect = (optionText) => {
    setSelectedOption(optionText);
    setShowAnswer(true);
    if (optionText === currentQuestion.correct_answer) {
      setScore((prev) => prev + 1);
    }
  };

  const handleNext = () => {
    if (currentIndex + 1 < questions.length) {
      setCurrentIndex(currentIndex + 1);
      setSelectedOption(null);
      setShowAnswer(false);
    } else {
      setGameOver(true);
    }
  };

  const resetGame = () => {
    setCurrentIndex(0);
    setScore(0);
    setGameOver(false);
    setSelectedOption(null);
    setShowAnswer(false);
  };

  const goBack = () => navigate('/categories');

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading questions...</div>;
  }
  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen text-red-500">
        <div className="text-3xl mb-4">❌ Error</div>
        <div>{error}</div>
        <button onClick={goBack} className="mt-6 px-8 py-3 bg-purple-600 text-white rounded-xl shadow-lg">Back to Categories</button>
      </div>
    );
  }
  if (!questions.length) {
    return <div className="flex items-center justify-center min-h-screen">No questions found.</div>;
  }

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-gradient-to-tr from-cyan-200 via-purple-100 to-pink-200">
      {gameOver ? (
        <div className="flex flex-col items-center justify-center min-h-[60vh] rounded-2xl shadow-2xl p-10 bg-gradient-to-br from-blue-100 via-blue-200 to-blue-300">
          <h2 className="text-4xl font-extrabold text-green-700 mb-2">🎉 Game Over!</h2>
          <p className="text-xl font-semibold text-purple-700 mb-2">Category: {categoryName}</p>
          <p className="text-2xl mt-4 mb-6 font-semibold text-gray-700">
            Your Score: <span className="text-pink-600">{score}</span> / {questions.length}
          </p>
          <div className="flex gap-4">
            <button className="mt-6 px-8 py-3 bg-purple-600 text-white rounded-xl shadow-lg" onClick={resetGame}>
              Play Again
            </button>
            <button className="mt-6 px-8 py-3 bg-gray-600 text-white rounded-xl shadow-lg" onClick={goBack}>
              Back to Categories
            </button>
          </div>
        </div>
      ) : (
        <div className="max-w-xl w-full mx-auto p-8 shadow-2xl rounded-2xl text-center bg-white/70">
          <div className="flex justify-between items-center mb-4">
            <span className="text-sm font-bold text-purple-600">
              Category: {categoryName}
            </span>
            <span className="text-sm font-bold text-purple-600">
              Question {currentIndex + 1} of {questions.length}
            </span>
          </div>
          <span className="block text-xl font-bold mb-6 text-purple-800">Choose the correct answer:</span>
          <div className="mb-4 flex flex-col items-center">
            <div className="w-full p-6 bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl border-4 border-purple-400 shadow-lg mb-5">
              <p className="text-lg font-medium text-gray-800 leading-relaxed">
                {currentQuestion.question_text}
              </p>
            </div>
          </div>
          <div className="flex flex-col gap-3">
            {currentQuestion.options.map((opt) => (
              <button
                key={opt.id}
                className={`w-full py-3 rounded-lg border text-lg font-medium shadow transition 
                  ${showAnswer
                    ? opt.option_text === currentQuestion.correct_answer
                      ? 'bg-green-400 border-green-600 text-white'
                      : selectedOption === opt.option_text
                        ? 'bg-red-400 border-red-600 text-white'
                        : 'bg-gray-100 border-gray-300'
                    : 'bg-white border-purple-300 hover:bg-purple-50'}
                `}
                onClick={() => handleOptionSelect(opt.option_text)}
                disabled={showAnswer}
              >
                {opt.option_text}
              </button>
            ))}
          </div>
          {showAnswer && (
            <button className="mt-6 px-8 py-3 bg-pink-500 text-white rounded-xl shadow-lg" onClick={handleNext}>
              {currentIndex === questions.length - 1 ? 'Finish Game' : 'Next Question'}
            </button>
          )}
          <div className="mt-5 flex items-center justify-center gap-4 text-lg">
            <div className="flex items-center gap-2">
              <span className="text-gray-600 font-semibold">Score:</span>
              <span className="font-bold text-pink-600 text-xl drop-shadow-md">{score}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-gray-600 font-semibold">Progress:</span>
              <span className="font-bold text-blue-600 text-xl drop-shadow-md">
                {Math.round(((currentIndex + 1) / questions.length) * 100)}%
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CardGame;