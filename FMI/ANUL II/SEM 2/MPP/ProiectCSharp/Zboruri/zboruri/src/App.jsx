import React, { useEffect, useState } from 'react';
import './App.css';
import { GetZboruri, DeleteZbor, AddZbor, ModifyZbor } from './utils/rest-calls';
import ZborTable from './ZborTable';
import ZborForm from './ZborForm';
import airplane from './assets/airplane.svg';

function App() {
    const [zboruri, setZboruri] = useState([]);
    const [updateZbor, setUpdateZbor] = useState(null);

    function addFunc(zbor) {
        console.log('inside add Func ' + zbor);
        AddZbor(zbor)
            .then(() => GetZboruri())
            .then(zboruri => setZboruri(zboruri))
            .catch(error => console.log('eroare add ', error));
    }

    function updateFunc(zbor) {
        console.log('inside updateFunc ' + zbor);
        ModifyZbor(zbor)
            .then(() => GetZboruri())
            .then(zboruri => setZboruri(zboruri))
            .catch(error => console.log('eroare update ', error));
    }

    function deleteFunc(zbor) {
        console.log('inside deleteFunc ' + zbor);
        DeleteZbor(zbor)
            .then(() => GetZboruri())
            .then(zboruri => setZboruri(zboruri))
            .catch(error => console.log('eroare delete', error));
    }

    useEffect(() => {
        console.log('inside useEffect');
        GetZboruri().then(zboruri => setZboruri(zboruri));
    }, []);

    return (
        <div className="App">
            <header>
                <img src={airplane} alt="Airplane" />
                <h1>Zboruri</h1>
            </header>
            <div className="container">
                <ZborForm addFunc={addFunc} updateFunc={updateFunc} updateZbor={updateZbor} setUpdateZbor={setUpdateZbor} />
                <ZborTable zboruri={zboruri} deleteFunc={deleteFunc} setUpdateZbor={setUpdateZbor} />
            </div>
        </div>
    );
}

export default App;