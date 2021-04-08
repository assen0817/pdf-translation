import PyPDF2
import time
# HTMLデータ抽出ライブラリ
from bs4 import BeautifulSoup
import urllib.parse
import re
from selenium import webdriver
# モジュールのインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox

# ファイル選択ダイアログの表示
root = tkinter.Tk()
root.withdraw()

# ここの1行を変更　fTyp = [("","*")] →　fTyp = [("","*.csv")]
fTyp = [("","*.pdf")]

iDir = os.path.abspath(os.path.dirname(__file__))
file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)





pdf = 'Biomedical Signal Processing and Control'


def cut_text(text):
    text = text.replace( '\n' , ' ')
    text = re.split('(?<=\. )', text)


    cut_t = []
    c_t = ''
    for t in text:
        c_t += f'{t}\n\n'
        if len(c_t) > 4000:
            cut_t.append(c_t)
            c_t = ''

    return cut_t


def get_jp(text):

    s_quote = urllib.parse.quote(text)
    url = f'https://www.deepl.com/translator#en/ja/{s_quote}'

    # PhantomJSをSelenium経由で利用します.
    driver = webdriver.PhantomJS()

    # PhantomJSで該当ページを取得＆レンダリングします
    driver.get(url)

    time.sleep(10)

    # レンダリング結果をPhantomJSから取得します.
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    return soup.find(id='target-dummydiv').text


reader = PyPDF2.PdfFileReader(file)

text = ''
for i in range(reader.getNumPages()):
    page = reader.getPage(i)
    text += page.extractText()

text = cut_text(text)
text_jp = []
print(f'{len(text) * 10}秒')
for t in text:
    text_jp.append(get_jp(t))

text = list(zip_longest(text,text_jp))
filename = str(file.split('/')[-1])
with open(f'{filename}.txt', mode='w', encoding='utf-8') as f:
    for m in text:
        t = m[0].split('\n\n')
        t_jp = m[1].split('\n\n')

        t = list(zip_longest(t, t_jp))
        for m in t:
            f.write(f'{m[0]}\n')
            f.write(f'{m[1]}\n\n')