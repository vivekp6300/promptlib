import pytest
from promptlib.converter import PromptConverter, InvalidMarkdownFormat
from pathlib import Path
import tempfile
import json


def test_valid_markdown_conversion():
    md_text = """---
title: Test Prompt
tags: [test, sample]
variables: [var1, var2]
---

This is a prompt using {{var1}} and {{var2}}.
"""
    json_str = PromptConverter.markdown_to_json(md_text)
    data = json.loads(json_str)
    assert data["title"] == "Test Prompt"
    assert "prompt" in data
    assert "{{var1}}" in data["prompt"]


def test_invalid_markdown_format():
    invalid_md = "This is not a valid front-matter markdown file."
    with pytest.raises(InvalidMarkdownFormat):
        PromptConverter.markdown_to_json(invalid_md)


def test_file_conversion(tmp_path):
    md_file = tmp_path / "test_prompt.md"
    md_file.write_text("""---
title: File Test
tags: [file]
variables: [a]
---

Do something with {{a}}.
""", encoding='utf-8')

    json_file = tmp_path / "test_prompt.json"
    PromptConverter.convert_file(md_file, json_file)

    data = json.loads(json_file.read_text(encoding='utf-8'))
    assert data["title"] == "File Test"


def test_batch_conversion(tmp_path):
    md1 = tmp_path / "prompt1.md"
    md2 = tmp_path / "prompt2.md"

    md1.write_text("""---
title: Prompt 1
tags: [batch]
variables: [x]
---

Prompt for {{x}}.
""", encoding='utf-8')

    md2.write_text("""---
title: Prompt 2
tags: [batch]
variables: [y]
---

Prompt for {{y}}.
""", encoding='utf-8')

    out_dir = tmp_path / "output"
    PromptConverter.batch_convert([md1, md2], out_dir)

    out1 = json.loads((out_dir / "prompt1.json").read_text(encoding='utf-8'))
    out2 = json.loads((out_dir / "prompt2.json").read_text(encoding='utf-8'))

    assert out1["title"] == "Prompt 1"
    assert out2["title"] == "Prompt 2"
