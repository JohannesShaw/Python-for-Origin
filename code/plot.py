import pandas as pd
import originpro as op
#这是用来合并文件路径的库，只调用了里面的os.path.join（）函数
import os

font = {
    'Times New Roman': 345,
    'Arial': 69,
    '宋体': 1,
    '微软雅黑': 55
}

class LayConfig:

    def __init__(self,
                 
                 x_axis_title       = 'x',
                 y_axis_title       = 'y',
                 x_axis_font        = 'Times New Roman',
                 y_axis_font        = 'Times New Roman',
                 legend_font        = 'Times New Roman',
                 x_axis_font_size   = 36,
                 y_axis_font_size   = 36,
                 legend_font_size   = 26,
                 x_axis_thickness   = 3,
                 y_axis_thickness   = 3,
                 x_axis_bold        = 1,
                 y_axis_bold        = 1,
                 x_axis_label_pt    = 26,
                 y_axis_label_pt    = 26,
                 x_axis_label_font  = 'Times New Roman',
                 y_axis_label_font  = 'Times New Roman',
                 x_axis_ticks       = 5,
                 y_axis_ticks       = 5,
                 x_from             = None,
                 x_to               = None,
                 y_from             = None,
                 y_to               = None
                 ):
        
        self.x_axis_title = x_axis_title
        self.y_axis_title = y_axis_title

        self.x_axis_font = font[x_axis_font]
        self.y_axis_font = font[y_axis_font]
        self.legend_font = font[legend_font]

        self.x_axis_font_size = x_axis_font_size
        self.y_axis_font_size = y_axis_font_size
        self.legend_font_size = legend_font_size

        self.x_axis_thickness = x_axis_thickness
        self.y_axis_thickness = y_axis_thickness

        self.x_axis_bold = x_axis_bold
        self.y_axis_bold = y_axis_bold

        self.x_axis_label_pt = x_axis_label_pt
        self.y_axis_label_pt = y_axis_label_pt

        self.x_axis_label_font = font[x_axis_label_font]
        self.y_axis_label_font = font[y_axis_label_font]

        self.x_axis_ticks = x_axis_ticks
        self.y_axis_ticks = y_axis_ticks

        self.x_from = x_from
        self.x_to = x_to
        self.y_from = y_from
        self.y_to = y_to


def lay_set(lay, config):

    # 设置坐标轴标题
    lay.axis('x').title = config.x_axis_title
    lay.axis('y').title = config.y_axis_title

    # 字体 & 大小
    lay.label('xb').set_int('font', config.x_axis_font)
    lay.label('xb').set_int('fsize', config.x_axis_font_size)
    
    lay.label('yl').set_int('font', config.y_axis_font)
    lay.label('yl').set_int('fsize', config.y_axis_font_size)

    lay.label('legend').set_int('font', config.legend_font)
    lay.label('legend').set_int('fsize', config.legend_font_size)

    # 坐标轴线厚度
    lay.set_float('x.thickness', config.x_axis_thickness)
    lay.set_float('y.thickness', config.y_axis_thickness)
    
    # 坐标轴加粗：True→1，False→0
    lay.set_float('x.label.bold', config.x_axis_bold )
    lay.set_float('y.label.bold', config.y_axis_bold )

    # 刻度数字大小 & 字体
    lay.set_float('x.label.pt', config.x_axis_label_pt)
    lay.set_float('y.label.pt', config.y_axis_label_pt)
    lay.set_float('x.label.font', config.x_axis_label_font)
    lay.set_float('y.label.font', config.y_axis_label_font)

    # 刻度朝向
    lay.set_float('x.ticks', config.x_axis_ticks)
    lay.set_float('y.ticks', config.y_axis_ticks)

    # 自动设置坐标轴的范围
    lay.rescale()

    # 轴范围
    if config.x_from is not None:
        lay.set_float('x.from', config.x_from)
    if config.x_to is not None:
        lay.set_float('x.to', config.x_to)
    if config.y_from is not None:
        lay.set_float('y.from', config.y_from)
    if config.y_to is not None:
        lay.set_float('y.to', config.y_to)


def read_data(input_file):

    if 'csv' in input_file:#判断是不是csv文件
        df = pd.read_csv(input_file)
    elif 'txt' in input_file:#判断是不是txt文件
        df = pd.read_csv(input_file,sep='\t')
    elif 'xlsx' in input_file:#判断是不是xlsx文件
        df = pd.read_excel(input_file)

    return df
 

