import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
const Sorting = () => {
  const location = useLocation();
  const { title, bins = [], cards = [] } = location.state || {};

  const [cardData, setCardData] = useState(cards);

  const [binData, setBinData] = useState(
    bins.reduce((acc, bin) => {
      acc[bin] = [];
      return acc;
    }, {})
  );

  const [showResults, setShowResults] = useState(false);

  const totalCards = cards.length;
  const cardsInBins = Object.values(binData).reduce(
    (acc, arr) => acc + arr.length,
    0
  );

  // Allow dropping any card in any bin
  const handleDragEnd = (result) => {
    const { destination, draggableId } = result;
    if (!destination) return;
    if (destination.droppableId === "card-pool") return;

    const draggedCard = cardData.find((card) => card.id === draggableId);
    if (!draggedCard) return;

    setBinData((prev) => {
      const newBins = { ...prev };
      newBins[destination.droppableId] = [
        ...newBins[destination.droppableId],
        draggedCard,
      ];
      return newBins;
    });

    setCardData((prev) => prev.filter((card) => card.id !== draggableId));
  };

  const checkAnswers = () => setShowResults(true);

  const resetGame = () => {
    setCardData(cards);
    setBinData(
      bins.reduce((acc, bin) => {
        acc[bin] = [];
        return acc;
      }, {})
    );
    setShowResults(false);
  };

  return (
    <div className="w-full min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex flex-col items-center justify-center p-4 sm:p-6 lg:p-8">
      <div className="w-full max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 mb-4 drop-shadow-lg">
            🧠 Sort the Cards
          </h1>
          <h2 className="text-2xl sm:text-3xl font-semibold text-gray-700 mb-6">
            {title ? <>Category: <span className="text-purple-600">{title}</span></> : null}
          </h2>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button
              onClick={checkAnswers}
              disabled={cardsInBins !== totalCards || showResults}
              className={`bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800
                text-white px-8 py-3 text-lg font-semibold rounded-full shadow-lg
                transition-all duration-200 hover:scale-105 hover:shadow-xl min-w-[200px]
                ${cardsInBins !== totalCards || showResults ? "opacity-50 cursor-not-allowed" : ""}
              `}
            >
              ✅ Submit Answers
            </button>
            <button
              onClick={resetGame}
              className="bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white px-8 py-3 text-lg font-semibold rounded-full shadow-lg transition-all duration-200 hover:scale-105 hover:shadow-xl min-w-[200px]"
            >
              🔄 Reset Game
            </button>
          </div>
        </div>
        <DragDropContext onDragEnd={handleDragEnd}>
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 w-full">
            {/* Card Pool */}
            <Droppable droppableId="card-pool">
              {(provided) => (
                <div
                  ref={provided.innerRef}
                  {...provided.droppableProps}
                  className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 min-h-[300px] shadow-xl border-2 border-blue-200"
                  style={{ overflow: "visible" }}
                >
                  <h3 className="font-bold text-xl text-center text-blue-700 mb-4 flex items-center justify-center gap-2">
                    🗃 Available Cards
                  </h3>
                  <div className="space-y-3">
                    {cardData.map((card, index) => (
                      <Draggable key={card.id} draggableId={card.id} index={index}>
                        {(provided, snapshot) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className={`bg-white rounded-xl p-4 shadow-md border-2 border-blue-300 text-center font-medium text-gray-800 select-none
                              ${
                                snapshot.isDragging
                                  ? 'border-purple-400 bg-purple-50 scale-105 rotate-1'
                                  : 'hover:border-purple-300 hover:scale-102'
                              }`}
                            style={{
                              ...provided.draggableProps.style,
                              cursor: snapshot.isDragging ? 'grabbing !important' : 'grab !important',
                              zIndex: snapshot.isDragging ? 9999 : 'auto',
                              boxShadow: snapshot.isDragging
                                ? '0 8px 32px rgba(80,0,180,0.18)'
                                : '0 2px 8px rgba(80,120,255,0.10)',
                              transition: snapshot.isDragging
                                ? 'box-shadow 0.15s, transform 0.15s cubic-bezier(.21,1.07,.53,.99)'
                                : 'box-shadow 0.15s, transform 0.15s cubic-bezier(.21,1.07,.53,.99), border-color 0.15s',
                            }}
                          >
                            {card.text}
                          </div>
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}
                  </div>
                </div>
              )}
            </Droppable>
            {/* Bins */}
            {bins.map((bin) => (
              <Droppable droppableId={bin} key={bin}>
                {(provided, snapshot) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.droppableProps}
                    className={`bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 min-h-[300px] shadow-xl border-2 transition-all duration-200 ${
                      snapshot.isDraggingOver 
                        ? 'border-green-400 bg-green-50 scale-105' 
                        : 'border-blue-300'
                    }`}
                  >
                    <h3 className="font-bold text-xl text-center text-blue-800 mb-4 flex items-center justify-center gap-2">
                      📦 {bin}
                    </h3>
                    <div className="space-y-3">
                      {binData[bin].map((card, index) => (
                        <div
                          key={card.id}
                          className={`p-4 rounded-xl border-2 font-medium text-center transition-all duration-300 shadow-md ${
                            showResults
                              ? card.correct === bin
                                ? "bg-gradient-to-r from-green-100 to-green-200 border-green-400 shadow-green-200 scale-105"
                                : "bg-gradient-to-r from-red-100 to-red-200 border-red-400 shadow-red-200"
                              : "bg-white border-blue-200 hover:shadow-lg hover:scale-102"
                          }`}
                        >
                          {card.text}
                          {showResults && (
                            <div className="mt-2 text-sm font-bold">
                              {card.correct === bin ? (
                                <span className="text-green-700 flex items-center justify-center gap-1">
                                  ✅ Correct!
                                </span>
                              ) : (
                                <span className="text-red-700 flex items-center justify-center gap-1">
                                  ❌ Should be in "{card.correct}"
                                </span>
                              )}
                            </div>
                          )}
                        </div>
                      ))}
                      {provided.placeholder}
                      {binData[bin].length === 0 && (
                        <div className="text-center text-gray-400 italic py-8 border-2 border-dashed border-gray-300 rounded-xl">
                          Drop cards here
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </Droppable>
            ))}
          </div>
        </DragDropContext>
      </div>
    </div>
  );
};

export default Sorting;