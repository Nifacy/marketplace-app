import * as exceptions from "../exceptions"
import * as types from "../types.ts"
import * as storage from "./storage.js"


export async function registerCustomer(registerForm: types.CustomerRegisterForm): Promise<types.Token> {
  console.log("[api] Called registerCustomer()");
  console.log("registerForm:", registerForm);

  const customers = await storage.get("db-customer") || [];

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
    favorites: [],
  });

  await storage.save("db-customer", customers);
  
  const token: types.Token = {token: (customers.length - 1).toString()};
  return token;
}


export async function authCustomer(credentials: types.CustomerCredentials): Promise<types.Token> {
  console.log("[api] Called authCustomer()");
  console.log("credentials:", credentials);

  const customers = await storage.get("db-customer") || [];

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


export async function registerSupplier(registerForm: types.SupplierRegisterForm): Promise<types.Token> {
  console.log("[api] Called registerSupplier()");
  console.log("registerForm:", registerForm);

  const suppliers = await storage.get("db-supplier") || [];

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

  await storage.save("db-supplier", suppliers);
  
  const token: types.Token = {token: (suppliers.length - 1).toString()};
  return token;
}


export async function authSupplier(credentials: types.SupplierCredentials): Promise<types.Token> {
  console.log("[api] Called authSupplier()");
  console.log("credentials:", credentials);

  const suppliers = await storage.get("db-supplier") || [];

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
