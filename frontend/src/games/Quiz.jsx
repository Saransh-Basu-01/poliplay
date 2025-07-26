import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import ApiService from '../services/Api';
import LoadingSpinner from './LoadingSpinner';

const QuizApp = () => {
  const location = useLocation();
  // get category from navigation state!
  const [selectedCategory, setSelectedCategory] = useState(location.state?.category || null);
  const [categories, setCategories] = useState([]);
  const [categoryData, setCategoryData] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [userAnswers, setUserAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [quizResults, setQuizResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [userName, setUserName] = useState('');

  // Only load all categories if you need them
  useEffect(() => {
    if (!selectedCategory) {
      setLoading(true);
      ApiService.fetchCategories()
        .then((categoriesData) => {
          setCategories(categoriesData);
        })
        .catch((err) => {
          setError('Failed to load categories. Make sure backend is running on port 8000.');
        })
        .finally(() => setLoading(false));
    }
  }, [selectedCategory]);

  // If selectedCategory is set, fetch its questions!
  useEffect(() => {
    if (selectedCategory) {
      setLoading(true);
      setError(null);
      ApiService.fetchCategoryData(selectedCategory)
        .then((data) => {
          setCategoryData(data);
          setCurrentQuestion(0);
          setUserAnswers({});
          setShowResults(false);
        })
        .catch((err) => {
          setError('Failed to load category data. Please try again.');
        })
        .finally(() => setLoading(false));
    }
  }, [selectedCategory]);

  const loadCategories = async () => {
    try {
      setLoading(true);
      setError(null);
      const categoriesData = await ApiService.fetchCategories();
      setCategories(categoriesData);
    } catch (err) {
      setError('Failed to load categories. Make sure backend is running on port 8000.');
      console.error('Error loading categories:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadCategoryData = async (categoryName) => {
    try {
      setLoading(true);
      setError(null);
      const data = await ApiService.fetchCategoryData(categoryName);
      setCategoryData(data);
      setSelectedCategory(categoryName);
      setCurrentQuestion(0);
      setUserAnswers({});
      setShowResults(false);
    } catch (err) {
      setError('Failed to load category data. Please try again.');
      console.error('Error loading category data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (questionId, selectedAnswer) => {
    setUserAnswers(prev => ({
      ...prev,
      [questionId]: selectedAnswer
    }));
  };

  const submitQuiz = async () => {
    if (Object.keys(userAnswers).length === 0) {
      setError('Please answer at least one question');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const category = categories.find(cat => cat.name === selectedCategory);
      const answers = Object.entries(userAnswers).map(([questionId, selectedAnswer]) => ({
        question_id: parseInt(questionId),
        selected_answer: selectedAnswer
      }));

      const quizData = {
        user_name: userName || 'Anonymous',
        category: category.id,
        answers: answers
      };

      const results = await ApiService.submitQuiz(quizData);
      setQuizResults(results);
      setShowResults(true);
    } catch (err) {
      setError('Failed to submit quiz. Please try again.');
      console.error('Error submitting quiz:', err);
    } finally {
      setLoading(false);
    }
  };

  const resetQuiz = () => {
    setSelectedCategory(null);
    setCategoryData(null);
    setCurrentQuestion(0);
    setUserAnswers({});
    setShowResults(false);
    setQuizResults(null);
    setError(null);
  };

  // Helper function to get category icons
  const getCategoryIcon = (categoryName) => {
    const iconMap = {
      'Manga & Anime': '🎌',
      'Science': '🔬',
      'History': '📚',
      'Geography': '🌍',
      'Technology': '💻',
      'Sports': '⚽',
      'Math': '🔢',
      'Literature': '📖',
      'Music': '🎵',
      'Art': '🎨'
    };
    return iconMap[categoryName] || '📝';
  };

  // Loading state
  if (loading && !categories.length) {
    return <LoadingSpinner message="Loading quiz app..." />;
  }

  // Error state
  if (error && !categories.length && !selectedCategory) {
    return (
      <div className="min-h-screen flex flex-col justify-center items-center bg-gray-50 p-6">
        <div className="bg-white rounded-xl shadow-lg p-8 max-w-md w-full text-center">
          <div className="text-6xl mb-4">😔</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Connection Error</h2>
          <div className="text-red-600 text-lg mb-6 p-4 bg-red-50 rounded-lg">
            {error}
          </div>
          <div className="space-y-3">
            <button 
              onClick={loadCategories}
              className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Try Again
            </button>
            <div className="text-xs text-gray-500">
              <p>Make sure Django backend is running on port 8000</p>
              <p>Current API URL: {import.meta.env.VITE_API_URL}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Results Screen
  if (showResults && quizResults) {
    const percentage = quizResults.percentage;
    const getResultMessage = () => {
      if (percentage >= 90) return { message: "Outstanding! 🏆", color: "text-purple-600", bg: "bg-purple-50" };
      if (percentage >= 80) return { message: "Excellent! 🎉", color: "text-green-600", bg: "bg-green-50" };
      if (percentage >= 70) return { message: "Great Job! 👏", color: "text-blue-600", bg: "bg-blue-50" };
      if (percentage >= 60) return { message: "Good Work! 👍", color: "text-indigo-600", bg: "bg-indigo-50" };
      if (percentage >= 40) return { message: "Keep Learning! 📚", color: "text-yellow-600", bg: "bg-yellow-50" };
      return { message: "Practice More! 💪", color: "text-red-600", bg: "bg-red-50" };
    };

    const result = getResultMessage();

    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-6">
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full text-center">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">🎯 Quiz Results</h1>
          <h2 className="text-2xl text-gray-600 mb-8">{selectedCategory}</h2>
          
          <div className={`${result.bg} rounded-xl p-6 mb-8`}>
            <div className="text-6xl font-bold mb-4">
              <span className="text-gray-800">{quizResults.score}</span>
              <span className="text-2xl text-gray-500">/{quizResults.total_questions}</span>
            </div>
            <div className={`text-4xl font-bold mb-2 ${result.color}`}>
              {quizResults.percentage}%
            </div>
            <div className={`text-2xl font-bold ${result.color}`}>
              {result.message}
            </div>
          </div>

          {/* Progress Bar */}
          <div className="mb-8">
            <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
              <div 
                className={`h-4 rounded-full transition-all duration-1000 ${
                  percentage >= 80 ? 'bg-gradient-to-r from-green-400 to-green-600' :
                  percentage >= 60 ? 'bg-gradient-to-r from-blue-400 to-blue-600' :
                  percentage >= 40 ? 'bg-gradient-to-r from-yellow-400 to-yellow-600' :
                  'bg-gradient-to-r from-red-400 to-red-600'
                }`}
                style={{ width: `${percentage}%` }}
              />
            </div>
            <div className="text-sm text-gray-600">
              You answered {quizResults.score} out of {quizResults.total_questions} questions correctly
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => loadCategoryData(selectedCategory)}
              className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold flex items-center justify-center"
            >
              <span className="mr-2">🔄</span>
              Retake Quiz
            </button>
            <button
              onClick={resetQuiz}
              className="px-8 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors font-semibold flex items-center justify-center"
            >
              <span className="mr-2">📚</span>
              Choose Another Category
            </button>
          </div>

          {/* Share Button */}
          <div className="mt-6">
            <button
              onClick={() => {
                const shareText = `I just scored ${percentage}% (${quizResults.score}/${quizResults.total_questions}) on the ${selectedCategory} quiz! 🧠✨`;
                if (navigator.share) {
                  navigator.share({
                    title: 'Quiz Results',
                    text: shareText,
                    url: window.location.href
                  });
                } else {
                  navigator.clipboard.writeText(shareText);
                  alert('Results copied to clipboard!');
                }
              }}
              className="px-6 py-2 bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-lg hover:from-pink-600 hover:to-purple-700 transition-all transform hover:scale-105"
            >
              📱 Share Results
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Category Selection Screen
  if (!selectedCategory) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 mb-4">
              🧠 Quiz Master
            </h1>
            <p className="text-xl text-gray-600 mb-2">
              Test your knowledge across multiple categories
            </p>
            <p className="text-sm text-gray-500">
              Developed by {import.meta.env.VITE_DEVELOPER || 'CrypticLuminary'} • {new Date().toLocaleDateString()}
            </p>
          </div>
          
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-8 text-center max-w-md mx-auto">
              <strong>Error:</strong> {error}
            </div>
          )}
          
          {/* User Name Input */}
          <div className="max-w-md mx-auto mb-8">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                👤 Your Name (Optional):
              </label>
              <input
                type="text"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                placeholder="Enter your name for the leaderboard"
              />
            </div>
          </div>

          <h2 className="text-3xl font-bold text-center mb-8 text-gray-800">
            Select a Category:
          </h2>
          
          {categories.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">📚</div>
              <h3 className="text-2xl font-bold text-gray-800 mb-4">No Categories Available</h3>
              <p className="text-gray-600 mb-6">Please check if the backend is running and has data loaded.</p>
              <button
                onClick={loadCategories}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Retry Loading
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {categories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => loadCategoryData(category.name)}
                  className="group bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all transform hover:scale-105 hover:bg-gradient-to-br hover:from-blue-50 hover:to-indigo-50 border border-gray-200"
                >
                  <div className="text-4xl mb-4">
                    {getCategoryIcon(category.name)}
                  </div>
                  <div className="text-xl font-bold text-gray-800 mb-2 group-hover:text-blue-600">
                    {category.name}
                  </div>
                  {category.description && (
                    <div className="text-sm text-gray-600 mb-3 line-clamp-2">
                      {category.description}
                    </div>
                  )}
                  <div className="flex justify-between items-center text-sm">
                    <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
                      {category.question_count} questions
                    </span>
                    <span className="text-blue-600 font-medium group-hover:text-blue-700">
                      Start Quiz →
                    </span>
                  </div>
                </button>
              ))}
            </div>
          )}

          <div className="text-center mt-8 text-gray-500">
            <p>Total Categories: {categories.length} | Total Questions: {categories.reduce((sum, cat) => sum + cat.question_count, 0)}</p>
            <p className="mt-2 text-xs">Last updated: {new Date().toLocaleDateString()}</p>
          </div>
        </div>
      </div>
    );
  }

  // Quiz Screen
  if (!categoryData || !categoryData.questions || categoryData.questions.length === 0) {
    return (
      <div className="min-h-screen flex justify-center items-center bg-gray-50">
        <div className="text-center">
          <div className="text-6xl mb-4">📝</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">No Questions Available</h2>
          <p className="text-gray-600 mb-6">This category doesn't have any questions yet.</p>
          <button
            onClick={resetQuiz}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Back to Categories
          </button>
        </div>
      </div>
    );
  }

  const currentQuestionData = categoryData.questions[currentQuestion];
  const isLastQuestion = currentQuestion === categoryData.questions.length - 1;
  const answeredQuestions = Object.keys(userAnswers).length;
  const completionPercentage = Math.round((answeredQuestions / categoryData.questions.length) * 100);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 p-6">
      <div className="max-w-4xl mx-auto">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Header with Back Button */}
        <div className="flex justify-between items-center mb-6">
          <button
            onClick={resetQuiz}
            className="flex items-center text-blue-600 hover:text-blue-800 transition-colors"
          >
            <span className="mr-2">←</span>
            Back to Categories
          </button>
          <div className="text-right">
            <div className="text-sm text-gray-500">Quiz Progress</div>
            <div className="text-lg font-bold text-blue-600">
              {currentQuestion + 1} / {categoryData.questions.length}
            </div>
          </div>
        </div>

        {/* Main Quiz Card */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-6">
          <h1 className="text-3xl font-bold text-center mb-6 text-gray-800">
            {selectedCategory}
          </h1>
          
          {/* Progress Section */}
          <div className="text-center mb-8">
            <div className="flex justify-center items-center space-x-6 mb-4">
              <span className="text-sm font-medium">Progress: {answeredQuestions}/{categoryData.questions.length}</span>
              <div className="w-48 bg-gray-200 rounded-full h-3">
                <div 
                  className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-300" 
                  style={{ width: `${completionPercentage}%` }}
                />
              </div>
              <span className="text-sm font-medium">{completionPercentage}% Complete</span>
            </div>
          </div>

          {/* Question Section */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-600">
                Question {currentQuestion + 1} of {categoryData.questions.length}
              </h3>
              {currentQuestionData.difficulty_level && (
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                  currentQuestionData.difficulty_level === 'easy' ? 'text-green-600 bg-green-100' :
                  currentQuestionData.difficulty_level === 'medium' ? 'text-yellow-600 bg-yellow-100' :
                  'text-red-600 bg-red-100'
                }`}>
                  {currentQuestionData.difficulty_level.toUpperCase()}
                </span>
              )}
            </div>
            <p className="text-2xl font-medium text-gray-800 mb-8 leading-relaxed">
              {currentQuestionData.question_text}
            </p>
          </div>

          {/* Options Section */}
          <div className="space-y-3 mb-8">
            {currentQuestionData.options && currentQuestionData.options.map((option, index) => (
              <button
                key={option.id}
                onClick={() => handleAnswer(currentQuestionData.id, option.option_text)}
                className={`w-full p-4 text-left rounded-xl border-2 transition-all transform hover:scale-[1.02] ${
                  userAnswers[currentQuestionData.id] === option.option_text
                    ? 'border-blue-500 bg-blue-50 shadow-lg'
                    : 'border-gray-200 hover:border-blue-300 hover:shadow-md bg-white'
                }`}
              >
                <div className="flex items-center gap-4">
                  <div className={`w-8 h-8 rounded-full border-2 flex items-center justify-center font-bold transition-colors ${
                    userAnswers[currentQuestionData.id] === option.option_text
                      ? 'border-blue-500 bg-blue-500 text-white'
                      : 'border-gray-300 text-gray-400'
                  }`}>
                    {String.fromCharCode(65 + index)}
                  </div>
                  <span className="text-lg flex-1">{option.option_text}</span>
                  {userAnswers[currentQuestionData.id] === option.option_text && (
                    <div className="text-blue-500 text-xl">✓</div>
                  )}
                </div>
              </button>
            ))}
          </div>

          {/* Navigation Section */}
          <div className="flex justify-between items-center">
            <button
              onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
              disabled={currentQuestion === 0}
              className="px-6 py-3 bg-gray-500 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-600 transition-colors flex items-center"
            >
              ← Previous
            </button>

            <div className="text-center">
              <p className="text-sm text-gray-600">
                {userAnswers[currentQuestionData.id] ? 
                  <span className="text-green-600 font-medium">Answered ✓</span> : 
                  <span className="text-gray-500">Not answered yet</span>
                }
              </p>
            </div>

            {isLastQuestion ? (
              <button
                onClick={submitQuiz}
                disabled={loading || answeredQuestions === 0}
                className="px-8 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-semibold flex items-center"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                    Submitting...
                  </>
                ) : (
                  `Submit Quiz (${answeredQuestions} answers)`
                )}
              </button>
            ) : (
              <button
                onClick={() => setCurrentQuestion(Math.min(categoryData.questions.length - 1, currentQuestion + 1))}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center"
              >
                Next →
              </button>
            )}
          </div>
        </div>

        {/* Question Navigation Grid */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h4 className="text-lg font-semibold mb-4 text-center">Question Navigation</h4>
          <div className="flex flex-wrap justify-center gap-2">
            {categoryData.questions.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentQuestion(index)}
                className={`w-10 h-10 rounded-lg transition-all font-medium ${
                  index === currentQuestion
                    ? 'bg-blue-600 text-white scale-110 shadow-lg'
                    : userAnswers[categoryData.questions[index].id]
                    ? 'bg-green-500 text-white hover:bg-green-600'
                    : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
                }`}
                title={`Question ${index + 1}${userAnswers[categoryData.questions[index].id] ? ' (answered)' : ''}`}
              >
                {index + 1}
              </button>
            ))}
          </div>
          <div className="flex justify-center mt-4 space-x-6 text-sm">
            <div className="flex items-center">
              <div className="w-4 h-4 bg-blue-600 rounded mr-2"></div>
              Current
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 bg-green-500 rounded mr-2"></div>
              Answered
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 bg-gray-200 rounded mr-2"></div>
              Unanswered
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuizApp;