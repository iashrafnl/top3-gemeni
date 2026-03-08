import os
import argparse

def human_readable_size(size, decimal_places=2):
    """Converts size in bytes to human-readable format."""
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

def get_top_files(directory, top_n=3):
    """
    Finds the top N largest files in a directory, skipping cloud storage locations.

    Args:
        directory (str): The directory to search.
        top_n (int): The number of top files to return.

    Returns:
        list: A list of tuples, where each tuple contains the file path and its size.
    """
    cloud_storage_dirs = ["Google Drive", "OneDrive", "Dropbox"]
    top_files = []

    for dirpath, dirnames, filenames in os.walk(directory):
        # Skip cloud storage directories
        for d in cloud_storage_dirs:
            if d in dirnames:
                dirnames.remove(d)

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if not os.path.isfile(file_path):
                continue

            try:
                size = os.path.getsize(file_path)
                if len(top_files) < top_n:
                    top_files.append((file_path, size))
                    top_files.sort(key=lambda x: x[1], reverse=True)
                elif size > top_files[-1][1]:
                    top_files.pop()
                    top_files.append((file_path, size))
                    top_files.sort(key=lambda x: x[1], reverse=True)
            except OSError:
                # Ignore files that can't be accessed
                pass

    return top_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List the top 3 largest files in a directory.")
    parser.add_argument("directory", help="The directory to search.")
    args = parser.parse_args()

    top_files = get_top_files(args.directory)

    print(f"Top {len(top_files)} largest files in '{args.directory}':")

    if not top_files:
        print("No files found.")
    else:
        # Prepare data for the table
        table_data = [(human_readable_size(size), file_path) for file_path, size in top_files]

        # Find the maximum width for the size column
        max_size_width = max(len(size_str) for size_str, _ in table_data) if table_data else 0

        # Print header
        header = f"{'Size':<{max_size_width}} | Name"
        print(header)
        print(f"{'-' * max_size_width}-|-{'-' * (len(header) - max_size_width - 3)}")

        # Print rows
        for size_str, file_path in table_data:
            print(f"{size_str:<{max_size_width}} | {file_path}")
