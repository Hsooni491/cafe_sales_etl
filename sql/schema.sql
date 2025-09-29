-- Active: 1757794289303@@localhost@5432@cafe_sales
CREATE TABLE cafe_sales (
	transaction_id TEXT PRIMARY KEY,
	item TEXT,
	quantity INTEGER,
	price_per_unit FLOAT,
	payment_method TEXT,
	location TEXT,
	transaction_date DATE,
	day_of_week TEXT
);