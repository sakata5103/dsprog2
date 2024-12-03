SELECT *
FROM minato_restaurant
WHERE block = '南麻布四丁目'
  AND business_type = '飲食店営業';

https://www.db-fiddle.com/f/nytA19vJHxwfHY1oXKU4wM/1



SELECT 
    block,
    COUNT(*) AS "other_business_count"
FROM 
    minato_restaurant
WHERE 
    business_type != '飲食店営業'
GROUP BY 
    block
ORDER BY 
    block ASC;

https://www.db-fiddle.com/f/nytA19vJHxwfHY1oXKU4wM/4





SELECT 
    DATE_PART('month', init_license_dt) AS "month",
    business_type,
    COUNT(*) AS store_count
FROM 
    minato_restaurant
WHERE 
    DATE_PART('year', init_license_dt) = 2022
GROUP BY 
    DATE_PART('month', init_license_dt),
    business_type
ORDER BY 
    "month",
    business_type,
    store_count ASC;


https://www.db-fiddle.com/f/nytA19vJHxwfHY1oXKU4wM/5