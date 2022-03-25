import re
import base64

def parse(filename:str, encoding:str="utf-8") -> list[str]:
    if filename is None:
        return None
    with open(filename, "r", encoding=encoding) as f:
        lines = f.readlines()
    return lines

def md_turn(img:str):
    path = img[img.find("(")+1:-1]
    try:
        with open(path, "rb") as f:
            img = img.replace(path, "data:image/png;base64," + base64.b64encode(f.read()).decode())
    except:
        pass
    return img

def html_turn(img:str):
    begin = img.find("src=\"") + 5
    end = img.find("\"", begin)
    path = img[begin:end]
    try:
        with open(path, "rb") as f:
            img = img.replace(path, "data:image/png;base64," + base64.b64encode(f.read()).decode())
    except:
        pass
    return img

def turn(lines:list[str]):
    if lines is None:
        return None
    result = []
    remd = re.compile("!\[.*\]\(.*\)")
    rehtml = re.compile("<img src=.*/>")
    for line in lines:
        mdimg = remd.findall(line)
        htmlimg = rehtml.findall(line)
        for img in mdimg:
            line = line.replace(img, md_turn(img))
        for img in htmlimg:
            line = line.replace(img, html_turn(img))
        result.append(line)
    return result

def img2base64(filename:str):
    lines = parse(filename)
    if lines is None:
        return False
    lines = turn(lines)
    with open("modified_"+filename, "w") as f:
        f.writelines(lines)
    return True

img2base64("test.md")
