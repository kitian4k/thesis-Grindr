import os
from concurrent.futures import ProcessPoolExecutor
from pdf2image import convert_from_path

def convert_pdf_to_images(pdf_path, buffer_folder_path, output_format="png", max_pages=None):
    """Converts a single PDF file to images and creates a corresponding buffer folder.

    Args:
        pdf_path (str): Path to the PDF file.
        buffer_folder_path (str): Path to the corresponding buffer folder.
        output_format (str, optional): Desired output format for images (default: "png").
            Supported formats are "png", "jpg", and "ppm".
        max_pages (int, optional): Maximum number of pages to convert (default: None, all pages).
    """

    try:
        pdf_name, _ = os.path.splitext(os.path.basename(pdf_path))  # Extract filename without extension
        images = convert_from_path(pdf_path, fmt=output_format, first_page=1, last_page=max_pages or None)  # Use None for all pages
        for i, image in enumerate(images):
            image_path = os.path.join(buffer_folder_path, f"page_{i+1}.{output_format}")
            image.save(image_path, output_format.upper())  # Use uppercase extension
        print(f"Converted PDF: {pdf_path} {(max_pages or 'all')}")  # Informative output
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")

def convert_pdfs_concurrently(pdf_folder_path, output_format="png", num_workers=4, max_pages=None):
    """Converts all PDF files in a folder to images concurrently using a process pool.

    Args:
        pdf_folder_path (str): Path to the folder containing PDF files.
        output_format (str, optional): Desired output format for images (default: "png").
            Supported formats are "png", "jpg", and "ppm".
        num_workers (int, optional): Number of worker processes to use (default: 4).
        max_pages (int, optional): Maximum number of pages to convert per PDF (default: None, all pages).
    """

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        for filename in os.listdir(pdf_folder_path):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(pdf_folder_path, filename)
                pdf_name, _ = os.path.splitext(filename)
                buffer_folder_path = os.path.join(pdf_folder_path, pdf_name)
                os.makedirs(buffer_folder_path, exist_ok=True)  # Create if not exists
                executor.submit(convert_pdf_to_images, pdf_path, buffer_folder_path, output_format, max_pages)

    print(f"PDF conversion completed for files in: {pdf_folder_path}")

if __name__ == "__main__":
    # Replace with your actual PDF folder path
    pdf_folder_path = "input"
    # Optionally specify the output format (default: "png"), number of workers, and max_pages
    output_format = "png"  # Choose from "png", "jpg", or "ppm"
    num_workers = 4  # Adjust based on your CPU cores
    max_pages = None  # Set to None for unlimited conversion (default)

    convert_pdfs_concurrently(pdf_folder_path, output_format, num_workers, max_pages)
