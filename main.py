#!/usr/bin/python3
from persistence import Hat, Order, Supplier, Repository
import sys
import os


input1 = open(sys.argv[1]) # config file path
input2 = open(sys.argv[2]) # orders file path
output = open(sys.argv[3], "w") # output file path
repo = Repository(sys.argv[4]) # database DAO object


content = input1.read().split("\n")
content2 = input2.read().split("\n")

numbers = content[0].split(",")
numOfHats = int(numbers[0])
numOfSuppliers = int(numbers[1])
numOfOrders = len(content2)

# parse hats
for i in range(1,numOfHats + 1):
    info =  content[i].split(",")
    new_hat = Hat(int(info[0]), info[1], int(info[2]), int(info[3]))
    repo.hats.insert(new_hat)

# parse suppliers
for i in range(numOfHats + 1, len(content)):
    info =  content[i].split(",")
    new_supplier= Supplier(int(info[0]), info[1])
    repo.suppliers.insert(new_supplier)

for i in range(numOfOrders):
    info = content2[i].split(",")
    
    resolvedInfo = repo.resolveOrder(info[1])
    new_order=Order(i+1, info[0], resolvedInfo[0])
    repo.orders.insert(new_order)
    
    to_write = info[1] + ","+ resolvedInfo[1] +"," + info[0] + "\n"
    output.write(to_write)