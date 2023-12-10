import * as exceptions from "../exceptions"


export async function registerCustomer(registerForm) {
  console.log("[api] Called registerCustomer()");
  console.log("registerForm:", registerForm);

  const customers = JSON.parse(localStorage.getItem("db.customer") || "[]");

  for (let supplier of customers) {
    if (supplier.credentials.login === registerForm.credentials.login) {
      throw new exceptions.AlreadyExists();
    }
  }

  if (registerForm.credentials.password.length < 5) {
    throw new exceptions.RequestFailed(null);
  }

  customers.push({
    id: customers.length,
    credentials: registerForm.credentials,
    info: registerForm.info,
  });

  localStorage.setItem("db.customer", JSON.stringify(customers));
  
  const token = {token: (customers.length - 1).toString()};
  return token;
}


export async function authCustomer(credentials) {
  console.log("[api] Called authCustomer()");
  console.log("credentials:", credentials);

  const customers = JSON.parse(localStorage.getItem("db.customer") || "[]");

  if (credentials.password.length < 5) {
    throw new exceptions.RequestFailed(null);
  }

  for (let customer of customers) {
    if (customer.credentials.login === credentials.login) {
      if (customer.credentials.password !== credentials.password) {
        throw new exceptions.InvalidCredentials(credentials);
      }

      return {token: customer.id};
    }
  }

  throw new exceptions.InvalidCredentials(credentials);
}


export async function registerSupplier(registerForm) {
  console.log("[api] Called registerSupplier()");
  console.log("registerForm:", registerForm);

  const suppliers = JSON.parse(localStorage.getItem("db.supplier") || "[]");

  for (let supplier of suppliers) {
    if (supplier.credentials.login === registerForm.credentials.login) {
      throw new exceptions.AlreadyExists();
    }
  }

  if (registerForm.credentials.password.length < 5) {
    throw new exceptions.RequestFailed(null);
  }

  suppliers.push({
    id: suppliers.length,
    credentials: registerForm.credentials,
    info: registerForm.info,
  });

  localStorage.setItem("db.supplier", JSON.stringify(suppliers));
  
  const token = {token: (suppliers.length - 1).toString()};
  return token;
}


export async function authSupplier(credentials) {
  console.log("[api] Called authSupplier()");
  console.log("credentials:", credentials);

  const suppliers = JSON.parse(localStorage.getItem("db.supplier") || "[]");

  if (credentials.password.length < 5) {
    throw new exceptions.RequestFailed(null);
  }

  for (let supplier of suppliers) {
    if (supplier.credentials.login === credentials.login) {
      if (supplier.credentials.password !== credentials.password) {
        throw new exceptions.InvalidCredentials(credentials);
      }

      return {token: supplier.id.toString()};
    }
  }

  throw new exceptions.InvalidCredentials(credentials);
}
