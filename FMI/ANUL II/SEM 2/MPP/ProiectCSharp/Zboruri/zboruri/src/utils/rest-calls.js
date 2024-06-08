import {ZBORURI_BASE_URL} from './consts';

function status(response) {
    console.log('response status '+response.status);
    if (response.status >= 200 && response.status < 300) {
        return Promise.resolve(response)
    } else {
        return Promise.reject(new Error(response.statusText))
    }
}

function json(response) {
    return response.json()
}

export function GetZboruri() {
    let headers = new Headers();
    headers.append('Accept', 'application/json');
    let init = { method : 'GET',
        headers : headers,
        mode : 'cors',
    };
    let request = new Request(ZBORURI_BASE_URL, init);

    console.log('Inainte de fetch GET pentru '+ZBORURI_BASE_URL);

    return fetch(request)
        .then(status)
        .then(json)
        .then(data => {
            console.log('Request succeeded with JSON response', data);
            return data;
        })
        .catch(error => {
            console.log('Request failed', error);
            return Promise.reject(error);
        });
}

export function DeleteZbor(id){
    console.log('inainte de fetch delete')
    let headers = new Headers();
    headers.append("Accept", "application/json");

    let antet = { method: 'DELETE',
        headers: headers,
       mode: 'cors'
    };

    const zboruriDelUrl = ZBORURI_BASE_URL+'/'+id;
    console.log('URL pentru delete   '+zboruriDelUrl)
    return fetch(zboruriDelUrl,antet)
        .then(status)
        .then(response=>{
            console.log('Delete status '+response.status);
            return response.text();
        }).catch(e=>{
            console.log('error '+e);
            return Promise.reject(e);
        });
}

export function AddZbor(zbor){
    console.log('inainte de fetch post'+JSON.stringify(zbor));

    let headers = new Headers();
    headers.append("Accept", "application/json");
    headers.append("Content-Type","application/json");

    let antet = { method: 'POST',
        headers: headers,
        mode: 'cors',
        body:JSON.stringify(zbor)};

    return fetch(ZBORURI_BASE_URL,antet)
        .then(status)
        .then(response=>{
            return response.text();
        }).catch(error=>{
            console.log('Request failed', error);
            return Promise.reject(error);
        });


}

export function ModifyZbor(zbor){
    console.log('inainte de fetch put'+JSON.stringify(zbor));

    let headers = new Headers();
    headers.append("Accept", "application/json");
    headers.append("Content-Type","application/json");

    let antet = { method: 'PUT',
        headers: headers,
        mode: 'cors',
        body:JSON.stringify(zbor)};

    const zboruriPutUrl = ZBORURI_BASE_URL+'/'+zbor.id;
    console.log('URL pentru put   '+zboruriPutUrl)
    return fetch(zboruriPutUrl,antet)
        .then(status)
        .then(response=>{
            return response.text();
        }).catch(error=>{
            console.log('Request failed', error);
            return Promise.reject(error);
        });
}