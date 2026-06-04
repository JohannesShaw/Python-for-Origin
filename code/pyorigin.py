import pandas as pd
import originpro as op
import os
from pathlib import Path

_FONT = {
    'Times New Roman': 345,
    'Arial': 69,
    '宋体': 1,
    '微软雅黑': 55,
    'inner': 5,
    'outer': 10
}

_RENAME_MAP = {
    'sec': 'Time(s)',
    'A': 'Current(A)',
    'V': 'Voltage(V)',
    'TLP': 'TLP(V)'
}

# 时间单位转换
_TIME_UNITS = {
    'sec': 1.0,
    'psec': 1e-12,
    'nsec': 1e-9,
    'fsec': 1e-15,
}

# 电流单位转换
_CURRENT_UNITS = {
    'A': 1.0,
    'mA': 1e-3,
    'uA': 1e-6,
    'nA': 1e-9,
    'pA': 1e-12,
    'fA': 1e-15,
}

# 电压单位转换
_VOLTAGE_UNITS = {
    'V': 1.0,
    'mV': 1e-3,
    'uV': 1e-6,
    'nV': 1e-9,
    'pV': 1e-12,
    'fV': 1e-15,
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
            x_axis_bold        = 1,                    # X轴数字是否加粗（1=加粗，0=不加粗）
            y_axis_bold        = 1,                    # Y轴数字是否加粗（1=加粗，0=不加粗）
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

        self.x_axis_font = _FONT[x_axis_font]
        self.y_axis_font = _FONT[y_axis_font]
        self.legend_font = _FONT[legend_font]

        self.x_axis_font_size = x_axis_font_size
        self.y_axis_font_size = y_axis_font_size
        self.legend_font_size = legend_font_size

        self.x_axis_thickness = x_axis_thickness
        self.y_axis_thickness = y_axis_thickness

        self.x_axis_bold = x_axis_bold
        self.y_axis_bold = y_axis_bold

        self.x_axis_label_pt = x_axis_label_pt
        self.y_axis_label_pt = y_axis_label_pt

        self.x_axis_label_font = _FONT[x_axis_label_font]
        self.y_axis_label_font = _FONT[y_axis_label_font]

        self.x_axis_ticks = _FONT[x_axis_ticks]
        self.y_axis_ticks = _FONT[y_axis_ticks]

        self.x_from = x_from
        self.x_to = x_to
        self.y_from = y_from
        self.y_to = y_to

# 内部类，用户不用关心
class __SaveParam:
    def __init__(self):
        self.args = None
        self.kwargs = None

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            return func(*args, **kwargs)
        return wrapper
    
    def get_template(self):

        return self.kwargs.get('template', '')

# 内部使用的装饰器，用于保存图像保存函数的参数，用户不用关心
__saver = __SaveParam()
op.new_graph = __saver(op.new_graph)

# 函数功能说明：配置一个图层的参数
# 参数说明：
# lay: 图层对象
# config: LayConfig类的实例，包含了图层的各种配置参数
# 使用示例：
# 生成两种配置,分别对应两个图层lay1和lay2,可以在LayConfig的构造函数中设置不同的参数来创建不同的配置实例,可以只改部分值,其他值就为默认值,例如：
# lay1_config = LayConfig(x_axis_title='Time (s)')
# lay2_config = LayConfig(x_axis_title='good ',y_axis_title='bad', y_axis_bold=0)
# 给lay1和lay2设置参数
# po.lay_set(lay1, lay1_config)
# po.lay_set(lay2, lay2_config)
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
        graph,          #图对象
        name:str,           #保存的图片名字，例如'1.png'
        path = None,    #保存路径
        width:int = 0,  #图像宽度，单位为像素，0表示使用默认宽度
        ratio:int = 0,  #图像宽高比，单位为百分比，0表示使用默认宽高比
        ):
    
    if not path:
        path = __path_set(name)

    if not __saver.get_template():
        graph.set_float('autoSize',1)
    op.find_graph(graph.name).save_fig(path,replace=True,width=width, ratio=ratio)

 
# 函数功能说明：保存项目
# 参数说明：
# name: 项目名称
# path: 项目保存路径
def project_save(name,path = None):

    if not path:
        path = __path_set(name)
    
    op.save(path)

# 解析列数据，提取数值和单位，并进行转换
def parse_column(series, unit_dict):
    pat = r'([-+]?\d*\.?\d+(?:[eE][+-]?\d+)?)\s*([a-zA-Z]+)'
    extracted = series.str.extract(pat)
    values = pd.to_numeric(extracted[0], errors='coerce')
    units = extracted[1].map(unit_dict)
    return values * units


# 函数功能说明：读取数据，根据文件类型自动选择读取方式
def read_data(file,path = None):

    if not path:
        path = __path_set(file)

    if 'csv' in str(path):
        df = pd.read_csv(path) 
    elif 'txt' in str(path):
        df = pd.read_csv(path,sep='\t')
    elif 'xlsx' in str(path):
        df = pd.read_excel(path)

    return df


# 函数功能说明：清洗数据
def clean(input_file, output_file):

    input_path = __path_set(input_file)
    output_path = __path_set(output_file)

    df = read_data(input_path)

    row = df.iloc[0]

    # 关键字匹配顺序：先长后短，避免 TLP 被 V 错误捕获
    patterns = [
        ('TLP', _RENAME_MAP['TLP'], _VOLTAGE_UNITS),
        ('sec', _RENAME_MAP['sec'], _TIME_UNITS),
        ('A',   _RENAME_MAP['A'],   _CURRENT_UNITS),
        ('V',   _RENAME_MAP['V'],   _VOLTAGE_UNITS),
    ]

    parsed_series = []
    name_counts = {}          # 记录每个 new_name 出现的次数，用于处理重名

    for col in df.columns:
        cell = str(row[col])
        for keyword, new_name, unit_dict in patterns:
            if keyword in cell:
                series_clean = parse_column(df[col], unit_dict)
                
                # 处理列名重复：第一个保留原名，后续加 _1, _2 ...
                if new_name in name_counts:
                    name_counts[new_name] += 1
                    unique_name = f"{new_name}_{name_counts[new_name]}"
                else:
                    name_counts[new_name] = 0
                    unique_name = new_name
                    
                parsed_series.append((unique_name, series_clean))
                break

    # 只输出识别到的列
    if parsed_series:
        result = pd.DataFrame({name: series for name, series in parsed_series})
    else:
        result = pd.DataFrame()

    result.to_csv(output_path, index=False, float_format='%.6e')

# 内部函数，用户不用关系
def __path_set(file:str):

    script_dir = Path(__file__).resolve().parent

    data_dir     = script_dir.parent / "data"
    image_dir    = script_dir.parent / "image"
    template_dir = script_dir.parent / "my_template"
    project_dir  = script_dir.parent / "project"

    if file.endswith(('.txt', '.csv', '.xlsx')):
        file_path = data_dir / file
    elif file.endswith('.png'):
        file_path = image_dir / file
    elif file.endswith('.otpu'):
        file_path = template_dir / file
    elif file.endswith('.opju'):
        file_path = project_dir / file

    return str(file_path)

