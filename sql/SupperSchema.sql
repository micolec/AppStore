
--table 1: buyer
CREATE TABLE IF NOT EXISTS buyer(
	username VARCHAR(32) PRIMARY KEY,
	password VARCHAR(32) NOT NULL,
	first_name VARCHAR(128) NOT NULL,
	last_name VARCHAR(128) NOT NULL,
	phone_number INTEGER UNIQUE NOT NULL CHECK (phone_number BETWEEN 80000000 AND 99999999), --users should have different phone numbers, check whether num is valid
	hall VARCHAR(32) NOT NULL CHECK (hall IN  ('Raffles','Temasek','Sheares', 'Kent Ridge','Eusoff','King Edward VII')), --check whether hall is within NUS
	wallet_balance MONEY NOT NULL CHECK (wallet_balance >= MONEY(5)), --pay for orders, must have at least balance of 5 dollars
	UNIQUE (username,hall)); 

--table 2: shop
CREATE TABLE IF NOT EXISTS shop(
	username VARCHAR(32) PRIMARY KEY,
	password VARCHAR(32) NOT NULL,
	shopname VARCHAR(128) UNIQUE NOT NULL, --different shops
	opening TIME(0),
	closing TIME(0),
	delivery_fee INTEGER NOT NULL, --every shop charges specific delivery fee
	UNIQUE (shopname,opening,closing) 
	);

--table 3: item - shop sells item
CREATE TABLE IF NOT EXISTS item(
	shopname VARCHAR(128) REFERENCES shop(shopname) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	item VARCHAR(32) NOT NULL,
	price MONEY NOT NULL,
	PRIMARY KEY (shopname, item), --different shops can have same item
	UNIQUE (shopname,item) 
);

--table 4: orderid - buyer creates new group order
CREATE TABLE IF NOT EXISTS orderid(
	group_order_id INTEGER PRIMARY KEY,
	creator VARCHAR(32),
	hall VARCHAR(32), --delivery destination
	shopname VARCHAR(128), --delivery source
	opening TIME(0),
	closing TIME(0),
	order_date DATE,
	order_by TIME(0)
	CHECK (order_by > opening AND order_by < closing), --check whether order is submitted during shop operating hours
	delivery_status VARCHAR(32) --buyers can query and sellers can update
	CHECK (delivery_status IN ('Order Open', 'Order Closed and Received', 'Vendor Preparing', 
							   'Food Dispatched', 'Food Delivered')),
	FOREIGN KEY(shopname, opening, closing) REFERENCES shop(shopname, opening, closing) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY (creator, hall) REFERENCES buyer(username, hall) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED, --ensures creator is from that hall
	UNIQUE(group_order_id, hall),
	UNIQUE(creator, hall, shopname, order_date, order_by) --only can haveone order from each shop at the same time and day to maximise the pool of buyers in an open order at anytime to save more delivery cost
	
);

--table 5: orders - buyer adds individual order to open group order
CREATE TABLE IF NOT EXISTS orders(
	username VARCHAR(32),	
	buyer_hall VARCHAR(32),
	group_order_id INTEGER,
	creator_hall VARCHAR(32) CHECK (creator_hall = buyer_hall), --destination is the same
	shopname VARCHAR(32),
	item VARCHAR(32),
	qty INTEGER NOT NULL CHECK(qty >= 1), --at least one item ordered
	paid VARCHAR(32) CHECK (paid IN ('Paid', 'Unpaid')),--individual order will only be submitted if the buyer has paid 
	FOREIGN KEY (username, buyer_hall) REFERENCES buyer(username, hall) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY (group_order_id, creator_hall) REFERENCES orderid(group_order_id, hall) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY (shopname,item) REFERENCES item(shopname,item) ON UPDATE CASCADE ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED, --shope indeed has the item
	PRIMARY KEY (username, group_order_id, item) --each buyer should order an item with varying quantity only once
);

