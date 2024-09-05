import javax.swing.JOptionPane;

public class P4f {
    public static void main(String[] args) {

        // Paint brand info
        String[] paintBrands = {"Valspar", "Kilz", "Behr", "Diamond Brite", "Glidden"};
        double[] gallonPrices = {41.98, 38.37, 34.98, 58.97, 17.98};
        double[] laborCharges = {18.25, 15.35, 12.65, 24.75, 11.85};
        double totalCostPaint = 0;
        double totalLaborCost = 0;
        double largestRoomSurfaceArea = 0;
        double largestRoomLaborCost = 0;

        // Introduction/greetings
        String first = JOptionPane.showInputDialog("Please enter your first name: ");
        JOptionPane.showMessageDialog(null, "Hello " + first + "\n" + "Welcome to Palette Perfection! ");

        // Number of rooms to be painted, with exception handling
        int numRooms;
        do {
            try {
                numRooms = getInt(first + ", please enter the number of rooms that you want to paint: ");
                if (numRooms <= 0) {
                    JOptionPane.showMessageDialog(null, "Error: enter a number greater than or equal to 1");
                } else {
                    break;
                }
            } catch (NumberFormatException e) {
                JOptionPane.showMessageDialog(null, "Error: invalid input. Enter a number");
            }
        } while (true);

        String summary = ""; // To store room-wise summary

        for (int i = 1; i <= numRooms; i++) {
            double squareFeet = getDouble(first + ", please enter the square feet of wall space for room " + i + ": ", 1);
            int brandIndex = getInt("Paint brands:\n" +
                    "1. Valspar\n2. Kilz\n3. Behr\n4. Diamond Brite\n5. Glidden", 1, paintBrands.length) - 1;

            double gallonsNeeded = calculateGallonsNeeded(squareFeet);
            double paintCost = calculatePaintCost(gallonsNeeded, gallonPrices[brandIndex]);
            double laborHours = calculateLaborHours(squareFeet);
            double laborCost = laborHours * laborCharges[brandIndex];
            double totalRoomCost = paintCost + laborCost;

            // Store room information
            totalCostPaint += paintCost;
            totalLaborCost += laborCost;
            summary += "Painting information for room " + i + ":\n" +
                    "Surface Area: " + String.format("%.2f", squareFeet) + " sq.ft\n" +
                    "Gallons Needed: " + String.format("%.2f", gallonsNeeded) + "\n" +
                    "Price per Gallon: $" + String.format("%.2f", gallonPrices[brandIndex]) + "\n" +
                    "Paint Cost: $" + String.format("%.2f", paintCost) + "\n" +
                    "Labor Hours: " + String.format("%.2f", laborHours) + " hours\n" +
                    "Labor Cost: $" + String.format("%.2f", laborCost) + "\n" +
                    "Total Room Cost: $" + String.format("%.2f", totalRoomCost) + "\n\n";

            // Update largest room information if applicable
            if (squareFeet > largestRoomSurfaceArea) {
                largestRoomSurfaceArea = squareFeet;
                largestRoomLaborCost = laborCost;
            }
        }

        // Check if discount applies
        if (totalCostPaint + totalLaborCost > 700) {
            double discountAmount = largestRoomLaborCost * 0.05;
            totalLaborCost -= discountAmount;
            summary += "5% Discount applied to labor cost of largest room ($" + String.format("%.2f", discountAmount) + ")\n\n";
        }

        // Display the summary for all rooms
        double totalCostAfterDiscount = totalCostPaint + totalLaborCost;
        summary += "Total Cost for paint job after discount: $" + String.format("%.2f", totalCostAfterDiscount) + "\n";
       JOptionPane.showMessageDialog(null, "Thank you " + first + ". We appreciate your business!");

        JOptionPane.showMessageDialog(null, "Painting Information:\n" + summary +
                " You are entitled to a discount!!!" + "\n" + "Total Cost for paint job after discount: $" + String.format("%.2f", totalCostAfterDiscount));

    }

    // Calculation methods
    private static double calculateGallonsNeeded(double surfaceArea) {
        final int SQ_FT_PER_GALLON = 115;
        return Math.ceil(surfaceArea / SQ_FT_PER_GALLON);
    }

    private static double calculateLaborHours(double surfaceArea) {
        final int SQ_FT_PER_GALLON = 115;
        return Math.ceil(surfaceArea / SQ_FT_PER_GALLON) * 8;
    }

    private static double calculatePaintCost(double gallonsRequired, double gallonPrice) {
        return gallonsRequired * gallonPrice;
    }

    // Exception handling for integer input
    public static int getInt(String msg) {
        int input;
        do {
            try {
                input = Integer.parseInt(JOptionPane.showInputDialog(msg));
                if (input <= 0) {
                    JOptionPane.showMessageDialog(null, "Error: Enter a number greater than 0");
                } else {
                    return input;
                }
            } catch (NumberFormatException e) {
                JOptionPane.showMessageDialog(null, "Please enter a valid integer.");
            }
        } while (true);
    }

    // Exception handling for integer input within a range
    public static int getInt(String msg, int lrange, int urange) {
        int input;
        do {
            try {
                input = Integer.parseInt(JOptionPane.showInputDialog(msg));
                if (input < lrange || input > urange) {
                    JOptionPane.showMessageDialog(null, "Input must be between " + lrange + " and " + urange);
                } else {
                    return input;
                }
            } catch (NumberFormatException e) {
                JOptionPane.showMessageDialog(null, "Please enter a valid integer.");
            }
        } while (true);
    }

    // Exception handling for double input
    public static double getDouble(String msg, double lrange) {
        double input;
        do {
            try {
                input = Double.parseDouble(JOptionPane.showInputDialog(msg));
                if (input < lrange) {
                    JOptionPane.showMessageDialog(null, "Input must be greater than or equal to " + lrange);
                } else {
                    return input;
                }
            } catch (NumberFormatException e) {
                JOptionPane.showMessageDialog(null, "Please enter a valid number.");
            }
        } while (true);
    }
}
