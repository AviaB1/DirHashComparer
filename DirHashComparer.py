import os
import hashlib
import click

def calculate_files_hash(file_path, chunk_size=65536):
    try:
        with open(file_path, 'rb') as f:
            hasher = hashlib.sha256()
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                hasher.update(data)
            return hasher.hexdigest()
    except Exception as e:
        print(f"Couldn't calculate hash for '{file_path}': {e}")

def add_to_list(directory, directory_list):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            hash_value = calculate_files_hash(file_path)
            directory_list.append((file_name, hash_value))

def compare_hashes(source_directory_list, reference_directory_list):
    for (source_file, source_hash), (reference_file, reference_hash) in zip(source_directory_list, reference_directory_list):
        if source_hash != reference_hash:
            print(f"The hash of the file '{source_file}' with the hash value of {source_hash} is not the same as the hash of the file '{reference_file}' with the hash value of {reference_hash}")

    for source_file, source_hash in source_directory_list[len(reference_directory_list):]:
        print(f"The file '{source_file}' is present only in the source directory - '{source_hash}'")

    for reference_file, reference_hash in reference_directory_list[len(source_directory_list):]:
        print(f"The file '{reference_file}' is present only in the reference directory - '{reference_hash}'")

    print("All the hashes have been compared.")

@click.command()
@click.option('--source-directory', '-s', type=click.Path(exists=True), help='Path to the source directory.')
@click.option('--reference-directory', '-r', type=click.Path(exists=True), help='Path to the reference directory.')
def main(source_directory, reference_directory):
    source_directory_list = []
    reference_directory_list = []
    add_to_list(source_directory, source_directory_list)
    add_to_list(reference_directory, reference_directory_list)
    compare_hashes(source_directory_list, reference_directory_list)

if __name__ == '__main__':
    main()
#python script.py --source-directory /path/to/source_directory --reference-directory /path/to/reference_directory
