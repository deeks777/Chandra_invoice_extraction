import subprocess
from pathlib import Path


def run_chandra(
    input_file,
    output_dir
):

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    command = [
        "chandra",
        input_file,
        str(output_dir),
        "--method",
        "hf"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    markdown_files = list(
        output_dir.glob("*.md")
    )

    if not markdown_files:
        raise RuntimeError(
            "No markdown output found"
        )

    return str(markdown_files[0])