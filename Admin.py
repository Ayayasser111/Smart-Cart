admin_data = {'admin1': 'adminpass1', 'admin2': 'adminpass2'}  # Admin database
products_view = {}
price = {}


def view_products(x):
    print('Product:', x, '      Quantity:', products_view[x])


def view_prices(x):
    print('Product:', x, '      price:', price[x])

def admin_login():
    admin_name = input('Admin Name:')
    admin_pass = input('Admin Password:')
    if admin_name in admin_data and admin_data[admin_name] == admin_pass:
        print('Welcome Admin {}'.format(admin_name))
        return True
    else:
        print('Incorrect Admin Credentials. Exiting.')
        return False
def add_remove():
    while True:
        asking = input('Edit Products list? (y/n): ')
        if asking.lower() == 'y':
            ask = input('Choose if you want to add, remove: ')
            if ask.lower() == 'add':
                new_item = input('Enter the new Item: ')
                new_quantity = int(input('Enter the quantity: '))
                new_price = float(input('Enter the price: '))
                new_unit = input('Enter the unit: ')
                products_view[new_item] = new_quantity
                price[new_item] = f'{new_unit} {new_price}$'
                with open("inventory", "a") as inventory_file:
                    inventory_file.write(f"{new_item} {new_quantity} {new_unit} {new_price}\n")
                print(f"{new_item} added to the inventory. Exiting.")
                break
        elif asking.lower() == 'n':
            break
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")

    for product in products_view:
        view_products(product)

    return products_view

def edit_quantity():
    while True:
        ask_2 = input('Want to edit quantity?(y/n):')
        if ask_2 == 'y':
            sold = input('Enter the sold Item:')
            new_quantity = int(input('Enter the new quantity of sold item:'))
            products_view[sold] = new_quantity
        elif ask_2 == 'n':
            break
    for product in products_view:
        view_products(product)
    return products_view
def edit_price():
    while True:
        ask_1 = input('Want to edit price?(y/n):')
        if ask_1 == 'y':
            edit = input('Enter the Item you want to edit the price:')
            new_price = float(input('Enter the new price:'))
            price[edit] = f'{new_price}$'
        elif ask_1 == 'n':
            break
    for product in price:
        view_prices(product)
    return price
def save_to_inventory():
    with open("inventory", "r") as inventory_file:
        existing_content = inventory_file.readlines()
    for line in existing_content:
        parts = line.strip().split()
        if len(parts) >= 4:
            item = parts[0]
            quantity = int(parts[1])
            products_view[item] = quantity
    for item, quantity in products_view.items():
        updated_line = f"{item} {quantity} {price.get(item, 0)}"
        existing_content.append(updated_line)
    with open("inventory", "w") as inventory_file:
        inventory_file.write("\n".join(existing_content))
def admin_menu():
    if admin_login():
        add_remove()
        edit_price()
        edit_quantity()
        save_to_inventory()
        print("Changes saved to the inventory file.")
