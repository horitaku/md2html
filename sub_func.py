# -*- coding: UTF-8 -*-

import sys

"""
 (md形式からhtml形式へ変換可能な項目は以下に限られる）
    1: #,##,###,#### を h1,h2,h3,h4タグにする
    2:[]() をhttpリンク(<a href)にする
    3:![]()　を画像参照(<img src)にする
    4:```で囲まれた部分をコード(<code>)扱いにする
    5: -,+,* リスト表示(<ul><li>)にする
    6:文末のスペース2個を<br />に変換する。但し、変換しない例外あり。
    7:文章に<p> </p>を追加。但し、変換しない例外あり。

"""


# Check version
# python 3.6.4 win32 (64bit)
# windows 10 (64bit)


def del_cr(listx0):
    listx1=[]
    for list0 in listx0:
        # 改行を削除する \r \n
        listx=list0.replace('\r','')
        listx=listx.replace('\n','')
        listx1.append(listx)
    return listx1

def add_cr(listx0):
    listx1=[]
    for list0 in listx0:
        # 改行コードを追加する
        listx=list0 +'\r'+'\n'
        listx1.append(listx)
    return listx1


def conv_h(listx):
    # #,##,###,####をh1,h2,h3,h4に変換する
    if listx.startswith('# '):
        listx=listx.replace('# ','<h1>',1)
        listx=listx+'</h1>'
    elif listx.startswith('## '):
        listx=listx.replace('## ','<h2>',1)
        listx=listx+'</h2>'
    elif listx.startswith('### '):
        listx=listx.replace('### ','<h3>',1)
        listx=listx+'</h3>'
    elif listx.startswith('#### '):
        listx=listx.replace('#### ','<h4>',1)
        listx=listx+'</h4>'
    return listx


def conv_img1(listx):
    # ![]()のimgを1組分だけ変換する。　<ul></ul>タグは後で追加すること。
    s1=listx.find('![')
    s2=listx.find(']')
    s3=listx.find('(')
    s4=listx.find(')')
    if s1 >= 0:
        if s2 >s1 and s3 > s2 and s4 > s3:
            #print ( listx[s1+2:s2], listx[s3+1:s4] )
            #print (listx[0:s1] + listx[s4+1:])
            list1= '<img src="' + listx[s3+1:s4] + '"' + ' alt="' + listx[s1+2:s2] + '" >'
            list2= listx[0:s1] + list1 + listx[s4+1:]
            return list2, True
        else:
            return listx, False
    else:
        return listx, False

def conv_img(listx):
    # ![]()のimgを変換する
    while(True):
        listx, rt_code =conv_img1(listx)
        if not rt_code :
            break
    return listx

def conv_http1(listx):
    # conv_imgより後に呼び出すこと
    # []()のhttpを1組分だけ変換する。
    s1=listx.find('[')
    s2=listx.find(']')
    s3=listx.find('(')
    s4=listx.find(')')
    
    if s1 >= 0:
        if s2 >s1 and s3 > s2 and s4 > s3:
            #print ( listx[s1+1:s2], listx[s3+1:s4] )
            #print (listx[0:s1] + listx[s4+1:])
            list3= listx[s3+1:s4]
            list3 = list3.replace('&lt;','')
            list3 = list3.replace('&gt;','')
            list1= '<a href="' + list3 + '">' + listx[s1+1:s2] + '</a>'
            list2= listx[0:s1] + list1 + listx[s4+1:]
            return list2, True
        else:
            return listx, False
    else:
        return listx, False

def conv_http(listx):
    # conv_imgより後に呼び出すこと
    # []()のhttpを変換する
    while(True):
        listx, rt_code =conv_http1(listx)
        if not rt_code :
            break
    return listx

def conv_hih(lines0):
    # h,img,httpを変換する
    listxs=[]
    for list0 in lines0:
        listx=conv_h(list0)
        listx=conv_img(listx)
        listx=conv_http(listx)  # conv_imgより後に呼び出すこと
        listxs.append(listx)
    return listxs



