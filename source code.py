'''
软件名：sequence tools
该软件主要用于
1. 系统发育分析前期从NCBI下载的序列更改ID，然后通过bioedit序列对比之后，便于拼接
2. 自己菌株测序后将序列ID批量改为NCBI提交所需要的固定格式
3. 不同位点基因的拼接
'''
'''
思路：
定义相关的功能函数，之后使用TK包进行界面化。然后使用pyinstaller打包成exe给普通用户使用
'''
#第一个功能，即修改下载的序列的ID，所需要的函数：
#定义一个更改单个文件中序列ID的函数
def modify_gene_name(file_path, contrast_file):
    # 导入os工具包
    import os
    # 将目录路径赋值给content_path
    content_path = os.path.split(file_path)[0]
    # 将文件名和其格式赋值给file_name_fm
    file_name_fm = "new" + os.path.split(file_path)[1]
    #以encoding="UTF-8"的方式读取文件并赋值给gene_data
    gene_data = open(file_path, encoding="UTF-8")
    #读取老旧名文件并赋值
    con_name = open(contrast_file, encoding="UTF-8")
    #创建一个新文件
    new_gene_name = open(os.path.join(content_path, file_name_fm), "w", encoding="UTF-8")
    #定义一个字典
    fd_name = {}
    #循环有老旧ID的文件，并将其值作为一个字典储存
    for len in con_name:
        len = len.strip().split("\t")
        fd_name[len[0]] = len[1]
    #循环主文件，进行读取
    for lien in gene_data:
        #通过“.”找到序列ID定义行，排除自己添加的自己菌株序列
        if "." in lien:
            #去空行和空格
            lien = lien.strip().split(" ")
            #取定义行中的genebank并赋值
            genebank = lien[0][1:-2]
            #genebank如果在字典中，则进行改ID
            if genebank in fd_name:
                #将新的ID赋值给lien
                lien = ">" + fd_name[genebank]
                #将新的定义行写入新文件中
                new_gene_name.write(lien)
                #加入空行
                new_gene_name.write("\n")
        else:
            #将序列写入新文件中
            new_gene_name.write(lien)
    #关闭相关文件
    gene_data.close()
    new_gene_name.close()
    con_name.close()
    #返回函数
    return
#定义一个可以更改多个文件的函数
def big_mgn(content_path, file_name, fd_file_name):
    # content_path = "D:\Workdata\otherman work\接\接"
    # file_name = ["ACT"]
    # fd_file_name = "fd_con_zxr"
    #导入工具包
    import os
    #因为从NCBI直接下载的序列为fasta格式，所以这里直接认为文件格式为fasta，并赋值
    file_fm = ".fasta"
    #定义一个txt格式后缀，并赋值
    fd_file_fm = ".txt"
    #给genebank/新名字的文件附上格式
    fd_file = fd_file_name + fd_file_fm
    #循环主文件的文件名
    for i in file_name:
        #附上格式给他
        filename_fm = i + file_fm
        #把这些参数写入modify_gene_name函数中，实现多个文件同时进行
        modify_gene_name(os.path.join(content_path, filename_fm), os.path.join(content_path, fd_file))
    #返回函数
    return
# big_mgn("D:\Workdata\otherman work\接\接", ["ACT", "CAL", "CHS"], "fd_con_zxr")
#导入界面化的工具包
from tkinter import *
#修改下载序列ID功能中，定义一个新函数用于窗口
def gui_gene():
    #通过窗口填入的目录路径内容将其赋值给a
    a = ent_content_path.get()
    #通过窗口填入的文件名，将其赋值给b
    b = file_name.get()
    #对b进行去空格
    b = b.strip()
    #由于有多个文件名，以，进行区分
    b = b.split(",")
    #将有genebank/新ID的文件名赋值给c
    c = fd_file_name.get()
    #abc作为参数写入批量处理文件的函数
    big_mgn(a, b, c)
    #返回函数
    return
