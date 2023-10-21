import './App.css';
import { useState, useEffect } from 'react';

function App() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/get', {
      method: 'GET', // Poprawione z 'methods' na 'method'
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((resp) => {
        if (!resp.ok) {
          throw new Error('Network response was not ok');
        }
        return resp.json();
      })
      .then((data) => {
        setUsers(data); // Tu możesz zaktualizować stan komponentu
      })
      .catch((error) => {
        console.log('Error:', error);
      });
  }, []); // Dodaj pustą tablicę, aby useEffect wykonywał się tylko raz po zamontowaniu komponentu

  return (
    <div className="App">
      <h1>Moja apka</h1>
      {users.map(product => {
        return (
          <div key = {product.title}>
            <h2>{product.description}</h2>
            <h2>{product.imageUrl}</h2>
          </div>
        )
      })}
    
    </div>
  );
}

export default App;
