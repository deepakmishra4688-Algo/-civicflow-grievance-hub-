import { useState } from 'react';

const responses = [
  {
    predicate: (text) => /submit|complaint/i.test(text),
    answer: 'Use the submission form to provide your name, location, complaint details, and attachments. Then press the button to classify.'
  },
  {
    predicate: (text) => /status|track/i.test(text),
    answer: 'The admin dashboard shows complaint status categories: New, In Progress, Resolved, and High Priority.'
  },
  {
    predicate: (text) => /priority/i.test(text),
    answer: 'Priority is assigned automatically based on the urgency of the complaint details.'
  },
  {
    predicate: (text) => /attachment|photo|pdf/i.test(text),
    answer: 'You can attach images, PDFs, or documents when submitting the complaint.'
  }
];

function getResponse(message) {
  const match = responses.find((item) => item.predicate(message));
  return match ? match.answer : 'Ask about submitting a complaint, checking status, or filing attachments.';
}

export default function Chatbot() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { text: 'Hello! I can help with complaint filing and tracking.', sender: 'bot' }
  ]);
  const [value, setValue] = useState('');

  const handleSend = () => {
    if (!value.trim()) return;
    const userMessage = { text: value.trim(), sender: 'user' };
    setMessages((current) => [...current, userMessage]);

    setTimeout(() => {
      const botMessage = { text: getResponse(value), sender: 'bot' };
      setMessages((current) => [...current, botMessage]);
    }, 300);

    setValue('');
  };

  return (
    <div className="chat-widget">
      <button className="chat-trigger" onClick={() => setOpen((prev) => !prev)}>
        {open ? 'Close Chat' : 'Need Help?'}
      </button>
      {open && (
        <div className="chat-panel">
          <div className="chat-header">
            <div>
              <strong>Support Bot</strong>
              <p>Ask about complaint submission and tracking.</p>
            </div>
          </div>
          <div className="chat-body">
            {messages.map((message, index) => (
              <div key={index} className={`chat-message ${message.sender}`}>
                {message.text}
              </div>
            ))}
          </div>
          <div className="chat-input-row">
            <input
              value={value}
              onChange={(event) => setValue(event.target.value)}
              onKeyDown={(event) => event.key === 'Enter' && handleSend()}
              placeholder="Type your question..."
            />
            <button className="button button-primary" onClick={handleSend}>
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
