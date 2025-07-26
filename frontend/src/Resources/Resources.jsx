import React from 'react';
import { Link } from 'react-router-dom';

const Resources = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-200 via-blue-300 to-blue-500 p-8 text-white">
      <h2 className="text-4xl font-extrabold mb-8 text-center text-black">📚 Resources</h2>
      <div className="grid gap-6 max-w-md mx-auto">
        <Link
          to="/resources/timeline"
          className="bg-white text-black font-semibold py-4 px-6 rounded-2xl shadow-lg hover:scale-105 hover:bg-blue-100 transition duration-300 flex items-center gap-3"
        >
          🕒 Timeline
        </Link>
        <Link
          to="/resources/documentation"
          className="bg-white text-black font-semibold py-4 px-6 rounded-2xl shadow-lg hover:scale-105 hover:bg-blue-100 transition duration-300 flex items-center gap-3"
        >
          📄 Documentation
        </Link>
        <Link
          to="/resources/chatbot"
          className="bg-white text-black font-semibold py-4 px-6 rounded-2xl shadow-lg hover:scale-105 hover:bg-blue-100 transition duration-300 flex items-center gap-3"
        >
          🤖 Chatbot
        </Link>
      </div>
    </div>
  );
};

export default Resources;
