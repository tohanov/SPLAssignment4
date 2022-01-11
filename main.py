from persistence import Hat, Order, Supplier, repo

import os

output = open("output.txt", "w")
input = open("config.txt")
content = input.read().split("\n")

numbers = content[0].split(",")
numOfHats = int(numbers[0])
numOfSuppliers = int(numbers[1])

for i in range(1,numOfHats + 1):
    print(i)
    info =  content[i].split(",")
    new_hat = Hat(int(info[0]), info[1], int(info[2]), int(info[3]))
    repo.hats.insert(new_hat)
    


for i in range(numOfHats + 1, len(content)):
    print(i)
    info =  content[i].split(",")
    new_supplier= Supplier(int(info[0]), info[1])
    repo.suppliers.insert(new_supplier)
    
        
hatsList = repo.getHats()
suppliersList = repo.getSuppliers()


print(hatsList)
print(suppliersList)

    