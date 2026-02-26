import { useState, useEffect, useRef } from 'react';
import './VoiceInput.css';

/**
 * Voice input component using Web Speech API.
 * Falls back gracefully if not supported.
 */
export default function VoiceInput({ onResult, disabled }) {
    const [isListening, setIsListening] = useState(false);
    const [isSupported, setIsSupported] = useState(false);
    const [interim, setInterim] = useState('');
    const recognitionRef = useRef(null);

    useEffect(() => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            setIsSupported(true);
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = 'en-IN';

            recognition.onresult = (event) => {
                let finalTranscript = '';
                let interimTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript;
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                    }
                }
                setInterim(interimTranscript);
                if (finalTranscript) {
                    onResult?.(finalTranscript);
                    setInterim('');
                    setIsListening(false);
                }
            };

            recognition.onerror = () => setIsListening(false);
            recognition.onend = () => setIsListening(false);
            recognitionRef.current = recognition;
        }

        return () => {
            recognitionRef.current?.abort();
        };
    }, [onResult]);

    const toggleListening = () => {
        if (!recognitionRef.current) return;
        if (isListening) {
            recognitionRef.current.stop();
            setIsListening(false);
        } else {
            setInterim('');
            recognitionRef.current.start();
            setIsListening(true);
        }
    };

    if (!isSupported) return null;

    return (
        <div className="voice-input">
            <button
                className={`voice-btn ${isListening ? 'listening' : ''}`}
                onClick={toggleListening}
                disabled={disabled}
                title={isListening ? 'Stop listening' : 'Start voice input'}
            >
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                    <line x1="12" y1="19" x2="12" y2="23" />
                    <line x1="8" y1="23" x2="16" y2="23" />
                </svg>
                {isListening && (
                    <span className="pulse-ring" />
                )}
            </button>
            {interim && <span className="interim-text">{interim}</span>}
        </div>
    );
}
