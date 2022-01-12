#file: persistence.py
import sqlite3
import atexit
import os



# Data Transfer Objects (DTO) 
class Hat:
	def __init__(self, id, topping, supplier, quantity):
		self.id = id
		self.topping = topping
		self.supplier = supplier
		self.quantity = quantity



class Supplier:
	def  __init__(self, id, name):
		self.id = id
		self.name = name



class Order:
	def __init__(self, id, location, hat):
		self.id = id
		self.location = location
		self.hat = hat
		


# Data Access Objects (DAO)
class _Hats:
	def __init__(self, conn):
		self._conn = conn
		

	def insert(self, hat):
		self._conn.execute("INSERT INTO hats VALUES(?,?,?,?)", [hat.id, hat.topping, hat.supplier, hat.quantity])
		

	def delete(self, hat_id):
		self._conn.execute("DELETE FROM hats WHERE id = ?",[hat_id])
		

	def find_by_id(self, hat_id):
		cursor = self._conn.cursor()
		cursor.execute("SELECT id, topping, supplier, quantity FROM hats WHERE id = ?", [hat_id])
		return Hat(*cursor.fetchone())
	

	def find_by_topping(self, topping):
		cursor = self._conn.cursor()
		cursor.execute("SELECT id, supplier FROM hats WHERE topping = ?", [topping])
		
		infoList = cursor.fetchall()
		
		if len(infoList) != 0:
			chosen_id = infoList[0][0]
			current_supplier_id = infoList[0][1]
			
			#for info in infoList:
			for i in range(len(infoList)):
				if infoList[i][1] < current_supplier_id:
					chosen_id = infoList[i][0]
					current_supplier_id = infoList[i][1]
		
		return chosen_id				 


	def decreaseQuantity(self, hat_id):
		currentQuantity = _Hats.find_by_id(self, hat_id).quantity - 1
			   
		self._conn.execute("UPDATE hats SET quantity = ? WHERE id = ?",[currentQuantity, hat_id])
		
		if(currentQuantity == 0):
			_Hats.delete(self, hat_id)
	


class _Suppliers:
	def __init__(self, conn):
		self._conn = conn
		

	def insert(self, supplier):
		self._conn.execute("INSERT INTO suppliers VALUES(?,?)", [supplier.id, supplier.name])
		

	def find(self, supplier_id):
		cursor = self._conn.cursor()
		cursor.execute("SELECT id,name FROM suppliers WHERE id = ?", [supplier_id])
		return Supplier(*cursor.fetchone())
	


class _Orders:
	def __init__(self, conn):
		self._conn = conn


	def insert(self, order):
		self._conn.execute("INSERT INTO orders VALUES(?,?,?)", [order.id, order.location, order.hat])


	def find(self, order_id):
		cursor = self._conn.cursor()
		cursor.execute("SELECT id, location, hats FROM orders WHERE id = ?", [order_id])
		return Hat(*cursor.fetchone())



class Repository(object):
	def __init__(self, path):
		self._conn = sqlite3.connect( path )
		self._create_tables()
		atexit.register(self._close)

		self.hats = _Hats(self._conn)
		self.suppliers = _Suppliers(self._conn)
		self.orders = _Orders(self._conn)


	def _close(self):
		self._conn.commit()
		self._conn.close()
			

	def _create_tables(self):
		cursor = self._conn.cursor()
		cursor.execute("""CREATE TABLE suppliers (
			id INTEGER PRIMARY KEY, 
			name TEXT NOT NULL
		)""");
		cursor.execute("""CREATE TABLE hats (
			id INTEGER PRIMARY KEY, 
			topping TEXT NOT NULL, 
			supplier INTEGER NOT NULL, 
			quantity INTEGER NOT NULL, 
			FOREIGN KEY(supplier) REFERENCES suppliers(id)
		)""");
		cursor.execute("""CREATE TABLE orders (
			id INTEGER PRIMARY KEY, 
			location TEXT NOT NULL, hat INTEGER NOT NULL, 
			FOREIGN KEY(hat) REFERENCES hats(id)
		)""");


	def resolveOrder(self, topping):
		chosen_hat_id = self.hats.find_by_topping(topping)

		chosen_hat = self.hats.find_by_id(chosen_hat_id)
		chosen_supplier = self.suppliers.find(chosen_hat.supplier)

		self.hats.decreaseQuantity(chosen_hat_id)

		return (chosen_hat_id, chosen_supplier.name)
		
	
	def getHats(self):
		cursor = self._conn.cursor()
		cursor.execute("SELECT * FROM hats")
		
		return cursor.fetchall() 


	def getSuppliers(self):
		cursor = self._conn.cursor()
		cursor.execute("SELECT * FROM suppliers")
		
		return cursor.fetchall() 
	

	def getOrders(self):
		cursor = self._conn.cursor()
		cursor.execute("SELECT * FROM orders")
		
		return cursor.fetchall()	
