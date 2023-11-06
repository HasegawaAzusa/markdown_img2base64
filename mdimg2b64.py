import base64
import click
import os
import re

RE_MARKDOWN_IAMGE = re.compile("^!\[.*\]\(.*\)$")
RE_HTML_IMAGE = re.compile("^<img src=.*/>$")

@click.command()
@click.option('-f', '--file', required=True, type=click.Path(exists=True, readable=True,resolve_path=True), help='file name')
def run(file: str):
    """
    Convert images in markdown to base64
    """
    dirpath = os.path.dirname(file)
    output_filename = 'modified_' + os.path.basename(file)
    output_filepath = os.path.join(dirpath, output_filename)
    output_filepath = os.path.normpath(output_filepath)
    with open(file, 'r', encoding='utf-8') as mdfile:
        lines = mdfile.read().splitlines()
    for idx, line in enumerate(lines):
        # Match markdown image tag
        if re.fullmatch(RE_MARKDOWN_IAMGE, line):
            # Get path of the image tag
            path = line[line.index('(')+1:-1]
            # Get the real path
            if os.path.exists(path):
                real_path = path
            elif os.path.exists(os.path.join(dirpath, path)):
                real_path = os.path.join(dirpath, path)
            else:
                click.echo(f'[x] Could not parse: {line}', color='red')
            real_path = os.path.normcase(real_path)
            # Turn image to base64 code
            with open(real_path, 'rb') as imgfile:
                b64img = base64.b64encode(imgfile.read()).decode()
            # Get image type
            img_suffix = os.path.splitext(real_path)
            img_type = img_suffix[-1].lower()[1:]
            # Turn to data url scheme
            lines[idx] = line.replace(path, f"data:image/{img_type};base64,{b64img}")
    # Output markdown file
    with open(output_filepath, 'w') as ofile:
        ofile.write('\n'.join(lines))

if __name__ == '__main__':
    run()