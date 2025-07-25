import React from 'react';

const medals = {
    1: "🥇",
    2: "🥈",
    3: "🥉",
};

const PlayerRow = ({ rank, name, score }) => {
    let bgColor = "bg-white";
    let textColor = "text-gray-800";
    if (rank === 1) {
        bgColor = "bg-yellow-400";
        textColor = "text-yellow-800 font-bold";
    } else if (rank === 2) {
        bgColor = "bg-gray-300";
        textColor = "text-gray-700 font-bold";
    } else if (rank === 3) {
        bgColor = "bg-amber-800";
        textColor = "text-amber-100 font-bold";
    }

    return (
        <tr className={`${bgColor} ${textColor} hover:bg-yellow-100 transition-colors`}>
            <td className="py-3 px-2 text-center font-mono text-sm sm:text-base">
                {medals[rank] ? (
                    <span className="text-2xl sm:text-4xl">{medals[rank]}</span>
                ) : (
                    <span className="text-base sm:text-lg">{rank}</span>
                )}
            </td>
            <td className="py-3 px-2 font-semibold text-sm sm:text-base">{name}</td>
            <td className="py-3 px-2 text-right font-mono text-sm sm:text-base">{score}</td>
        </tr>
    );
};

const LeaderBoard = () => {

    const players = [
        { name: "AriaSun", score: 9850 },
        { name: "Maximus", score: 9380 },
        { name: "LunaBee", score: 9120 },
        { name: "NovaStar", score: 8700 },
        { name: "EchoWolf", score: 8450 },
        { name: "Zephyr", score: 8120 },
        { name: "Kairos", score: 7890 },
        { name: "VegaSky", score: 7650 },
        { name: "Orion", score: 7400 },
        { name: "Sierra", score: 7100 },
        { name: "Phoenix", score: 6850 },
        { name: "Solstice", score: 6700 },
        { name: "Nixie", score: 6500 },
        { name: "ZaraMoon", score: 6300 },
        { name: "Talon", score: 6000 },
    ];

    return (
        <div className="min-h-screen w-full bg-gradient-to-br from-blue-100 via-blue-200 to-blue-300 p-4 sm:p-8">
            <div className="max-w-5xl mx-auto bg-gradient-to-r from-blue-50 to-blue-100 rounded-xl shadow-lg p-4 sm:p-8">
                <h2 className="text-3xl sm:text-5xl font-bold text-center italic mb-6 sm:mb-8 tracking-wide">
                    Leaderboard
                </h2>

                {/* Responsive Table Container */}
                <div className="overflow-x-auto">
                    <table className="min-w-full text-left rounded-lg overflow-hidden">
                        <thead className="bg-blue-400 text-black">
                            <tr>
                                <th className="py-3 px-2 text-center text-sm sm:text-base">Rank</th>
                                <th className="py-3 px-2 text-sm sm:text-base">Player</th>
                                <th className="py-3 px-2 text-right text-sm sm:text-base">Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            {players.map((player, index) => (
                                <PlayerRow
                                    key={player.name}
                                    rank={index + 1}
                                    name={player.name}
                                    score={player.score}
                                />
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default LeaderBoard;
