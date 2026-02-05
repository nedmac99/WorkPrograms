# Import the FPDF class from the fpdf library for creating PDF files
from fpdf import FPDF

# Import the Image class from the PIL (Pillow) library for handling image files
from PIL import Image


# Define a custom class Shirt that inherits from FPDF
class Shirt(FPDF):
    # Constructor method for the Shirt class
    def __init__(self, name, shirt_image_path):
        # Initialize the FPDF class with portrait orientation and A4 page size
        super().__init__(orientation="P", format="A4")

        # Store the user's name
        self.name = name

        # Store the path to the shirt image
        self.shirt_image_path = shirt_image_path

    # Define a custom header for the PDF
    def header(self):
        # Set the font to Helvetica, bold, size 24
        self.set_font("Helvetica", "B", 24)

        # Set the text color to black (0, 0, 0)
        self.set_text_color(0)

        # Add a centered title at the top of the page
        self.cell(w=0, h=20, text="CS50 Shirtificate", align="C")

    # Method to add the shirt image and overlay the user's name
    def add_shirt_image_with_name(self):
        # Open the shirt image using PIL to get dimensions
        image = Image.open(self.shirt_image_path)

        # Calculate the aspect ratio of the image
        image_aspect_ratio = image.height / image.width

        # Add the image(shirt) to the PDF at the specified position and size. Alter values as needed
        self.image(
            self.shirt_image_path,
            x=((210 - 150) / 2),
            y=40,
            w=150,
            h=(150 * image_aspect_ratio),
        )

        # Set the text color to white for visibility on dark backgrounds
        self.set_text_color(255, 255, 255)

        # Set the font to Helvetica with size 18
        self.set_font("Helvetica", size=18)

        # Calculate the width of the name text
        text_width = self.get_string_width(self.name) + 2

        # Center the name text horizontally
        name_x = (210 - text_width) / 2

        # Set the vertical position of the name text relative to the image. Adjust this based on actual shirt image
        name_y = 20 + 70

        # Set the text position
        self.set_xy(name_x, name_y)

        # Add the user's name to the PDF, centered within the cell
        self.cell(text_width, 10, self.name, align="C")

    # Method to create and save the final PDF
    def generate(self, output_path="shirtificate.pdf"):
        # Add a new page to the PDF
        self.add_page()

        # Add the shirt image and overlay the name
        self.add_shirt_image_with_name()

        # Save the PDF to the specified path
        self.output(output_path)

        # Print confirmation message
        print(f"PDF saved as '{output_path}'.")


# Define the main function (currently a placeholder)
def main():
    # Set the filename of the shirt image
    shirt_image = "shirtificate.png"

    # Prompt the user to enter their name
    name = input("Enter your name: ")

    # Create a Shirt object with the user's name and image path
    pdf = Shirt(f"{name} took CS50", shirt_image)

    # Generate the PDF file
    pdf.generate()


# Entry point: only run the following code if this file is executed directly
if __name__ == "__main__":
    main()

