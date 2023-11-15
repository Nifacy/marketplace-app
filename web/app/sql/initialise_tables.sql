CREATE DOMAIN public.email AS text
CHECK (VALUE ~ '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$');

CREATE DOMAIN public.phone AS text
CHECK (VALUE ~ '^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$');

CREATE TABLE contacts (
  id SERIAL PRIMARY KEY,
  phone public.phone,
  email public.email,
  telegram VARCHAR(50)
); -- Убрал запятую

CREATE TABLE addresses (
  id SERIAL PRIMARY KEY,
  street VARCHAR(50) NOT NULL, -- Добавил NOT NULL
  city VARCHAR(50) NOT NULL, -- Добавил NOT NULL
  country VARCHAR(50) NOT NULL, -- Добавил NOT NULL
  postal_code VARCHAR(50) NOT NULL, -- Добавил NOT NULL
  house INT NOT NULL, -- Добавил NOT NULL
  entrance INT,
  appartment INT
);

CREATE TABLE suppliers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE, -- Добавил NOT NULL
  contacts INT NOT NULL REFERENCES contacts(id), -- Добавил NOT NULL
  address INT NOT NULL REFERENCES addresses(id) -- Добавил NOT NULL
);

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  price NUMERIC(10, 2) NOT NULL, -- Добавил NOT NULL
  product_name VARCHAR(50) NOT NULL, -- Добавил NOT NULL
  description TEXT,
  suppliers_id INT NOT NULL REFERENCES suppliers(id), -- Добавил NOT NULL
  is_for_sale BOOLEAN NOT NULL -- Добавил NOT NULL
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
  first_name VARCHAR(50) NOT NULL, -- Добавил NOT NULL
  last_name VARCHAR(50) NOT NULL, -- Добавил NOT NULL
  contacts INT NOT NULL REFERENCES contacts(id), -- Добавил NOT NULL
  address INT NOT NULL REFERENCES addresses(id) -- Добавил NOT NULL
);

CREATE TABLE favorite_products (
  customer_id INT NOT NULL REFERENCES customers(id), -- Добавил NOT NULL
  product_id INT NOT NULL REFERENCES products(id) -- Добавил NOT NULL
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  status order_status NOT NULL, -- Добавил NOT NULL
  cancel_description TEXT,
  price NUMERIC(10, 2) NOT NULL, -- Добавил NOT NULL
  product_id INT NOT NULL REFERENCES products(id), -- Добавил NOT NULL
  creation_datetime TIMESTAMP NOT NULL, -- Добавил NOT NULL
  target_address INT NOT NULL REFERENCES addresses(id), -- Добавил NOT NULL
  customer_id INT NOT NULL REFERENCES customers(id) -- Добавил NOT NULL
);

CREATE TABLE product_images (
  id SERIAL PRIMARY KEY,
  product INT NOT NULL REFERENCES products(id), -- Добавил NOT NULL
  url TEXT NOT NULL -- Добавил NOT NULL
);

CREATE TABLE supplier_credentials (
  login VARCHAR(50) NOT NULL UNIQUE, -- Добавил NOT NULL и UNIQUE
  password CHAR(64) NOT NULL, -- Добавил NOT NULL
  account_id INT NOT NULL REFERENCES suppliers(id) -- Добавил NOT NULL
);

CREATE TABLE customer_credentials (
  login VARCHAR(50) NOT NULL UNIQUE, -- Добавил NOT NULL и UNIQUE
  password CHAR(64) NOT NULL, -- Добавил NOT NULL
  account_id INT NOT NULL REFERENCES customers(id) -- Добавил NOT NULL
);