def template(input_file,output_file):

    # 读：固定目录里的文件，这里大家要修改为自己文件夹所在的路径，不然会读不到数据文件
    input_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file)
    # 写：固定目录里的文件，这里大家要修改为自己文件夹所在的路径，不然会把图片输出到错误的位置
    output_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\image', output_file)

    df = read_data(input_path)

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
        'Time(ns)': time_ns,#将这一列数据重新在origin sheet里重新命名为Time(ns)
        'Voltage(V)': df['Vout(V)'],#将这一列数据重新在origin sheet里重新命名为Voltage(V)
        'Current(A)': df['Iout(A)']#将这一列数据重新在origin sheet里重新命名为Current(A)
    }))

    gp1 = op.new_graph()
    lay1 = gp1[0] #取该图的第一个图层绘图
    #开始画图
    #x轴的数据来自于Time(ns)列
    #y轴的数据来自于Voltage(V)列
    #type表示要绘制线条形式
    #type(str): 'l'(Line Plot) 's'(Scatter Plot) 'y' (Line Symbols) 'c' (Column) '?' auto(template)
    plot1 = lay1.add_plot(wks, colx='Time(ns)', coly='Voltage(V)',type = 'l')

    plot1.set_float('line.width', 3)  # 设置线宽为 1.5
    plot1.color = 'red' # 设置线条颜色为黑色

    lay_set(lay1,LayConfig())
    
    # 找到绘制的图片
    gp1.lname = 'Voltage vs Time'#该图片的名字为Voltage vs Time

    gp1.set_float('autoSize',1)

    g1 = op.find_graph('graph1')
    # 导出为图片
    # 该函数还有很多参数，可以设置导出图片的宽度等等，大家可以点进函数看看
    g1.save_fig(output_path)
  
    # 将origin工程文件保存到指定位置，名字默认为'Analysis_Result.opju'(可自己修改)，这里大家要修改为自己想保存的路径，
    op.save(os.path.join(r'D:\VsCode File\Python Code\data_analysis\code', 'Analysis_Result.opju'))

    #op.exit()  # 关闭 Origin 应用程序
    
    print("绘图完成")


