CREATE DOMAIN public.email AS text
CHECK (VALUE ~ '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$');

CREATE DOMAIN public.phone AS text
CHECK (VALUE ~ '^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$');

CREATE TABLE contacts (
  id SERIAL PRIMARY KEY,
  phone public.phone,
  email public.email,
  telegram VARCHAR(50)
);

CREATE TABLE addresses (
  id SERIAL PRIMARY KEY,
  street VARCHAR(50) NOT NULL,
  city VARCHAR(50) NOT NULL,
  country VARCHAR(50) NOT NULL,
  postal_code VARCHAR(50) NOT NULL,
  house INT NOT NULL,
  entrance INT,
  appartment INT
);

CREATE TABLE suppliers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  contacts INT NOT NULL REFERENCES contacts(id),
  address INT NOT NULL REFERENCES addresses(id)
);

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  price NUMERIC(10, 2) NOT NULL,
  product_name VARCHAR(50) NOT NULL,
  description TEXT,
  suppliers_id INT NOT NULL REFERENCES suppliers(id),
  is_for_sale BOOLEAN NOT NULL
);

CREATE TYPE order_status AS ENUM (
  'CREATED',
  'CONFIRMED',
  'PAID',
  'SENT_TO_DELIVERY',
  'PICKED_UP',
  'CANCELED'
);

CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  contacts INT NOT NULL REFERENCES contacts(id),
  address INT NOT NULL REFERENCES addresses(id)
);

CREATE TABLE favorite_products (
  customer_id INT NOT NULL REFERENCES customers(id),
  product_id INT NOT NULL REFERENCES products(id)
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  status order_status NOT NULL,
  cancel_description TEXT,
  price NUMERIC(10, 2) NOT NULL,
  product_id INT NOT NULL REFERENCES products(id),
  creation_datetime TIMESTAMP NOT NULL,
  target_address INT NOT NULL REFERENCES addresses(id),
  customer_id INT NOT NULL REFERENCES customers(id)
);

CREATE TABLE product_images (
  id SERIAL PRIMARY KEY,
  product INT NOT NULL REFERENCES products(id),
  url TEXT NOT NULL
);

CREATE TABLE supplier_credentials (
  login VARCHAR(50) NOT NULL UNIQUE,
  password CHAR(64) NOT NULL,
  account_id INT NOT NULL REFERENCES suppliers(id)
);

CREATE TABLE customer_credentials (
  login VARCHAR(50) NOT NULL UNIQUE,
  password CHAR(64) NOT NULL,
  account_id INT NOT NULL REFERENCES customers(id)
);
