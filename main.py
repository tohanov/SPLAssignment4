from persistence import Hat, Order, Supplier, repo

import os

output = open("output.txt", "w")
input1 = open("config.txt")
input2 = open("orders.txt")

content = input1.read().split("\n")
content2 = input2.read().split("\n")

numbers = content[0].split(",")
numOfHats = int(numbers[0])
numOfSuppliers = int(numbers[1])
numOfOrders = len(content2)

for i in range(1,numOfHats + 1):
    
    info =  content[i].split(",")
    new_hat = Hat(int(info[0]), info[1], int(info[2]), int(info[3]))
    repo.hats.insert(new_hat)
    


for i in range(numOfHats + 1, len(content)):
    
    info =  content[i].split(",")
    new_supplier= Supplier(int(info[0]), info[1])
    repo.suppliers.insert(new_supplier)
    

        
hatsList = repo.getHats()
suppliersList = repo.getSuppliers()


print(hatsList)
print(suppliersList)

for i in range(numOfOrders):
    info = content2[i].split(",")
    
    resolvedInfo = repo.resolveOrder(info[1])
    new_order=Order(i+1, info[0], resolvedInfo[0])
    repo.orders.insert(new_order)
    
    to_write = info[1] + ","+ resolvedInfo[1] +"," + info[0] + "\n"
    print(to_write)
    output.write(to_write)
    

orderList = repo.getOrders()    
print(orderList)    