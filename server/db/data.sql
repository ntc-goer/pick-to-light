-- Insert categories
INSERT INTO categories (id, category_name)
VALUES ('3c2bbe29-95fe-44ff-b728-e990e1d3558b',
        'Shirt');
INSERT INTO categories (id, category_name)
VALUES ('de955f42-7ac1-4f57-aaed-582a6d3ffe43',
        'Pant');

-- Insert products
INSERT INTO products (product_name, category_id, product_image, price, stock)
VALUES ('Casual Shirt',
        '3c2bbe29-95fe-44ff-b728-e990e1d3558b',
        'page/images/shirt1.jpg',
        29.99,
        100);

INSERT INTO products (product_name, category_id, product_image, price, stock)
VALUES ('Jeans Pant',
        'de955f42-7ac1-4f57-aaed-582a6d3ffe43',
        'page/images/pant1.jpg',
        49.99,
        80);

-- Insert carts
INSERT INTO carts (id, user_id)
VALUES ('7b1f8a38-7f8e-4e8c-9c6a-3b9f68e5b8a3',
        '7b1f8a38-7f8e-4e8c-9c6a-3b9f68e5b8a2');