<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sanika Cafe and Snacks</title>
  <style>
    body {
      font-family: "Segoe UI", sans-serif;
      background-color: #f4f6f7;
      margin: 0;
      padding: 20px;
    }
    h1 {
      background-color: #5dade2;
      color: white;
      padding: 10px;
      text-align: center;
    }
    .container {
      max-width: 1000px;
      margin: auto;
    }
    label {
      margin-right: 10px;
    }
    select, input {
      padding: 5px;
      margin-right: 15px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 15px;
    }
    th, td {
      padding: 10px;
      border: 1px solid #bbb;
      text-align: center;
    }
    .totals {
      margin-top: 20px;
    }
    .totals div {
      margin: 5px 0;
    }
    .btn {
      margin-top: 15px;
      padding: 10px 20px;
      background-color: #3498db;
      color: white;
      border: none;
      cursor: pointer;
    }
    .btn:hover {
      background-color: #2980b9;
    }
  </style>
</head>
<body>
  <h1>☕ SANIKA CAFE AND SNACKS 🍔</h1>
  <div class="container">
    <div>
      <label>Category:</label>
      <select id="category" onchange="updateItems()">
        <option value="Veg">Veg</option>
        <option value="Non-Veg">Non-Veg</option>
        <option value="Beverages">Beverages</option>
      </select>

      <label>Item:</label>
      <select id="item" onchange="updatePrice()"></select>

      <label>Qty:</label>
      <input type="number" id="qty" min="1" value="1">

      <label>Price:</label>
      <span id="price">₹0</span>

      <button class="btn" onclick="addToCart()">➕ Add to Cart</button>
    </div>

    <table id="cart">
      <thead>
        <tr>
          <th>Item</th>
          <th>Qty</th>
          <th>Rate</th>
          <th>Total</th>
          <th>Remove</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>

    <div class="totals">
      <div>Subtotal: <span id="subtotal">₹0</span></div>
      <div>Discount (10%): <span id="discount">₹0</span></div>
      <div>Tax (5%): <span id="tax">₹0</span></div>
      <div><strong>Total: <span id="total">₹0</span></strong></div>
    </div>

    <button class="btn" onclick="printBill()">🖨 Print Bill</button>
  </div>

  <script>
    const database = {
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
    };

    let cart = [];

    function updateItems() {
      const category = document.getElementById("category").value;
      const items = Object.keys(database[category]);
      const itemSelect = document.getElementById("item");
      itemSelect.innerHTML = "";
      items.forEach(item => {
        const opt = document.createElement("option");
        opt.value = item;
        opt.textContent = item;
        itemSelect.appendChild(opt);
      });
      updatePrice();
    }

    function updatePrice() {
      const category = document.getElementById("category").value;
      const item = document.getElementById("item").value;
      const price = database[category][item];
      document.getElementById("price").textContent = "₹" + price;
    }

    function addToCart() {
      const category = document.getElementById("category").value;
      const item = document.getElementById("item").value;
      const qty = parseInt(document.getElementById("qty").value);
      const price = database[category][item];
      const total = qty * price;

      cart.push({ item, qty, price, total });
      renderCart();
    }

    function renderCart() {
      const tbody = document.querySelector("#cart tbody");
      tbody.innerHTML = "";

      let subtotal = 0;

      cart.forEach((entry, index) => {
        subtotal += entry.total;
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${entry.item}</td>
          <td>${entry.qty}</td>
          <td>₹${entry.price}</td>
          <td>₹${entry.total}</td>
          <td><button onclick="removeItem(${index})">❌</button></td>
        `;
        tbody.appendChild(row);
      });

      const discount = +(subtotal * 0.10).toFixed(2);
      const tax = +((subtotal - discount) * 0.05).toFixed(2);
      const total = +(subtotal - discount + tax).toFixed(2);

      document.getElementById("subtotal").textContent = "₹" + subtotal;
      document.getElementById("discount").textContent = "₹" + discount;
      document.getElementById("tax").textContent = "₹" + tax;
      document.getElementById("total").textContent = "₹" + total;
    }

    function removeItem(index) {
      cart.splice(index, 1);
      renderCart();
    }

    function printBill() {
      if (cart.length === 0) {
        alert("Cart is empty!");
        return;
      }

      let bill = "SANIKA CAFE AND SNACKS\n===========================\n";
      cart.forEach(item => {
        bill += `${item.item} x${item.qty} @ ₹${item.price} = ₹${item.total}\n`;
      });
      bill += "===========================\n";
      bill += `Subtotal: ${document.getElementById("subtotal").textContent}\n`;
      bill += `Discount: ${document.getElementById("discount").textContent}\n`;
      bill += `Tax: ${document.getElementById("tax").textContent}\n`;
      bill += `Total: ${document.getElementById("total").textContent}\n`;
      alert(bill);
    }

    // Load initial items
    updateItems();
  </script>
</body>
</html>

