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
    project_path = r'D:\VsCode File\Python Code\data_analysis\code'

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

    #将数据加载到表格里
    wks.from_df(pd.DataFrame({
        'Time(ns)': time_ns,            # 将这一列数据重新在origin sheet里重新命名为Time(ns)
        'Voltage(V)': df['Vout(V)'],    # 将这一列数据重新在origin sheet里重新命名为Voltage(V)
        'Current(A)': df['Iout(A)']     # 将这一列数据重新在origin sheet里重新命名为Current(A)
    }))


    gp1 = op.new_graph()                # 新建一个图(该图默认只有一个图层)
    lay1 = gp1[0]                       # 取该图的第一个图层绘图(默认只有一个图层)

    #type(str): 'l'(Line Plot) 's'(Scatter Plot) 'y' (Line Symbols) 'c' (Column) '?' auto(template)

    po.plot_set(wks, lay1, colx='Time(ns)', coly='Voltage(V)', color='blue', width=3, type='l')

    po.lay_set(lay1,po.LayConfig())
    
    po.graph_save(gp1,output_path)
  
    po.project_save('template.opju', project_path)

    # 关闭 Origin 应用程序
    #op.exit()                           
    
    print("绘图完成")

#绘制两个图的示例
def plot_time_x(input_file, output_file1, output_file2):

    # 读：固定目录里的文件，这里大家要修改为自己文件夹所在的路径，不然会读不到数据文件
    input_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file)   

    # 写：固定目录里的文件，这里大家要修改为自己文件夹所在的路径，不然会把图片输出到错误的位置
    output_path1 = os.path.join(r'D:\VsCode File\Python Code\data_analysis\image', output_file1)  
    output_path2 = os.path.join(r'D:\VsCode File\Python Code\data_analysis\image', output_file2)

    df = po.read_data(input_path)
    
    time_ns = df['Time(s)'] * 1e9 #df['Time(s)']表达的是我取的Time(s)这一列的数据，这一列每一行的值都会乘以1e9

    # 显示绘图过程
    op.set_show(True)  

    #打开新的项目
    op.new()

    # W普通表格工作簿
    wb = op.new_book('w', 'Data')
    
    #在 book里新建sheet,这里可以新建很多sheet
    #   wks = wb.add_sheet() 自动命名为sheet1,sheet2,......
    #   wks1 = wb.add_sheet()
    #   wks2 = wb.add_sheet()
    wks = wb.add_sheet()
    
    wks.from_df(pd.DataFrame({
        'Time(ns)': time_ns,#将这一列数据重新在origin sheet里重新命名为Time(ns)
        'Voltage(V)': df['Vout(V)'],#将这一列数据重新在origin sheet里重新命名为Voltage(V)
        'Current(A)': df['Iout(A)']#将这一列数据重新在origin sheet里重新命名为Current(A)
    }))

    gp1 = op.new_graph()
    lay1 = gp1[0]#取该图的第一个图层绘图
    
    #开始画图，
    #x轴的数据来自于Time(ns)列
    #y轴的数据来自于Voltage(V)列
    #type表示要绘制线条形式
    #type(str): 'l'(Line Plot) 's'(Scatter Plot) 'y' (Line Symbols) 'c' (Column) '?' auto(template)
    plot1 = lay1.add_plot(wks, colx='Time(ns)', coly='Voltage(V)',type = 'l')
    
    plot1.set_float('line.width', 3)  # 设置线宽为 1.5
    plot1.color = 'black' # 设置线条颜色为黑色


    gp1.lname = 'Voltage vs Time'#该图片的名字为Voltage vs Time

    po.lay_set(lay1,po.LayConfig())

    # 图2
    gp2 = op.new_graph()
    lay2 = gp2[0]
    plot2 = lay2.add_plot(wks, colx='Time(ns)', coly='Current(A)',type = 'l')

    # 设置线宽为 1.5
    plot2.set_float('line.width', 3) 
    plot2.color = 'black'

    gp2.lname = 'Current vs Time'

    # 设置横纵坐标字体和大小
    po.lay_set(lay2,po.LayConfig())
    
    # 找到绘制的图片
    g1 = op.find_graph('graph1')
    g2 = op.find_graph('graph2')

    # 导出为图片
    # 该函数还有很多参数，可以设置导出图片的宽度等等，大家可以点进函数看看
    g1.save_fig(output_path1)
    g2.save_fig(output_path2)

    # 保存为 Origin 项目文件
    op.save(os.path.join(r'D:\VsCode File\Python Code\data_analysis\code', 'Analysis_Result.opju'))

    op.exit()  # 关闭 Origin 应用程序
    
    print("绘图完成")
    
