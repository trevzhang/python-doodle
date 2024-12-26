import os
from PyPDF2 import PdfMerger
import time

def merge_pdfs(input_folder, output_file):
    merger = PdfMerger()

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            file_path = os.path.join(input_folder, filename)
            try:
                merger.append(file_path)
            except:
                print(f"Error merging file: {file_path}")

    # Write the merged PDF to the output file
    merger.write(output_file)
    merger.close()


# Example usage

if __name__ == "__main__":
    input_folder = "E:/wzgs-mysql/invoice_to_data/to_be_processed/"
    output_file = "E:/wzgs-mysql/invoice_to_data/merged"+ time.strftime("%Y%m%d-%H%M%S") + ".pdf"
    merge_pdfs(input_folder, output_file)