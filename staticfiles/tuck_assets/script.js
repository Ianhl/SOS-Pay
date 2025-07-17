// document.addEventListener('DOMContentLoaded', () => {
//     const cartIcon = document.querySelector('#cart-icon');
//     const cart = document.querySelector('.cart');
//     const closeCart = document.querySelector('#close-cart');

//     cartIcon.addEventListener('click', () => cart.classList.add('active'));
//     closeCart.addEventListener('click', () => cart.classList.remove('active'));

//     const initCartFunctions = () => {
//         document.querySelectorAll('.cart-remove').forEach((button) => {
//             button.addEventListener('click', removeCartItem);
//         });

//         document.querySelectorAll('.cart-quantity').forEach((input) => {
//             input.addEventListener('change', quantityChanged);
//         });

//         document.querySelectorAll('.add-cart').forEach((button) => {
//             button.addEventListener('click', addCartClicked);
//         });

//         document.querySelector('.btn-buy').addEventListener('click', buyButtonClicked);
//     };

//     initCartFunctions();

//     function buyButtonClicked() {
//         const cartContent = document.querySelector('.cart-content');
//         const cartItems = cartContent.querySelectorAll('.cart-box');
//         if (cartItems.length === 0) {
//             alert('Your cart is empty');
//         } else {
            
//             alert('Order successfully placed');
//             while (cartContent.firstChild) {
//                 cartContent.removeChild(cartContent.firstChild);
//             }
//             document.querySelector('.total-price').innerText = '0,00 €';
//         }
//     }

//     function removeCartItem(event) {
//         event.target.parentElement.remove();
//         updateTotalPrice();
//     }

//     function quantityChanged(event) {
//         const input = event.target;
//         if (isNaN(input.value) || input.value <= 0) {
//             input.value = 1;
//         }
//         updateTotalPrice();
//     }

//     let isAddingToCart = false;

//     function addCartClicked(event) {
//         isAddingToCart = true;
//         const button = event.target;
//         const shopProducts = button.parentElement;
//         const title = shopProducts.querySelector('.product-title').innerText;
//         const price = shopProducts.querySelector('.price').innerText;
//         const productImg = shopProducts.querySelector('.product-img').src;
//         // const productId = shopProducts.querySelector('.product-id').src;
//         addProductToCart(title, price, productImg);
//         updateTotalPrice();
//         setTimeout(() => (isAddingToCart = false), 100);
//     }

//     function addProductToCart(title, price, productImg) {
//         const cartItems = document.querySelector('.cart-content');
//         const cartItemNames = cartItems.querySelectorAll('.cart-product-title');

//         if (Array.from(cartItemNames).some((itemName) => itemName.innerText === title)) {
//             alert('This item is already in your cart');
//             return;
//         }

//         const cartShopBox = document.createElement('div');
//         cartShopBox.classList.add('cart-box');
//         cartShopBox.innerHTML = `
//             <img src="${productImg}" alt="${title}" class="cart-img">
//             <div class="detail-box">
//                 <div class="cart-product-title">${title}</div>
//                 <div class="cart-price">${price}</div>
//                 <input type="number" value="1" class="cart-quantity">
//             </div>
//             <i class="bx bxs-trash-alt cart-remove"></i>`;
//         cartItems.append(cartShopBox);

//         cartShopBox.querySelector('.cart-remove').addEventListener('click', removeCartItem);
//         cartShopBox.querySelector('.cart-quantity').addEventListener('change', quantityChanged);

//         cart.classList.add('active');
//     }

//     function updateTotalPrice() {
//         const cartContent = document.querySelector('.cart-content');
//         const cartBoxes = cartContent.querySelectorAll('.cart-box');
//         let total = 0;
//         cartBoxes.forEach((cartBox) => {
//             const priceElement = cartBox.querySelector('.cart-price');
//             const quantityElement = cartBox.querySelector('.cart-quantity');
//             let price = parseFloat(priceElement.innerText.replace('GHC', '').replace(',', '.'));
//             let quantity = parseInt(quantityElement.value);
//             total += price * quantity;
//         });

//         document.querySelector('.total-price').innerText = `GHC ${total.toFixed(2)}`;
//     }

//     document.addEventListener('click', (event) => {
//         if (!cart.contains(event.target) && !cartIcon.contains(event.target) && !isAddingToCart && cart.classList.contains('active')) {
//             cart.classList.remove('active');
//         }
//     });
// });

