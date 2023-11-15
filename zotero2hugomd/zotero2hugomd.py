import json, sys, os
from IPython.core.display import HTML



def make_author_string(cite):
    output = ""
    if "author" in cite:
        output += ", ".join(map(lambda a : f'{a["family"]}, {a["given"][0]}.', cite["author"]))
    return output

def make_title_string(cite):
    title_string = cite["title"]
    if title_string[-1] != ".":
        title_string += "."
    if "URL" not in cite:
        return title_string 
    return f'<a href=\"{cite["URL"]}\">{title_string}</a>'
    
def make_date_string(cite):
    date_parts = cite["issued"]["date-parts"]
    return f"{date_parts[0][0]}"

def get_md_authors(cite):
    output = ""
    if "author" in cite:
        output += ", ".join(map(lambda a : f'{a["family"]}, {a["given"][0]}.', cite["author"]))
    return output

def get_md_year(cite):
    date_parts = cite["issued"]["date-parts"]
    return f"{date_parts[0][0]}"

def get_md_date(cite):
    return f"{get_md_year(cite)}-01-01"

def get_md_title(cite):
    return cite['title']

def get_md_journal(cite):
    if 'container-title' in cite:
        return cite['container-title']
    elif 'publisher' in cite:
        return cite['publisher']
    elif 'event-title' in cite:
        return cite['event-title']
    else:
        return False

def get_bibtex_id(cite):
    output = ""
    if "author" in cite:
        output += "_".join(map(lambda a : f'{a["family"]}', cite["author"]))
    output += get_md_year(cite)
    output += get_md_title(cite).split(" ")[0]
    output = "".join([c for c in output if c.isalnum() or c == "_"])
    return output.lower()

def get_md_link(cite):
    return cite["URL"]

def cite2md(cite):
    output = f"""+++
author = "{get_md_authors(cite)}"
date = "{get_md_date(cite)}"
year = "{get_md_year(cite)}"
title = "{get_md_title(cite)}"
"""
    
    journal = get_md_journal(cite)
    if (False != journal):
        output += f"journal = \"{journal}\"\n"
    
    if ("URL" in cite):
        output += f"link = \"{get_md_link(cite)}\"" + "\n"
    
    output += "+++"
    return output

def cite2filename(cite):
    return get_bibtex_id(cite) + ".md"

with open(sys.argv[1],"r+") as file:
    print(f"processing {sys.argv[1]}...")
    data = json.load(file)
    if (not os.path.exists("output")):
        os.mkdir("output")

    for cite in data:
        filename = cite2filename(cite)
        with open(f"output/{filename}","w") as f:
            f.write(cite2md(cite))
