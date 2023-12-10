const storageServerUrl = "http://localhost:8001"


export async function save(key, value) {
    console.log("Saving : ", JSON.stringify({
        key: key,
        value: value
    }));

    const response = await fetch(`${storageServerUrl}/items/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            key: key,
            value: value
        })
    });

    if (!response.ok) {
        const message = `An error has occurred: ${response.status}`;
        throw new Error(message);
    }

    const data = await response.json();
    return data;
}


export async function get(key) {
    const response = await fetch(`${storageServerUrl}/items/${key}`);

    if (!response.ok) {
        if (response.status === 404) {
            return null;
        }
        const message = `An error has occurred: ${response.status}`;
        throw new Error(message);
    }

    const data = await response.json();
    return data;
}
