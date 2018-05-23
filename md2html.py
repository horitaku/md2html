# -*- coding: UTF-8 -*-

"""
md2html
-----

## 内容
   Markdownファイル（ファイル拡張子がmd)を読み込んでhtml形式のプロトタイプを出力する。  
   変換できるものはmarkdownの一部の項目に限られる。（次節参照）  
   出力の文字コードはUTF-8で、改行は\r\nのwindows形式である。  
   Python3用。  
 
## html形式へ変換可能な項目は以下に限られる
   1. #,##,###,#### を h1,h2,h3,h4タグにする。
   2. []() をhttpリンク(<a href)にする。参照目的のリンクの別定義（段落外・文章最後）は未対応。
   3. ![]()　を画像参照(<img src)にする
   4. ```で囲まれた部分をコード(<code>)扱いにする
   5: 先頭に4個以上の空白があればコード(<code>)扱いにする
   6.  -,+,* リスト表示(<ul><li>)にする。
   7: 1. 2. などを順番付きリスト(<ol><li>)にする。サブアイテムは未対応。
   8. 文末のスペース2個を<br />に変換する。但し、変換しない例外あり。
   9. 文章に<p> </p>を追加。但し、変換しない例外あり。
   10. 見出し。先頭行の次行が====,----のとき。

## スタイルシート
   出力のhtmlファイルとの同じディレクトリーに　style.css　を置くこと。  
    
## 動作方法
   python3 md2html.py [file name ex: README.md]

## 追加の操作
   htmlヘッダー内の　title（デフォルト：<h1></h1>で囲まれた文字） とdescription（デフォルト：先頭の文章）を適時編集すること。  
   html出力の中で不自然な箇所は適時 手修正すること。  
    
## その他
   強調、引用、水平線なども未対応。  
   python2の場合、文字コード変換やinputでエラーがでる。  
   Ubuntu環境でUnicodeDecoderError:が発生した場合は、geditなどを使って入力ファイルのエンコーディングをUTF-8に変更すること。  

"""
import sys
import os
import codecs
from sub_func import *

# Check version
# python 3.6.4 win32 (64bit)
# windows 10 (64bit)

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print("Usage: python3 md2html.py [file name ex: README.md]")
        sys.exit()
    else:
        fin=sys.argv[1]
        fname, ext = os.path.splitext(fin)
        fout= fname + '.html'
    
    fname, ext = os.path.splitext(fin)
    fout= fname + '.html'
    
    # 入力のmdファイルを読み込む
    f=open(fin, 'r')
    lines0 = f.readlines()
    f.close()
    
    # 改行コードを削除する
    lines0= del_cr(lines0)
    
    # conv2htmllで変換できる内容に書き換える
    listxs=pre_conv1(lines0)
    
    # html形式に変換する
    listxs=conv2html(listxs)
    
    # ヘッダー情報を追加する
    listxs=make_header(listxs)
    list0=get_title(listxs)  # list0 "必要に応じて内容を編集する"
    listxs.insert(5, '<title>' + list0 + '</title>')  
    list0=get_description(listxs) # list0 "必要に応じて内容を編集する"
    listxs.insert(6, '<meta name="description" content="' + list0 + '" />')  
    listxs=make_terminate(listxs)
    
    # 改行コードを追加する
    listxs= add_cr(listxs)
    
    # 既に出力と同一ファイルがある場合、上書きしてよいかどうか確認する
    if os.path.exists(fout):
        choice=input("Do you over write output file " + fout +" ?   Input  'yes' or 'no' [y/N]: ").lower()
        if not choice in ['y', 'ye', 'yes']:
             sys.exit()
    
    # 出力ファイルへUTF-8で書き出し
    f=codecs.open(fout, 'w','utf-8')
    for list0 in listxs:
        f.write(list0)
    f.close()

    # finish    
    print ('wrote out into ', fout)


