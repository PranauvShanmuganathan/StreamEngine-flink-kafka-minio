import csv
import os
import random
from faker import Faker


def generate_restaurant_data(output_path="/Users/pranauvshanmuganathan/Documents/Resources/restaurant_data.csv", num_records=500):
    """
    Generate fake restaurant data with 4-digit random IDs and save it to a CSV file.
    """
    fake = Faker("en_US")

    headers = [
        "restaurant_id",
        "restaurant_name",
        "restaurant_type",
        "rating",
        "restaurant_address",
        "contact_number"
    ]

    cuisines = [
        "Indian", "Chinese", "Italian", "Mexican", "Japanese", "Thai",
        "French", "American", "Greek", "Mediterranean", "Korean", "Vietnamese"
    ]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    restaurant_ids = set()

    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        while len(restaurant_ids) < num_records:
            restaurant_id = random.randint(1000, 9999)
            if restaurant_id in restaurant_ids:
                continue  # Ensure uniqueness
            restaurant_ids.add(restaurant_id)

            name = f"{fake.last_name()}'s {random.choice(['Grill', 'Kitchen', 'Diner', 'Bistro', 'Cafe', 'House', 'Bar'])}"
            cuisine = random.choice(cuisines)
            rating = round(random.uniform(3.0, 5.0), 1)
            address = fake.address().replace('\n', ', ')
            phone = fake.numerify(text="(%###) %%%-%%%%")

            row = [
                restaurant_id,
                name,
                cuisine,
                rating,
                address,
                phone
            ]
            writer.writerow(row)

    print(f"✅ Successfully generated {num_records} restaurant records at: {output_path}")


if __name__ == "__main__":
    generate_restaurant_data()