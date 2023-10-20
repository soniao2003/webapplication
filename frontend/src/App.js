
import './App.css';
import {useState, useEffect} from 'react';

function App() {

  const[products, setProdcuts] = useState([])

  useEffect(() => {
    fetch('http://127.0.0.1/get', {
      'methods':'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(resp => resp.json())
    .then(resp => console.log(resp))
    .catch(error => console.log(error))
  })
  return (
    <div className="App">
     <h1>Moja apka</h1>
    </div>
  );
}

export default App;
