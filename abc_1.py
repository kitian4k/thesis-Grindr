
import os
import threading
import concurrent.futures
from multiprocessing import Pool  # Import for multiprocessing
import re
#from docx import Document  # Assuming DOCX support is desired
from pdfminer.high_level import extract_text  # Import for PDF text extraction
import time

# Additional libraries for new file types
#import openpyxl  # For basic XLSX handling (consider pandas for structured data)
#from pptx import Presentation  # For PPTX presentations (install with: pip install python-pptx)

try:
    from docx import Document
except ImportError:
    print("To enable DOCX support, install python-docx: pip install python-docx")


class DecodingError(Exception):
    pass


def compile_keywords(categories_keywords_dict):
    """Pre-compiles keyword lists for faster matching"""
    compiled_keywords = {category: [re.compile(keyword, re.IGNORECASE) for keyword in keywords]
                         for category, keywords in categories_keywords_dict.items()}
    return compiled_keywords


def categorize_text_chunk(text_chunk, compiled_keywords):
    """Categorizes a chunk of text using compiled keywords"""
    for category, keyword_list in compiled_keywords.items():
        if all(keyword.search(text_chunk) for keyword in keyword_list):
            return category
    return 'Uncategorized'


def categorize_file(file_path, compiled_keywords):
    try:
        if file_path.endswith('.pdf'):
            text = extract_text(file_path)  # Use pdfminer to extract text (CPU-bound)
            return file_path, categorize_text_chunk(text, compiled_keywords)
        elif file_path.endswith('.docx') and Document:
            # ... (code for DOCX files - potentially I/O bound)
            try:
                doc = Document(file_path)
                text = '\n'.join(paragraph.text for paragraph in doc.paragraphs)  # Combine all paragraphs
                return file_path, categorize_text_chunk(text, compiled_keywords)
            except Exception as e:
                print(f"Error processing DOCX '{file_path}': {e}")
                return file_path, 'Uncategorized (Error)'
        elif file_path.endswith('.txt'):
            with open(file_path, 'r') as f:
                text = f.read()
            return file_path, categorize_text_chunk(text, compiled_keywords)
        else:
            print(f"Unsupported file type: {file_path}")
            return None, 'Unsupported File Type'
    except Exception as e:
        print(f"Error processing '{file_path}': {e}")
        return file_path, 'Uncategorized (Error)'


def threaded_worker(file_paths_categories, output_dir):
    for file_path, category in file_paths_categories:
        if category is not None:  # Skip unsupported files
            category_dir = os.path.join(output_dir, category)
            os.makedirs(category_dir, exist_ok=True)
            os.rename(file_path, os.path.join(category_dir, os.path.basename(file_path)))


def multi_process_categorizer(input_dir, output_dir, categories_keywords_dict, num_processes):
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]

    # Use multiprocessing pool for CPU-bound text processing
    with Pool(processes=num_processes) as pool:
        results = pool.starmap(categorize_file, [(file_path, categories_keywords_dict) for file_path in files])

    # Use concurrent.futures for potentially I/O-bound tasks like moving files
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(threaded_worker, results, output_dir)


def chunks(lst, chunk_size):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

