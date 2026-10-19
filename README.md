# Image Folder to PDF

A lightweight, zero-dependency CLI tool built with Python to automatically combine subdirectories of images into individual PDF files. Designed specifically for batch processing multi-volume content like scanned documents, comics, manga, or photo collections.

## Features

- **Natural Numerical Sorting:** Handles non-standard filenames seamlessly (e.g., `08.png`, `079.png`, `080.png` are sorted mathematically in exact numerical order).
- **Batch Processing:** Converts dozens of subfolders into separate PDFs in a single execution.
- **Dry-Run Mode:** Test your setup and verify page ordering without altering files or writing PDFs to disk.
- **Smart Image Handling:** Automatically converts RGBA/Palette images (PNGs with transparency) to standard RGB for PDF compatibility.
- **Flexible Folder Structure:** Works with nested subdirectories or standalone image directories.

## Requirements

- Python 3.7+
- `Pillow` (PIL) library

Install the required dependency using pip:

```bash
pip install Pillow
```

## Usage

### Basic Usage

Run the script against your target directory containing subfolders:

```bash
python image_folder_to_pdf.py -d "/path/to/your/root_folder"
```

### Dry Run (Simulation)

To preview the file order and PDF names without creating any files:

```bash
python image_folder_to_pdf.py -d "/path/to/your/root_folder" --dry-run
```

### Custom Output Directory

Specify a custom directory to save generated PDFs:

```bash
python image_folder_to_pdf.py -d "/path/to/your/root_folder" -o "/path/to/output_pdfs"
```

## Folder Structure Example

Given a folder structure like this:

```text
MyManga/
│
├── Volume_01/
│   ├── 00.png
│   ├── 01.jpeg
│   └── 02.png
│
└── Volume_02/
    ├── 000.png
    └── 001.png
```

Executing:

```bash
python image_folder_to_pdf.py -d "./MyManga"
```

Will output:

```text
MyManga/
└── PDFs_Output/
    ├── MyManga_Volume_01.pdf
    └── MyManga_Volume_02.pdf
```

## Command Line Arguments

| Argument | Long Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| `-d` | `--directory` | Path to root folder containing subfolders or images | Current directory (`.`) |
| `-o` | `--output` | Target folder for generated PDFs | `<root>/PDFs_Output` |
| | `--dry-run` | Simulates execution without generating PDFs | `False` |

## License

MIT