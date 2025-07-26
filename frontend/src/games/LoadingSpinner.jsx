import React from 'react';

const LoadingSpinner = ({ message = "Loading..." }) => {
  return (
    <div className="flex flex-col justify-center items-center min-h-screen bg-gray-50">
      <div className="relative">
        <div className="animate-spin rounded-full h-20 w-20 border-4 border-blue-200"></div>
        <div className="animate-spin rounded-full h-20 w-20 border-4 border-blue-600 border-t-transparent absolute top-0"></div>
      </div>
      <div className="mt-4 text-lg text-gray-600 font-medium">{message}</div>
      <div className="mt-2 text-sm text-gray-500">Please wait...</div>
    </div>
  );
};

export default LoadingSpinner;