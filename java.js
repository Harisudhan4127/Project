let cart = {};

function addToCart(flavor, price) {
  if (cart[flavor]) {
    cart[flavor].quantity += 1;
  } else {
    cart[flavor] = { price: price, quantity: 1 };
  }

  updateCart();
}

function updateCart() {
  const cartList = document.getElementById("cart-items");
  const totalPrice = document.getElementById("total-price");

  cartList.innerHTML = "";
  let total = 0;

  for (const flavor in cart) {
    const item = cart[flavor];
    const listItem = document.createElement("li");
    listItem.textContent = `${flavor} x${item.quantity} - ₹${item.price * item.quantity}`;
    cartList.appendChild(listItem);
    total += item.price * item.quantity;
  }

  totalPrice.textContent = total.toFixed(2);
}