def conv_code1(listxs):
    # ```で囲まれたコードを1組分だけ変換する
    # <pre> </pre> も追加されるので注意
    s1=-1
    s2=-1
    rt_code=False
    for i,list0 in enumerate(listxs):
        if list0.startswith('```'):
            if s1 < 0 :
                s1=i
            else:
                s2=i
                rt_code=True
                break
    if rt_code:
        listxs[s1]='<div class="highlighter-rouge"><div class="highlight"><pre class="highlight"><code>'
        listxs[s2]='</code></pre></div></div>'
    
    return listxs, rt_code

def conv_code(listxs):
    # ```で囲まれたコードを変換する
    while(True):
        listxs, rt_code =conv_code1(listxs)
        if not rt_code :
            break
    return listxs


def conv_li1(listx):
    # <li></li>だけ変換する　<ul></ul>タグは後で追加すること。
    if listx.startswith('- '):
        listx=listx.replace('- ','<li>',1)
        listx=listx+'</li>'
    elif listx.startswith('+ '):
        listx=listx.replace('+ ','<li>',1)
        listx=listx+'</li>'
    elif listx.startswith('* '):
        listx=listx.replace('* ','<li>',1)
        listx=listx+'</li>'
    return listx
    
def conv_ul1(listxs):
    # <ul></ul>を1組分だけ変換する
    s1=-1
    s2=-1
    rt_code=False
    for i,list0 in enumerate(listxs):
        if s1== -1 and (list0.startswith('- ') or list0.startswith('+ ') or list0.startswith('* ')):
            s1=i
            s2=i
            rt_code=True
        if s1 >-1 and not (list0.startswith('- ') or list0.startswith('+ ') or list0.startswith('* ')):
            s2=i-1
            break

    if rt_code:
        for i in range(s1,s2+1):
            listxs[i]=conv_li1(listxs[i])
        listxs.insert(s1,'<ul>')
        listxs.insert(s2+2,'</ul>')
    
    return listxs, rt_code
    
def conv_ul(listxs):
    # <ul></ul>に変換する
    while(True):
        listxs, rt_code =conv_ul1(listxs)
        if not rt_code :
            break
    return listxs


def conv_br1(listx):
    # 1行の文末のスペース2個を<br />に変換する
    if listx.endswith('  '):
        listx=listx[:-2] # 最後のスペース2個を削除
        if len(listx) > 0 : # 空行は無視する
            listx=listx + '<br />'
    return listx

def conv_br(listxs):
    # 文末のスペース2個を<br />に変換する
    listxs2=[]
    for list0 in listxs:
        listxs2.append( conv_br1(list0))
    return listxs2
    

def check_p_start(listx,state_code):
    if listx.startswith('<h'):
        return False, state_code
    elif listx.startswith('<div class="highlighter-rouge"><div class="highlight"><pre class="highlight"><code>'):
        state_code=1   # <div code ～</code の間
        return False, state_code
    elif listx.startswith('</code></pre></div></div>'):
        state_code=0
        return False, state_code
    elif listx.startswith('<ul>'):
        state_code=2  # <ul> ～</ul>の間
        return False, state_code
    elif listx.startswith('</ul>'):
        state_code=0
        return False, state_code
    elif len(listx) == 0:  # 空白の行は無視する
        return False, state_code
    else:
        return True, state_code