#绘制两个图的示例
def plot_time_x(input_file, output_file1, output_file2):
    # 读：固定目录里的文件，这里大家要修改为自己文件夹所在的路径，不然会读不到数据文件
    input_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file)   

    # 写：固定目录里的文件，这里大家要修改为自己文件夹所在的路径，不然会把图片输出到错误的位置
    output_path1 = os.path.join(r'D:\VsCode File\Python Code\data_analysis\image', output_file1)  
    output_path2 = os.path.join(r'D:\VsCode File\Python Code\data_analysis\image', output_file2)

    # 根据文件类型读取数据
    if 'csv' in input_file:#判断是不是csv文件
        df = pd.read_csv(input_path)
    elif 'txt' in input_file:#判断是不是txt文件
        df = pd.read_csv(input_path,sep='\t')
    elif 'xlsx' in input_file:#判断是不是xlsx文件
        df = pd.read_excel(input_path)
    
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

    lay1.axis('x').title = 'Time (nsec)'#x轴的名字为Time (nsec)
    lay1.axis('y').title = 'Voltage (V)'#y轴的名字为Voltage (V)

    gp1.lname = 'Voltage vs Time'#该图片的名字为Voltage vs Time

    # 设置横纵坐标标题字体和大小
    #xb代表x bottom 也就是位于图片下面的x轴的标题
    #xt代表x top 也就是位于图片上面的x轴的标题
    #yl代表y left 也就是位于图片左边的y轴的标题
    #yr代表y right 也就是位于图片右边的y轴的标题
    
    xb = lay1.label('xb')#获取xb这个对象，也即是下边x轴的标题，方便对其进行字体或者大小的改变
    xb.set_int('font', 345)#改变xb这个对象的字体，345代表是Times New Romans, 69代表是Arial, 1代表是宋体, 55代表是微软雅黑
    xb.set_int('fsize', 36)#改变xb这个对象的字体大小

    yl = lay1.label('yl')#获取yl这个对象，也即是左边y轴的标题，方便对其进行字体或者大小的改变
    yl.set_int('font', 345)#改变yl这个对象的字体，345代表是Times New Romans, 69代表是Arial, 1代表是宋体, 55代表是微软雅黑
    yl.set_int('fsize', 36)#改变yl这个对象的字体大小

    le = lay1.label('legend')#获取le这个对象，也即是右上角的标题，方便对其进行字体或者大小的改变
    le.set_int('font', 345)  # 设置字体为345代表是Times New Romans, 69代表是Arial, 1代表是宋体, 55代表是微软雅黑
    le.set_int('fsize', 26)  # 设置字体大小为 20

    #调整坐标轴线厚度
    op.lt_exec('layer.x.thickness=3;')
    op.lt_exec('layer.y.thickness=3;')

    #调整坐标轴字体
    op.lt_exec('layer.x.label.font=font(times new roman);')
    op.lt_exec('layer.y.label.font=font(times new roman);')

    #坐标轴字体是否加粗1代表加粗，0代表不加粗
    op.lt_exec('layer.x.label.bold=1;')
    op.lt_exec('layer.y.label.bold=1;')

    #坐标轴数字大小
    op.lt_exec('layer.x.label.pt=26;')
    op.lt_exec('layer.y.label.pt=26;')

    op.lt_exec('page.autoSize=1;')
    
    lay1.rescale()#刷新有关该图层的设置
    
    # 图2
    gp2 = op.new_graph()
    lay2 = gp2[0]
    plot2 = lay2.add_plot(wks, colx='Time(ns)', coly='Current(A)',type = 'l')

    # 设置线宽为 1.5
    plot2.set_float('line.width', 3) 
    plot2.color = 'black'

    lay2.axis('x').title = 'Time (nsec)'
    lay2.axis('y').title = 'Current (A)'

    gp2.lname = 'Current vs Time'

    # 设置横纵坐标字体和大小
    xb2 = lay2.label('xb')
    xb2.set_int('font', 345)
    xb2.set_int('fsize', 36)

    yl2 = lay2.label('yl')
    yl2.set_int('font', 345)
    yl2.set_int('fsize', 36)

    le2 = lay2.label('legend')
    le2.set_int('font', 345)  # 设置字体为 345 对应字体为Times New Roman
    le2.set_int('fsize', 26)  # 设置字体大小为 28

    op.lt_exec('layer.x.thickness=3;')
    op.lt_exec('layer.y.thickness=3;')

    #调整坐标轴字体
    op.lt_exec('layer.x.label.font=font(times new roman);')
    op.lt_exec('layer.y.label.font=font(times new roman);')

    #坐标轴字体是否加粗1代表加粗，0代表不加粗
    op.lt_exec('layer.x.label.bold=1;')
    op.lt_exec('layer.y.label.bold=1;')

    #坐标轴数字大小
    op.lt_exec('layer.x.label.pt=26;')
    op.lt_exec('layer.y.label.pt=26;')

    op.lt_exec('page.autoSize=1;')
    
    lay2.rescale()
    
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
    
     # 根据文件类型读取数据
    if 'csv' in input_file:#判断是不是csv文件
        df = pd.read_csv(input_path)
    elif 'txt' in input_file:#判断是不是txt文件
        df = pd.read_csv(input_path,sep='\t')
    elif 'xlsx' in input_file:#判断是不是xlsx文件
        df = pd.read_excel(input_path)
    
     # 根据文件类型读取数据
    if 'csv' in input_file:#判断是不是csv文件
        df1 = pd.read_csv(input_path1)
    elif 'txt' in input_file:#判断是不是txt文件
        df1 = pd.read_csv(input_path1,sep='\t')
    elif 'xlsx' in input_file:#判断是不是xlsx文件
        df1 = pd.read_excel(input_path1)

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

    #设置横纵坐标标题
    lay1.axis('x').title = 'Time (nsec)'
    lay1.axis('y').title = 'Voltage (V)'

    #设置横纵坐标字体和大小
    xb = lay1.label('xb')
    xb.set_int('font', 345)  # 设置字体为 345 对应  
    xb.set_int('fsize', 36)  # 设置字体大小为 36

    yl = lay1.label('yl')
    yl.set_int('font', 345)  # 设置字体为 345 对应
    yl.set_int('fsize', 36)  # 设置字体大小为 36

    le = lay1.label('legend')
    le.set_int('font', 345)  # 设置字体为 345 对应字体为Times New Roman
    le.set_int('fsize', 26)  # 设置字体大小为 26

    #调整坐标轴线厚度
    op.lt_exec('layer.x.thickness=3;')
    op.lt_exec('layer.y.thickness=3;')

    #调整坐标轴字体
    op.lt_exec('layer.x.label.font=font(times new roman);')
    op.lt_exec('layer.y.label.font=font(times new roman);')

    #坐标轴字体是否加粗1代表加粗，0代表不加粗
    op.lt_exec('layer.x.label.bold=1;')
    op.lt_exec('layer.y.label.bold=1;')

    #坐标轴数字大小
    op.lt_exec('layer.x.label.pt=26;')
    op.lt_exec('layer.y.label.pt=26;')

    gp1.lname = 'Voltage vs Voltage1'

    op.lt_exec('page.autoSize=1;')
    #设置第一个图的名称
    #刷新该图层，使设置生效
    lay1.rescale()

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

    # 根据文件类型读取数据
    if 'csv' in input_file:#判断是不是csv文件
        df = pd.read_csv(input_path)
    elif 'txt' in input_file:#判断是不是txt文件
        df = pd.read_csv(input_path,sep='\t')
    elif 'xlsx' in input_file:#判断是不是xlsx文件
        df = pd.read_excel(input_path)
    
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