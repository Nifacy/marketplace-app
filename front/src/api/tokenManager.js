const tokenItemName = "token";


export function saveToken(userType, token) {
    console.log("[api.token] save token...")
    localStorage.setItem(
        tokenItemName,
        JSON.stringify({type: userType, token: token}),
    );
    console.log("[api.token] token saved");
}


export function getToken() {
    console.log("[api.token] getting token...");
    const data = localStorage.getItem(tokenItemName);

    if (data === null) {
        console.log("[api.token] token not generated before");
        return null;
    }
    
    console.log("[api.token] found token");
    return JSON.parse(data);
}
