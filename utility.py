import json
import ast

from google import search
from config import *


def add_dict(json_data, txtname):
    path = os.path.join(rootpath, 'output', txtname)
    if not os.path.exists(path):
        with open(path, 'w') as f:
            # json.dump(data, f)
            f.write(str(json_data))
    else:
        with open(path, 'a') as f:
            f.write("\n")
            # json.dump(data, f)
            f.write(str(json_data))


def read_dict(txtname):
    path = os.path.join(rootpath, 'output', txtname)
    if os.path.exists(path):
        with open(path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip("\n")
                data = ast.literal_eval(line)
                # data = json.dumps(line)
                # data = json.loads(data)
                # data = json.loads(line)
                print (data)
                print (type(data))


def google_search(keyword):
    for url in search(keyword, stop=20):
        print(url)


def get_keyword1(df):
    return df['First Name'] + " " + df['Last Name'] + ' at ' + df['Company / Account']


dict_data = [{'a':'b', 'c':'d'}, {'a':'f', 'c':'h'}]
def make_doc(doc_name, dict_data):
    from docx import Document
    from docx.shared import Inches

    document = Document()

    # document.add_heading(Heading, 0)

    p = document.add_paragraph('A plain paragraph having some ')
    p.add_run('bold').bold = True
    p.add_run(' and some ')
    p.add_run('italic.').italic = True

    document.add_heading('Heading, level 1', level=1)
    document.add_paragraph('Intense quote', style='IntenseQuote')

    document.add_paragraph(
        'first item in unordered list', style='ListBullet'
    )
    document.add_paragraph(
        'first item in ordered list', style='ListNumber'
    )

    document.add_picture('https://t47.thumb.pipl.com/cgi-bin/fdt.fcgi?hg=160&wd=160&th=1&favicon=1&dsid=55&fd=www.linkedin.com&def=1&rem=1&eurl=AE2861B20B7D6E22D4C9479C5C7387EF9C9CE823D35EABEA7AAFCEB4822D4BE6583BC7DC98D6B5210198C7212B2FD21476031CB6F10DC74A8CC8271B4F1A186FEA9BC63952E279BD491EA6BC&dsid2=&eurl2=&vid=', width=Inches(1.25))

    table = document.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Qty'
    hdr_cells[1].text = 'Id'
    hdr_cells[2].text = 'Desc'
    for item in dict_data:
        row_cells = table.add_row().cells
        row_cells[0].text = str(item['a'])
        row_cells[1].text = str(item['c'])

    document.add_page_break()

    document.save(doc_name)


def excel_addColumns(filename, column_data):
    from openpyxl import load_workbook
    from pandas import ExcelWriter
    book = load_workbook(filename)
    writer = ExcelWriter(filename, engine='openpyxl')
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)



# google_search("Ariel Crohn at Coverys")
# https://pipl.com/search/?q=jimmy.bourdon%40parexel.com&in=5&l=&sloc=

# make_doc("webina", dict_data)


# a = {'a':'b', 'c':'d'}
# b = {'e':'f', 'g':'h'}
# add_json(a, 'a.txt')
# add_json(b, 'a.txt')
read_dict("a.txt")
