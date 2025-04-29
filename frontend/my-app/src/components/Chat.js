import { useState } from 'react';
import ReactMarkdown from 'react-markdown'; 

function Chat() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [reasoning, setReasoning] = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  
  const sendMessage = async () => {
    if (!message.trim()) return;
    // Clear previous response and reasoning
    setResponse('');
    setReasoning('');
    const formData = new FormData();
    formData.append('query', message);
    formData.append('session_id', 'default_session'); // Add a session ID (replace with dynamic ID if needed)


    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error('Failed to get response');
      }

      const data = await res.json();
      setResponse(data.response);
      setReasoning(data.reasoning);
      setHistory(data.history); // Set reasoning steps
    } catch (error) {
      console.error(error);
      setResponse('Failed to get a response.');
      setReasoning('');
      setHistory(prev => [...prev, { role: 'assistant', content: 'Failed to get a response.' }]);

    } finally {
      setLoading(false);
    }
  };

  

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Ask the AI ✨</h2>

      <div style={styles.chatBox}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your question here..."
          style={styles.input}
        />
        <button onClick={sendMessage} style={styles.button}>
          Send
        </button>
      </div>

      {loading && <p style={styles.loading}>Loading...</p>}

      {response && (
        <div style={styles.responseBox}>
          <h4>AI Response:</h4>
          <p>{response}</p>
        </div>
      )}
  {history.map((msg, i) => (
    <div
      key={i}
      style={{
        marginBottom: '1rem',
        padding: '0.8rem',
        borderRadius: '8px',
        backgroundColor: msg.role === 'user' ? '#e0f7fa' : '#e8f5e9', // Different colors for user and AI
        alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start', // Align messages based on role
        maxWidth: '80%',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
      }}
    >
      <strong style={{ color: msg.role === 'user' ? '#00796b' : '#388e3c' }}>
        {msg.role === 'user' ? '🧑 You' : '🤖 AI'}:
      </strong>
      <ReactMarkdown>{msg.content}</ReactMarkdown>
    </div>
  ))}

  {reasoning && (
    <div style={styles.reasoningBox}>
      <h4>Reasoning Steps:</h4>
      <ReactMarkdown style={styles.reasoning}>
        {reasoning}
      </ReactMarkdown>
    </div>
  )}

    </div>
  );
}

const styles = {
  container: {
    maxWidth: '600px',
    margin: '3rem auto',
    padding: '2rem',
    backgroundColor: '#f9f9f9',
    borderRadius: '12px',
    boxShadow: '0 0 10px rgba(0,0,0,0.1)',
    fontFamily: '"Inter", sans-serif',
  },
  title: {
    textAlign: 'center',
    marginBottom: '2rem',
    fontSize: '2rem',
    color: '#333',
  },
  chatBox: {
    display: 'flex',
    gap: '0.5rem',
    marginBottom: '1rem',
  },
  input: {
    flexGrow: 1,
    padding: '0.8rem',
    borderRadius: '8px',
    border: '1px solid #ccc',
    fontSize: '1rem',
  },
  button: {
    padding: '0.8rem 1.2rem',
    borderRadius: '8px',
    backgroundColor: '#4f46e5',
    color: '#fff',
    border: 'none',
    cursor: 'pointer',
    fontSize: '1rem',
  },
  loading: {
    textAlign: 'center',
    color: '#666',
  },
  responseBox: {
    backgroundColor: '#fff',
    padding: '1rem',
    borderRadius: '8px',
    border: '1px solid #eee',
    marginTop: '1rem',
  },
  reasoningBox: {
    backgroundColor: '#f4f4f4',
    padding: '1rem',
    borderRadius: '8px',
    border: '1px solid #ddd',
    marginTop: '1rem',
    fontFamily: 'monospace',
    whiteSpace: 'pre-wrap',
    overflow: 'auto',
    maxHeight: '200px', 
  },
  reasoning: {
    color: '#555',
  },
};

export default Chat;