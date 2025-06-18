import argparse
from pathlib import Path
from promptlib.converter import PromptConverter

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown prompt files to JSON.")
    parser.add_argument("input", help="Markdown file or directory path")
    parser.add_argument("output", help="Output file or directory path")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if input_path.is_file():
        PromptConverter.convert_file(input_path, output_path)
    else:
        PromptConverter.batch_convert(input_path, output_path)

if __name__ == "__main__":
    main()
