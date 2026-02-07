import csv
import os
from typing import List, Dict, Tuple, Optional


class SalesAnalyzer:
    """
    A class to analyze sales data from CSV files.
    
    This class provides methods to load sales data, calculate total sales,
    and identify the top-selling product by revenue.
    """

    def __init__(self, filename: str):
        """
        Initialize the SalesAnalyzer with a filename.
        
        Args:
            filename (str): The path to the CSV file containing sales data.
                           Expected columns: 'product_name', 'price', 'quantity'
        """
        self.filename = filename
        self.data: List[Dict[str, any]] = []
        self.total_sales = 0.0
        self.top_product = None

    def load_data(self) -> bool:
        """
        Load sales data from the CSV file.
        
        Reads the CSV file specified in the constructor and validates the data.
        Skips rows with invalid price or quantity values.
        
        Returns:
            bool: True if data was successfully loaded, False otherwise.
        """
        if not os.path.exists(self.filename):
            print(f"Error: The file '{self.filename}' was not found.")
            return False

        try:
            self.data = []
            with open(self.filename, mode='r') as file:
                csv_reader = csv.DictReader(file)
                
                if csv_reader.fieldnames is None or 'product_name' not in csv_reader.fieldnames:
                    print("Error: CSV file must contain 'product_name', 'price', and 'quantity' columns.")
                    return False

                for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 (after header)
                    try:
                        # Validate and parse the data
                        product_name = row.get('product_name', '').strip()
                        price_str = row.get('price', '').strip()
                        quantity_str = row.get('quantity', '').strip()

                        if not product_name:
                            print(f"Row {row_num}: Skipping row with empty product name.")
                            continue

                        try:
                            price = float(price_str)
                        except ValueError:
                            print(f"Row {row_num}: ValueError - Price '{price_str}' is not a valid number. Skipping row.")
                            continue

                        try:
                            quantity = int(quantity_str)
                        except ValueError:
                            print(f"Row {row_num}: ValueError - Quantity '{quantity_str}' is not a valid integer. Skipping row.")
                            continue

                        # Validate non-negative values
                        if price < 0:
                            print(f"Row {row_num}: ValueError - Price cannot be negative ({price}). Skipping row.")
                            continue

                        if quantity < 0:
                            print(f"Row {row_num}: ValueError - Quantity cannot be negative ({quantity}). Skipping row.")
                            continue

                        # Add valid row to data
                        self.data.append({
                            'product_name': product_name,
                            'price': price,
                            'quantity': quantity
                        })

                    except Exception as e:
                        print(f"Row {row_num}: Unexpected error - {e}. Skipping row.")
                        continue

            if not self.data:
                print("Warning: No valid data rows found in the CSV file.")
                return False

            return True

        except FileNotFoundError:
            print(f"FileNotFoundError: The file '{self.filename}' was not found.")
            return False
        except Exception as e:
            print(f"UnexpectedError: An error occurred while loading '{self.filename}': {e}")
            return False

    def calculate_total_sales(self) -> float:
        """
        Calculate the total sales from the loaded data.
        
        Iterates through all valid data rows and computes the sum of
        (price * quantity) for each product.
        
        Returns:
            float: The total sales amount. Returns 0.0 if no data is loaded.
        """
        if not self.data:
            print("Error: No data loaded. Call load_data() first.")
            return 0.0

        self.total_sales = sum(item['price'] * item['quantity'] for item in self.data)
        return self.total_sales

    def find_top_product(self) -> Optional[Dict[str, any]]:
        """
        Find the top-selling product by total revenue.
        
        Identifies the product with the highest total revenue (price * quantity)
        from the loaded data.
        
        Returns:
            dict or None: A dictionary containing:
                         - 'product_name': The name of the product
                         - 'price': Unit price
                         - 'quantity': Quantity sold
                         - 'total_revenue': Total revenue (price * quantity)
                         Returns None if no data is loaded.
        """
        if not self.data:
            print("Error: No data loaded. Call load_data() first.")
            return None

        # Calculate total revenue for each product
        products_with_revenue = [
            {
                'product_name': item['product_name'],
                'price': item['price'],
                'quantity': item['quantity'],
                'total_revenue': item['price'] * item['quantity']
            }
            for item in self.data
        ]

        # Find and store the product with the highest revenue
        self.top_product = max(products_with_revenue, key=lambda x: x['total_revenue'])
        return self.top_product

    def display_results(self) -> None:
        """
        Display the analysis results in a formatted output.
        
        Shows the total sales and the top-selling product with detailed
        information in a clearly formatted table.
        """
        print(f"Total sales from {self.filename}: ${self.total_sales:.2f}")

        if self.top_product:
            print("\n" + "=" * 60)
            print("TOP-SELLING PRODUCT ANALYSIS")
            print("=" * 60)
            print(f"\nProduct Name:      {self.top_product['product_name']}")
            print(f"Unit Price:        ${self.top_product['price']:.2f}")
            print(f"Quantity Sold:     {self.top_product['quantity']} units")
            print(f"Total Revenue:     ${self.top_product['total_revenue']:.2f}")
            print("=" * 60 + "\n")
        else:
            print("Warning: No top product found.")


if __name__ == "__main__":
    sales_data_file = 'sales_data.csv'

    # Create an instance of SalesAnalyzer
    analyzer = SalesAnalyzer(sales_data_file)

    # Load the data from the CSV file
    if analyzer.load_data():
        # Calculate total sales
        analyzer.calculate_total_sales()

        # Find the top-selling product
        analyzer.find_top_product()

        # Display the results
        analyzer.display_results()
    else:
        print("Failed to load data. Exiting.")
