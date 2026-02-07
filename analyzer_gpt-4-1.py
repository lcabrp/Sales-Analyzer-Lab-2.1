import csv
import os
from typing import List, Dict, Optional

class SalesAnalyzer:
    """
    Analyze sales data from a CSV file.

    The class is initialized with the path to a CSV file and provides
    methods to load data, calculate total sales, and find the top-selling
    product by revenue (price * quantity).
    """
    def __init__(self, filename: str):
        """
        Initialize the SalesAnalyzer with a filename.

        Args:
            filename: Path to the CSV file. Expected columns: 'product_name', 'price', 'quantity'.
        """
        self.filename = filename
        self.data: List[Dict[str, any]] = []
        self.total_sales: float = 0.0
        self.top_product: Optional[Dict[str, any]] = None

    def load_data(self) -> bool:
        """
        Load and validate sales data from the CSV file.

        Returns True if data was loaded successfully, False otherwise.
        Rows with invalid or missing values are skipped and reported.
        """
        if not os.path.exists(self.filename):
            print(f"Error: The file '{self.filename}' was not found.")
            return False

        try:
            self.data = []
            with open(self.filename, mode='r', newline='') as f:
                reader = csv.DictReader(f)

                expected = {'product_name', 'price', 'quantity'}
                if reader.fieldnames is None or not expected.issubset(set(reader.fieldnames)):
                    print("Error: CSV file must contain 'product_name', 'price', and 'quantity' columns.")
                    return False

                for row_num, row in enumerate(reader, start=2):
                    product = (row.get('product_name') or '').strip()
                    price_str = (row.get('price') or '').strip()
                    qty_str = (row.get('quantity') or '').strip()

                    if not product:
                        print(f"Row {row_num}: Skipping row with empty product name.")
                        continue

                    try:
                        price = float(price_str)
                    except ValueError:
                        print(f"Row {row_num}: ValueError - Price '{price_str}' is not a valid number. Skipping row.")
                        continue

                    try:
                        quantity = int(qty_str)
                    except ValueError:
                        print(f"Row {row_num}: ValueError - Quantity '{qty_str}' is not a valid integer. Skipping row.")
                        continue

                    if price < 0:
                        print(f"Row {row_num}: ValueError - Price cannot be negative ({price}). Skipping row.")
                        continue

                    if quantity < 0:
                        print(f"Row {row_num}: ValueError - Quantity cannot be negative ({quantity}). Skipping row.")
                        continue

                    self.data.append({'product_name': product, 'price': price, 'quantity': quantity})

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
        Calculate and return the total sales (sum of price * quantity) for loaded data.

        Returns 0.0 if no data is loaded.
        """
        if not self.data:
            print("Error: No data loaded. Call load_data() first.")
            return 0.0

        self.total_sales = sum(item['price'] * item['quantity'] for item in self.data)
        return self.total_sales

    def find_top_product(self) -> Optional[Dict[str, any]]:
        """
        Identify the top-selling product by total revenue (price * quantity).

        Returns a dictionary with keys: 'product_name', 'price', 'quantity', 'total_revenue', or None if no data.
        """
        if not self.data:
            print("Error: No data loaded. Call load_data() first.")
            return None

        products = [
            {
                'product_name': d['product_name'],
                'price': d['price'],
                'quantity': d['quantity'],
                'total_revenue': d['price'] * d['quantity']
            }
            for d in self.data
        ]

        self.top_product = max(products, key=lambda x: x['total_revenue'])
        return self.top_product

if __name__ == "__main__":
    sales_data_file = 'sales_data.csv'

    analyzer = SalesAnalyzer(sales_data_file)

    if analyzer.load_data():
        analyzer.calculate_total_sales()
        analyzer.find_top_product()

        # Display results formatted like previous scripts
        print(f"Total sales from {sales_data_file}: ${analyzer.total_sales:.2f}")

        if analyzer.top_product:
            print("\n" + "=" * 60)
            print("TOP-SELLING PRODUCT ANALYSIS")
            print("=" * 60)
            print(f"\nProduct Name:      {analyzer.top_product['product_name']}")
            print(f"Unit Price:        ${analyzer.top_product['price']:.2f}")
            print(f"Quantity Sold:     {analyzer.top_product['quantity']} units")
            print(f"Total Revenue:     ${analyzer.top_product['total_revenue']:.2f}")
            print("=" * 60 + "\n")
    else:
        print("Failed to load data. Exiting.")
