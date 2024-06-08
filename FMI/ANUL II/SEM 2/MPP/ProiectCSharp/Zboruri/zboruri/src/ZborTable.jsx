import React from "react";

function ZborRow({zbor, deleteFunc, setUpdateZbor}) {
    function formatDate(dateString) {
        const date = new Date(dateString);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');

        return `${year}-${month}-${day} ${hours}:${minutes}`;
    }

    function handleDelete(event) {
        console.log('delete button pentru ' + zbor.id);
        deleteFunc(zbor.id);
    }

    function handleUpdate(event) {
        console.log('update button pentru ' + zbor.id);
        setUpdateZbor(zbor);
    }

    const formattedPlecare = formatDate(zbor.plecare);
    return (
        <tr>
            <td>{zbor.aeroport}</td>
            <td>{zbor.destinatie}</td>
            <td>{formattedPlecare}</td>
            <td>{zbor.nrLocuri}</td>
            <td>
                <button onClick={handleDelete}>Delete</button>
                <br/><br/>
                <button onClick={handleUpdate}>Update</button>
            </td>
        </tr>
    );
}

export default function ZborTable({zboruri, deleteFunc, setUpdateZbor}) {
    console.log("In ZborTable");
    console.log(zboruri);
    let rows = [];
    zboruri.forEach(zbor => {
        rows.push(<ZborRow zbor={zbor} key={zbor.id} deleteFunc={deleteFunc} setUpdateZbor={setUpdateZbor}/>);
    });
    return (
        <div className="ZborTable">
            <table className="center">
                <thead>
                <tr>
                    <th>Aeroport</th>
                    <th>Destinatie</th>
                    <th>Plecare</th>
                    <th>Locuri</th>
                    <th>Actions</th>
                </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
    );
}
