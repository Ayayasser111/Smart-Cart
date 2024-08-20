user_database_file = "user_database.txt"
user_database = {}

def save_user_database():
    with open(user_database_file, 'w') as file:
        for username, password in user_database.items():
            file.write(f"{username}:{password}\n")

def load_user_database():
    try:
        with open(user_database_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                username, password = line.strip().split(':')
                user_database[username] = password
    except FileNotFoundError:
        pass
def read_inventory_file():
    file_name = "inventory"
    with open(file_name, 'r') as file:
        return file.read()

def write_to_inventory_file(lines):
    file_name = "inventory"
    with open(file_name, 'w') as file:
        file.write('\n'.join(lines))

def read_cart_file(username):
    file_name = f"{username}_cart.txt"
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return ''

def write_to_cart_file(username, item):
    file_name = f"{username}_cart.txt"
    with open(file_name, 'a') as file:
        file.write(item + '\n')

def replace_unit_with_inventory(cart_line, item_name=None):
    inventory_content = read_inventory_file()
    lines = inventory_content.split('\n')

    for inventory_line in lines:
        columns = inventory_line.split()
        if 'Quantity' in columns and 'Unit' in columns:
            quantity_index = columns.index('Quantity')
            unit_index = columns.index('Unit')

            if item_name and item_name.lower() in columns[0].lower():
                return cart_line.replace("1.0", columns[unit_index])
            elif "Quantity:" in cart_line and columns[0].lower() in cart_line.lower():
                return cart_line.replace("1.0", f"{columns[quantity_index + 1]} {columns[unit_index]}")

    return cart_line


def view_cart(username, item_name=None):
    cart_content = read_cart_file(username)
    if cart_content:
        print("\nItems in the Cart:")
        lines = cart_content.split('\n')
        if item_name:
            print(f"Items for {item_name}:")
            for line in lines:
                print(replace_unit_with_inventory(line, item_name))
            if not any(f"Quantity: {item_name}" in line for line in lines):
                print(f"{item_name} not found in the cart.")
        else:
            for line in lines:
                print(replace_unit_with_inventory(line))
    else:
        print("Cart is empty")
def remove_item_from_cart(username):
    cart_content = read_cart_file(username)
    if not cart_content:
        print("Cart is empty. No items to remove.")
        return

    item_to_remove = input("Enter the item you want to remove from the cart: ")
    lines = cart_content.split('\n')
    updated_lines = []

    for line in lines:
        if item_to_remove.lower() not in line.lower():
            updated_lines.append(line)
        else:

            try:
                quantity_str = line.split("Quantity:")[1].strip()
                quantity, unit = quantity_str.split()
                quantity = int(quantity)
            except ValueError:
                print(f"\nError parsing quantity for item '{item_to_remove}' in the cart. Please check the format.")
                return
            inventory_content = read_inventory_file()
            inventory_lines = inventory_content.split('\n')
            header = inventory_lines[0].split()
            item_index = header.index('Item')

            for i, inv_line in enumerate(inventory_lines[1:]):
                columns = inv_line.split()
                if item_to_remove.lower() in columns[item_index].lower():
                    try:
                        quantity_index = header.index('Quantity')
                        available_quantity_str = columns[quantity_index]
                        available_quantity_str_parts = available_quantity_str.split()

                        if len(available_quantity_str_parts) == 2:
                            available_quantity, unit = available_quantity_str_parts
                            available_quantity = int(available_quantity)
                        elif len(available_quantity_str_parts) == 1:
                            available_quantity = int(available_quantity_str_parts[0])
                            unit = ''
                        else:
                            raise ValueError("Invalid quantity format in the inventory.")
                        updated_quantity = available_quantity + quantity
                        columns[quantity_index] = f"{updated_quantity} {unit}"
                        inventory_lines[i + 1] = ' '.join(columns)
                        write_to_inventory_file(inventory_lines)
                        break
                    except ValueError as e:
                        print(f"process invalid ")
                        return

    updated_cart = '\n'.join(updated_lines)
    with open(f"{username}_cart.txt", 'w') as file:
        file.write(updated_cart)

    print(f"\nItem '{item_to_remove}' removed from the cart. Quantity returned to inventory.")

def search_item_in_inventory(item):
    inventory_content = read_inventory_file()
    lines = inventory_content.split('\n')
    header = lines[0].split()
    item_index = header.index('Item')
    for line in lines[1:]:
        columns = line.split()
        if item.lower() in columns[item_index].lower():
            return line
    return None
def add_to_cart_with_quantity(username, item, quantity):
    inventory_content = read_inventory_file()
    inventory_lines = inventory_content.split('\n')
    header = inventory_lines[0].split()
    item_index = header.index('Item')

    for i, line in enumerate(inventory_lines[1:]):
        columns = line.split()
        if item.lower() in columns[item_index].lower():
            try:
                available_quantity_str = columns[header.index('Quantity')]
                if len(available_quantity_str.split()) == 2:
                    available_quantity, unit = available_quantity_str.split()
                else:
                    available_quantity = available_quantity_str
                    unit = ''
                available_quantity = int(available_quantity)
            except ValueError:
                print(f"\nError parsing quantity for item '{item}' in the inventory. Please check the format.")
                print(f"Available Quantity String: {available_quantity_str}")
                return

            requested_quantity = int(quantity)

            if requested_quantity <= available_quantity:
                updated_quantity = available_quantity - requested_quantity
                columns[header.index('Quantity')] = f"{updated_quantity} {unit}"
                inventory_lines[i + 1] = ' '.join(columns)
                write_to_inventory_file(inventory_lines)
                cart_content = read_cart_file(username)
                lines = cart_content.split('\n')
                for cart_line in lines:
                    if item.lower() in cart_line.lower():
                        try:
                            existing_quantity_str = cart_line.split("Quantity:")[1].strip()
                            existing_quantity, unit = existing_quantity_str.split()
                            existing_quantity = int(existing_quantity)
                        except ValueError:
                            print(f"\nError parsing quantity for item '{item}' in the cart. Please check the format.")
                            return
                        total_quantity = existing_quantity + requested_quantity
                        updated_cart_line = f"{columns[0]} Quantity: {total_quantity} {columns[-1]}"
                        cart_content = cart_content.replace(cart_line, updated_cart_line)
                        with open(f"{username}_cart.txt", 'w') as file:
                            file.write(cart_content)
                        print(f"\nItem '{item}' quantity updated to {total_quantity} in the cart.")
                        return
                item_with_quantity = f"{columns[0]} Quantity: {requested_quantity} {columns[-1]}"
                write_to_cart_file(username, item_with_quantity)
                print(f"\nItem '{item}' added to the cart with quantity {requested_quantity}.")
                return
            else:
                print(f"\nInsufficient quantity in the inventory for item '{item}'. Available quantity: {available_quantity}.")
                return
    print(f"\nItem '{item}' not found in the inventory.")
def confirm_and_save_order(username):
    view_cart(username)
    total_price = calculate_cart_total(username)
    if total_price is not None:
        proceed_to_payment = input(f"Do you want to proceed with payment for a total price of ${total_price:.2f}? (yes/no): ").lower()
        if proceed_to_payment == 'yes':
            make_payment(username)
            with open(f"{username}_cart.txt", 'w') as cart_file:
                cart_file.write('')

            print("Order completed. Thank you!")
        else:
            print("Order not saved. Returning to the main menu.")
    else:
        print("Error calculating total price. Please check the format of the cart content.")
def calculate_cart_total(username):
    cart_content = read_cart_file(username)
    lines = cart_content.split('\n')
    total_price = 0.0
    for line in lines:
        if "Quantity:" in line:
            try:
                quantity_str = line.split("Quantity:")[1].strip()
                quantity, unit = quantity_str.split()
                quantity = int(quantity)
            except (ValueError, IndexError) as e:
                print(f"\n process invalid.")
                return None
            price_tokens = line.split()
            if len(price_tokens) > 0:
                try:
                    unit_price = float(price_tokens[-1])
                except ValueError:
                    print(f"\nprocess invalid.")
                    return None
                total_price += quantity * unit_price
            else:
                print(f"\nprocess invalid")
                return None

    return total_price
def make_payment(username):
    total_price = calculate_cart_total(username)
    if total_price is not None:
        original_total_price = total_price
        total_price = apply_promo_code(username, total_price)
        print("\nPayment Options:")
        print("1. Cash")
        print("2. Visa")
        payment_option = input("Choose a payment option (1 or 2): ")
        if payment_option == '1':
            feedback = input("Please provide feedback on a scale from 1 to 10 (10 being the best): ")
            try:
                feedback_score = int(feedback)
                if 1 <= feedback_score <= 10:
                    print(f"Thank you for your feedback! Score: {feedback_score}")
                else:
                    print("Invalid feedback score. Please provide a number between 1 and 10.")
            except ValueError:
                print("Invalid input. Please provide a number between 1 and 10.")

            print(f"Original Total Price: ${original_total_price:.2f}")
            print(f"Discounted Total Price: ${total_price:.2f}")
            print("Payment by cash. Thank you for your purchase!")
        elif payment_option == '2':
            visa_number = input("Enter the last three digits of your Visa number: ")
            print(f"Confirmed! Thank you for your purchase!")
            feedback = input("Please provide feedback on a scale from 1 to 10 (10 being the best): ")
            try:
                feedback_score = int(feedback)
                if 1 <= feedback_score <= 10:
                    print(f"Thank you for your feedback! Score: {feedback_score}")
                else:
                    print("Invalid feedback score. Please provide a number between 1 and 10.")
            except ValueError:
                print("Invalid input. Please provide a number between 1 and 10.")

            print(f"Original Total Price: ${original_total_price:.2f}")
            print(f"Discounted Total Price: ${total_price:.2f}")
        else:
            print("Invalid payment option. Payment not completed.")
    else:
        print("process invalid.")
def load_promo_codes():
    promo_codes_file = "promo_codes.txt"
    promo_codes = {}
    try:
        with open(promo_codes_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                code, discount = line.strip().split(':')
                promo_codes[code] = float(discount)
    except FileNotFoundError:
        pass
    return promo_codes
def apply_promo_code(username, total_price):
    promo_codes = load_promo_codes()
    promo_code = input("Do you have a promo code? (Type 'no' if not): ")

    if promo_code.lower() == 'no':
        return total_price
    while promo_code not in promo_codes:
        promo_code = input("Invalid promo code. Please enter a valid code (Type 'no' to skip): ")
        if promo_code.lower() == 'no':
            return total_price
    discount = promo_codes[promo_code]
    discounted_price = total_price - (total_price * discount)
    print(f"Promo code '{promo_code}' applied. Discount: {discount * 100}%")
    print(f"Discounted Total Price: ${discounted_price:.2f}")
    return discounted_price

def user(username):
    p = "Welcome to the Khair Supermarket "
    print(p.center(150))
    while True:
        print("Options:")
        print("1. View all items in the inventory")
        print("2. View all items in the cart & total price")
        print("3. Search for an item in the inventory")
        print("4. Add an item to the cart")
        print("5. Remove item from cart")
        print("6. Save and confirm order")
        print("7. Exit")

        choice = input("Enter your choice (1, 2, 3, 4, 5, 6, or 7): ")

        if choice == '1':
            print("\nItems in the Inventory:")
            print(read_inventory_file())
        elif choice == '2':
            view_cart(username)
            total_price = calculate_cart_total(username)
            if total_price is not None:
                print(f"\nTotal Price of items in the cart: ${total_price:.2f}")
        elif choice == '3':
            search_term = input("Enter the item you want to search for in the inventory: ")
            result = search_item_in_inventory(search_term)
            if result:
                print("\nItem Found in the Inventory:")
                print(result)
            else:
                print(f"\nItem '{search_term}' not found in the inventory.")
        elif choice == '4':
            search_term = input("Enter the item you want to add to the cart: ")
            result = search_item_in_inventory(search_term)
            if result:
                quantity = input("Enter the quantity for the item: ")
                result0 = search_term
                add_to_cart_with_quantity(username, result0, quantity)
            else:
                print(f"\nItem '{search_term}' not found in the inventory.")
        elif choice == '5':
            remove_item_from_cart(username)
        elif choice == '6':
            confirm_and_save_order(username)
        elif choice == '7':
            save_user_database()
            print("Exiting the Khair Supermarket. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, or 7.")
def clientregister():
    n = "User Registration"
    print(n.center(150))
    username = input("Enter your username: ")
    if username in user_database:
        print("Username already exists. Please choose another one.")
        return
    password = input("Enter your password: ")
    confirm_password = input("Confirm your password: ")
    while password != confirm_password:
        print("Passwords do not match. Please try again.")
        confirm_password = input("Confirm your password again: ")
    user_database[username] = password
    save_user_database()
    cart_file_name = f"{username}_cart.txt"
    with open(cart_file_name, 'w') as file:
        file.write('')
    print("Registration successful!")

