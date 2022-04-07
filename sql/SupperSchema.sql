
--table 1: buyer
CREATE TABLE IF NOT EXISTS buyer(
	username VARCHAR(32) PRIMARY KEY,
	password VARCHAR(32) NOT NULL,
	first_name VARCHAR(128) NOT NULL,
	last_name VARCHAR(128) NOT NULL,
	phone_number INTEGER UNIQUE NOT NULL CHECK (phone_number BETWEEN 80000000 AND 99999999),
	hall VARCHAR(32) NOT NULL CHECK (hall IN  ('Raffles','Temasek','Sheares', 'Kent Ridge','Eusoff','King Edward VII')),
	wallet_balance MONEY NOT NULL CHECK (wallet_balance >= MONEY(5)),
	UNIQUE (username,hall)); 

--table 2: shop
CREATE TABLE IF NOT EXISTS shop(
	username VARCHAR(32) PRIMARY KEY,
	password VARCHAR(32) NOT NULL,
	shopname VARCHAR(128) UNIQUE NOT NULL,
	opening TIME(0),
	closing TIME(0),
	delivery_fee INTEGER NOT NULL,
	UNIQUE (shopname,opening,closing)
	);

--table 3: item
CREATE TABLE IF NOT EXISTS item(
	shopname VARCHAR(128) REFERENCES shop(shopname) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	item VARCHAR(32) NOT NULL,
	price MONEY NOT NULL,
	PRIMARY KEY (shopname, item),
	UNIQUE (shopname,item)
);

--table 4: orderid
CREATE TABLE IF NOT EXISTS orderid(
	group_order_id INTEGER PRIMARY KEY,
	creator VARCHAR(32),
	hall VARCHAR(32),
	shopname VARCHAR(128),
	opening TIME(0),
	closing TIME(0),
	order_date DATE,
	order_by TIME(0)
	CHECK (order_by > opening AND order_by < closing),
	delivery_status VARCHAR(32)
	CHECK (delivery_status IN ('Order Open', 'Order Closed and Received', 'Vendor Preparing', 
							   'Food Dispatched', 'Food Delivered')),
	FOREIGN KEY(shopname, opening, closing) REFERENCES shop(shopname, opening, closing) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY (creator, hall) REFERENCES buyer(username, hall) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	UNIQUE(group_order_id, hall),
	UNIQUE(creator, hall, shopname, order_date, order_by)
	
);

--table 5: orders
CREATE TABLE IF NOT EXISTS orders(
	username VARCHAR(32),	
	buyer_hall VARCHAR(32),
	group_order_id INTEGER,
	creator_hall VARCHAR(32) CHECK (creator_hall = buyer_hall),
	shopname VARCHAR(32),
	item VARCHAR(32),
	qty INTEGER NOT NULL CHECK(qty >= 1),
	paid VARCHAR(32) CHECK (paid IN ('Paid', 'Unpaid')),
	FOREIGN KEY (username, buyer_hall) REFERENCES buyer(username, hall) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY (group_order_id, creator_hall) REFERENCES orderid(group_order_id, hall) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY (shopname,item) REFERENCES item(shopname,item) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY (username, group_order_id, item)
);

