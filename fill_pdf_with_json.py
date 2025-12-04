import json
import os
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def load_json_data(json_file_path):
    """Load JSON data from file"""
    with open(json_file_path, 'r') as f:
        return json.load(f)

def get_field_value(fields, field_name):
    """Extract value from JSON fields by field name"""
    for field in fields:
        if field.get('name') == field_name:
            return field.get('value', '')
    return ''

def fill_pdf_fields(template_pdf_path, json_data_path, output_pdf_path):
    """
    Fill PDF form fields with data from JSON file
    
    Args:
        template_pdf_path: Path to the template PDF
        json_data_path: Path to the JSON data file
        output_pdf_path: Path to save the filled PDF
    """
    
    # Load JSON data
    data = load_json_data(json_data_path)
    fields = data.get('fields', [])
    
    # Create a dictionary of field values
    field_values = {}
    for field in fields:
        field_name = field.get('name')
        field_value = field.get('value', '')
        if field_name:
            field_values[field_name] = field_value
    
    try:
        # Read the PDF template
        reader = PdfReader(template_pdf_path)
        writer = PdfWriter()
        
        # Check if PDF has form fields
        if reader.get_fields() is None:
            print("Warning: PDF does not contain fillable form fields")
            print("Creating overlay with text instead...")
            
            # If no form fields, create an overlay
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                writer.add_page(page)
            
            # Add text overlay
            packet = BytesIO()
            overlay_canvas = canvas.Canvas(packet, pagesize=letter)
            
            y_position = 750
            for field_name, field_value in field_values.items():
                if field_value:  # Only add non-empty values
                    overlay_canvas.drawString(100, y_position, f"{field_name}: {field_value}")
                    y_position -= 20
            
            overlay_canvas.save()
            packet.seek(0)
            
            overlay_reader = PdfReader(packet)
            overlay_page = overlay_reader.pages[0]
            
            # Merge overlay with first page
            if len(writer.pages) > 0:
                writer.pages[0].merge_page(overlay_page)
        
        else:
            # Fill form fields directly
            writer.append_pages_from_reader(reader)
            
            # Update form field values
            if reader.get_fields():
                for field_name, field_value in field_values.items():
                    if field_name in reader.get_fields():
                        writer.update_page_form_field_values(
                            writer.pages[0], {field_name: field_value}
                        )
        
        # Write output PDF
        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"✓ PDF successfully filled and saved to: {output_pdf_path}")
        return True
    
    except Exception as e:
        print(f"✗ Error filling PDF: {e}")
        return False

def main():
    """Main function"""
    # File paths
    script_dir = Path(__file__).parent
    
    # Look for PDF template in the same directory
    pdf_files = list(script_dir.glob('*.pdf'))
    
    if not pdf_files:
        print("Error: No PDF files found in the current directory")
        print("Please place a PDF template in the same folder as this script")
        return
    
    template_pdf = pdf_files[0]  # Use the first PDF found
    json_data_file = script_dir / 'Patient_Intake_form_dummy_data.json'
    output_pdf = script_dir / 'Patient_Intake_form_filled.pdf'
    
    print(f"Template PDF: {template_pdf}")
    print(f"JSON Data: {json_data_file}")
    print(f"Output PDF: {output_pdf}")
    print("-" * 50)
    
    # Check if JSON file exists
    if not json_data_file.exists():
        print(f"Error: JSON file not found: {json_data_file}")
        return
    
    # Fill PDF
    fill_pdf_fields(str(template_pdf), str(json_data_file), str(output_pdf))

if __name__ == '__main__':
    main()
