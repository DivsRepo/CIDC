import json
import sys
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import traceback

class PDFFormFiller:
    """Fill PDF form fields with JSON data"""
    
    def __init__(self, template_pdf_path, json_data_path):
        self.template_pdf = template_pdf_path
        self.json_data = json_data_path
        self.fields_data = self._load_json_data()
    
    def _load_json_data(self):
        """Load and parse JSON data file"""
        try:
            with open(self.json_data, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✓ Loaded JSON data from: {self.json_data}")
            return data
        except FileNotFoundError:
            print(f"✗ JSON file not found: {self.json_data}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"✗ Invalid JSON format: {e}")
            sys.exit(1)
    
    def _extract_field_values(self):
        """Extract field name-value pairs from JSON structure"""
        field_values = {}
        
        for field in self.fields_data.get('fields', []):
            field_type = field.get('type')
            
            if field_type == 'single':
                # Single field
                name = field.get('name')
                value = field.get('value', '')
                if name:
                    field_values[name] = value
            
            elif field_type == 'group':
                # Group of checkboxes/radio buttons
                group_name = field.get('group_name', '')
                options = field.get('options', [])
                
                for option in options:
                    option_label = option.get('label', '')
                    option_value = option.get('value', '')
                    
                    # Create a key combining group name and option label
                    if group_name and option_label:
                        key = f"{group_name}_{option_label}"
                        field_values[key] = option_value
        
        return field_values
    
    def fill_pdf(self, output_path):
        """Fill PDF with JSON data"""
        try:
            print(f"Reading PDF template: {self.template_pdf}")
            reader = PdfReader(self.template_pdf)
            writer = PdfWriter()
            
            # Extract field values from JSON
            field_values = self._extract_field_values()
            
            print(f"Found {len(field_values)} fields to fill")
            print("-" * 50)
            
            # Get PDF form fields
            pdf_form_fields = reader.get_fields()
            
            if pdf_form_fields:
                print(f"PDF contains {len(pdf_form_fields)} form fields")
                
                # Copy all pages
                for page in reader.pages:
                    writer.add_page(page)
                
                # Fill matching fields
                matched_count = 0
                for pdf_field_name in pdf_form_fields.keys():
                    # Try exact match first
                    if pdf_field_name in field_values:
                        value = field_values[pdf_field_name]
                        writer.update_page_form_field_values(
                            writer.pages[0], 
                            {pdf_field_name: value}
                        )
                        matched_count += 1
                        if value:
                            print(f"  ✓ {pdf_field_name} = {value}")
                
                print(f"\nMatched and filled {matched_count} fields")
            
            else:
                print("⚠ No form fields found in PDF - adding text overlay")
                # Add all pages
                for page in reader.pages:
                    writer.add_page(page)
            
            # Write output
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            print("-" * 50)
            print(f"✓ PDF successfully saved to: {output_path}")
            return True
        
        except Exception as e:
            print(f"✗ Error: {e}")
            traceback.print_exc()
            return False

def main():
    """Main entry point"""
    script_dir = Path(__file__).parent
    
    # Find PDF file
    pdf_files = list(script_dir.glob('*.pdf'))
    
    if not pdf_files:
        print("✗ No PDF template found in current directory")
        print(f"  Looking in: {script_dir}")
        sys.exit(1)
    
    template_pdf = str(pdf_files[0])
    json_file = str(script_dir / 'Patient_Intake_form_dummy_data.json')
    output_pdf = str(script_dir / 'Patient_Intake_form_filled.pdf')
    
    print("=" * 50)
    print("PDF Form Filler")
    print("=" * 50)
    print(f"Template: {Path(template_pdf).name}")
    print(f"Data:     {Path(json_file).name}")
    print(f"Output:   {Path(output_pdf).name}")
    print("=" * 50)
    
    # Fill PDF
    filler = PDFFormFiller(template_pdf, json_file)
    success = filler.fill_pdf(output_pdf)
    
    if success:
        print("\n✓ Process completed successfully!")
    else:
        print("\n✗ Process failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
