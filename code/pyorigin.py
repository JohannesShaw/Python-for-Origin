import pandas as pd
import originpro as op
import os

FONT = {
    'Times New Roman': 345,
    'Arial': 69,
    '宋体': 1,
    '微软雅黑': 55,
    'inner': 5,
    'outer': 10
}

# 定义一个类来存储图层配置参数
class LayConfig:

    def __init__(
            self,
            x_axis_title       = 'x',                  # X轴标题文字
            y_axis_title       = 'y',                  # Y轴标题文字
            x_axis_font        = 'Times New Roman',    # X轴标题字体
            y_axis_font        = 'Times New Roman',    # Y轴标题字体
            legend_font        = 'Times New Roman',    # 图例字体
            x_axis_font_size   = 36,                   # X轴标题字体大小
            y_axis_font_size   = 36,                   # Y轴标题字体大小
            legend_font_size   = 26,                   # 图例字体大小
            x_axis_thickness   = 3,                    # X轴线条粗细
            y_axis_thickness   = 3,                    # Y轴线条粗细
            x_axis_bold        = 1,                    # X轴标题是否加粗（1=加粗，0=不加粗）
            y_axis_bold        = 1,                    # Y轴标题是否加粗（1=加粗，0=不加粗）
            x_axis_label_pt    = 26,                   # X轴刻度标签字体大小
            y_axis_label_pt    = 26,                   # Y轴刻度标签字体大小
            x_axis_label_font  = 'Times New Roman',    # X轴刻度标签字体
            y_axis_label_font  = 'Times New Roman',    # Y轴刻度标签字体
            x_axis_ticks       = 'inner',              # X轴刻度朝向
            y_axis_ticks       = 'inner',              # Y轴刻度朝向
            x_from             = None,                 # X轴起始值（None表示自动计算）
            x_to               = None,                 # X轴结束值（None表示自动计算）
            y_from             = None,                 # Y轴起始值（None表示自动计算）
            y_to               = None                  # Y轴结束值（None表示自动计算）
                ):
        
        self.x_axis_title = x_axis_title
        self.y_axis_title = y_axis_title

        self.x_axis_font = FONT[x_axis_font]
        self.y_axis_font = FONT[y_axis_font]
        self.legend_font = FONT[legend_font]

        self.x_axis_font_size = x_axis_font_size
        self.y_axis_font_size = y_axis_font_size
        self.legend_font_size = legend_font_size

        self.x_axis_thickness = x_axis_thickness
        self.y_axis_thickness = y_axis_thickness

        self.x_axis_bold = x_axis_bold
        self.y_axis_bold = y_axis_bold

        self.x_axis_label_pt = x_axis_label_pt
        self.y_axis_label_pt = y_axis_label_pt

        self.x_axis_label_font = FONT[x_axis_label_font]
        self.y_axis_label_font = FONT[y_axis_label_font]

        self.x_axis_ticks = FONT[x_axis_ticks]
        self.y_axis_ticks = FONT[y_axis_ticks]

        self.x_from = x_from
        self.x_to = x_to
        self.y_from = y_from
        self.y_to = y_to

# 函数功能说明：配置一个图层的参数
# 参数说明：
# lay: 图层对象
# config: LayConfig类的实例，包含了图层的各种配置参数
# 使用示例：
# 生成两种配置,分别对应两个图层lay1和lay2,可以在LayConfig的构造函数中设置不同的参数来创建不同的配置实例,可以只改部分值,其他值就为默认值,例如：
# lay_config1 = LayConfig(x_axis_title='Time (s)')
# lay_config2 = LayConfig(x_axis_title='good ',y_axis_title='bad', y_axis_bold=0)
# 给lay1和lay2设置参数
# po.lay_set(lay1, lay_config1)
# po.lay_set(lay2, lay_config2)
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

# 函数功能说明：在一个图层中绘制一条线
def plot_set(
        data,               #worksheet数据源
        lay,                #图层对象
        colx,               #worksheet中作为x轴数据的列名
        coly,               #worksheet中作为y轴数据的列名
        color='black',      #线条颜色
        width:float = 3,    #线条宽度
        type='l'            #图表类型，'l'(Line Plot) 's'(Scatter Plot) 'y' (Line Symbols) 'c' (Column) '?' auto(template)
        ):

    plot = lay.add_plot(data, colx=colx, coly=coly, type=type)
    plot.set_float('line.width', width)  # 设置线宽
    plot.color = color

# 函数功能说明：保存图像
def graph_save(
        graph,              #图对象
        path,               #保存路径
        width:int = 0,      #图像宽度，单位为像素，0表示使用默认宽度
        ratio:int = 0,      #图像宽高比，单位为百分比，0表示使用默认宽高比
        name='graph'        #图像名称
        ):
    
    graph.name = name
    graph.set_float('autoSize',1)
    op.find_graph(graph.name).save_fig(path,replace=True,width=width, ratio=ratio)

# 函数功能说明：读取数据，根据文件类型自动选择读取方式
def read_data(input_file):

    if 'csv' in input_file:#判断是不是csv文件
        df = pd.read_csv(input_file)
    elif 'txt' in input_file:#判断是不是txt文件
        df = pd.read_csv(input_file,sep='\t')
    elif 'xlsx' in input_file:#判断是不是xlsx文件
        df = pd.read_excel(input_file)

    return df
 
# 函数功能说明：保存项目
# 参数说明：
# name: 项目名称
# path: 项目保存路径
def project_save(name,path):

    path1 = os.path.join(path, name)
    op.save(path1)
