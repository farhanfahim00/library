# Library Organizer

A Python-based desktop application for managing personal book libraries. It features a user-friendly GUI, multiple library support, OCR-powered data entry from images, and a robust testing suite.

---

## Features

- Add, delete (soft), lend, and search books
- Search by title, author, year, or status
- Maintain multiple libraries in JSON format
- OCR integration to extract book data from scanned images
- Draw rectangles to OCR custom regions in an image
- Generate up to 1 million records for performance testing
- Full testing suite (unit, integration, system)

---

## GUI Overview

Built with **Tkinter**, the GUI supports:
- Entry fields: `Title`, `Author`, `Year`, `Status`
- Buttons:
  - Add Book
  - Delete Book
  - Lend Book
  - Search Book
  - Display All
  - Create/Switch Library
  - Extract Text from Images (OCR)
- Status dropdown: `available`, `lent out`, `deleted`, `missing`

---

## Project Structure

library/
├── data/
│ └── library.json # Book database (JSON)
│
├── src/
│ ├── library_main.py # GUI + controller
│ ├── library_model.py # Backend model logic
│ └── library_image.py # OCR tools
│
├── tests/
│ ├── unit_test.py # Unit tests
│ ├── integration_test.py # Integration tests
│ └── system_test.py # System tests
│
├── .gitignore
├── README.md
└── requirements.txt


---

## Getting Started

### Prerequisites

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Make sure Tesseract OCR is installed and in your system PATH.
Install Tesseract: https://github.com/tesseract-ocr/tesseract?utm_source=chatgpt.com


### OCR Features

OCR allows you to extract text from images using pyocr and Pillow.

Modes:

Batch Mode: Automatically scans all images in ocr_images/ folder.

Manual Mode: Opens an image viewer. You can draw a rectangle to OCR a specific region.

Text is matched against your existing library, and if not found, you are prompted to add it.

### Running Tests

Navigate to the root directory and run:
```bash
python -m unittest discover tests/
```

This runs:

unit_test.py → Verifies core model functions

integration_test.py → Ensures model + GUI connect properly

system_test.py → End-to-end UI + backend simulation

### How It Works

Click the "How It Works" button inside the GUI for an in-app walkthrough.

Or call the how_it_works() function from library_model.py directly in code.

### License

This project is licensed under the MIT License.
See the LICENSE file for full details.

### Contributions

Contributions, issues, and feature requests are welcome!

Steps to contribute:

Fork the repo

Create a new branch:
```bash
git checkout -b feature-name
```

Commit your changes:
```bash
git commit -m "Add some feature"
```

Push to your branch:
```bash
git push origin feature-name

```
Submit a pull request 🚀


---
```ymal
### ✅ Copy & Paste This

Replace the existing section in your `README.md` with this block.

Let me know if you also want:
- A **badge block** (e.g., Python version, license, test status)
- A **GitHub Actions** testing workflow (`.yml`)
- A **"Demo GIF" or screenshot section**
```


