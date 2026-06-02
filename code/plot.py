import pyorigin as po
import originpro as op
import pandas as pd
import os


def template(input_file,output_file):

    # 设置读取文件的路径
    input_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file)

    # 设置输出图片的路径
    output_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\image', output_file)

    # 设置保存origin工程文件的路径
    project_path = r'D:\VsCode File\Python Code\data_analysis\project'

    # 读取数据
    df = po.read_data(input_path)

    # 打开origin软件
    op.set_show(True)  

    #新建工程
    op.new()

    #新建一个工作表格
    wb = op.new_book('w', 'Data')
    
    #在 book里新建sheet,这里可以新建很多sheet
    #   wks = wb.add_sheet() 自动命名为sheet1,sheet2,......
    #   wks1 = wb.add_sheet()
    #   wks2 = wb.add_sheet()
    wks = wb.add_sheet()
    
    time_ns = df['Time(s)'] * 1e9

    #将数据加载到sheet里
    wks.from_df(pd.DataFrame({
        'Time(ns)': time_ns,            # 将这一列数据重新在origin sheet里重新命名为Time(ns)
        'Voltage(V)': df['Vout(V)'],    # 将这一列数据重新在origin sheet里重新命名为Voltage(V)
        'Current(A)': df['Iout(A)']     # 将这一列数据重新在origin sheet里重新命名为Current(A)
    }))


    gp1 = op.new_graph()                # 新建一个图(该图默认只有一个图层)
    lay1 = gp1[0]                       # 取该图的第一个图层绘图(默认只有一个图层)

#------------------------参数设置------------------------
    po.plot_set(wks, lay1, colx='Time(ns)', coly='Voltage(V)', color='black', width=3, type='l')

    po.lay_set(lay1,po.LayConfig())
    
    po.graph_save(gp1,output_path)
  
    po.project_save('template1.opju', project_path)

#------------------------参数设置------------------------
    # 关闭 Origin 应用程序
    #op.exit()                           
    
    print("绘图完成")

#绘制两个图的示例
def plot_time_x(input_file, output_file1, output_file2):

    
    input_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file)   

    output_path1 = os.path.join(r'D:\VsCode File\Python Code\data_analysis\image', output_file1)  
    output_path2 = os.path.join(r'D:\VsCode File\Python Code\data_analysis\image', output_file2)

    project_path = r'D:\VsCode File\Python Code\data_analysis\project'


    df = po.read_data(input_path)
    
    time_ns = df['Time(s)'] * 1e9 

    op.set_show(True)  

    op.new()

    wb = op.new_book('w', 'Data')
    
    wks = wb.add_sheet()
    
    wks.from_df(pd.DataFrame({
        'Time(ns)': time_ns,
        'Voltage(V)': df['Vout(V)'],
        'Current(A)': df['Iout(A)']
    }))

    gp1 = op.new_graph()
    lay1 = gp1[0]
    
    po.plot_set(wks, lay1, colx='Time(ns)', coly='Voltage(V)', color='black', width=3, type='l')

    po.lay_set(lay1,po.LayConfig())

    # 图2
    gp2 = op.new_graph()
    lay2 = gp2[0]

    po.plot_set(wks, lay2, colx='Time(ns)', coly='Current(A)', color='black', width=3, type='l')

    po.lay_set(lay2,po.LayConfig())
    
    po.graph_save(gp1,output_path1)
    po.graph_save(gp2,output_path2)

    po.project_save('template2.opju', project_path)

    #op.exit()  

    print("绘图完成")
    
#在一个图绘制两条线的示例
def plot_two_lines(input_file,input_file1,output_file):


    input_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file)   


    input_path1 = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file1)  

    output_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\image', output_file)  
    
    project_path = r'D:\VsCode File\Python Code\data_analysis\project'

    df = po.read_data(input_path)
    
    df1 = po.read_data(input_path1)

    #展示绘图过程
    op.set_show(True)

    op.new()

    wb = op.new_book('w', 'Data')

    wks = wb.add_sheet()

    time_ns = df['Time(s)'] * 1e9

    wks.from_df(pd.DataFrame({
        'Time(ns)': time_ns,
        'Voltage(V)': df['Vout(V)'],
        'Voltage(V)1': df1['Vout(V)']
    }))

    gp1 = op.new_graph()
    lay1 = gp1[0]

    po.plot_set(wks, lay1, colx='Time(ns)', coly='Voltage(V)', color='black', width=3, type='l')

    po.plot_set(wks, lay1, colx='Time(ns)', coly='Voltage(V)1', color='red', width=3, type='l')

    po.lay_set(lay1,po.LayConfig())

    po.graph_save(gp1,output_path)

    po.project_save('template3.opju', project_path)

    # 关闭 Origin 应用程序
    #op.exit()  
    
    print("绘图完成")
    
#在一个图中绘制多个图层，重点就是改变gp = op.new_graph(template='PAN2HORZ')使用的模板
def plot_two_in_graph(input_file,output_file):

    input_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file)
    output_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\image', output_file) 

    project_path = r'D:\VsCode File\Python Code\data_analysis\project'

    df = po.read_data(input_path)
    
    op.set_show(True)  

    op.new()

    wb = op.new_book('w', 'Data')
    
    wks = wb.add_sheet()
    
    time_ns = df['Time(s)'] * 1e9 

    wks.from_df(pd.DataFrame({
        'Time(ns)': time_ns,
        'Voltage(V)': df['Vout(V)'],
        'Current(A)': df['Iout(A)']
    }))

    # 使用 Origin 内置的2面板水平模板,也可用 'PAN2VERT' 上下排列,还有'PAN4'可以放四个图
    gp = op.new_graph(template='PAN2VERT')

    lay1 = gp[0]
    lay2 = gp[1]

    po.plot_set(wks, lay1, colx='Time(ns)', coly='Voltage(V)', color='black', width=3, type='l')
    po.plot_set(wks, lay2, colx='Time(ns)', coly='Current(A)', color='black', width=3, type='l')

    po.lay_set(lay1,po.LayConfig())
    po.lay_set(lay2,po.LayConfig())

    po.graph_save(gp,output_path)

    po.project_save('template4.opju', project_path)

    # 关闭 Origin 应用程序
    #op.exit()  
    
    print("绘图完成")