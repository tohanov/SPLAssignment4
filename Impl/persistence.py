#file: persistence.py

import sqlite3
import os
import importlib
import atexit
 
# Data Transfer Objects (DTO) 
class _Hat:
    def __init__(self, id, topping, supplier, quantity):
        self.id = id
        self.topping = topping
        self.supplier = supplier
        self.quantity = quantity
                   
class _Supplier:
    def  ___init__(self, id, name):
        self.id = id
        self.name = name
    
class _Order:
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
        
    def find(self, hat_id):
        cursor = self._conn.cursor()
        cursor.execute("SELECT id, topping, supplier, quantity FROM hats WHERE id = ?", [hat_id])
        return _Hat(*cursor.fetchone())
    
    def decreaseQuantity(self, hat_id):
        currentQuantity = _Hats.find(self, hat_id).quantity
        self._conn.execute("UPDATE hats SET quantity = (?)) WHERE id = (?)",[currentQuantity, hat_id])
    
class _Suppliers:
    def __init__(self, conn):
        self._conn = conn
        
    def insert(self, supplier):
        self._conn.execute("INSERT INTO suppliers VALUES(?,?)", [supplier.id, supplier.name])
        
    def find(self, supplier_id):
        cursor = self._conn.cursor()
        cursor.execute("SELECT id,name FROM suppliers WHERE id = ?", [supplier_id])
        return _Supplier(*cursor.fetchone())
    
class _Orders:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, order):
        self._conn.execute("INSERT INTO orders VALUES(?,?,?)", [order.id, order.location, order.hat])

    def find(self, order_id):
        cursor = self._conn.cursor()
        cursor.execute("SELECT id, location, hats FROM orders WHERE id = ?", [order_id])
        return _Hat(*cursor.fetchone())
               
class _Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('pizza_hat.db')
        self.hats = _Hats(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.orders = _Orders(self._conn)
 
    def _close(self):
        self._conn.close()
            
    def _create_tables(self):
        self._conn.executescript("""
            CREATE TABLE hats (
                id          INT             PRIMARY KEY,
                topping     TEXT            NOT NULL
                FOREIGN KEY(SUPPLIER)       REFERENCES suppliers(id)
                quantity    INTEGER         NOT NULL
            );
    
            CREATE TABLE suppliers (
                id       INT     PRIMARY KEY,
                name     TEXT    NOT NULL
            );
            
            CREATE TABLE orders (
                id  INTEGER PRIMARY KEY
                location    TEXT    NOT NULL
                FOREIGN KEY(hat) REFERENCES hats(id)        
            );
    
        """)
    
repo = _Repository()
atexit.register(repo._close)
