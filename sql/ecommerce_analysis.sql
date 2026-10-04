-- ============================================
-- E-COMMERCE CUSTOMER INTELLIGENCE PROJECT
-- SQL ANALYSIS
-- ============================================


-- 1. TOTAL REVENUE
-- Calculate total revenue from all positive sales

SELECT
    SUM(Quantity * Price) AS Total_Revenue
FROM online_retail;


-- 2. TOTAL ORDERS

SELECT
    COUNT(DISTINCT Invoice) AS Total_Orders
FROM online_retail;


-- 3. TOTAL CUSTOMERS

SELECT
    COUNT(DISTINCT Customer_ID) AS Total_Customers
FROM online_retail
WHERE Customer_ID IS NOT NULL;


-- 4. TOP 10 PRODUCTS BY REVENUE

SELECT
    Description,
    SUM(Quantity * Price) AS Revenue
FROM online_retail
WHERE Quantity > 0
GROUP BY Description
ORDER BY Revenue DESC
LIMIT 10;


-- 5. TOP 10 PRODUCTS BY QUANTITY SOLD

SELECT
    Description,
    SUM(Quantity) AS Total_Quantity_Sold
FROM online_retail
WHERE Quantity > 0
GROUP BY Description
ORDER BY Total_Quantity_Sold DESC
LIMIT 10;


-- 6. TOP 10 CUSTOMERS BY SPENDING

SELECT
    Customer_ID,
    SUM(Quantity * Price) AS Total_Spending
FROM online_retail
WHERE Quantity > 0
  AND Customer_ID IS NOT NULL
GROUP BY Customer_ID
ORDER BY Total_Spending DESC
LIMIT 10;


-- 7. CUSTOMER ORDER FREQUENCY

SELECT
    Customer_ID,
    COUNT(DISTINCT Invoice) AS Number_of_Orders
FROM online_retail
WHERE Customer_ID IS NOT NULL
  AND Quantity > 0
GROUP BY Customer_ID
ORDER BY Number_of_Orders DESC;


-- 8. MONTHLY REVENUE

SELECT
    YEAR(InvoiceDate) AS Year,
    MONTH(InvoiceDate) AS Month,
    SUM(Quantity * Price) AS Monthly_Revenue
FROM online_retail
WHERE Quantity > 0
GROUP BY
    YEAR(InvoiceDate),
    MONTH(InvoiceDate)
ORDER BY
    Year,
    Month;


-- 9. COUNTRY-WISE REVENUE

SELECT
    Country,
    SUM(Quantity * Price) AS Revenue
FROM online_retail
WHERE Quantity > 0
GROUP BY Country
ORDER BY Revenue DESC;


-- 10. AVERAGE ORDER VALUE

SELECT
    SUM(Quantity * Price) / COUNT(DISTINCT Invoice)
        AS Average_Order_Value
FROM online_retail
WHERE Quantity > 0;