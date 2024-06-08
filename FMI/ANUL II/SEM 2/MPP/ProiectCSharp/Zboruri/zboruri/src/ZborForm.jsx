import React, { useEffect, useState } from 'react';

export default function ZborForm({ addFunc, updateFunc, updateZbor, setUpdateZbor }) {
    const [aeroport, setAeroport] = useState('');
    const [destinatie, setDestinatie] = useState('');
    const [plecare, setPlecare] = useState('');
    const [nrLocuri, setNrLocuri] = useState(0);

    useEffect(() => {
        if (updateZbor) {
            setAeroport(updateZbor.aeroport);
            setDestinatie(updateZbor.destinatie);
            setPlecare(updateZbor.plecare.substring(0, 16));
            setNrLocuri(updateZbor.nrLocuri);
        }
    }, [updateZbor]);

    function handleSubmit(event) {
        event.preventDefault();
        const zbor = {
            id: updateZbor ? updateZbor.id : undefined, 
            aeroport: aeroport,
            destinatie: destinatie,
            plecare: plecare + ':00',
            nrLocuri: nrLocuri
        };

        if (updateZbor) {
            updateFunc(zbor);
            setUpdateZbor(null);
        } else {
            addFunc(zbor);
        }
        
        setAeroport('');
        setDestinatie('');
        setPlecare('');
        setNrLocuri(0);
    }

    function handleCancelUpdate() {
        setUpdateZbor(null); 
        setAeroport('');
        setDestinatie('');
        setPlecare('');
        setNrLocuri(0);
    }

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Aeroport:
                <input type="text" value={aeroport} onChange={e => setAeroport(e.target.value)} />
            </label><br/>
            <label>
                Destinatie:
                <input type="text" value={destinatie} onChange={e => setDestinatie(e.target.value)} />
            </label><br/>
            <label>
                Plecare:
                <input type="datetime-local" value={plecare} onChange={e => setPlecare(e.target.value)} />
            </label><br/>
            <label>
                Locuri:
                <input type="number" value={nrLocuri} onChange={e => setNrLocuri(e.target.value)} />
            </label><br/>
            
            <input type="submit" value={updateZbor ? "Update zbor" : "Add zbor"} />
            {updateZbor && (
                <button type="button" className="cancelButton" onClick={handleCancelUpdate}>Cancel Update</button>
            )}
        </form>
    );
}
