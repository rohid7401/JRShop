CREATE DATABASE JRDB2;
USE JRDB2;

-- 					Tables for the DB
-- Users Table
CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  password VARCHAR(255),
  shipping_address VARCHAR(255),
  purchase_history TEXT
);
-- Sellers Table
CREATE TABLE sellers (
  seller_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) UNIQUE,
  seller_description TEXT,
  contact_info TEXT
);
-- Products Table
CREATE TABLE products (
  product_id INT AUTO_INCREMENT PRIMARY KEY,
  seller_id INT,
  product_name VARCHAR(255),
  product_description TEXT,
  price DECIMAL(10,2),
  stock INT,
  image_url VARCHAR(255),
  FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);
-- Orders Table
CREATE TABLE orders (
  order_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  seller_id INT,
  order_date DATETIME,
  order_status ENUM('pending', 'shipped', 'delivered'),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);
-- Orders_items Table
CREATE TABLE order_items (
  order_id INT,
  product_id INT,
  quantity INT,
  PRIMARY KEY (order_id, product_id),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);
-- Product_review Table
CREATE TABLE product_reviews (
  review_id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT,
  user_id INT,
  rating INT,
  comment TEXT,
  FOREIGN KEY (product_id) REFERENCES products(product_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 					Stored procedures
-- User CRUD
-- Get all Users
DELIMITER //
CREATE PROCEDURE get_all_users()
BEGIN
  SELECT * FROM users;
END //
DELIMITER ;
-- Get a User
DELIMITER //
CREATE PROCEDURE get_user_by_id (
  IN p_user_id INT
)
BEGIN
  SELECT * FROM users
  WHERE user_id = p_user_id;
END //
DELIMITER ;
-- Create User
DELIMITER //
CREATE PROCEDURE insert_user (
  IN p_name VARCHAR(255),
  IN p_email VARCHAR(255),
  IN p_password VARCHAR(255),
  IN p_shipping_address VARCHAR(255)
)
BEGIN
  INSERT INTO users (name, email, password, shipping_address)
  VALUES (p_name, p_email, p_password, p_shipping_address);
END //
DELIMITER ;
-- Update User
DELIMITER //
CREATE PROCEDURE update_user (
  IN p_user_id INT,
  IN p_name VARCHAR(255),
  IN p_email VARCHAR(255),
  IN p_password VARCHAR(255),
  IN p_shipping_address VARCHAR(255)
)
BEGIN
  UPDATE users
  SET name = p_name, email = p_email, password = p_password, shipping_address = p_shipping_address
  WHERE user_id = p_user_id;
END //
DELIMITER ;
-- Delete User
DELIMITER //
CREATE PROCEDURE delete_user (
  IN p_user_id INT
)
BEGIN
  DELETE FROM users
  WHERE user_id = p_user_id;
END //
DELIMITER ;

-- Seller CRUD
-- Get all Sellers
DELIMITER //
CREATE PROCEDURE get_all_sellers()
BEGIN
  SELECT * FROM sellers;
END //
DELIMITER ;
-- Get a Seller
DELIMITER //
CREATE PROCEDURE get_seller_by_id (
  IN p_seller_id INT
)
BEGIN
  SELECT * FROM sellers
  WHERE seller_id = p_seller_id;
END //
DELIMITER ;
-- Create Seller
DELIMITER //
CREATE PROCEDURE insert_seller (
  IN p_name VARCHAR(255)
)
BEGIN
  INSERT INTO sellers (username)
  VALUES (p_name);
END //
DELIMITER ;
-- Update Seller
DELIMITER //
CREATE PROCEDURE update_seller (
  IN p_seller_id INT,
  IN p_name VARCHAR(255)
)
BEGIN
  UPDATE sellers
  SET name = p_name
  WHERE seller_id = p_seller_id;
END //
DELIMITER ;
-- Delete Seller
DELIMITER //
CREATE PROCEDURE delete_seller (
  IN p_seller_id INT
)
BEGIN
  DELETE FROM sellers
  WHERE seller_id = p_seller_id;
END //
DELIMITER ;

-- Products CRUD
-- Get all Products
DELIMITER //
CREATE PROCEDURE get_all_products()
BEGIN
  SELECT * FROM products;
END //
DELIMITER ;
-- Get a product
DELIMITER //
CREATE PROCEDURE get_product_by_id (
  IN p_product_id INT
)
BEGIN
  SELECT * FROM products
  WHERE product_id = p_product_id;
END //
DELIMITER ;
-- Create product
DELIMITER //
CREATE PROCEDURE insert_product (
  IN p_name VARCHAR(255),
  IN p_description TEXT,
  IN p_price DECIMAL(10,2),
  IN p_quantity INT,
  IN p_vendor_id INT
)
BEGIN
  INSERT INTO products (name, description, price, quantity, vendor_id)
  VALUES (p_name, p_description, p_price, p_quantity, p_vendor_id);
END //
DELIMITER ;
-- Update product
DELIMITER //
CREATE PROCEDURE update_product (
  IN p_product_id INT,
  IN p_name VARCHAR(255),
  IN p_description TEXT,
  IN p_price DECIMAL(10,2),
  IN p_quantity INT,
  IN p_vendor_id INT
)
BEGIN
  UPDATE products
  SET name = p_name, description = p_description, price = p_price, quantity = p_quantity, vendor_id = p_vendor_id
  WHERE product_id = p_product_id;
END //
DELIMITER ;
-- Delete product
DELIMITER //
CREATE PROCEDURE delete_product (
  IN p_product_id INT
)
BEGIN
  DELETE FROM products
  WHERE product_id = p_product_id;
END //
DELIMITER ;

-- Orders CRUD
-- Get all Orders
DELIMITER //
CREATE PROCEDURE get_all_orders()
BEGIN
  SELECT * FROM orders;
END //
DELIMITER ;
-- Get a Order
DELIMITER //
CREATE PROCEDURE get_order_by_id (
  IN p_order_id INT
)
BEGIN
  SELECT * FROM orders
  WHERE order_id = p_order_id;
END //
DELIMITER ;
-- Create Order
DELIMITER //
CREATE PROCEDURE insert_order (
  IN p_customer_name VARCHAR(255),
  IN p_customer_email VARCHAR(255),
  IN p_customer_phone VARCHAR(255),
  IN p_shipping_address TEXT,
  IN p_shipping_city VARCHAR(255),
  IN p_shipping_zipcode VARCHAR(255),
  IN p_shipping_country VARCHAR(255),
  IN p_total_price DECIMAL(10,2),
  IN p_status VARCHAR(50),
  IN p_vendor_id INT
)
BEGIN
  INSERT INTO orders (customer_name, customer_email, customer_phone, shipping_address, shipping_city, shipping_zipcode, shipping_country, total_price, status, vendor_id)
  VALUES (p_customer_name, p_customer_email, p_customer_phone, p_shipping_address, p_shipping_city, p_shipping_zipcode, p_shipping_country, p_total_price, p_status, p_vendor_id);
END //
DELIMITER ;
-- Update Order
DELIMITER //
CREATE PROCEDURE update_order (
  IN p_order_id INT,
  IN p_customer_name VARCHAR(255),
  IN p_customer_email VARCHAR(255),
  IN p_customer_phone VARCHAR(255),
  IN p_shipping_address TEXT,
  IN p_shipping_city VARCHAR(255),
  IN p_shipping_zipcode VARCHAR(255),
  IN p_shipping_country VARCHAR(255),
  IN p_total_price DECIMAL(10,2),
  IN p_status VARCHAR(50),
  IN p_vendor_id INT
)
BEGIN
  UPDATE orders
  SET customer_name = p_customer_name, customer_email = p_customer_email, customer_phone = p_customer_phone, shipping_address = p_shipping_address, shipping_city = p_shipping_city, shipping_zipcode = p_shipping_zipcode, shipping_country = p_shipping_country, total_price = p_total_price, status = p_status, vendor_id = p_vendor_id
  WHERE order_id = p_order_id;
END //
DELIMITER ;
-- Updating the order status
DELIMITER //
CREATE PROCEDURE update_order_status (
  IN p_order_id INT,
  IN p_order_status ENUM('pending', 'shipped', 'delivered')
)
BEGIN
  UPDATE orders
  SET order_status = p_order_status
  WHERE order_id = p_order_id;
END //
DELIMITER ;
-- Delete Order
DELIMITER //
CREATE PROCEDURE delete_order (
  IN p_order_id INT
)
BEGIN
  DELETE FROM orders
  WHERE order_id = p_order_id;
END //
DELIMITER ;

-- Orders_items CRUD
-- Get all Orders_items
DELIMITER //
CREATE PROCEDURE get_all_order_items()
BEGIN
  SELECT * FROM orders_items;
END //
DELIMITER ;
-- Get a Orders_item
DELIMITER //
CREATE PROCEDURE get_order_items_by_order_id (
  IN p_order_id INT
)
BEGIN
  SELECT * FROM orders_items
  WHERE order_id = p_order_id;
END //
DELIMITER ;
-- Create Orders_item
DELIMITER //
CREATE PROCEDURE insert_order_item (
  IN p_order_id INT,
  IN p_product_id INT,
  IN p_quantity INT,
  IN p_price DECIMAL(10,2)
)
BEGIN
  INSERT INTO orders_items (order_id, product_id, quantity, price)
  VALUES (p_order_id, p_product_id, p_quantity, p_price);
END //
DELIMITER ;
-- Update Orders_item
DELIMITER //
CREATE PROCEDURE update_order_item (
  IN p_order_item_id INT,
  IN p_order_id INT,
  IN p_product_id INT,
  IN p_quantity INT,
  IN p_price DECIMAL(10,2)
)
BEGIN
  UPDATE orders_items
  SET order_id = p_order_id, product_id = p_product_id, quantity = p_quantity, price = p_price
  WHERE order_item_id = p_order_item_id;
END //
DELIMITER ;
-- Delete Orders_item
DELIMITER //
CREATE PROCEDURE delete_order_item (
  IN p_order_item_id INT
)
BEGIN
  DELETE FROM orders_items
  WHERE order_item_id = p_order_item_id;
END //
DELIMITER ;

-- Product_reviews CRUD
-- Get all Product_reviews
DELIMITER //
CREATE PROCEDURE get_all_product_reviews()
BEGIN
  SELECT * FROM product_reviews;
END //
DELIMITER ;
-- Get a Product_review
DELIMITER //
CREATE PROCEDURE get_product_reviews_by_product_id (
  IN p_product_id INT
)
BEGIN
  SELECT * FROM product_reviews
  WHERE product_id = p_product_id;
END //
DELIMITER ;
-- Create Product_review
DELIMITER //
CREATE PROCEDURE insert_product_review (
  IN p_product_id INT,
  IN p_user_id INT,
  IN p_rating INT,
  IN p_review_text TEXT
)
BEGIN
  INSERT INTO product_reviews (product_id, user_id, rating, review_text)
  VALUES (p_product_id, p_user_id, p_rating, p_review_text);
END //
DELIMITER ;
-- Update Product_review
DELIMITER //
CREATE PROCEDURE update_product_review (
  IN p_product_review_id INT,
  IN p_product_id INT,
  IN p_user_id INT,
  IN p_rating INT,
  IN p_review_text TEXT
)
BEGIN
  UPDATE product_reviews
  SET product_id = p_product_id, user_id = p_user_id, rating = p_rating, review_text = p_review_text
  WHERE product_review_id = p_product_review_id;
END //
DELIMITER ;
-- Delete Product_review
DELIMITER //
CREATE PROCEDURE delete_product_review (
  IN p_product_review_id INT
)
BEGIN
  DELETE FROM product_reviews
  WHERE product_review_id = p_product_review_id;
END //
DELIMITER ;
-- Retrieving the average rating for a product:
DELIMITER //
CREATE PROCEDURE get_average_rating (
  IN p_product_id INT,
  OUT p_avg_rating FLOAT
)
BEGIN
  SELECT AVG(rating) INTO p_avg_rating
  FROM product_reviews
  WHERE product_id = p_product_id;
END //
DELIMITER ;

