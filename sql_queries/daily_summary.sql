SELECT
    TO_TIMESTAMP(transaction_date / 1000)::DATE AS day,
    COUNT(*) AS total_transactions,
    SUM(total_spent) AS daily_revenue
FROM sales_data
GROUP BY day
ORDER BY day;
