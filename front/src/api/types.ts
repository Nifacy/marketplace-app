export type Contacts = {
    phone: string;
    email: string;
    telegram?: string;
    whatsapp?: string;
};
  
export type Address = {
    street: string;
    city: string;
    country: string;
    postal_code: string;
    house: number;
    entrance: number;
    appartment: number;
};

export type SupplierInfo = {
    name: string;
    contacts: Contacts;
    address: Address;
};

export type Supplier = {
    id: number;
    info: SupplierInfo;
};

export type SupplierCredentials = {
    login: string;
    password: string;
};

export type SupplierRegisterForm = {
    credentials: SupplierCredentials;
    info: SupplierInfo;
};

export type CustomerInfo = {
    first_name: string;
    last_name: string;
    contacts: Contacts;
    address: Address;
};

export type Customer = {
    id: number;
    info: CustomerInfo;
};

export type CustomerCredentials = {
    login: string;
    password: string;
};

export type CustomerRegisterForm = {
    credentials: CustomerCredentials;
    info: CustomerInfo;
};
  
export type ProductInfo = {
    images: string[];
    price: number;
    product_name: string;
    description: string;
};

export type Product = {
    id: number;
    in_favorites: boolean;
    info: ProductInfo;
    supplier: Supplier;
};

export type OrderStatus = 'created' | 'confirmed' | 'paid' | 'sent_to_delivery' | 'picked_up' | 'canceled';

export type OrderCreateSchema = {
  product_id: number;
  target_address: Address;
};

export type Order = {
  id: number;
  status: OrderStatus;
  cancel_description?: string | null;
  price: number;
  creation_datetime: string;
  product: Product;
  target_address: Address;
  customer: Customer;
};

export type Token = {
  token: string;
};
