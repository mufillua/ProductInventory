# Product Inventory Project 
# This project is bassically designed to create a inventry for product using the mongodb database 
# mongodb is a no SQL and document based database which can be accessed in python using hte pymongo library 
# In the Inventory management system the user can store, update and delete the product from the inventory  

import tkinter as tk         
# Python library for creating GUI applications. It provides various widgets,
# such as buttons, labels, entry fields, and more, that you can use to build the graphical part of your application.     
from tkinter import ttk          
# This module provides classes to allow using Tk themed widget set.
import pymongo

# Python driver for MongoDB, a NoSQL database. It allows you to connect to a MongoDB server, interact with databases and collections, 
# and perform operations like inserting, updating, deleting, and querying documents in the database.

# Connect to the MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")     # connection string 
db = client["inventory"]                                       # creating the Database name inventory
products = db["products"]                                      # creating the document in the inventory database

# Function to add a product to the MongoDB collection
def add_product():                                             # function definition
    product_name = name_entry.get()                            # to fetch the name_entry input 
    quantity = int(quantity_entry.get())                       # to fetch the quantity_entry input and convert into int
    price = float(price_entry.get())                           # to fetch the price_entry input 

    product = {                                                # product dictionary for storing the dic in the database
        "name": product_name,
        "quantity": quantity,
        "price": price
    }

    products.insert_one(product)                               # insert command to insert the dictionary 

    refresh_product_list()                                     # function call to refresh the list shown
    clear_input_fields()                                       # to clear the text input 

# Function to update a product in the MongoDB collection
def update_product():                                          # function definition
    product_name = name_entry.get()
    new_quantity = int(quantity_entry.get())
    new_price = float(price_entry.get())

    product = products.find_one({"name": product_name})

    if product:
        products.update_one(                                   # to update the data from the document
            {"_id": product["_id"]},
            {"$set": {"quantity": new_quantity, "price": new_price}}
        )
        refresh_product_list()
        clear_input_fields()
    else:
        print("Product not found")                             # validation for entry product not match   

# Function to delete a product from the MongoDB collection
def delete_product():                                          # function definition
    product_name = name_entry.get()
    product = products.find_one({"name": product_name})

    if product:
        products.delete_one({"_id": product["_id"]})           # to delete the data from the document
        refresh_product_list()
        clear_input_fields()
    else:
        print("Product not found")                             # product not match validation

# Function to refresh the product list in the GUI
def refresh_product_list():                                    # function definition
    product_list.delete(0, "end")       # to clears the existing items in the product_list from the first item (index 0) to the end.
    for product in products.find():     # to show the from the product document
        product_name = product["name"]  # assigning the values again to show the updated data in the list
        quantity = product["quantity"]  
        price = product["price"]
        product_list.insert("end", f"{product_name} - Quantity: {quantity} - Price: {price}") # inserting the data to the list 

# Function to clear the input fields
def clear_input_fields():
    name_entry.delete(0, "end")         # to clear the input fields from 0 index to end of the text 
    quantity_entry.delete(0, "end")
    price_entry.delete(0, "end")

# Create the main window
root = tk.Tk()                                # to create the main window form    
root.title("Inventory Management System")     # to declare the title 
root.geometry("600x400")                      # overall size of the window

# Create and configure a style for widgets
style = ttk.Style()                           # for modern widgits               
style.configure('TLabel', font=('Helvetica', 12))         # label font size and font family
style.configure('TButton', font=('Helvetica', 12), padding=10) # button font size and family

# Create and configure input fields and labels
# Creates a new frame widget
input_frame = ttk.Frame(root)  #The ttk.Frame widget is a container that can hold other widgets, allowing you to group and organize elements within your GUI.     
input_frame.pack(pady=10)

name_label = ttk.Label(input_frame, text="Product Name:")   # to inset the label in the frame
name_label.grid(row=0, column=0, padx=10, pady=5)           # insert the styling padding x and y of 5 
name_entry = ttk.Entry(input_frame)                         # to insert the name input in the frame 
name_entry.grid(row=0, column=1, padx=10, pady=5)           # insert the styling padding x and y of 10 and 5

quantity_label = ttk.Label(input_frame, text="Quantity:")   # same process for other label and input 
quantity_label.grid(row=1, column=0, padx=10, pady=5)
quantity_entry = ttk.Entry(input_frame)
quantity_entry.grid(row=1, column=1, padx=10, pady=5)

price_label = ttk.Label(input_frame, text="Price:")
price_label.grid(row=2, column=0, padx=10, pady=5)
price_entry = ttk.Entry(input_frame)
price_entry.grid(row=2, column=1, padx=10, pady=5)

# Create and configure buttons for adding, updating, and deleting products
button_frame = ttk.Frame(root)
button_frame.pack()            # to wrape the elements in the frame    

# to insert the button and its name and onclick event using command attribute
add_button = ttk.Button(button_frame, text="Add Product", command=add_product)
add_button.grid(row=0, column=0, padx=10, pady=5)

# to insert the button and its name and onclick event using command attribute
update_button = ttk.Button(button_frame, text="Update Product", command=update_product)
update_button.grid(row=0, column=1, padx=10, pady=5)

# to insert the button and its name and onclick event using command attribute
delete_button = ttk.Button(button_frame, text="Delete Product", command=delete_product)
delete_button.grid(row=0, column=2, padx=10, pady=5)

# Create and configure a list to display products
product_list = tk.Listbox(root, font=('Helvetica', 12))
product_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Button to refresh the product list
# to insert the button and its name and onclick event using command attribute
refresh_button = ttk.Button(root, text="Refresh Product List", command=refresh_product_list)
refresh_button.pack()

# Start the GUI main loop
root.mainloop()            # to execute the window form GUI using the tkinter library