def conv_p(listxs):
    # <p></p>を挿入する
    listxs2=[]
    s1=-1
    state_code=0
    for i,list0 in enumerate(listxs):
        rt_code, state_code= check_p_start(list0, state_code)
        if rt_code and state_code ==0 and s1 <0:
            listxs2.append('<p>' + list0)
            s1=i  # <p>の始まり区間の行番号をセット
        elif s1 >=0 :
            if (not rt_code)  or  state_code != 0:  #<p>対象区間でない　<div code, <ul　区間でない場合
                s1=-1 # リセット
                listxs2[len(listxs2)-1]= listxs2[len(listxs2)-1]  + '</p>' # 1行前の末尾に</p>を追加
            listxs2.append(list0)
        else:
            listxs2.append(list0)
    
    if s1 >=0:  # 最後の行で閉じる場合
    	listxs2[ len(listxs2)-1]= listxs2[ len(listxs2)-1] + ('</p>')
    
    return listxs2


def make_header(listxs):
    listxs.insert(0,"<!DOCTYPE html>")
    listxs.insert(1, '<html lang="ja">')
    listxs.insert(2, '<head>')
    listxs.insert(3, '<meta charset="UTF-8">')
    listxs.insert(4, '<meta name="viewport" content="width=device-width, initial-scale=1">')
    listxs.insert(5, '<link href="style.css" rel="stylesheet">')
    listxs.insert(6, '</head>')
    listxs.insert(7, "<body>")
    listxs.insert(8, '<div class="container-lg px-3 my-5 markdown-body">')
    
    return listxs


def make_terminate(listxs):
    listxs.append("</div>")
    listxs.append("</body>")
    listxs.append("</html>")
    
    return listxs


def conv2html(lines0):
    # h,img,httpを変換する
    listxs= conv_hih(lines0)
    
    # ```で囲まれたコードを変換する
    listxs=conv_code(listxs)
    
    # <ul></ul>に変換する
    listxs=conv_ul(listxs)
    
    # 文末のスペース2個を<br />に変換する
    listxs=conv_br(listxs)
    
    # <p></p>を挿入する
    listxs=conv_p(listxs)
    
    return listxs



"""
 header情報　取得のための関数

"""
def get_title( listxs):
    # はじめの、先頭行が <h1>の内容を返す
    list0=""
    for listxs0 in listxs:
        if listxs0.startswith('<h1>'):
            list0= listxs0.replace('<h1>',"")
            list0= list0.replace('</h1>',"")
            break
    return list0

def get_description( listxs):
    # はじめの、先頭行が <p>の内容を返す
    list0=""
    for listxs0 in listxs:
        if listxs0.startswith('<p>'):
            list0= listxs0.replace('<p>',"")
            list0= list0.replace('</p>',"")
            list0= list0.replace('<br />',"")
            break
    return list0



"""
conv2htmllで変換できる内容に書き換える

"""
def pre_conv1( listxs):
    
    # 見出し。
    # ２行目が ===== -----ならば　1行目に# を追加して、2行目を削除する
    if listxs[1].startswith('====') or listxs[1].startswith('----'):
        listxs[0]= '# ' + listxs[0]
        del listxs[1]
    
    #　空白が4個ある行のとき　''' で囲む
    listxs2=[]
    s1=-1
    s2=-1
    c0=0
    for i,listxs0 in enumerate(listxs):
        listxs1=listxs0
        if listxs0.startswith('    ') and len(str.lstrip(listxs0)) > 0:  #　且つ、空白行でないとき
            if s1 < 0: # 空白4個の開始
                s1=i
                s2=i
            elif i > s1: # 2行目以降
                s2=i
            listxs1=str.lstrip(listxs0)  # 先頭の空白を削除する
        elif s1 > 0: # 空白4個の終了
            listxs2.insert(s1+c0,'```')
            listxs2.append('```')
            s1=-1
            s2=-1
            c0+=2  #　２行追加した分をカウント
        
        listxs2.append( listxs1)
    
    if s1 > 0:
        listxs2.insert(s1+c0,'```')
        listxs2.append('```')
        s1=-1
        s2=-1
    
    # < >を特殊文字に置き換える
    listxs3=[]
    for list0 in listxs2:
        list0=list0.replace('<','&lt;')
        list0=list0.replace('>','&gt;')
        listxs3.append(list0)
    
    return listxs3

