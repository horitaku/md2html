# -*- coding: UTF-8 -*-

import sys

"""
 (md形式からhtml形式へ変換可能な項目は以下に限られる）
    1: #,##,###,#### を h1,h2,h3,h4タグにする
    2:[]() をhttpリンク(<a href)にする
    3:![]()　を画像参照(<img src)にする
    4:```で囲まれた部分をコード(<code>)扱いにする
    5:先頭に4個以上の空白があればコード(<code>)扱いにする
    6: -,+,* リスト表示(<ul><li>)にする
    7: 1. 2.  順番付きリストを(<ol><li>)にする
    8:文末のスペース2個を<br />に変換する。但し、変換しない例外あり。
    9:文章に<p> </p>を追加。但し、変換しない例外あり。
    10: 先頭が<br />の行は、そのまま出力する。

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
        if s2 >s1 and s3 > s2 and s4 > s3 and (s4-s3)> 1:  # 条件に()が空白の場合を追加
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
        if s2 >s1 and s3 > s2 and s4 > s3 and (s4-s3) > 1 : # 条件に()が空白の場合を追加
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

def count_head_space(list0):
    list1=str.lstrip(list0,' ')
    len0=len(list0) - len(list1)
    #print ('number of space ', len0)
    return len0


def head_space_code1(listxs):
    #　空白が4個以上ある行のとき　''' で囲む
    s1=-1
    s2=-1
    n0=0
    rt_code=False
    for i,list0 in enumerate(listxs):
        if s1 == -1 and count_head_space(list0) >= 4:
            s1=i
            s2=i
            n0=count_head_space(list0)
            rt_code=True
        elif s1 > -1:
            if count_head_space(list0) >= 4:
                s2=i
            else:
                break
    
    if rt_code:
        for i in range(s1,s2+1):
            listxs[i]= listxs[i][n0:] # 先頭の空白を削除する
        listxs.insert(s1,'<div class="highlighter-rouge"><div class="highlight"><pre class="highlight"><code>')
        listxs.insert(s2+2,'</code></pre></div></div>')
    
    
    return listxs, rt_code
    

def conv_head_space_code(listxs):
    # 先頭　空白4個以上の行をコードを変換する
    while(True):
        listxs, rt_code =head_space_code1(listxs)
        if not rt_code :
            break
    return listxs






def conv_li1(listx, state_list, i):
    # <li></li>だけ変換する　<ul></ul>タグは後で追加すること。
    state_li_start, state_hanging_indents, state_nest_indents = get_state_code()
    
    if state_list[i] == state_li_start:
        listx = '<li>' + str.lstrip(listx[1:],' ')
        if state_list[i+1] == state_hanging_indents:
            listx= listx + '<br />'
        else:
            listx= listx + '</li>'
    
    if state_list[i] == state_hanging_indents  or state_list[i] == state_nest_indents:
        if state_list[i+1] == state_hanging_indents :    # hangin indentsが継続中
            listx= str.lstrip(listx,' ') 
            if not (listx.startswith('- ') or listx.startswith('+ ') or listx.startswith('* ')): # リストでないとき
                listx= str.lstrip(listx,' ') + '<br />'
        elif state_list[i+1] == state_nest_indents :    # nest indentsが継続中
            listx= str.lstrip(listx,' ') 
            if not (listx.startswith('- ') or listx.startswith('+ ') or listx.startswith('* ')): # リストでないとき
                listx= str.lstrip(listx,' ') + '<br />'
        else:
            listx= str.lstrip(listx,' ') + '</li>'
    
    return listx

def get_state_code():
    state_li_start=1
    state_hanging_indents=3
    state_nest_indents=4
    return state_li_start, state_hanging_indents, state_nest_indents

def conv_ul1(listxs):
    # <ul></ul>を1組分だけ変換する
    s1=-1
    s2=-1
    hanging_indents=0
    state_list = [0 for i in range( len(listxs)+1 )]
    state_li_start, state_hanging_indents, state_nest_indents = get_state_code()
    rt_code=False
    
    nest_indents=-1
    
    for i,list0 in enumerate(listxs):
        if s1== -1 and (list0.startswith('- ') or list0.startswith('+ ') or list0.startswith('* ')):
            s1=i
            s2=i
            hanging_indents= count_head_space( list0[1:]) + 1
            state_list[i]=state_li_start
            # print ('...1st, list0, hanging_indents', list0, hanging_indents)
            rt_code=True
        elif s1 >-1:
            if not (list0.startswith('- ') or list0.startswith('+ ') or list0.startswith('* ')):
                if count_head_space( list0) == hanging_indents:
                    state_list[i]=state_hanging_indents
                    # print ('...hanging_indents')
                    s2=i
                else:
                    # hanging_indentsに一致しないがindentsがある
                    n0=count_head_space( list0)
                    list2=list0[n0:]
                    # 内部にlist宣言がある場合
                    if (list2.startswith('- ') or list2.startswith('+ ') or list2.startswith('* ')):
                        # nest list の先頭行のとき
                        if state_list[i-1]==state_li_start:
                            nest_indents=n0
                            state_list[i]=state_nest_indents
                            # print ('...nest_indents')
                            s2=i
                        elif n0==nest_indents:
                            state_list[i]=state_nest_indents
                            # print ('...nest_indents')
                            s2=i
                    else:
                        s2=i-1
                        break
            else:
                s2=i
                hanging_indents= count_head_space( list0[1:]) + 1
                state_list[i]=state_li_start
                # print ('...next, list0, hanging_indents', list0, hanging_indents)
    
    
    if rt_code:
        for i in range(s1,s2+1):
            listxs[i]=conv_li1(listxs[i], state_list, i)
        listxs.insert(s1,'<ul>')
        listxs[s2+1]= str.rstrip(listxs[s2+1],'/li>')  # </li>を次の</ul>行に移動
        listxs[s2+1]= str.rstrip(listxs[s2+1],'<')     # >が欠ける対策で２行に分ける
        listxs.insert(s2+2,'</li></ul>')
    
    return listxs, rt_code
    
def conv_ul(listxs):
    # <ul></ul>に変換する
    while(True):
        listxs, rt_code =conv_ul1(listxs)
        if not rt_code :
            break
    return listxs

def check_olist(list0):
    s1= list0.find('. ')   # 数字. を見つける
    list1=list0
    rtcode= False
    if s1 > 0 and list0[0].isdigit() and list0[:s1].isdigit():  # . 前の部分が数字か
        list1=list0[s1+2:]
        rtcode=True
    
    return rtcode, list1

def conv_li2(listx):
    # <li></li>だけ変換する　<ol></ol>タグは後で追加すること。
    _ , list1 = check_olist(listx)
    listx='<li>' + list1 + '</li>'
    return listx
    
def conv_ol1(listxs):
    # <ol></ol>を1組分だけ変換する
    s1=-1
    s2=-1
    rt_code=False
    for i,list0 in enumerate(listxs):
        rt_code1, _ = check_olist(list0)
        if s1== -1 and rt_code1:
            s1=i
            s2=i
            rt_code=True
        if s1 >-1 and not rt_code1 :
            s2=i-1
            break

    if rt_code:
        for i in range(s1,s2+1):
            listxs[i]=conv_li2(listxs[i])
        listxs.insert(s1,'<ol>')
        listxs.insert(s2+2,'</ol>')
    
    return listxs, rt_code
    
def conv_ol(listxs):
    # <ol></ol>に変換する
    while(True):
        listxs, rt_code =conv_ol1(listxs)
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
    elif listx.startswith('<ol>'):
        state_code=2  # <ol> ～</ol>の間
        return False, state_code
    elif listx.startswith('</ol>'):
        state_code=0
        return False, state_code
    elif listx.startswith('<br />'): # 先頭が<br />の行
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
    
    # <ol></ol>に変換する
    listxs=conv_ol(listxs)
    
    # 文末のスペース2個を<br />に変換する
    listxs=conv_br(listxs)
    
    # 先頭　空白4個以上の行をコードを変換する
    listxs=conv_head_space_code(listxs)
    
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
    
    # TABを空白4個に変換する
    listxs2=[]
    for listxs0 in listxs:
        listxs2.append(listxs0.expandtabs(4))
    
    # < >を特殊文字に置き換える
    # 但し、先頭が<br />の行は変換しない
    listxs3=[]
    for list0 in listxs2:
        if not list0.startswith('<br />'):
            list0=list0.replace('<','&lt;')
            list0=list0.replace('>','&gt;')
            listxs3.append(list0)
        else:
            listxs3.append(list0)
    
    return listxs3




