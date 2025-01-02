import xmlrpc.client
import streamlit as st
from PIL import Image

# Menu data
menu_items = [
    {'name': 'Americano', 'price': 1500, 'image': './images/americano.jpg'},
    {'name': 'Latte', 'price': 3000, 'image': './images/latte.jpg'},
    {'name': 'Green Tea Latte', 'price': 4000, 'image': './images/green_tea_latte.jpg'},
    {'name': 'Frappuccino', 'price': 5000, 'image': './images/frappuccino.jpg'}
]

# Initialize shopping cart
if 'cart' not in st.session_state:
    st.session_state.cart = {item['name']: {'quantity': 0, 'subtotal': 0} for item in menu_items}

# Function to update cart
def update_cart(item_name, price):
    st.session_state.cart[item_name]['quantity'] += 1
    st.session_state.cart[item_name]['subtotal'] += price
    st.success(f'{item_name} added to the cart!')

# Function to reset the cart
def reset_cart():
    st.session_state.cart = {item['name']: {'quantity': 0, 'subtotal': 0} for item in menu_items}

# Layout: Menu and Shopping Cart
col_menu, col_cart = st.columns([3, 1], gap='large')

# Menu area
with col_menu:
    st.title('OSBucks Kiosk')
    for item in menu_items:
        col1, col2 = st.columns([1, 2])
        
        # Display image
        with col1:
            img = Image.open(item['image'])
            st.image(img, use_container_width=True)
        
        # Display item name, price, and add-to-cart button
        with col2:
            st.subheader(item['name'])
            st.write(f'Price: ₩{item["price"]}')
            if st.button(f'Add {item["name"]}', key=item['name']):
                update_cart(item['name'], item['price'])

# Shopping Cart area
with col_cart:
    st.title('Order')
    total_price = 0
    has_items = False
    order_list = []

    for item_name, details in st.session_state.cart.items():
        if details['quantity'] > 0:
            has_items = True
            st.write(f'{item_name} x {details["quantity"]} = ₩{details["subtotal"]}')
            total_price += details['subtotal']
            order_list.append({'item': item_name, 'quantity': details['quantity']})
    
    if has_items:
        st.write('---')
        st.subheader(f'Total: ₩{total_price}')
        if st.button('Order'):
            try:
                # Send orders to the server
                server = xmlrpc.client.ServerProxy("http://localhost:9000/")
                server.process_order(order_list)
                st.success("Order placed successfully!")
                reset_cart()  # Reset the cart after the order is placed
            except Exception as e:
                st.error(f"Failed to place order: {e}")
    else:
        st.write('Your cart is empty.')
