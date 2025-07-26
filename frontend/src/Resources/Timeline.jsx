import React, { useState } from 'react';

// 30 events with only Nepali dates (B.S.)
const timelineData = [
  { date: '2007 B.S.', title: 'End of Rana Regime', description: 'The 104-year autocratic Rana regime ended, introducing democracy in Nepal and opening doors for social reforms.' },
  { date: '2017 B.S.', title: 'King Mahendra’s Coup', description: 'King Mahendra dissolved the democratic government and imposed the Panchayat system.' },
  { date: '2028 B.S.', title: 'Formation of Supreme Court', description: 'Supreme Court of Nepal established as the highest judicial authority.' },
  { date: '2036 B.S.', title: 'Referendum', description: 'Referendum held to choose between Panchayat system and multiparty democracy; Panchayat system continued.' },
  { date: '2046 B.S.', title: 'People\'s Movement I', description: 'Mass movement led to constitutional monarchy and multiparty democracy, restoring civil rights.' },
  { date: '2047 B.S.', title: 'New Constitution', description: 'Constitution of the Kingdom of Nepal 2047 promulgated, establishing constitutional monarchy.' },
  { date: '2052 B.S.', title: 'Start of Maoist Insurgency', description: 'The Maoists launched an armed insurgency, demanding the abolition of monarchy.' },
  { date: '2056 B.S.', title: 'General Election', description: 'Nepal held its third general election under multiparty democracy.' },
  { date: '2058 B.S.', title: 'Royal Massacre', description: 'King Birendra and most of the royal family were killed, Gyanendra became king.' },
  { date: '2061 B.S.', title: 'King’s Direct Rule', description: 'King Gyanendra took direct control, citing inability of government to control Maoist insurgency.' },
  { date: '2062 B.S.', title: 'People\'s Movement II', description: 'Uprising forced King Gyanendra to relinquish direct rule and restored the House of Representatives.' },
  { date: '2063 B.S.', title: 'Interim Constitution', description: 'Nepal promulgated an interim constitution, ensuring fundamental rights.' },
  { date: '2064 B.S.', title: 'Interim Legislature-Parliament Formed', description: 'Interim Legislature-Parliament formed, ending previous parliament.' },
  { date: '2065 B.S.', title: 'Nepal Becomes a Republic', description: 'The monarchy was abolished and Nepal was declared a federal democratic republic.' },
  { date: '2065 B.S.', title: 'First Constituent Assembly', description: 'First Constituent Assembly election held to draft a new constitution.' },
  { date: '2068 B.S.', title: 'Prime Minister Jhala Nath Khanal', description: 'Jhala Nath Khanal became Prime Minister of Nepal.' },
  { date: '2069 B.S.', title: 'Dissolution of First Constituent Assembly', description: 'First Constituent Assembly dissolved after failure to draft constitution.' },
  { date: '2070 B.S.', title: 'Second Constituent Assembly', description: 'Election for Second Constituent Assembly held.' },
  { date: '2072 B.S.', title: 'Earthquake', description: 'A major earthquake struck Nepal, causing massive damage and loss of life.' },
  { date: '2072 B.S.', title: 'New Constitution Promulgated', description: 'Nepal adopted a new constitution, establishing a secular, federal democratic republic.' },
  { date: '2073 B.S.', title: 'Promulgation of New Laws', description: 'Several new laws promulgated to support federalism.' },
  { date: '2074 B.S.', title: 'First Federal Elections', description: 'Nepal held its first federal and provincial elections under the new constitution.' },
  { date: '2075 B.S.', title: 'First Provincial Governments', description: 'First provincial governments formed after federal elections.' },
  { date: '2076 B.S.', title: 'Nepal Hosts SAG Games', description: 'Nepal hosts South Asian Games, winning several medals.' },
  { date: '2077 B.S.', title: 'COVID-19 Pandemic', description: 'COVID-19 pandemic affects Nepal, leading to lockdowns and health crisis.' },
  { date: '2078 B.S.', title: 'Vaccination Drive', description: 'Nationwide vaccination drive against COVID-19 begins.' },
  { date: '2079 B.S.', title: 'Local Elections', description: 'Nationwide local elections conducted successfully.' },
  { date: '2080 B.S.', title: 'Digital Nepal Framework', description: 'Government launches Digital Nepal Framework for digital transformation.' },
  { date: '2081 B.S.', title: 'Climate Change Policy', description: 'Government adopts new climate change policy to address environmental concerns.' },
  { date: '2082 B.S.', title: 'Education Reform', description: 'Comprehensive education reform implemented in Nepal.' }
];

