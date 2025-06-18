import re
import yaml
import json
from pathlib import Path
from typing import Union, List


class InvalidMarkdownFormat(Exception):
    pass


class PromptConverter:
    @staticmethod
    def markdown_to_json(md_text: str) -> str:
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', md_text.strip(), re.DOTALL)
        if not match:
            raise InvalidMarkdownFormat("Markdown must start with a YAML front matter block.")

        front_matter = yaml.safe_load(match.group(1))
        body = match.group(2).strip()

        data = {
            "title": front_matter.get("title", "Untitled"),
            "tags": front_matter.get("tags", []),
            "variables": front_matter.get("variables", []),
            "prompt": body
        }

        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def convert_file(input_path: Union[str, Path], output_path: Union[str, Path]) -> None:
        input_path = Path(input_path)
        output_path = Path(output_path)

        with input_path.open('r', encoding='utf-8') as f:
            md_text = f.read()

        json_str = PromptConverter.markdown_to_json(md_text)

        with output_path.open('w', encoding='utf-8') as f:
            f.write(json_str)

    @staticmethod
    def batch_convert(inputs: Union[str, List[str]], output_dir: Union[str, Path]) -> None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        if isinstance(inputs, str):
            inputs = list(Path(inputs).glob("*.md"))

        for file_path in inputs:
            input_path = Path(file_path)
            output_path = output_dir / f"{input_path.stem}.json"
            try:
                PromptConverter.convert_file(input_path, output_path)
                print(f"✔ {input_path.name} → {output_path.name}")
            except Exception as e:
                print(f"✘ {input_path.name}: {e}")