document.addEventListener('DOMContentLoaded', () => {
    const cartIcon = document.querySelector('#cart-icon');
    const cart = document.querySelector('.cart');
    const closeCart = document.querySelector('#close-cart');

    cartIcon.addEventListener('click', () => cart.classList.add('active'));
    closeCart.addEventListener('click', () => cart.classList.remove('active'));

    const initCartFunctions = () => {
        document.querySelectorAll('.cart-remove').forEach((button) => {
            button.addEventListener('click', removeCartItem);
        });

        document.querySelectorAll('.cart-quantity').forEach((input) => {
            input.addEventListener('change', quantityChanged);
        });

        document.querySelectorAll('.add-cart').forEach((button) => {
            button.addEventListener('click', addCartClicked);
        });

        document.querySelector('.btn-buy').addEventListener('click', buyButtonClicked);
    };

    initCartFunctions();

    function buyButtonClicked() {
        const cartContent = document.querySelector('.cart-content');
        const cartItems = cartContent.querySelectorAll('.cart-box');
        if (cartItems.length === 0) {
            alert('Your cart is empty');
            return;
        }

        let orderData = {
            items: []
        };

        cartItems.forEach((cartBox) => {
            const productIdElement = cartBox.querySelector('.cart-product-id');
            let productId = null;
            
            if (productIdElement) {
                productId = productIdElement.getAttribute('data-products-id');
            } else {
                console.error('Error: .cart-data-info element not found in cartBox');
            }
            
            const title = cartBox.querySelector('.cart-product-title').innerText;
            const price = cartBox.querySelector('.cart-price').innerText;
            const image = cartBox.querySelector('.cart-img').src;
            const quantity = cartBox.querySelector('.cart-quantity').value;


            orderData.items.push({
                product_id: productId,
                title: title,
                price: price,
                quantity: quantity,
                image: image,
            });
        });

        fetch('/tuckshop/save-order/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() // CSRF protection
            },
            body: JSON.stringify(orderData)
        })
        .then(response => {
            // Log the raw response to inspect it
            console.log('Response:', response);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
           
            return response.json();
        })

        .then(data => {
            console.log('Response data:', data);
            if (data.order_id) {
                window.location.href = `/tuckshop/order-confirmation/${data.order_id}/`;
            } else {
                alert('There was an error placing your order.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error placing your order.');
        });
    }

    function removeCartItem(event) {
        event.target.parentElement.remove();
        updateTotalPrice();
    }

    function quantityChanged(event) {
        const input = event.target;
        if (isNaN(input.value) || input.value <= 0) {
            input.value = 1;
        }
        updateTotalPrice();
    }

    let isAddingToCart = false;

    function addCartClicked(event) {
        isAddingToCart = true;
        const button = event.target;
        const shopProducts = button.parentElement;
        const title = shopProducts.querySelector('.product-title').innerText;
        const price = shopProducts.querySelector('.price').innerText;
        const productImg = shopProducts.querySelector('.product-img').src;
        const productIdElement = shopProducts.querySelector('.product-id');
        const productId = productIdElement.getAttribute('data-product-id');

        console.log(productId);

        addProductToCart(title, price, productImg, productId);
        updateTotalPrice();
        setTimeout(() => (isAddingToCart = false), 100);
    }
    ProductIds = []


    function addProductToCart(title, price, productImg, productId) {
        const cartItems = document.querySelector('.cart-content');  
        const productElements = document.querySelectorAll('.cart-product-id');
        const productIds = [];
        productElements.forEach(element => {
        const productId = element.getAttribute('data-products-id');
        if (productId) {
            productIds.push(productId);
        }
        });
        console.log(productIds);
        for (let i = 0; i < productIds.length; i++) {
            if (productIds[i] === productId) {
                alert('This item is already in your cart');
                return;
              };
          }

        const cartShopBox = document.createElement('div');
        cartShopBox.classList.add('cart-box');
        cartShopBox.innerHTML = `
            <img src="${productImg}" alt="${title}" class="cart-img">
            <div class="detail-box">
                <div class="cart-product-title">${title}</div>
                <div class="cart-price">${price}</div>
                <input type="number" value="1" class="cart-quantity">
                <div class="cart-product-id" data-products-id="${productId}"></div>
                <input type="hidden" class="cart-product-id" value="${productId}">
            </div>
            <i class="bx bxs-trash-alt cart-remove"></i>`;
        cartItems.append(cartShopBox);
        cartShopBox.querySelector('.cart-remove').addEventListener('click', removeCartItem);
        cartShopBox.querySelector('.cart-quantity').addEventListener('change', quantityChanged);

        cart.classList.add('active');
    }

    function updateTotalPrice() {
        const cartContent = document.querySelector('.cart-content');
        const cartBoxes = cartContent.querySelectorAll('.cart-box');
        let total = 0;
        cartBoxes.forEach((cartBox) => {
            const priceElement = cartBox.querySelector('.cart-price');
            const quantityElement = cartBox.querySelector('.cart-quantity');
            let price = parseFloat(priceElement.innerText.replace('GHC', '').replace(',', '.'));
            let quantity = parseInt(quantityElement.value);
            total += price * quantity;
        });

        document.querySelector('.total-price').innerText = `GHC ${total.toFixed(2)}`;
    }

    function getCSRFToken() {
        const tokenElement = document.querySelector('meta[name="csrf-token"]');
        if (tokenElement) {
            console.log('CSRF Token:', tokenElement.content); 
            return tokenElement.content;
            
        }
        return ''; // Return empty string or handle error
    }

    document.addEventListener('click', (event) => {
        if (!cart.contains(event.target) && !cartIcon.contains(event.target) && !isAddingToCart && cart.classList.contains('active')) {
            cart.classList.remove('active');
        }
    });
});
