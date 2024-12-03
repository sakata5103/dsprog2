SELECT 
    SUM(products.price * orders.quantity) AS total_sales
FROM 
    orders
JOIN 
    products ON orders.product_id = products.product_id
JOIN 
    customers ON orders.customer_id = customers.customer_id
WHERE 
    customers.gender = 'Female'
    AND customers.age >= 20
    AND orders.order_date BETWEEN '2024-01-01' AND '2024-03-31';

https://www.db-fiddle.com/f/r8kQZ3M1dENa8LqE8UGDfC/1




SELECT 
    product_name, 
    price
FROM 
    products
WHERE 
    category = 'Electronics'
    AND price = (
        SELECT 
            MAX(price)
        FROM 
            products
        WHERE 
            category = 'Electronics'
    );


https://www.db-fiddle.com/f/r8kQZ3M1dENa8LqE8UGDfC/2


SELECT 
    customers.customer_name, 
    SUM(products.price * orders.quantity) AS total_purchase
FROM 
    orders
JOIN 
    products 
ON 
    orders.product_id = products.product_id
JOIN 
    customers 
ON 
    orders.customer_id = customers.customer_id
WHERE 
    orders.order_date BETWEEN '2025-01-01' AND '2025-06-30'
GROUP BY 
    customers.customer_id, 
    customers.customer_name
ORDER BY 
    total_purchase DESC
LIMIT 3;

https://www.db-fiddle.com/f/r8kQZ3M1dENa8LqE8UGDfC/3