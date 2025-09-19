import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time

# Updated categorized database
database = {
    "Veg": {
        "Coffee": 40,
        "Tea": 20,
        "Burger": 90,
        "Pizza": 120,
        "Fries": 50,
        "Ice Cream": 50,
        "Momos": 60,
        "Samosa": 15,
        "Sandwich": 40,
        "Vada Pav": 15,
        "Pav Bhaji": 50,
        "Chole Bhature": 60,
        "Paneer Roll": 55,
        "Maggi": 30,
        "Spring Roll": 50,
        "Garlic Bread": 45,
        "Dosa": 60,
        "Idli": 30
    },
    "Non-Veg": {
        "Chicken Burger": 110,
        "Chicken Pizza": 140,
        "Egg Roll": 40,
        "Chicken Momos": 70,
        "Fish Fingers": 90,
        "Chicken Nuggets": 80,
        "Grilled Chicken Sandwich": 75,
        "Butter Chicken Roll": 85
    },
    "Beverages": {
        "Cold Drink": 25,
        "Lassi": 30,
        "Buttermilk": 20,
        "Mojito": 40,
        "Milkshake": 50,
        "Iced Tea": 35,
        "Cold Coffee": 45
    }
}

cart = []

root = tk.Tk()
root.title("NETTECH CAFE AND SNACKS")
root.geometry("960x650")
root.configure(bg="#f4f6f7")

unit_price_var = tk.StringVar(value="\u20b90")
category_var = tk.StringVar(value="Veg")

# Helper to update item list based on category
def update_item_list(*args):
    items = list(database[category_var.get()].keys())
    item_combo.config(values=items)
    if items:
        item_combo.set(items[0])
        update_unit_price()

# Update unit price when item selected
def update_unit_price(event=None):
    item = item_combo.get()
    price = database[category_var.get()].get(item, 0)
    unit_price_var.set(f"\u20b9{price}")

# Add item to cart
def add_to_cart():
    category = category_var.get()
    item = item_combo.get()
    qty = int(qty_spinbox.get())
    price = database[category][item]
    total = price * qty
    cart.append((item, qty, price, total))
    cart_tree.insert('', 'end', values=(item, qty, f"\u20b9{price}", f"\u20b9{total}"))
    update_totals()

# Remove selected items
def remove_selected():
    for selected in cart_tree.selection():
        vals = cart_tree.item(selected, "values")
        cart.remove((vals[0], int(vals[1]), int(vals[2][1:]), int(vals[3][1:])))
        cart_tree.delete(selected)
    update_totals()

# Clear cart
def clear_cart():
    cart.clear()
    cart_tree.delete(*cart_tree.get_children())
    update_totals()

# Update billing totals
def update_totals():
    subtotal = sum(item[3] for item in cart)
    discount = round(subtotal * 0.10, 2)
    tax = round((subtotal - discount) * 0.05, 2)
    total = round(subtotal - discount + tax, 2)
    subtotal_var.set(f"\u20b9{subtotal}")
    discount_var.set(f"\u20b9{discount}")
    tax_var.set(f"\u20b9{tax}")
    total_var.set(f"\u20b9{total}")

# Print bill
def print_bill():
    if not cart:
        messagebox.showwarning("Empty", "Cart is empty!")
        return
    bill = "\nNETTECH CAFE AND SNACKS\n" + "="*30 + "\n"
    for item, qty, price, total in cart:
        bill += f"{item} x{qty} @\u20b9{price} = \u20b9{total}\n"
    bill += "="*30 + f"\nSubtotal: {subtotal_var.get()}\nDiscount: {discount_var.get()}\nTax: {tax_var.get()}\nTotal: {total_var.get()}"
    messagebox.showinfo("Your Bill", bill)

def update_time():
    clock_label.config(text="🕒 " + time.strftime("%H:%M:%S"))
    root.after(1000, update_time)

def exit_app():
    root.destroy()

