import subprocess


def markdown_to_latex(md_content):
    with open("temp.md", "w") as file:
        file.write(md_content)
    subprocess.run(["pandoc", "temp.md", "-o", "output.tex"])
markdown_content = """
# Markdown Example

This is an example of Markdown text to convert to LaTeX.
"""
markdown_to_latex(markdown_content)
