import * as config from "../config"
import * as exceptions from "../exceptions"


export async function registerCustomer(registerForm) {
  console.log("[api] Called registerCustomer()");
  console.log("registerForm:", registerForm);

  const response = await fetch(
    `${config.BackendUrl}/customer/register/`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(registerForm),
    }
  );

  if (!response.ok) {
    console.warn(`[api] Got error response (${response.status}):`, await response.json());
    
    if (response.status === 409) {
      throw new exceptions.AlreadyExists();
    } else {
      throw new exceptions.RequestFailed(response.status);
    }
  }

  console.log("[api] Got success response");
  const token = await response.json();
  return token;
}


export async function authCustomer(credentials) {
  console.log("[api] Called authCustomer()");
  console.log("credentials:", credentials);

  const response = await fetch(
    `${config.BackendUrl}/customer/login/`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
    }
  );

  if (!response.ok) {
    console.warn(`[api] Got error response (${response.status}):`, await response.json());
    
    if (response.status === 401) {
      throw new exceptions.InvalidCredentials(credentials);
    } else {
      throw new exceptions.RequestFailed(response.status);
    }
  }

  console.log("[api] Got success response");
  const token = await response.json();
  return token;
}


export async function registerSupplier(registerForm) {
  console.log("[api] Called registerSupplier()");
  console.log("registerForm:", registerForm);

  const response = await fetch(
    `${config.BackendUrl}/supplier/register/`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(registerForm),
    }
  );

  if (!response.ok) {
    console.warn(`[api] Got error response (${response.status}):`, await response.json());
    
    if (response.status === 409) {
      throw new exceptions.AlreadyExists();
    } else {
      throw new exceptions.RequestFailed(response.status);
    }
  }

  console.log("[api] Got success response");
  const token = await response.json();
  return token;
}


export async function authSupplier(credentials) {
  console.log("[api] Called authSupplier()");
  console.log("credentials:", credentials);

  const response = await fetch(
    `${config.BackendUrl}/supplier/login/`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
    }
  );

  if (!response.ok) {
    console.warn(`[api] Got error response (${response.status}):`, await response.json());
    
    if (response.status === 401) {
      throw new exceptions.InvalidCredentials(credentials);
    } else {
      throw new exceptions.RequestFailed(response.status);
    }
  }

  console.log("[api] Got success response");
  const token = await response.json();
  return token;
}
