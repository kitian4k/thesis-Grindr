import abc_1
import time
import sys
from docx import Document  # Assuming DOCX support is desired
from pdfminer.high_level import extract_text  # Import for PDF text extraction
import json

if __name__ == '__main__':
    start = time.time()
    if len(sys.argv) < 2:
        print("Error: Missing JSON data argument")
        exit()

    json_string = sys.argv[1]
    data = json.loads(json_string)

    categories_keywords_dict = data['category_data']
    folder_path = data['folder_path']

    #categories_keywords_dict1 = {
       # 'AI': ['Artificial', 'Intelligence'],
      #  'Automata': ['finite', 'state', 'machines'],  
     #'DT': ['game', 'theory']
    #}
 
    input = folder_path#file path here
    output='output'#and here
    print(categories_keywords_dict)
  
    compiled_keywords = abc_1.compile_keywords(categories_keywords_dict)
    abc_1.multi_process_categorizer(input, output , compiled_keywords, num_processes=8)  # Adjust processes as needed
    end = time.time()
    print(f"Categorization completed in {end - start:.2f} seconds")