import pyorigin as po
import originpro as op
import pandas as pd


def template(input_file,output_file):

    # 读取数据
    df = po.read_data(input_file)

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


    gp1 = po.create_graph()                # 新建一个图(该图默认只有一个图层)
    lay1 = gp1[0]                       # 取该图的第一个图层绘图(默认只有一个图层)

#------------------------参数设置------------------------

    po.plot_set(wks, lay1, colx='Time(ns)', coly='Voltage(V)', color='black', width=3, type='l')

    po.lay_set(gp1,lay1,po.LayConfig())
    
#------------------------参数设置------------------------

    print("绘图完成")

#------------------------保存设置------------------------

    po.graph_save(gp1,output_file)
  
    po.project_save('template1.opju')

#------------------------保存设置------------------------

    # 关闭 Origin 应用程序
    #op.exit()                           
    

#绘制两个图的示例
def plot_time_x(input_file, output_file1, output_file2):


    df = po.read_data(input_file)
    
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

    gp1 = po.create_graph()
    lay1 = gp1[0]
#------------------------参数设置------------------------

    po.plot_set(wks, lay1, colx='Time(ns)', coly='Voltage(V)', color='black', width=3, type='l')

    po.lay_set(gp1,lay1,po.LayConfig())

    # 图2
    gp2 = po.create_graph()
    lay2 = gp2[0]

    po.plot_set(wks, lay2, colx='Time(ns)', coly='Current(A)', color='black', width=3, type='l')

    po.lay_set(gp1,lay2,po.LayConfig())

#------------------------参数设置------------------------

    print("绘图完成")

#------------------------保存设置------------------------

    po.graph_save(gp1,output_file1)
    po.graph_save(gp2,output_file2)

    po.project_save('template2.opju')

#------------------------保存设置------------------------

    
#在一个图绘制两条线的示例
def plot_two_lines(input_file,input_file1,output_file):

    df = po.read_data(input_file)
    
    df1 = po.read_data(input_file1)

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

    gp1 = po.create_graph()
    lay1 = gp1[0]

#------------------------参数设置------------------------

    po.plot_set(wks, lay1, colx='Time(ns)', coly='Voltage(V)', color='black', width=3, type='l')

    po.plot_set(wks, lay1, colx='Time(ns)', coly='Voltage(V)1', color='red', width=3, type='l')

    po.lay_set(gp1,lay1,po.LayConfig())

#------------------------参数设置------------------------

    print("绘图完成")

#------------------------保存设置------------------------

    po.graph_save(gp1,output_file)

    po.project_save('template3.opju')

#------------------------保存设置------------------------
    # 关闭 Origin 应用程序
    #op.exit()  
    
    
#在一个图中绘制多个图层，重点就是改变gp = op.new_graph(template='PAN2HORZ')使用的模板
def plot_two_in_graph(input_file,output_file):

    df = po.read_data(input_file)
    
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
    # gp = op.new_graph(template='PAN2VERT') 使用内置的不用加 .otpu 
    # 使用自己的模板要加 .otpu ,路径已经写好,这里只需要写模板名字即可，如下所示
    # gp = op.new_graph(template='example.otpu')
    gp = po.create_graph(template='PAN2VERT')
    
    lay1 = gp[0]
    lay2 = gp[1]

#------------------------参数设置------------------------

    po.plot_set(wks, lay1, colx='Time(ns)', coly='Voltage(V)', color='black', width=3, type='l')
    po.plot_set(wks, lay2, colx='Time(ns)', coly='Current(A)', color='black', width=3, type='l')

    po.lay_set(gp,lay1,po.LayConfig())
    po.lay_set(gp,lay2,po.LayConfig())

#------------------------参数设置------------------------

    print("绘图完成")
    
#------------------------保存设置------------------------

    po.graph_save(gp,output_file)

    po.project_save('template4.opju')
#------------------------保存设置------------------------

    # 关闭 Origin 应用程序
    #op.exit()  
    