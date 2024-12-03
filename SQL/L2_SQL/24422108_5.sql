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