# Header
tk.Label(root, text="☕ SANIKA CAFE AND SNACKS 🍔", font=("Times New Roman", 24, "bold"), fg="#ffffff", bg="#5dade2").pack(fill="x")

# Clock
clock_label = tk.Label(root, font=("Times New Roman", 12, "bold"), bg="#fef9e7")
clock_label.pack(fill="x")
update_time()

# Selection Frame
sel_frame = tk.LabelFrame(root, text="🍽 Select Category & Item", font=("Times New Roman", 12, "bold"), bg="#e8f8f5")
sel_frame.pack(fill="x", padx=20, pady=10)

ttk.Label(sel_frame, text="Category:", font=("Times New Roman", 11), background="#e8f8f5").grid(row=0, column=0, padx=5)
category_combo = ttk.Combobox(sel_frame, values=list(database.keys()), textvariable=category_var, state="readonly", font=("Times New Roman", 11))
category_combo.grid(row=0, column=1, padx=5)
category_combo.bind("<<ComboboxSelected>>", update_item_list)

item_combo = ttk.Combobox(sel_frame, font=("Times New Roman", 11), state="readonly")
item_combo.grid(row=0, column=2, padx=5)
item_combo.bind("<<ComboboxSelected>>", update_unit_price)

qty_spinbox = tk.Spinbox(sel_frame, from_=1, to=10, width=5, font=("Times New Roman", 11))
qty_spinbox.grid(row=0, column=3, padx=5)

tk.Label(sel_frame, textvariable=unit_price_var, font=("Times New Roman", 11, "bold"), bg="#e8f8f5").grid(row=0, column=4, padx=5)

ttk.Button(sel_frame, text="➕ Add to Cart", command=add_to_cart).grid(row=0, column=5, padx=5)
ttk.Button(sel_frame, text="🗑 Remove Selected", command=remove_selected).grid(row=0, column=6, padx=5)

# Cart Tree
cart_frame = tk.LabelFrame(root, text="🛒 Cart Items", font=("Times New Roman", 12, "bold"), bg="#f0f3f4")
cart_frame.pack(fill="both", expand=True, padx=20, pady=10)

cart_tree = ttk.Treeview(cart_frame, columns=("Item", "Qty", "Rate", "Total"), show="headings")
for col in ("Item", "Qty", "Rate", "Total"):
    cart_tree.heading(col, text=col)
    cart_tree.column(col, anchor="center")
cart_tree.pack(fill="both", expand=True)

# Billing section
totals_frame = tk.LabelFrame(root, text="💰 Billing", font=("Times New Roman", 12, "bold"), bg="#f4f6f7")
totals_frame.pack(fill="x", padx=20, pady=10)

subtotal_var = tk.StringVar(value="\u20b90")
discount_var = tk.StringVar(value="\u20b90")
tax_var = tk.StringVar(value="\u20b90")
total_var = tk.StringVar(value="\u20b90")

for i, (label, var) in enumerate([
    ("Subtotal", subtotal_var),
    ("Discount (10%)", discount_var),
    ("Tax (5%)", tax_var),
    ("Total", total_var)
]):
    tk.Label(totals_frame, text=label+":", font=("Times New Roman", 11), bg="#f4f6f7").grid(row=i, column=0, sticky="e", padx=10)
    tk.Label(totals_frame, textvariable=var, font=("Times New Roman", 11), fg="green", bg="#f4f6f7").grid(row=i, column=1, sticky="w", padx=5)

# Action Buttons
btn_frame = tk.Frame(root, bg="#f4f6f7")
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="🧹 Clear Cart", command=clear_cart).grid(row=0, column=0, padx=15)
ttk.Button(btn_frame, text="🖨 Print Bill", command=print_bill).grid(row=0, column=1, padx=15)
ttk.Button(btn_frame, text="🚪 Exit", command=exit_app).grid(row=0, column=2, padx=15)

# Initialize item list on load
update_item_list()

root.mainloop()