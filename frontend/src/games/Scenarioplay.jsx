import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const Scenarioplay = () => {
  const location = useLocation();
  const categoryData = location?.state;


  if (!categoryData || !categoryData.category || !categoryData.questions) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-blue-200 to-blue-400">
        <div className="bg-white p-8 rounded-xl shadow-xl text-xl text-blue-800">
          No scenario data found.<br />
          Please select a category from the home page.
        </div>
      </div>
    );
  }

  const questions = categoryData.questions;

  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [showNext, setShowNext] = useState(false);
  const [game, setGame] = useState(true);
  const [shuffledQuestions, setShuffledQuestions] = useState([]);


  const shuffleArray = (array) => {
    return [...array].sort(() => 0.5 - Math.random());
  };


  useEffect(() => {
    const shuffledQs = [...questions].sort(() => 0.5 - Math.random()).map(q => {
      const correctValue = q.options[q.answer];
      const shuffledOptions = shuffleArray(q.options);
      const newAnswerIndex = shuffledOptions.findIndex(opt => opt === correctValue);
      return {
        ...q,
        options: shuffledOptions,
        answer: newAnswerIndex
      };
    });
    setShuffledQuestions(shuffledQs);
    setCurrentQuestionIndex(0);
    setScore(0);
    setSelectedAnswer(null);
    setShowNext(false);
    setGame(true);
  }, [categoryData]);

  if (shuffledQuestions.length === 0) {
    return (
      <div className="text-center text-lg mt-20 text-blue-800">
        Loading scenario questions...
      </div>
    );
  }

  const currentQuestion = shuffledQuestions[currentQuestionIndex];

  const clickOption = (option) => {
    if (selectedAnswer !== null) return;
    setSelectedAnswer(option);
    setShowNext(true);

    if (option === currentQuestion.options[currentQuestion.answer]) {
      setScore(prev => prev + 1);
    }
  };

  const nextQuestion = () => {
    if (currentQuestionIndex < shuffledQuestions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
      setSelectedAnswer(null);
      setShowNext(false);
    } else {
      setGame(false);
    }
  };

  const newQuiz = () => {
    const shuffledQs = [...questions].sort(() => 0.5 - Math.random()).map(q => {
      const correctValue = q.options[q.answer];
      const shuffledOptions = shuffleArray(q.options);
      const newAnswerIndex = shuffledOptions.findIndex(opt => opt === correctValue);
      return {
        ...q,
        options: shuffledOptions,
        answer: newAnswerIndex
      };
    });
    setShuffledQuestions(shuffledQs);
    setCurrentQuestionIndex(0);
    setScore(0);
    setSelectedAnswer(null);
    setShowNext(false);
    setGame(true);
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-blue-200 to-blue-400">
      <div className="h-auto w-[90%] sm:w-96 bg-white shadow-2xl rounded-2xl p-6 relative flex flex-col items-center text-center space-y-6 border-2 border-blue-600">

 
        <div className="w-full text-center mb-2">
          <span className="inline-block bg-blue-600 text-white px-4 py-1 text-sm rounded-full shadow font-bold tracking-wide">
            {categoryData.category}
          </span>
        </div>


        {!game ? (
          <>
            <h2 className="text-2xl font-bold text-blue-800">Scenario Completed!</h2>
            <p className="text-lg text-blue-700 mt-2">Your Score: {score} / {shuffledQuestions.length}</p>
            <button
              onClick={newQuiz}
              className="mt-6 bg-blue-500 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-md shadow transition-all duration-200"
            >
              Replay
            </button>
          </>
        ) : (
          <>
        

      
            <h1 className="text-lg sm:text-xl font-bold text-black">
              {currentQuestion.question}
            </h1>

      
            <div className="flex flex-col space-y-3 w-full">
              {currentQuestion.options.map((option, index) => {
                let bgColor = "bg-blue-50 hover:bg-blue-100";

                if (selectedAnswer) {
                  if (index === currentQuestion.answer) {
                    bgColor = "bg-green-300 text-black font-semibold";
                  } else if (option === selectedAnswer && index !== currentQuestion.answer) {
                    bgColor = "bg-red-300 text-black font-semibold";
                  }
                }

                return (
                  <button
                    key={index}
                    onClick={() => clickOption(option)}
                    disabled={selectedAnswer !== null}
                    className={`${bgColor} text-blue-900 py-2 px-4 rounded shadow text-sm sm:text-base transition-all`}
                  >
                    {option}
                  </button>
                );
              })}
            </div>

            {selectedAnswer && (
              <div className="mt-2 text-blue-900 text-sm italic bg-blue-100 rounded p-2">
                {currentQuestion.learning}
              </div>
            )}

           
            {showNext && (
              <button
                onClick={nextQuestion}
                className="bg-blue-500 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-md shadow transition-all duration-200"
              >
                Next
              </button>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Scenarioplay;