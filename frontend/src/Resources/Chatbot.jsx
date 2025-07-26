import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, FileText, Globe, Clock } from 'lucide-react';
import ChatService from '../services/ChatService';

/**
 * Chatbot UI Component
 * Enhanced with Tailwind CSS and best UX practices.
 * Structure: Header, Messages Area, Input Bar.
 */
function Chatbot() {
  // State hooks for message management, input, API status, etc.
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState('');
  const [apiStatus, setApiStatus] = useState(null);
  const messagesEndRef = useRef(null);

  // On mount: session ID + API status check + welcome message
  useEffect(() => {
    setSessionId(generateSessionId());
    checkApiStatus();
  }, []);

  // Scroll to bottom on new message
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Generate session ID for chat context
  const generateSessionId = () => 'session_' + Math.random().toString(36).substr(2, 9);

  // API health check and welcome message
  const checkApiStatus = async () => {
    try {
      const status = await ChatService.getApiStatus();
      setApiStatus(status);
      setMessages([{
        id: 'welcome',
        type: 'bot',
        content: `👋 Welcome to the Nepal Legal Chatbot!\n\nAsk me legal questions in English or Nepali (नेपाली).\n\n**Features:**\n• Nepal Constitution & Legal Docs\n• Business & Contract Law\n• Powered by GPT-4o + Pinecone `,
        timestamp: new Date(),
        sources: [],
        language: 'english'
      }]);
    } catch {
      setMessages([{
        id: 'error-welcome',
        type: 'bot',
        content: ` Welcome to the Nepal Legal Chatbot!\n\nAsk me legal questions in English or Nepali (नेपाली).\n\n**Features:**\n• Nepal Constitution & Legal Docs\n• Business & Contract Law\n• Powered by GPT-4o + Pinecone`,
        timestamp: new Date(),
        sources: [],
        isError: true
      }]);
    }
  };

  // Smooth scroll to latest message
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Send chat message handler
  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date(),
      language: detectLanguage(inputMessage)
    };
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await ChatService.sendMessage(inputMessage, sessionId);
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.answer,
        timestamp: new Date(),
        sources: response.sources || [],
        language: response.language?.detected || 'english',
        model: response.model_info?.llm || 'unknown',
        sourcesFound: response.model_info?.sources_found || 0
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        type: 'bot',
        content: `❌ Error: ${error.message}`,
        timestamp: new Date(),
        sources: [],
        isError: true
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Simple regex-based Nepali detection
  const detectLanguage = (text) => /[\u0900-\u097F]/.test(text) ? 'nepali' : 'english';

  // Enter-to-send shortcut
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Format time for message
  const formatTimestamp = (timestamp) => (
    timestamp.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  );

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-100 via-blue-200 to-blue-400">
      {/* ---- HEADER ---- */}
      <header className="w-full shadow-2xl bg-gradient-to-r from-blue-400 via-blue-500 to-blue-700 py-6 px-2 rounded-b-3xl">
        <div className="max-w-2xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="rounded-full bg-blue-700 shadow-2xl p-4 animate-pulse-slow">
              <Bot className="text-white w-10 h-10 drop-shadow-xl" />
            </div>
            <div>
              <h1 className="text-3xl sm:text-4xl font-extrabold text-white drop-shadow-lg tracking-wider">
                NAYARA
              </h1>
              <p className="text-blue-200 font-semibold text-base">Chat with AI</p>
            </div>
          </div>
          {apiStatus && (
            <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-white/20 shadow font-semibold text-white border border-blue-200 animate-pulse">
              <span className="w-3 h-3 bg-emerald-400 rounded-full animate-pulse"></span>
              <span>API Online</span>
            </div>
          )}
        </div>
      </header>

      {/* ---- CHAT MESSAGES ---- */}
      <main className="flex-1 flex flex-col max-w-2xl w-full mx-auto py-4 px-3">
        <div className="flex-1 overflow-y-auto">
          <div className="flex flex-col gap-4 mt-2">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}
              >
                <div
                  className={`
                    flex gap-3 max-w-[88%]
                    ${message.type === 'user' ? 'flex-row-reverse' : ''}
                  `}
                >
                  {/* Avatar */}
                  <div className={`rounded-full shadow-xl p-3
                    ${message.type === 'user' 
                      ? 'bg-gradient-to-tr from-blue-200 via-blue-300 to-blue-400 border-2 border-white'
                      : 'bg-blue-700 border-2 border-blue-300'
                    }
                  `}>
                    {message.type === 'user'
                      ? <User className="text-blue-800 w-7 h-7" />
                      : <Bot className="text-blue-100 w-7 h-7" />
                    }
                  </div>
                  {/* Message Bubble */}
                  <div className={`
                    px-5 py-3 rounded-2xl shadow-2xl
                    ${message.type === 'user'
                      ? 'bg-gradient-to-br from-white to-blue-100 text-blue-900 font-bold rounded-br-3xl border border-blue-200'
                      : 'bg-gradient-to-br from-blue-600 via-blue-300 to-blue-700 text-white font-semibold rounded-bl-3xl border border-blue-400'
                    }
                    ${message.isError ? 'text-red-200 border-red-400 bg-gradient-to-br from-blue-700 to-red-400/50' : ''}
                  `}>
                    {/* Meta */}
                    <div className="flex items-center gap-2 mb-1 text-xs opacity-80 font-semibold select-none">
                      <span>
                        {message.type === 'user' ? 'You' : 'Legal Assistant'}
                      </span>
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {formatTimestamp(message.timestamp)}
                      </span>
                      {message.language && (
                        <span className="flex items-center gap-1">
                          <Globe className="w-3 h-3" />
                          {message.language}
                        </span>
                      )}
                    </div>
                    {/* Text */}
                    <div className="whitespace-pre-line mt-1 mb-2 text-base leading-snug">
                      {message.content.split('\n').map((line, idx) => (
                        <div key={idx} className="py-0.5">
                          {line.startsWith('**') && line.endsWith('**') ? (
                            <strong className="font-extrabold text-blue-50">{line.slice(2, -2)}</strong>
                          ) : line.startsWith('•') ? (
                            <li className="ml-6 list-disc text-blue-100">{line.slice(1).trim()}</li>
                          ) : (
                            line
                          )}
                        </div>
                      ))}
                    </div>

                    {/* Sources */}
                    {message.sources && message.sources.length > 0 && (
                      <div className="mt-2 bg-blue-900/80 rounded-xl px-3 py-2 text-xs">
                        <div className="flex items-center gap-1 font-bold mb-1 text-blue-300">
                          <FileText className="w-4 h-4" />
                          <span>Sources ({message.sources.length})</span>
                        </div>
                        {message.sources.slice(0, 3).map((source, idx) => (
                          <div key={idx} className="ml-3 text-blue-200/80 font-mono truncate">
                            <span className="font-semibold">{source.source ? source.source.split('\\').pop() : 'Legal Document'}: </span>
                            <span className="opacity-80">{source.content?.substring(0, 100)}...</span>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Model Info */}
                    {message.model && message.type === 'bot' && (
                      <div className="mt-2 text-xs text-blue-200/90 flex gap-2 items-center">
                        <span>Model: {message.model}</span>
                        {message.sourcesFound !== undefined && (
                          <span>• Sources: {message.sourcesFound}</span>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}

            {/* Loading Spinner */}
            {isLoading && (
              <div className="flex justify-start animate-pulse">
                <div className="flex gap-3">
                  <div className="rounded-full bg-blue-700 shadow-xl p-3">
                    <Bot className="text-blue-100 w-7 h-7" />
                  </div>
                  <div className="px-5 py-3 rounded-2xl bg-gradient-to-br from-blue-700 via-blue-300 to-blue-800 text-blue-100 font-semibold rounded-bl-3xl border border-blue-300 shadow-2xl">
                    <div className="flex gap-2 items-center text-xs opacity-80 font-semibold">
                      <span>Legal Assistant</span>
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        <span>...</span>
                      </span>
                    </div>
                    <div className="flex gap-1 mt-2">
                      <span className="w-2 h-2 rounded-full bg-blue-200 animate-bounce"></span>
                      <span className="w-2 h-2 rounded-full bg-blue-300 animate-bounce delay-150"></span>
                      <span className="w-2 h-2 rounded-full bg-blue-400 animate-bounce delay-300"></span>
                    </div>
                    <span className="block mt-1 text-xs text-blue-100/80">Thinking...</span>
                  </div>
                </div>
              </div>
            )}
            {/* Empty div for scroll anchor */}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* ---- INPUT AREA ---- */}
        <div className="w-full bg-gradient-to-r from-blue-400 via-blue-200 to-blue-300 rounded-t-3xl shadow-2xl p-5 flex flex-col gap-1 border-t-2 border-blue-200">
          <div className="flex items-end gap-3">
            {/* Message input box */}
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your legal question... (Press Enter to send)"
              className="flex-1 resize-none rounded-xl px-4 py-3 text-base font-semibold bg-blue-100 text-blue-900 shadow-inner border-2 border-blue-200 placeholder-blue-400 focus:outline-none focus:ring-2 focus:ring-blue-400 transition min-h-[48px] max-h-40"
              disabled={isLoading}
              rows={1}
            />
            {/* Send button */}
            <button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className={`
                ml-2 rounded-full bg-gradient-to-tr from-blue-400 via-blue-200 to-blue-600 shadow-lg p-4 transition hover:scale-110 hover:shadow-2xl
                ${(!inputMessage.trim() || isLoading) ? 'opacity-50 cursor-not-allowed' : ''}
              `}
              title="Send"
            >
              <Send className="w-7 h-7 text-blue-700" />
            </button>
          </div>
          {/* Suggestion */}
          <div className="text-xs text-blue-700 mt-2 ml-2 font-semibold select-none">
            💡 Try: <span className="italic text-blue-800">"What is contract law?"</span> or <span className="italic text-blue-800">"करार कानून के हो?"</span>
          </div>
        </div>
      </main>
    </div>
  );
}

export default Chatbot;