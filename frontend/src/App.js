import React, { useState } from 'react';
import './App.css';
import AudioRecorder from './components/AudioRecorder';
import ConversationDisplay from './components/ConversationDisplay';

function App() {
  const [conversation, setConversation] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleNewAudio = async (audioBlob) => {
    setIsProcessing(true);
    
    // TODO: Send to backend and get response
    // For now, simulate the process
    
    setTimeout(() => {
      const newEntry = {
        id: Date.now(),
        userAudio: audioBlob,
        transcript: "I'm feeling anxious about my upcoming presentation",
        sentiment: { sentiment: "negative", compound: -0.6 },
        response: "I understand that presentations can be really stressful. It's completely normal to feel anxious about something important like this. Would you like to talk more about what specifically is worrying you?",
        timestamp: new Date().toLocaleTimeString()
      };
      
      setConversation(prev => [...prev, newEntry]);
      setIsProcessing(false);
    }, 2000);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤗 Emotional Support AI</h1>
        <p>I'm here to listen and support you</p>
      </header>
      
      <main className="App-main">
        <AudioRecorder onAudioRecorded={handleNewAudio} isProcessing={isProcessing} />
        
        {isProcessing && (
          <div className="processing-message">
            <p>I'm listening and analyzing your message...</p>
          </div>
        )}
        
        <ConversationDisplay conversation={conversation} />
      </main>
    </div>
  );
}

export default App;
