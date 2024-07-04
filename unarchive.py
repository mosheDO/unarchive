import os
import zipfile
import tarfile
import gzip
import rarfile  # Make sure to install `rarfile` package (`pip install rarfile`)
import shutil
import argparse

class ArchiveExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        base_name = os.path.basename(file_path)
        name, _ = os.path.splitext(base_name)
        self.extract_path = os.path.join(os.path.dirname(file_path), f"{name}_extracted")

    def extract(self):
        if not os.path.exists(self.extract_path):
            os.makedirs(self.extract_path)
        self._extract()
        self._check_for_nested_archives()

    def _extract(self):
        raise NotImplementedError("Subclasses must implement this method")

    def _check_for_nested_archives(self):
        for root, _, files in os.walk(self.extract_path):
            for file in files:
                file_path = os.path.join(root, file)
                extractor = identify_and_create_extractor(file_path)
                if extractor:
                    print(f"Found nested archive: {file_path}")
                    extractor.extract()

class ZipExtractor(ArchiveExtractor):
    def _extract(self):
        with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_path)
        print(f"Extracted ZIP file to {self.extract_path}")

class TarExtractor(ArchiveExtractor):
    def _extract(self):
        with tarfile.open(self.file_path, 'r:*') as tar_ref:
            tar_ref.extractall(self.extract_path)
        print(f"Extracted TAR file to {self.extract_path}")

class GzipExtractor(ArchiveExtractor):
    def _extract(self):
        output_file = os.path.join(self.extract_path, os.path.basename(self.file_path).replace('.gz', ''))
        with gzip.open(self.file_path, 'rb') as gz_ref:
            with open(output_file, 'wb') as out_f:
                shutil.copyfileobj(gz_ref, out_f)
        print(f"Extracted GZIP file to {output_file}")
        # Check if the extracted file is another archive
        if identify_and_create_extractor(output_file):
            extractor = identify_and_create_extractor(output_file)
            if extractor:
                extractor.extract()

class RarExtractor(ArchiveExtractor):
    def _extract(self):
        with rarfile.RarFile(self.file_path, 'r') as rar_ref:
            rar_ref.extractall(self.extract_path)
        print(f"Extracted RAR file to {self.extract_path}")
        
def identify_and_create_extractor(file_path):
    if zipfile.is_zipfile(file_path):
        return ZipExtractor(file_path)
    elif tarfile.is_tarfile(file_path):
        return TarExtractor(file_path)
    elif is_gzip(file_path):
        return GzipExtractor(file_path)
    elif rarfile.is_rarfile(file_path):
        return RarExtractor(file_path)
    else:
        return None

def is_gzip(file_path):
    try:
        with gzip.open(file_path, 'rb') as gz_ref:
            gz_ref.read(1)
        return True
    except:
        return False

def main():
    parser = argparse.ArgumentParser(description="Extract various types of archives.")
    parser.add_argument('file_path', type=str, help="The path to the archive file to be extracted.")
    args = parser.parse_args()

    extractor = identify_and_create_extractor(args.file_path)
    if extractor:
        extractor.extract()

if __name__ == "__main__":
    main()
