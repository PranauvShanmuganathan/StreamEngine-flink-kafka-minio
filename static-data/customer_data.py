import csv
from faker import Faker
import os
import random


def generate_customer_data(output_path="/Users/pranauvshanmuganathan/Documents/Resources/customer_data.csv", num_records=1500):
    """
    Generate realistic customer data with US-format mobile numbers and save it to a CSV file.
    """
    # Initialize Faker with US locale
    fake = Faker('en_US')

    # Define the headers
    headers = ['customer_id', 'customer_name', 'email', 'mobile_number', 'address']

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write to CSV
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for i in range(1, num_records + 1):
            full_name = fake.name()
            name_parts = full_name.lower().replace('.', '').split()

            # Generate name-based email
            if len(name_parts) >= 2:
                email_prefix = f"{name_parts[0]}.{name_parts[1]}"
            else:
                email_prefix = name_parts[0]
            domains = ["example.com", "mail.com", "testmail.com"]
            email = f"{email_prefix}@{random.choice(domains)}"

            # Generate US-format phone number
            phone_number = fake.phone_number()
            phone_number = fake.numerify(text="(%###) %%%-%%%%")  # Ensures US format

            customer_data = [
                i,
                full_name,
                email,
                phone_number,
                fake.address().replace('\n', ', ')
            ]
            writer.writerow(customer_data)

    print(f"✅ Successfully generated {num_records} customer records at: {output_path}")


if __name__ == "__main__":
    generate_customer_data()