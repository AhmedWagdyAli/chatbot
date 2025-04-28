import { useState } from 'react';
import Chat from './components/Chat';
import FileUpload from './components/FileUpload';  // Assuming you have Upload component already

function App() {
  const [activeTab, setActiveTab] = useState('chat'); // default tab

  return (
    <div style={styles.container}>
      <div style={styles.tabBar}>
        <button
          onClick={() => setActiveTab('upload')}
          style={activeTab === 'upload' ? styles.activeTab : styles.tab}
        >
          📄 Upload
        </button>
        <button
          onClick={() => setActiveTab('chat')}
          style={activeTab === 'chat' ? styles.activeTab : styles.tab}
        >
          💬 Chat
        </button>
      </div>

      <div style={styles.content}>
        {activeTab === 'upload' && <FileUpload />}
        {activeTab === 'chat' && <Chat />}
      </div>
    </div>
  );
}

const styles = {
  container: {
    fontFamily: '"Inter", sans-serif',
    margin: '2rem auto',
    maxWidth: '800px',
    padding: '2rem',
  },
  tabBar: {
    display: 'flex',
    gap: '1rem',
    justifyContent: 'center',
    marginBottom: '2rem',
  },
  tab: {
    padding: '0.8rem 2rem',
    backgroundColor: '#e0e0e0',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '1rem',
  },
  activeTab: {
    padding: '0.8rem 2rem',
    backgroundColor: '#4f46e5',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '1rem',
  },
  content: {
    marginTop: '1rem',
  },
};

export default App;