#通过TK定义主窗口为fm_main
fm_main = Tk()
#定义主窗口左上角显示软件的名称
fm_main.title("sequence tools")
#设置窗口长宽
fm_main.geometry('970x500')
label_x = 20
button_x = 250
can1_label_y = 40
#设置标签
l_can1 = Label(fm_main, text = 'Rename', bg = 'green', fg = 'white', width = 133,height =1).place(x=20 , y = can1_label_y - 25)
l1 = Label(fm_main, text='目录路径如:C:\Windows\Boot\EFI').place(x=label_x,y=can1_label_y)
l2 = Label(fm_main, text='文件名称如:ACT,CHS,ITS,CAL').place(x=label_x,y=can1_label_y + 30)
l3 = Label(fm_main, text='genebank和newname的txt文件名称').place(x=label_x,y=can1_label_y + 60)
#在主窗口fm_main中添加一个宽度为100的文本框，用于填写文件目录路径
ent_content_path = Entry(fm_main, width=100)
#在主窗口fm_main中添加一个宽度为100的文本框，用于填写主文件名
file_name = Entry(fm_main, width=100)
#在主窗口fm_main中添加一个宽度为100的文本框，用于填写有genebank/新ID的文件的名字
fd_file_name = Entry(fm_main, width=100)
#在主窗口fm_main中添加一个启动gui——gene的函数
acting = Button(fm_main, text="Start", command=gui_gene, width=132)
can1_entry_y = can1_label_y
#在主窗口fm_main将上述的定义全部按自然顺序进行显示
ent_content_path.place(x=button_x,y=can1_entry_y)
file_name.place(x=button_x,y=can1_entry_y + 30)
fd_file_name.place(x=button_x,y=can1_entry_y + 60)
acting.place(x=label_x,y=can1_entry_y + 90)
#第二个功能，即格式NCBI化，方便提交序列
can2_label_y = 190
#设置标签
l_can2 = Label(fm_main, text = 'NCBI Formalized', bg = 'green', fg = 'white', width = 133,height =1).place(x=20 , y = can2_label_y - 25)
l4 = Label(fm_main, text='菌株学名').place(x=label_x,y=can2_label_y)
l5 = Label(fm_main, text="文件名及位点信息\n请按照说明文档中的格式进行填写").place(x=label_x,y=can2_label_y + 30)
l6 = Label(fm_main, text='目录路径').place(x=label_x,y=can2_label_y+ 80)
l7 = Label(fm_main, text='文件格式：.txt/.fasta/.fas').place(x=20,y=can2_label_y + 110)
# 定义一个将自己文件中的序列定义行更改为NCBI提交的固定格式的函数
def gg_modify(fug_name, gene_locad_imfor, file_path):
    # 导入工具包os
    import os
    # '''
    # #菌株学名
    # fug_name = "Exserohilum rostratum"
    #
    # 基因位点信息
    # gene_locad_imfor = "partial tubb gene for beta tubulin"
    #
    # 需要上传获得个genebank的文件路径
    # file_path = r"D:\Workdata\测序结果\get_genebank\TUB2.fasta"
    # '''
    # 打开文件
    data = open(file_path, encoding="UTF-8")
    # 将文件路径拆分为目录路径和文件名+格式
    content_path, filename_fm = os.path.split(file_path)
    # 将文件名+格式拆分为文件名和格式
    filename, file_fm = os.path.splitext(filename_fm)
    # 在目标路径下新建一个文件
    new_file_path = os.path.join(content_path, "new" + filename_fm)
    # 打开该新建文件
    data2 = open(new_file_path, "w", encoding="UTF-8")
    # 循环序列文件
    for line in data:
        # 找到定义行
        if ">" in line:
            # 将定义行去空格并列表化
            line = [line.strip()]
            # 去掉“>”
            line1 = line[0][1:]
            # 在定义行中添加序列名如：seq1
            line = ">" + filename + line1
            # 定义菌株名称
            isolate_name = "CN" + line1.upper()
            # 在定义行中添加格式化的内容
            line = line + " [organism=%s] [isolate=%s] %s" % (fug_name, isolate_name, gene_locad_imfor)
            # 将定义行写入新建文件中
            data2.write(line)
            # 将空行写入新建文件中
            data2.write("\n")
        else:
            # 降序列内容写入新建文件中
            data2.write(line)
    # 关闭相关文件
    data.close()
    data2.close()
    # 返回函数
    return
