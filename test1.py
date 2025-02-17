import os
import re

class IndexParser:
    def __init__(self, index_file_path, package_path):
        self.index_file_path = index_file_path
        self.package_path = package_path

    def parse_index(self):
        index_contents = []
        with open(self.index_file_path, 'r', encoding='utf-16') as file:
            lines = file.readlines()
        
        for line in lines:
            content = self.parse_line(line)
            if content:
                index_contents.append(content)

        return index_contents

    def parse_line(self, line):
        match = re.match(r"(\s*)(.+)", line)
        if not match:
            return None

        content = match.group(2)
        content = re.sub(r'├───|│|└───', '', content).strip()

        return content

    def compare_with_index(self):
        index_contents = self.parse_index()
        missing_in_package = []
        extra_in_package = []

        package_contents = self.get_package_contents()

        for content in index_contents:
            expected_location = os.path.join(self.package_path, content)  # Full expected path
            if not self.exists_in_package(content, package_contents):
                relative_location = os.path.relpath(expected_location, self.package_path)
                missing_in_package.append((content, relative_location))  # Store relative location

        for item, path in package_contents.items():
            if item not in index_contents:
                relative_path = os.path.relpath(path, self.package_path)
                extra_in_package.append((item, relative_path))

        self.print_comparison_result(missing_in_package, extra_in_package)

    def exists_in_package(self, name, package_contents):
        return name in package_contents

    def get_package_contents(self):
        package_contents = {}
        for root, dirs, files in os.walk(self.package_path):
            for dir in dirs:
                package_contents[dir] = os.path.join(root, dir)
            for file in files:
                package_contents[file] = os.path.join(root, file)
        return package_contents

    def print_comparison_result(self, missing_in_package, extra_in_package):
        if not missing_in_package and not extra_in_package:
            print("OKkkkkkkoookkkkkkk")
        else:
            print("KO")

            if missing_in_package:
                print("Folders or files missing in package:")
                for item, relative_path in missing_in_package:
                    full_path = os.path.join(self.package_path, item)  # Print the full expected path
                    print(f"Missing: {full_path}")

            if extra_in_package:
                print("Folders or files extra in package:")
                for item, path in extra_in_package:
                    print(f"Extra: {path}")

        print(f"Missing count: {len(missing_in_package)}")
        print(f"Extra count: {len(extra_in_package)}")

# Example usage
index_file_path = "/app/index.txt"  # Update to the mounted path in the container
package_path = "/app/package"  # Update to the mounted path in the container


parser = IndexParser(index_file_path, package_path)
parser.compare_with_index()
