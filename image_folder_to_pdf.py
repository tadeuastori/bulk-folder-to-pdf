import argparse
import os
import re
from PIL import Image


def extract_number(filename: str) -> int:
    """Extracts the first sequence of digits from a filename for natural numerical sorting.

    Args:
        filename (str): Name of the file.

    Returns:
        int: Extracted number or 0 if no digits are found.
    """
    numbers = re.findall(r"\d+", filename)
    return int(numbers[0]) if numbers else 0


def process_folder(
    folder_path: str, output_path: str, pdf_filename: str, dry_run: bool = False
) -> bool:
    """Processes a single directory containing images and merges them into a single PDF.

    Args:
        folder_path (str): Path to the folder containing images.
        output_path (str): Directory where the output PDF will be saved.
        pdf_filename (str): Target filename for the generated PDF.
        dry_run (bool): If True, simulates execution without creating files.

    Returns:
        bool: True if images were processed/found, False otherwise.
    """
    valid_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".webp")

    # Filter and sort image files using natural numerical sorting
    raw_files = [
        f
        for f in os.listdir(folder_path)
        if f.lower().endswith(valid_extensions)
    ]
    image_files = sorted(raw_files, key=extract_number)

    folder_name = os.path.basename(os.path.normpath(folder_path))
    print(f"Directory: {folder_name}")
    print(f"  -> Found {len(image_files)} valid image(s)")

    if image_files:
        print(f"  -> First page: {image_files[0]}")
        print(f"  -> Last page:  {image_files[-1]}")
    print(f"  -> Target PDF: {pdf_filename}")

    if not image_files:
        print("  -> [WARNING] No images found in this directory.\n")
        return False

    if dry_run:
        print("  -> [SIMULATION] PDF would be generated successfully.\n")
        return True

    images = []
    try:
        for file in image_files:
            file_path = os.path.join(folder_path, file)
            img = Image.open(file_path)

            # Convert images with transparency or color palettes to standard RGB
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            images.append(img)

        if images:
            destination_file = os.path.join(output_path, pdf_filename)
            first_image = images[0]
            remaining_images = images[1:]

            first_image.save(
                destination_file,
                "PDF",
                save_all=True,
                append_images=remaining_images,
            )
            print(f"  -> [SUCCESS] PDF generated: {pdf_filename}\n")
            return True

    except Exception as e:
        print(f"  -> [ERROR] Failed to process {folder_name}: {e}\n")
        return False

    return False


def convert_folders_to_pdf(
    root_dir: str, output_dir: str = None, dry_run: bool = False
):
    """Scans subdirectories (or a single directory) and generates PDFs for each.

    Args:
        root_dir (str): Root directory containing subfolders with images.
        output_dir (str, optional): Directory to store output PDFs.
        dry_run (bool): If True, runs in simulation mode.
    """
    if not os.path.exists(root_dir):
        print(f"[ERROR] The specified path does not exist: '{root_dir}'")
        return

    root_dir = os.path.abspath(root_dir)
    root_name = os.path.basename(os.path.normpath(root_dir))

    # Default output directory is 'PDFs_Output' inside the root directory
    if not output_dir:
        output_dir = os.path.join(root_dir, "PDFs_Output")

    if dry_run:
        print(
            "=== DRY RUN MODE ENABLED (No files will be created or modified) ===\n"
        )
    else:
        os.makedirs(output_dir, exist_ok=True)

    entries = sorted(os.listdir(root_dir))
    subfolders = [
        e
        for e in entries
        if os.path.isdir(os.path.join(root_dir, e))
        and os.path.abspath(os.path.join(root_dir, e))
        != os.path.abspath(output_dir)
    ]

    processed_count = 0

    # Case 1: Subdirectories exist inside root
    if subfolders:
        for subfolder in subfolders:
            subfolder_path = os.path.join(root_dir, subfolder)
            pdf_filename = f"{root_name}_{subfolder}.pdf"

            if process_folder(
                subfolder_path, output_dir, pdf_filename, dry_run
            ):
                processed_count += 1
    # Case 2: No subdirectories, process root directly if it contains images
    else:
        pdf_filename = f"{root_name}.pdf"
        if process_folder(root_dir, output_dir, pdf_filename, dry_run):
            processed_count += 1

    summary_msg = "Simulation complete!" if dry_run else "Processing complete!"
    print(f"\n{summary_msg} Total PDFs processed: {processed_count}")
    if not dry_run and processed_count > 0:
        print(f"Saved PDFs to: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Bulk convert image folders/subfolders into PDF documents with natural numerical sorting."
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default=".",
        help="Path to the root directory containing subfolders with images (default: current directory).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Path to save generated PDFs (default: <root_dir>/PDFs_Output).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the execution without creating PDF files.",
    )

    args = parser.parse_args()
    convert_folders_to_pdf(args.directory, args.output, args.dry_run)


if __name__ == "__main__":
    main()