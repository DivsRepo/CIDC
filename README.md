# PDF Form Filler - Patient Intake Form

This project contains Python scripts to automatically fill PDF form fields with data from a JSON file.

## Files Included

1. **Patient_Intake_form_dummy_data.json** - Dummy data for all form fields
2. **fill_pdf_with_json.py** - Basic PDF filler script
3. **pdf_filler_advanced.py** - Advanced PDF filler with better logging and field matching
4. **requirements.txt** - Python dependencies
5. **README.md** - This file

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- **PyPDF2**: For reading and writing PDF files
- **reportlab**: For creating PDF overlays (fallback)

### 2. Prepare Files

Make sure you have:
- A PDF template file (e.g., `Patient_Intake_form-Fillable.pdf`) in the same directory
- The dummy data file (`Patient_Intake_form_dummy_data.json`)

## Usage

### Quick Start (Recommended)

```bash
python pdf_filler_advanced.py
```

This will:
1. Find the PDF template in the directory
2. Load the dummy data from JSON
3. Fill the form fields
4. Save the output as `Patient_Intake_form_filled.pdf`

### Alternative Method

```bash
python fill_pdf_with_json.py
```

## How It Works

### Data Structure

The JSON file contains a `fields` array with two types of entries:

**Single Field:**
```json
{
  "name": "Name",
  "type": "single",
  "field_type": 7,
  "label": "Information",
  "value": "John Michael Smith"
}
```

**Group Field (Checkboxes/Radio Buttons):**
```json
{
  "group_name": "Gender:",
  "type": "group",
  "options": [
    {
      "label": "Male",
      "value": "On",
      "type": "checkbox"
    }
  ]
}
```

### Field Mapping

The script matches JSON field names with PDF form field names:
- **Single fields**: Matched by the `name` property
- **Group fields**: Field keys are created as `{group_name}_{option_label}`
- **Checkbox values**: "On" = checked, "Off" = unchecked

## Output

The filled PDF will be saved as:
- `Patient_Intake_form_filled.pdf`

## Troubleshooting

### PDF has no form fields

If the PDF doesn't contain interactive form fields, the script will add a text overlay instead (PyPDF2 limitation).

### Field not found

Check that the PDF form field name matches the JSON field name exactly.

### Import errors

Make sure all dependencies are installed:
```bash
pip install --upgrade PyPDF2 reportlab
```

## Customization

To use different files, edit the script:

```python
template_pdf = "your_template.pdf"
json_file = "your_data.json"
output_pdf = "your_output.pdf"
```

## Requirements

- Python 3.7+
- PyPDF2
- reportlab

## Notes

- The dummy data includes realistic patient information
- All required fields are filled with appropriate values
- Checkbox fields use "On"/"Off" convention
- Date format: MMDDYYYY
- Phone format: XXX-XXX-XXXX

## License

For internal use only.
