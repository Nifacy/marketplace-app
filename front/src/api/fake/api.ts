import * as storage from "./storage"
import * as types from "../types"
import * as exceptions from "../exceptions"
import * as tokenManager from "../tokenManager";


type TokenData = {
  type: "supplier" | "customer";
  id: number;
}


let currentToken: TokenData | null = JSON.parse(tokenManager.getToken().token);


async function getUser(): Promise<types.Customer | types.Supplier> {
  if (currentToken === null) {
    throw new exceptions.Unauthorized();
  }

  const dbKey = currentToken.type === "supplier" ? "db-supplier" : "db-customer";
  const users: types.Customer[] | types.Supplier[] = await storage.get(dbKey);

  for (let user of users) {
    if (user.id === currentToken.id) {
      return user;
    }
  }

  throw new exceptions.Unauthorized();
}


function checkUserType(expectedType?: "supplier" | "customer"): void {
  if (currentToken === null) throw new exceptions.Unauthorized();
  if (expectedType === undefined) return;
  if (currentToken.type !== expectedType) throw new exceptions.Unauthorized();
}


export async function getProducts(name?: string): Promise<types.Product[]> {
  console.log(`[api] called getProducts(name=${name})`);
  
  checkUserType();

  let products: types.Product[] = await storage.get("db-products") || [];

  if (name !== undefined) {
    products = products.filter(product => {
      product.info.product_name.toLowerCase().includes(name.toLowerCase());
    });
  }
  
  if (currentToken?.type === "customer") {
    const favoriteIds = (await getFavorites()).map(product => product.id);

    for (let product of products) {
      if (favoriteIds.includes(product.id)) {
        product.in_favorites = true;
      }
    }
  }

  console.log("[api] found products:")
  console.log(products);
  return products;
}


export async function addToFavorites(productId: number): Promise<types.Product> {
  console.log(`[api] called addToFavorites(${productId})`);

  if (currentToken === null) throw new exceptions.Unauthorized();
  checkUserType("customer");

  let products: types.Product[] = await storage.get("db-products") || [];

  for (const product of products) {
    if (product.id === productId) {
      let favorites = await storage.get("db-favorites") || {};
      const userId = currentToken.id.toString();

      if (favorites[userId] === undefined) {
        favorites[userId] = [];
      }

      if (!favorites[userId].includes(productId)) {
        console.log("[api] Product added to favorites");
        favorites[userId].push(productId);
      } else {
        console.log("[api] Product already in favorites");
      }

      await storage.save("db-favorites", favorites);
      return product;
    }
  }

  throw new exceptions.NotFound();
}


export async function removeFromFavorites(productId: number): Promise<types.Product> {
  console.log(`[api] called addToFavorites(${productId})`);

  if (currentToken === null) throw new exceptions.Unauthorized();
  checkUserType("customer");

  let products: types.Product[] = await storage.get("db-products") || [];

  for (const product of products) {
    if (product.id === productId) {
      let favorites = await storage.get("db-favorites") || {};
      const userId = currentToken.id.toString();

      if (favorites[userId] === undefined) {
        favorites[userId] = [];
      }

      if (favorites[userId].includes(productId)) {
        favorites[userId].splice(
          favorites[userId].indexOf(productId),
          1,
        );
        console.log("[api] Product removed to favorites");
      } else {
        console.log("[api] Product already removed from favorites");
      }

      await storage.save("db-favorites", favorites);
      return product;
    }
  }

  throw new exceptions.NotFound();
}


export async function getFavorites(): Promise<types.Product[]> {
  console.log(`[api] called getFavorites()`);

  if (currentToken === null) throw new exceptions.Unauthorized();
  checkUserType("customer");

  let favorites = await storage.get("db-favorites") || {};
  const userId = currentToken.id.toString();

  if (favorites[userId] === undefined) {
    favorites[userId] = [];
  }

  let products: types.Product[] = await storage.get("db-products") || [];
  let favoriteProducts: types.Product[] = [];

  for (const product of products) {
    if (favorites[userId].includes(product.id)) {
      favoriteProducts.push(product);
    }
  }

  return favoriteProducts;
}


export async function getOrders(): Promise<types.Order[]> {
  console.log(`[api] called getOrders()`);
  console.log("[api] currentToken: ", currentToken);

  if (currentToken === null) throw new exceptions.Unauthorized();
  let products = await storage.get("db-products") || [];
  let orders = await storage.get("db-orders") || [];
  let customers = await storage.get("db-customer") || [];
  let foundOrders: types.Order[] = [];

  for (let order of orders) {
    const product = products.find(product => product.id === order.productId);
    const customer = customers.find(customer => customer.id === order.customerId);
    
    const fullOrder = {
      id: order.id,
      status: order.status,
      cancel_description: order.cancel_description,
      price: order.price,
      creation_datetime: order.creation_datetime,
      product: product,
      target_address: order.target_address,
      customer: customer,
    };

    if (currentToken.type === "supplier") {
      if (product?.supplier.id === currentToken.id) {
        foundOrders.push(fullOrder);
      }
    } else if (customer?.id === currentToken.id) {
      foundOrders.push(fullOrder);
    }
  }

  console.log("[api] found orders:")
  console.log(foundOrders);
  return foundOrders;
}
