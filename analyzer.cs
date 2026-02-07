using System;
using System.IO;
using System.Linq;
using System.Globalization;

// 1. Data Model (Equivalent to a dictionary row structure)
public record SalesItem(string ProductName, decimal Price, int Quantity);
public record TopSellingProductResult(string ProductName, decimal Price, int Quantity, decimal TotalRevenue);

public class CsvProcessor
{
    // C# method equivalent to the Python 'calculate_total_sales' function
    public static decimal CalculateTotalSales(string filename)
    {
        // Use decimal for financial accuracy (Python's float is often imprecise)
        decimal total = 0.0m;

        try
        {
            // Read lines from the file, similar to Python's 'with open...'
            // We skip the header row (index 0) immediately.
            var dataLines = File.ReadLines(filename).Skip(1);

            // Process each data line using LINQ
            foreach (string line in dataLines)
            {
                // Equivalent to line.split(',')
                string[] columns = line.Split(',');

                if (columns.Length == 3)
                {
                    // Attempt to parse the values. Use InvariantCulture for consistent decimal parsing.
                    // The 'm' suffix on 0.0m ensures the variable is treated as a decimal.
                    if (decimal.TryParse(columns[1], NumberStyles.Any, CultureInfo.InvariantCulture, out decimal price) &&
                        int.TryParse(columns[2], out int quantity))
                    {
                        total += price * quantity;
                    }
                    else
                    {
                        Console.WriteLine($"Skipping malformed data in row: {line}");
                    }
                }
            }
        }
        catch (FileNotFoundException)
        {
            // Python equivalent of handling file open failure
            Console.WriteLine($"Error: The file '{filename}' was not found.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An unexpected error occurred: {ex.Message}");
        }

        return total;
    }
    public static decimal CalculateTotalSalesRefactored(string filename)
    {
        decimal total = 0.0m;
        int rowNumber = 1; // Track row number (starting at 1 for header)
        int skippedRows = 0;

        try
        {
            // Check if file exists before attempting to read
            if (!File.Exists(filename))
            {
                throw new FileNotFoundException($"The CSV file '{filename}' was not found at the specified location.");
            }

            // Read lines from the file and skip the header row
            var dataLines = File.ReadLines(filename).Skip(1).ToList();

            if (dataLines.Count == 0)
            {
                Console.WriteLine("Warning: The CSV file contains no data rows (only header).");
                return total;
            }

            // Process each data line
            foreach (string line in dataLines)
            {
                rowNumber++;

                // Skip empty lines
                if (string.IsNullOrWhiteSpace(line))
                {
                    Console.WriteLine($"Row {rowNumber}: Skipping empty line.");
                    skippedRows++;
                    continue;
                }

                string[] columns = line.Split(',');

                // Validate column count
                if (columns.Length != 3)
                {
                    Console.WriteLine($"Row {rowNumber}: ERROR - Expected 3 columns, found {columns.Length}. Skipping row: {line}");
                    skippedRows++;
                    continue;
                }

                string productName = columns[0].Trim();
                string priceStr = columns[1].Trim();
                string quantityStr = columns[2].Trim();

                // Attempt to parse price (ValueError equivalent)
                if (!decimal.TryParse(priceStr, NumberStyles.Any, CultureInfo.InvariantCulture, out decimal price))
                {
                    Console.WriteLine($"Row {rowNumber}: ValueError - Price '{priceStr}' is not a valid number. Skipping row: {line}");
                    skippedRows++;
                    continue;
                }

                // Attempt to parse quantity (ValueError equivalent)
                if (!int.TryParse(quantityStr, out int quantity))
                {
                    Console.WriteLine($"Row {rowNumber}: ValueError - Quantity '{quantityStr}' is not a valid integer. Skipping row: {line}");
                    skippedRows++;
                    continue;
                }

                // Validate positive values
                if (price < 0)
                {
                    Console.WriteLine($"Row {rowNumber}: ValueError - Price cannot be negative ({price}). Skipping row: {line}");
                    skippedRows++;
                    continue;
                }

                if (quantity < 0)
                {
                    Console.WriteLine($"Row {rowNumber}: ValueError - Quantity cannot be negative ({quantity}). Skipping row: {line}");
                    skippedRows++;
                    continue;
                }

                // Valid row - add to total
                total += price * quantity;
            }

            if (skippedRows > 0)
            {
                Console.WriteLine($"\nWarning: {skippedRows} row(s) were skipped due to errors.");
            }
        }
        catch (FileNotFoundException ex)
        {
            Console.WriteLine($"FileNotFoundError: {ex.Message}");
            return 0.0m;
        }
        catch (UnauthorizedAccessException ex)
        {
            Console.WriteLine($"AccessError: Permission denied to read file '{filename}': {ex.Message}");
            return 0.0m;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"UnexpectedError: An unexpected error occurred while processing '{filename}': {ex.Message}");
            return 0.0m;
        }

