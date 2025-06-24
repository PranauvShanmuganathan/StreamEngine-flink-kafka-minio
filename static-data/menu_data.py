import csv
import random
from faker import Faker
import os

# Initialize Faker for US locale to get prices in dollars
fake = Faker('en_US')

# --- Define the master list of menu items for each category ---
# Total items will be around 65, which is within the 50-75 range per restaurant.
food_items = {
    "Breakfast": [
        "Classic Pancakes", "Belgian Waffles", "Scrambled Eggs Platter",
        "Western Omelette", "Bacon and Eggs Special", "Avocado Toast",
        "French Toast Delight", "Bagel with Cream Cheese", "Hearty Oatmeal Bowl",
        "Sunrise Breakfast Burrito", "Eggs Benedict", "Fruit & Yogurt Parfait"
    ],
    "Lunch": [
        "Classic Club Sandwich", "Grilled Chicken Caesar Salad", "Creamy Tomato Soup",
        "Gourmet Angus Burger", "Crispy Chicken Tenders", "Margherita Pizza",
        "Spicy Chicken Wrap", "Steak and Cheese Sub", "Quinoa Salad Bowl",
        "Fish Tacos", "BLT Sandwich", "Soup of the Day"
    ],
    "Dinner": [
        "New York Strip Steak", "Grilled Atlantic Salmon", "Herb-Roasted Chicken",
        "Pasta Carbonara", "Homemade Beef Lasagna", "Shepherd's Pie",
        "Fettuccine Alfredo", "BBQ Ribs", "Vegetable Stir-fry",
        "Pan-Seared Scallops", "Mushroom Risotto", "Lobster Mac & Cheese"
    ],
    "Snacks": [
        "Crispy Mozzarella Sticks", "Buffalo Chicken Wings", "Loaded Nachos Supreme",
        "Golden Onion Rings", "Vegetable Spring Rolls", "Garlic Bread with Cheese",
        "Spicy Jalapeño Poppers", "Fried Calamari", "Hummus with Pita Bread"
    ],
    "Indian": [
        "Vegetable Samosa", "Chicken Tikka Masala", "Palak Paneer", "Aloo Gobi",
        "Chana Masala", "Butter Chicken", "Garlic Naan", "Chicken Biryani",
        "Tandoori Chicken", "Dal Makhani", "Paneer Butter Masala", "Rogan Josh",
        "Malai Kofta", "Lamb Vindaloo"
    ]
}


# --- Function to read restaurant IDs from the provided CSV ---
def get_restaurant_ids(file_path):
    """Reads the first column (expected to be restaurant IDs) from a CSV file."""
    ids = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                if row:  # Ensure the row is not empty
                    ids.append(row[0])
        print(f"Successfully read {len(ids)} restaurant IDs from {file_path}.")
        return ids
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found. Please check the path.")
        return None
    except Exception as e:
        print(f"An error occurred while reading {file_path}: {e}")
        return None


# --- Generate the Menu Data ---
# Define the full path to the restaurant data file
restaurant_data_path = '/Users/pranauvshanmuganathan/Documents/Resources/restaurant_data.csv'
restaurant_ids = get_restaurant_ids(restaurant_data_path)
all_menu_data = []
menu_item_id = 1

if restaurant_ids:
    print("Generating menu data for each restaurant...")

    # Create a flattened list of all possible dishes with their categories
    master_dish_list = []
    for category, dishes in food_items.items():
        for dish_name in dishes:
            master_dish_list.append({'name': dish_name, 'category': category})

    # Loop through each restaurant ID and generate a menu for it
    for restaurant_id in restaurant_ids:
        # Each restaurant will have between 50 and 75 menu items
        num_items_for_restaurant = random.randint(50, 75)

        # Randomly select dishes from the master list, allowing for repetitions.
        # This fixes the "Sample larger than population" error.
        restaurant_menu = random.choices(master_dish_list, k=num_items_for_restaurant)

        for item in restaurant_menu:
            # Generate a realistic price (e.g., from $5.99 to $29.99)
            price = f"{random.randint(5, 29)}.{random.choice(['49', '99'])}"

            # Generate a random rating between 3.5 and 5.0, rounded to one decimal place
            rating = round(random.uniform(3.5, 5.0), 1)

            # Append the generated item to our data list
            all_menu_data.append({
                'id': menu_item_id,
                'restaurant_id': restaurant_id,
                'name': item['name'],
                'category': item['category'],
                'price': price,
                'rating': rating
            })
            menu_item_id += 1

    # --- Write data to CSV file ---
    # Define the output directory and ensure it exists
    output_dir = '/Users/pranauvshanmuganathan/Documents/Resources'
    os.makedirs(output_dir, exist_ok=True)

    # Define the full path for the output file
    output_file = os.path.join(output_dir, 'menu_data.csv')

    headers = ['id', 'restaurant_id', 'name', 'category', 'price', 'rating']

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(all_menu_data)

        print(f"Successfully created {output_file} with {len(all_menu_data)} total menu items.")

    except IOError:
        print(f"Error: Could not write to the file {output_file}.")