const ITEMS_PER_PAGE = 6;

const Timeline = () => {
  const [startIndex, setStartIndex] = useState(0);
  const [currentIndex, setCurrentIndex] = useState(null);

  const visibleEvents = timelineData.slice(startIndex, startIndex + ITEMS_PER_PAGE);

  const handlePrev = () => setStartIndex((prev) => Math.max(prev - ITEMS_PER_PAGE, 0));
  const handleNext = () => setStartIndex((prev) => Math.min(prev + ITEMS_PER_PAGE, timelineData.length - ITEMS_PER_PAGE));

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-200 via-blue-300 to-blue-400 flex flex-col items-center justify-center p-6">
      <h2 className="text-3xl font-bold text-black mb-12">Nepal Historical Timeline</h2>
      <div className="relative w-full flex flex-col items-center justify-center">
        {/* Timeline Line */}
        <div className="absolute top-1/2 left-12 right-12 h-1 bg-black opacity-70" style={{transform: 'translateY(-50%)'}}></div>
        {/* Timeline Items */}
        <div className="flex w-full max-w-6xl mx-auto justify-between z-10 pt-6 pb-6">
          {visibleEvents.map((event, i) => {
            const globalIndex = startIndex + i;
            return (
              <div key={event.date + globalIndex} className="flex flex-col items-center cursor-pointer" onClick={() => setCurrentIndex(globalIndex)}>
                {/* Circle */}
                <div className={`flex items-center justify-center w-14 h-14 rounded-full border-4 transition duration-200 ${
                  currentIndex === globalIndex ? 'border-blue-900 bg-white text-blue-900 shadow-xl scale-110' : 'border-blue-700 bg-blue-700 text-white'
                }`}>
                  <span className="font-bold text-xs text-center">{event.date}</span>
                </div>
                {/* Event Title */}
                <div className="mt-1 mb-12 text-black text-center font-semibold max-w-[150px]">{event.title}</div>
              </div>
            );
          })}
        </div>
        {/* Prev/Next Buttons */}
        <div className="flex gap-4 mt-2 mb-4">
          <button
            className={`px-6 py-3 rounded-xl font-bold text-white transition ${startIndex === 0 ? 'bg-blue-300 cursor-not-allowed' : 'bg-blue-700 hover:bg-blue-900'}`}
            onClick={handlePrev}
            disabled={startIndex === 0}
          >
            Prev
          </button>
          <button
            className={`px-6 py-3 rounded-xl font-bold text-white transition ${startIndex >= timelineData.length - ITEMS_PER_PAGE ? 'bg-blue-300 cursor-not-allowed' : 'bg-blue-700 hover:bg-blue-900'}`}
            onClick={handleNext}
            disabled={startIndex >= timelineData.length - ITEMS_PER_PAGE}
          >
            Next
          </button>
        </div>
      </div>
      {/* Event Details */}
      {currentIndex !== null && (
        <div className="mt-8 bg-blue-50 text-blue-900 rounded-2xl shadow-lg p-8 max-w-xl w-full text-center animate-fade-in">
          <h2 className="text-2xl font-bold mb-2">{timelineData[currentIndex].date}</h2>
          <h3 className="text-xl font-semibold mb-4">{timelineData[currentIndex].title}</h3>
          <p className="text-base">{timelineData[currentIndex].description}</p>
          <button
            className="mt-6 px-6 py-3 rounded-xl font-bold text-white bg-blue-700 hover:bg-blue-900 transition"
            onClick={() => setCurrentIndex(null)}
          >
            Close
          </button>
        </div>
      )}
      {/* Mobile Note */}
      <div className="mt-8 text-blue-700 text-sm opacity-80 text-center">
        Tap or click on a circle to see details of each event.
      </div>
    </div>
  );
};

export default Timeline;