import React, { useState, useRef } from 'react';
import { Mic, Square, Loader } from 'lucide-react';
import AudioRecorder from 'react-audio-voice-recorder';

const AudioRecorderComponent = ({ onAudioRecorded, isProcessing }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);

  const handleRecordingComplete = (blob) => {
    setAudioBlob(blob);
    onAudioRecorded(blob);
  };

  if (isProcessing) {
    return (
      <div className="audio-recorder processing">
        <Loader className="spinner" />
        <p>Processing your message...</p>
      </div>
    );
  }

  return (
    <div className="audio-recorder">
      <h2>Share how you're feeling</h2>
      <p>Click the microphone and speak from your heart</p>
      
      <div className="recorder-container">
        <AudioRecorder
          onRecordingComplete={handleRecordingComplete}
          downloadOnSavePress={false}
          downloadFileExtension="wav"
          classes={{
            AudioRecorderClass: 'custom-audio-recorder'
          }}
        />
      </div>
      
      {audioBlob && (
        <div className="audio-preview">
          <p>✅ Message recorded! Processing...</p>
        </div>
      )}
    </div>
  );
};

export default AudioRecorderComponent; 