        return total;
    }
    public static decimal CalculateTotalSalesLinq(string filename)
    {
        decimal total = 0.0m;

        try
        {
            var dataLines = File.ReadLines(filename).Skip(1);

            // Use LINQ Sum() instead of manual loop
            total = dataLines
                .Select(line => line.Split(','))
                .Where(columns => columns.Length == 3)
                .Where(columns => 
                    decimal.TryParse(columns[1], NumberStyles.Any, CultureInfo.InvariantCulture, out decimal price) &&
                    int.TryParse(columns[2], out int quantity))
                .Sum(columns => 
                    decimal.Parse(columns[1], NumberStyles.Any, CultureInfo.InvariantCulture) * 
                    int.Parse(columns[2]));
        }
        catch (FileNotFoundException)
        {
            Console.WriteLine($"Error: The file '{filename}' was not found.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An unexpected error occurred: {ex.Message}");
        }

        return total;
    }

    // Get the top-selling product by total revenue (price * quantity)
    public static TopSellingProductResult GetTopSellingProduct(string filename)
    {
        var topProduct = new TopSellingProductResult("", 0m, 0, 0m);

        try
        {
            // Check if file exists
            if (!File.Exists(filename))
            {
                Console.WriteLine($"Error: The file '{filename}' was not found.");
                return topProduct;
            }

            // Read lines and skip header
            var dataLines = File.ReadLines(filename).Skip(1).ToList();

            if (dataLines.Count == 0)
            {
                Console.WriteLine("Error: No data rows found in the CSV file.");
                return topProduct;
            }

            // Parse and find the product with the highest total revenue
            var result = dataLines
                .Select(line => line.Split(','))
                .Where(columns => columns.Length == 3)
                .Where(columns =>
                    decimal.TryParse(columns[1].Trim(), NumberStyles.Any, CultureInfo.InvariantCulture, out decimal price) &&
                    int.TryParse(columns[2].Trim(), out int quantity) &&
                    price >= 0 && quantity >= 0)
                .Select(columns =>
                {
                    string productName = columns[0].Trim();
                    decimal price = decimal.Parse(columns[1].Trim(), NumberStyles.Any, CultureInfo.InvariantCulture);
                    int quantity = int.Parse(columns[2].Trim());
                    decimal totalRevenue = price * quantity;
                    return new TopSellingProductResult(productName, price, quantity, totalRevenue);
                })
                .OrderByDescending(item => item.TotalRevenue)
                .FirstOrDefault();

            if (result != null && result.ProductName != "")
            {
                topProduct = result;
            }
            else
            {
                Console.WriteLine("Error: No valid products found in the CSV file.");
            }
        }
        catch (FileNotFoundException ex)
        {
            Console.WriteLine($"FileNotFoundError: {ex.Message}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"UnexpectedError: An unexpected error occurred while processing '{filename}': {ex.Message}");
        }

        return topProduct;
    }

    // C# Main method equivalent to Python's 'if __name__ == "__main__":' block
    public static void Main(string[] args)
    {
        // Note: For this to run, a file named 'sales_data.csv' must exist
        // in the output directory (e.g., bin/Debug/net8.0/).
        string salesDataFile = "sales_data.csv";
        
        // Example: Create a dummy file if it doesn't exist for testing
        if (!File.Exists(salesDataFile))
        {
            // You should replace this with a real file in a live environment
            File.WriteAllText(salesDataFile, "product_name,price,quantity\nLaptop,1200.00,5\nMouse,25.50,10\n");
        }

        // Display total sales
        decimal totalSales = CalculateTotalSales(salesDataFile);
        Console.WriteLine($"Total sales from {salesDataFile}: {totalSales.ToString("C", CultureInfo.CurrentCulture)}");
        
        // Display top-selling product with detailed formatting
        Console.WriteLine("\n" + new string('=', 60));
        Console.WriteLine("TOP-SELLING PRODUCT ANALYSIS");
        Console.WriteLine(new string('=', 60));

        var topProduct = GetTopSellingProduct(salesDataFile);

        if (topProduct.ProductName != "")
        {
            Console.WriteLine($"\nProduct Name:      {topProduct.ProductName}");
            Console.WriteLine($"Unit Price:        {topProduct.Price.ToString("C", CultureInfo.CurrentCulture)}");
            Console.WriteLine($"Quantity Sold:     {topProduct.Quantity} units");
            Console.WriteLine($"Total Revenue:     {topProduct.TotalRevenue.ToString("C", CultureInfo.CurrentCulture)}");
            Console.WriteLine(new string('=', 60) + "\n");
        }
    }
}