# 定义一个批量将自己文件中的序列定义行更改为NCBI提交的固定格式的函数
def big_ggmodify(fug_name, gene_locad_imfor, conment_path, file_fm):
    # fug_name = "Exserohilum rostratum"
    #     # gene_locad_imfor = {"fg3-ITS":"genomic DNA sequence contains 18S rRNA gene, ITS1, 5.8S rRNA gene and ITS2, strain CBS 132708",
    #     #                   "fg3-tub2":"partial tubb gene for beta tubulin, strain CBS 127233"}
    #     # conment_path = r"D:\Users\njlcl\PycharmProjects\lean_python\E_Rbiogene"
    # filefm = ".txt"
    # 导入工具包os
    import os
    # 循环字典gene_locad_imfor，
    for k in gene_locad_imfor:
        # 链接目录路径和文件名＋格式，形成文件路径
        file_path = os.path.join(conment_path, k + file_fm)
        # 通过key值k找到值并赋值给 solo_locad_infor
        solo_locad_infor = gene_locad_imfor[k]
        # 将参数写入gg_modify函数中
        gg_modify(fug_name, solo_locad_infor, file_path)
    # 返回函数
    return
# 第二个功能，格式化自己序列功能中，定义一个新函数用于窗口
def gui_gg_gene():
    # 获得文本框中菌株学名并赋值给a
    a = fug_name.get()
    b1 = lous_imform.get("0.0", "end")
    b = eval(b1)
    c = big_conmentpath.get()
    d = file_fm.get()
    big_ggmodify(a, b, c, d)
    return
#在主窗口fm_main中添加一个宽度为100的文本框，用于填写菌株学名
fug_name = Entry(fm_main, width=100)
#在主窗口fm_main中添加一个宽度为100的文本框，用于填写文件名和位点信息
lous_imform = Text(fm_main, width=100, height=3)
#在主窗口fm_main中添加一个宽度为100的文本框，用于填写目录路径
big_conmentpath = Entry(fm_main, width=100)
#在主窗口fm_main中添加一个宽度为100的文本框，用于填写文件格式
file_fm = Entry(fm_main, width=100)
#在主窗口fm_main中添加一个启动gui——gene的函数
acting1 = Button(fm_main, text="Start", command=gui_gg_gene, width=132)
fug_name.place(x=button_x, y=can2_label_y)
lous_imform.place(x=button_x, y=can2_label_y + 30)
big_conmentpath.place(x=button_x, y=can2_label_y + 80)
file_fm.place(x=button_x, y=can2_label_y + 110)
acting1.place(x=label_x, y=can2_label_y + 140)
#第三个功能，拼接序列
def splice(conment_path=str, file1=str, file2=str, format="fasta"):
    from Bio import SeqIO
    import os
    path1 = os.path.join(conment_path, file1+"." + format)
    path2 = os.path.join(conment_path, file2+"." + format)
    new_path = os.path.join(conment_path, "connection" + "." + format)
    orchid_dict1 = SeqIO.to_dict(SeqIO.parse(path1, format))
    orchid_dict2 = SeqIO.to_dict(SeqIO.parse(path2, format))
    b = [orchid_dict1[k]+orchid_dict2[k] for k in orchid_dict1]
    SeqIO.write(b, new_path, "fasta")
# splice(r"D:\Users\njlcl\PycharmProjects\modify_gene_ID_GUI", "ITS", "tub2")
def big_splice(conment_path = str, li = list, format = "fasta"):
    k = len(li)
    count = 0
    splice(conment_path, li[count], li[count+1], format)
    while count < k-2:
        count += 1
        splice(conment_path, "connection", li[count+1], format)
# big_splice(r"D:\Users\njlcl\PycharmProjects\modify_gene_ID_GUI", ["ITS","tub2", "CAL"])
can3_label_y = 390
def gui_splice():
    a = conment_path.get()
    b = li.get().split(",")
    big_splice(a, b)
conment_path = Entry(fm_main, width=100)
conment_path.place(x=button_x, y=can3_label_y)
l_can3 = Label(fm_main, text = 'Concatenate Sequence', bg = 'green', fg = 'white', width = 133,height =1).place(x=20 , y = can3_label_y - 25)
l8 = Label(fm_main, text='请输入文件所在目录路径').place(x=label_x, y=can3_label_y)
li = Entry(fm_main, width=100)
li.place(x=button_x, y=can3_label_y + 30)
l9 = Label(fm_main, text='请输入文件名称').place(x=label_x, y=can3_label_y + 30)
acting2 = Button(fm_main, text='Start', command=gui_splice, width=132)
acting2.place(x=label_x, y=can3_label_y+60)
#无限循环主窗口使其一直显示等待用户输入指令
fm_main.mainloop()
# pyinstaller --onefile *****.py
