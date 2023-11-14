-- Создание доменов, хз, нада ли эта хуйня, вообще, ааааааааааааааа
CREATE DOMAIN public.email AS text
CHECK (VALUE ~ '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$');

CREATE DOMAIN public.phone AS text
CHECK (VALUE ~ '^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$');

-- Создание таблиц
CREATE TABLE contacts (
  id SERIAL PRIMARY KEY,
  phone public.phone,
  email public.email,
  telegram VARCHAR(50),
  whatsapp VARCHAR(50)
);

CREATE TABLE addresses (
  id SERIAL PRIMARY KEY,
  street VARCHAR(50),
  city VARCHAR(50),
  country VARCHAR(50),
  postal_code VARCHAR(50),
  house INT,
  entrance INT,
  appartment INT
);

CREATE TABLE suppliers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50),
  contacts INT REFERENCES contacts(id),
  address INT REFERENCES addresses(id)
);

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  price NUMERIC(10, 2),
  product_name VARCHAR(50),
  description TEXT,
  suppliers_id INT REFERENCES suppliers(id),
  is_for_sale BOOLEAN
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
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  contacts INT REFERENCES contacts(id),
  address INT REFERENCES addresses(id)
);

CREATE TABLE favorite_products (
  customer_id INT REFERENCES customers(id),
  product_id INT REFERENCES products(id)
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  status order_status,
  cancel_description TEXT,
  price NUMERIC(10, 2),
  product_id INT REFERENCES products(id),
  creation_datetime TIMESTAMP,
  target_address INT REFERENCES addresses(id),
  customer_id INT REFERENCES customers(id)
);

CREATE TABLE product_images (
  id SERIAL PRIMARY KEY,
  product INT REFERENCES products(id),
  url TEXT
);

CREATE TABLE supplier_credentials (
  login VARCHAR(50),
  password CHAR(64),
  account_id INT REFERENCES suppliers(id)
);

CREATE TABLE customer_credentials (
  login VARCHAR(50),
  password CHAR(64),
  account_id INT REFERENCES customers(id)
);
