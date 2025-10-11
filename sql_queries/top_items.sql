SELECT item, SUM(total_spent) AS revenue
FROM sales_data
GROUP BY item
ORDER BY revenue DESC
LIMIT 5;