#在一个图绘制两条线的示例
def plot_two_lines(input_file,input_file1,output_file):

    # 读：固定目录里的文件
    input_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file)   

    # 读：固定目录里的文件
    input_path1 = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file1)  

    # 写：固定目录里的文件
    output_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\image', output_file)  
    
    df = po.read_data(input_path)
    
    df1 = po.read_data(input_path1)

    time_ns = df['Time(s)'] * 1e9

    #展示绘图过程
    op.set_show(True)

    op.new()

    # W普通表格工作簿
    wb = op.new_book('w', 'Data')
    
    #在 book里新建sheet
    wks = wb.add_sheet()

    wks.from_df(pd.DataFrame({
        'Time(ns)': time_ns,
        'Voltage(V)': df['Vout(V)'],
        'Voltage(V)1': df1['Vout(V)'],
    }))

    # 图1
    gp1 = op.new_graph()#绘制一个图
    lay1 = gp1[0]#获取图层1

    #画第一条线
    plot1 = lay1.add_plot(wks, colx='Time(ns)', coly='Voltage(V)',type='l')

    plot1.set_float('line.width', 3)  # 设置线宽为 3
    plot1.color = 'black'

    #画第二条线
    plot2 = lay1.add_plot(wks, colx='Time(ns)', coly='Voltage(V)1',type='l')

    plot2.set_float('line.width', 3)  # 设置线宽为 3
    plot2.color = 'red'

    po.lay_set(lay1,po.LayConfig())

    gp1.lname = 'Voltage vs Voltage1'

    op.lt_exec('page.autoSize=1;')

    #导出为图片
    g = op.find_graph('graph1')

    g.save_fig(output_path)

    #保存为 Origin 项目文件
    op.save(os.path.join(r'D:\VsCode File\Python Code\data_analysis\code', 'Analysis_Result.opju'))

    # 关闭 Origin 应用程序
    #op.exit()  

    print("绘图完成")
    
#在一个图中绘制多个图层，重点就是改变gp = op.new_graph(template='PAN2HORZ')使用的模板
def plot_two_in_graph(input_file,output_file):

    input_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file)
    output_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\image', output_file) 

    df = po.read_data(input_path)
    
    time_ns = df['Time(s)'] * 1e9 #df['Time(s)']表达的是我取的Time(s)这一列的数据，这一列每一行的值都会乘以1e9

    # 显示绘图过程
    op.set_show(True)  

    #打开新的项目
    op.new()

    # W普通表格工作簿
    wb = op.new_book('w', 'Data')
    
    #在 book里新建sheet,这里可以新建很多sheet
    #   wks = wb.add_sheet() 自动命名为sheet1,sheet2,......
    #   wks1 = wb.add_sheet()
    #   wks2 = wb.add_sheet()
    wks = wb.add_sheet()
    
    wks.from_df(pd.DataFrame({
        'Time(ns)': time_ns,#将这一列数据重新在origin sheet里重新命名为Time(ns)
        'Voltage(V)': df['Vout(V)'],#将这一列数据重新在origin sheet里重新命名为Voltage(V)
        'Current(A)': df['Iout(A)']#将这一列数据重新在origin sheet里重新命名为Current(A)
    }))

    # 图1
    # template表示绘制图形的模板，该模板有很多,会在下文进行部分展示
    gp = op.new_graph(template='PAN2HORZ')# 使用 Origin 内置的2面板水平模板,也可用 'PAN2VERT' 上下排列,还有'PAN4'可以放四个图

    lay1 = gp[0]
    lay2 = gp[1]

    lay1.add_plot(wks, colx='Time(ns)', coly='Voltage(V)',type = 'l')
    lay2.add_plot(wks, colx='Time(ns)', coly='Current(A)',type = 'l')

    lay1.axis('x').title = 'Time (nsec)'#x轴的名字为Time (nsec)
    lay1.axis('y').title = 'Voltage (V)'#y轴的名字为Voltage (V)

    lay2.axis('x').title = 'Time (nsec)'#x轴的名字为Time (nsec)
    lay2.axis('y').title = 'Current(A)'#y轴的名字为Current(A)

    gp.lname = 'V & C'

    #op.lt_exec('page.autoSize=1;')

    lay1.rescale()
    lay2.rescale()


    g = op.find_graph('graph3')
    g.save_fig(output_path)

    # 保存为 Origin 项目文件
    op.save(os.path.join(r'D:\VsCode File\Python Code\data_analysis\code', 'Analysis_Result.opju'))

    op.exit()  # 关闭 Origin 应用程序
    
    print("绘图完成")