SELECT location, SUM(total_spent) AS total_revenue
FROM sales_data
GROUP BY location
ORDER BY total_revenue DESC;
