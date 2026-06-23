"""
此文件为底层实现, 优化了打包环境下的路径兼容性和控制台输出安全性
"""

import sys
import pandas as pd
import originpro as op
from pathlib import Path
from dataclasses import dataclass, field
from typing import ClassVar
import re

# ================= 核心优化 1：安全打印与路径基准 =================

def safe_print(*args, **kwargs):
    """防止在打包为无控制台(-w)模式时，print导致程序崩溃"""
    try:
        if sys.stdout is not None:
            print(*args, **kwargs)
    except Exception:
        pass

def get_base_dir() -> Path:
    """
    获取程序运行的基准目录。
    - 开发环境：返回当前脚本所在的目录。
    - 打包环境：返回 .exe 文件所在的目录（确保 data/image 等文件夹与 exe 同级即可）。
    """
    if getattr(sys, 'frozen', False):
        # 打包后：exe 所在目录作为基准
        return Path(sys.executable).resolve().parent
    else:
        # 开发时：当前脚本所在目录的上一级（保持与原代码逻辑一致）
        return Path(__file__).resolve().parent.parent

# ================================================================

"""坐标轴类"""
@dataclass
class AxisConfig:
    
    # ========== 坐标轴标题相关设置 ==========
    title: str                              = ''                # 标题，默认为空
    title_font: str                         = 'Times New Roman' # 标题字体名称
    title_color: str | tuple[int,int,int]   = 'black'           # 标题颜色，支持颜色名称字符串或RGB元组,例如title_color=(123,23,23)
    title_bold: int                         = 1                 # 标题是否加粗，1为加粗，0为不加粗
    title_italic:int                        = 0                 # 标题是否斜体，1为斜体，0为不斜体
    title_underline:int                     = 0                 # 标题是否加下划线，1为加，0为不加
    title_font_size: int                    = 36                # 标题字体大小（磅值）

    # ========== 坐标轴刻度数字相关设置 ==========
    axis_thickness: float                   = 3                 # 坐标轴轴线的线宽（粗细）
    axis_bold: int                          = 1                 # 刻度数字是否加粗，1为加粗，0为不加粗
    axis_pt: int                            = 26                # 刻度数字的字体大小（磅值）
    axis_font: str                          = 'Times New Roman' # 刻度数字的字体名称
    axis_color: str | tuple[int,int,int]    = 'black'           # 坐标轴及刻度数字颜色，支持颜色名称或RGB元组
    axis_ticks: str                         = 'inner'           # 刻度朝向，'inner'朝内，'outer'朝外
    axis_show:int                           = 3                 #  0不显示,1显示左下前,2显示右上后,3都显示

    # ========== 坐标轴范围设置 ==========
    begin: float | None                     = None              # 坐标轴起始值，None表示自动
    end: float | None                       = None              # 坐标轴结束值，None表示自动
    step: float | None                      = None              # 坐标轴刻度步长（间隔），None表示自动

    # ========== 内部常量映射 ==========
    _FONT: ClassVar[dict]                   = {'inner': 5,'outer': 10}  # 刻度朝向的枚举映射表，inner对应Origin内部值5，outer对应10

    # ========== 内部转换后的 ID (不对外暴露，不参与 repr 打印) ==========
    _title_font_id: int   = field(init=False, repr=False)   # 标题字体在Origin中的内部ID，由font()函数解析得到
    _title_color_id: int  = field(init=False, repr=False)   # 标题颜色在Origin中的内部ID，由color()函数解析得到
    _axis_font_id: int    = field(init=False, repr=False)   # 刻度数字字体在Origin中的内部ID
    _axis_color_id: int   = field(init=False, repr=False)   # 刻度数字颜色在Origin中的内部ID
    _axis_ticks_id: int   = field(init=False, repr=False)   # 刻度朝向在Origin中的内部ID（5=朝内，10=朝外）


    def __post_init__(self):
        
        self._title_font_id  = op.lt_int(f'font({self.title_font})')

        safe_title_color = _parse_origin_color(self.title_color)
        self._title_color_id = op.lt_int(f'color({safe_title_color})')

        self._axis_font_id   = op.lt_int(f'font({self.axis_font})')

        safe_axis_color = _parse_origin_color(self.axis_color)
        self._axis_color_id  = op.lt_int(f'color({safe_axis_color})')

        self._axis_ticks_id  = self._FONT.get(self.axis_ticks, 5)

    # axis:所有的参数
    # X:底部, X2:顶部, Y:左边, Y2:右边, Z:前面, Z2:后面
    # Zh is the ZhX axis, Zh2 is the back ZhY axis, and Zh3 is the back ZhZ axis.
    def axis_set(self,axis:str,lay:op.GLayer):
        
        # 坐标轴厚度
        lay.set_float(f'{axis}.thickness', self.axis_thickness)
        
        # 坐标轴数字加粗
        lay.set_int(f'{axis}.label.bold', self.axis_bold)
        
        # 刻度数字大小
        lay.set_int(f'{axis}.label.pt', self.axis_pt)

        # 刻度数字字体
        lay.set_int(f'{axis}.label.font', self._axis_font_id)
    
        # 刻度朝向
        lay.set_int(f'{axis}.ticks', self._axis_ticks_id)

        # 刻度显示
        lay.set_int(f'{axis}.showAxes',self.axis_show)
    
        # 设置颜色
        lay.set_int(f'{axis}.color',self._axis_color_id)
        
        # 手动设置坐标轴范围
        lay.axis(axis).set_limits(self.begin, self.end, self.step)

    # text:xb,yl,xt,yr,zb,zf
    def title_set(self,text:str,lay:op.GLayer):

        label = lay.label(text)
        label.set_str('text',self.title)
        label.set_int('font', self._title_font_id)
        label.set_int('fsize', self.title_font_size)
        label.set_int('color', self._title_color_id)

        self._bold_set(text)
        self._italic_set(text)
        self._underline_set(text)

    # 加粗设置
    def _bold_set(self,text):

        if self.title_bold:
            name = op.get_lt_str(f'{text}.text$')
            op.lt_exec(f'{text}.text$="\\b({name})"')

    # 斜体设置
    def _italic_set(self,text):

        if self.title_italic:
            name = op.get_lt_str(f'{text}.text$')
            op.lt_exec(f'{text}.text$="\\i({name})"')

    # 下划线设置
    def _underline_set(self,text):

        if self.title_underline:
            name = op.get_lt_str(f'{text}.text$')
            op.lt_exec(f'{text}.text$="\\u({name})"')


"""文本类"""
@dataclass
class TextConfig:
    title: str | list[str] | None       = None              # 图例文本，可以是单个字符串、字符串列表或None；为列表时每个元素对应一条曲线的图例名
    font: str                           = 'Times New Roman' # 图例文本字体名称
    color: str | tuple[int, int, int]   = 'black'           # 图例文本颜色，支持颜色名称或RGB元组,如color = (0,231,123)
    bold: int                           = 1                 # 图例文本是否加粗，1为加粗，0为不加粗
    italic:int                          = 0                 # 图例文本是否斜体，1为斜体，0不为斜体
    underline:int                       = 0                 # 图例文本是否加下划线，1加下划线，0不加下划线
    font_size: int                      = 26                # 图例文本字体大小（磅值）
    background: int                     = 0                 # 图例背景透明度，0为透明背景，其他值为不同背景样式
    
    # ========== 内部转换后的 ID ==========
    _font_id: int = field(init=False, repr=False)       # 字体在Origin中的内部ID
    _color_id: int = field(init=False, repr=False)      # 颜色在Origin中的内部ID
    
    def __post_init__(self):
        self._font_id = op.lt_int(f'font({self.font})')

        safe_color = _parse_origin_color(self.color)
        self._color_id = op.lt_int(f'color({safe_color})')

        # 检查self.title是否是字符串类型，如果是，将其转换成列表
        if isinstance(self.title, str):
            self.title = [self.title]

    def text_set(self,text:str,lay:op.GLayer):

        label = lay.label(text)
    
        label.set_str('text',self.__legend_format_set())
        label.set_int('font', self._font_id)
        label.set_int('fsize', self.font_size)
        label.set_int('color', self._color_id)
        label.set_int('background', self.background)

    
    def __legend_format_set(self) -> str:

        # op.lt_exec('layer -c;')
        # count = op.lt_int('count')
        contend = op.get_lt_str(f'legend.text$')

        results = []
    
        # 优化：先过滤掉空行，确保行索引(i)与列表的索引严格对应
        lines = [line.strip() for line in contend.strip().splitlines() if line.strip()]

        for i, line in enumerate(lines):
            # ========== 第一步：提取与分离 ==========
            # 1. 提取 \l(序号) 部分
            l_match = re.search(r'(\\l\(\d+\))', line)
            l_part = l_match.group(1) if l_match else ''
        
            # 2. 提取纯数据内容
            rest = line.split(')', 1)[-1] if ')' in line else line
            extracted_data = rest.replace('%','').replace('(', '').replace(')', '').strip()

            # 判断是否使用列表中的指定数据覆盖
            if self.title is not None and i < len(self.title):
                data = str(self.title[i]).strip()
            else:
                data = f'\\%({extracted_data})' # 使用原标题
            
            # ========== 带格式符的拼接 ==========
            if self.bold:
                data_part = f'\\b({data})'
            else:
                data_part = f'{data}'

            if self.italic:
                data_part = f'\\i({data_part})'
            
            if self.underline:
                data_part = f'\\u({data_part})'
            
            results.append(f'{l_part} {data_part}')
        
        return '\n'.join(results)

@dataclass
class LayConfig:
   
    x: AxisConfig | None            = None
    y: AxisConfig | None            = None
    legend: TextConfig | None       = None
    frame: int                      = 1
    aa: int                         = 1

    def __post_init__(self):
        if self.x is None:
            self.x = AxisConfig(title='x')
        if self.y is None:
            self.y = AxisConfig(title='y')
        if self.legend is None:
            self.legend = TextConfig()


# 函数功能说明：配置一个图层的参数
def lay_set(Graph: op.GPage, lay: op.GLayer, config: LayConfig):

    lay.activate()

    # 自动设置坐标轴的范围
    lay.rescale()
    
    config.x.axis_set('x',lay)
    config.y.axis_set('y',lay)
    config.x.axis_set('x2',lay)
    config.y.axis_set('y2',lay)

    config.x.title_set('xb',lay)
    config.y.title_set('yl',lay)

    config.legend.text_set('legend',lay)

    # 抗锯齿 & 框架
    Graph.set_int('aa', config.aa)
    lay.set_int('SHOWFRAME', config.frame)


# 函数功能说明：在一个图层中绘制一条线
def plot_set(
        data: op.MSheet | op.WSheet,     # worksheet数据源
        lay: op.GLayer,                  # 图层对象
        colx,                            # worksheet中作为x轴数据的列名
        coly,                            # worksheet中作为y轴数据的列名
        color='black',                   # 线条颜色
        width: float = 3,                # 线条宽度
        type='l'                         # 图表类型
        ):

    lay.activate()
    plot = lay.add_plot(data, colx=colx, coly=coly, type=type)
    plot.set_float('line.width', width)  # 设置线宽
    plot.color = color

def _parse_origin_color(color_input):
    """
    将多种颜色输入格式统一转换为 Origin LabTalk 支持的十六进制字符串
    支持: RGB元组 (255,0,0), 颜色名称 'red', 十六进制 '#FF0000'
    """
    # 如果已经是合法的十六进制字符串，直接返回
    if isinstance(color_input, str):
        if color_input.startswith('#') and len(color_input) == 7:
            return color_input
        # 如果是颜色名称如 'red', 'blue'，Origin原生支持，直接返回
        return color_input
    
    # 如果是 RGB 元组或列表，转换为十六进制
    if isinstance(color_input, (tuple, list)) and len(color_input) == 3:
        try:
            r, g, b = [int(c) for c in color_input]
            return f"#{r:02x}{g:02x}{b:02x}"
        except (ValueError, TypeError):
            pass
            
    # 兜底默认黑色
    return "#000000"

# 函数功能说明：保存图像,目前支持.png格式
def graph_save(
        graph: op.GPage,     # 图对象
        name: str,           # 保存的图片名字
        path: str = None,    # 保存路径
        width: int = 0,      # 图像宽度
        ratio: int = 0,      # 图像宽高比
        ):
    
    if not path:
        path = _path_set(name)
    else:
        path = str(Path(path) / name)

    used_template = getattr(graph, '_custom_template', '')
    
    if not used_template:
        graph.set_float('autoSize', 1)

    if name.endswith('.png'):
        op.find_graph(graph.name).save_fig(path, replace=True, width=width, ratio=ratio)
        safe_print(f"图片文件保存成功😊,保存在{path}")
    else:
        safe_print("不支持该图片文件格式保存")

# 备份原生方法，防止被污染
_original_new_graph = op.new_graph

"""
创建图形对象。
参数说明：
template:绘图模板
调用示例:gp = po.create_graph(template='my_template.otpu') 调用自己的模板需要加后缀,默认调用my_template文件夹里的模板
        gp = po.create_graph(template='PAN2VERT') 调用系统自带的模板不需要加.otpu后缀
完美兼容 op.new_graph 的所有原生参数，并将 template 状态绑定到对象自身。
"""
def create_graph(*args, **kwargs) -> op.GPage:

    # 1. 动态拦截并处理 template 参数
    # 使用 pop 取出，避免后续重复传递；如果没传则默认为空字符串
    template = kwargs.pop('template', '') 
    
    if template and 'otpu' in str(template):
        new_template = _path_set(str(template))
        kwargs['template'] = new_template  # 处理后重新塞回 kwargs
        template = new_template
    elif template:
        kwargs['template'] = template      # 不含 'otpu' 则原样塞回
        template = str(template)
    else:
        template = ''                      # 没传 template，保持空

    # 2. 调用原生方法 (完美透传所有位置参数和关键字参数)
    graph = _original_new_graph(*args, **kwargs)
    
    # 3. 【核心】将状态私有化绑定到当前 graph 实例
    graph.__dict__['_custom_template'] = template 
    
    return graph


# 函数功能说明：保存项目
def project_save(
        name: str,           # 项目的名字
        path: str = None     # 项目保存的路径
        ):

    if not path:
        path = _path_set(name)
    else:
        path = str(Path(path) / name)

    if name.endswith('.opju'):
        op.save(path)
        safe_print(f"工程文件保存成功😊,保存在{path}")
    else:
        safe_print("不支持该工程文件格式保存")


# 函数功能说明：读取数据
def read_data(
        name: str,           # 文件的名字
        path: str = None     # 文件的路径
        ):

    if not path:
        # 【优化】：支持传入绝对路径（GUI拖拽进来的通常是绝对路径）
        if Path(name).is_absolute() and Path(name).exists():
            path = str(name)
        else:
            path = _path_set(name)
    else:
        path = str(Path(path) / name)

    if path.endswith('.csv'):
        df = pd.read_csv(path)
    elif path.endswith('.txt'):
        df = pd.read_csv(path, sep='\t')
    elif path.endswith('.xlsx'):
        df = pd.read_excel(path)
    else:
        df = pd.DataFrame() # 防止未匹配到格式时报错

    return df


# 函数功能说明：保存文件
def file_save(
        dataframe: pd.DataFrame,     
        name: str,
        path: str = None,
        index: bool = False,
        float_format='%.6e'
        ):
    if not path:
        path = _path_set(name)
    else:
        path = str(Path(path) / name)

    if name.endswith('.txt'):
        
        dataframe.to_csv(path, sep='\t', index=index, float_format=float_format)
        safe_print(f"文件保存成功,保存在{path}")

    elif name.endswith('.csv'):

        dataframe.to_csv(path, index=index, float_format=float_format)
        safe_print(f"文件保存成功,保存在{path}")

    else:
        safe_print("不支持该文件格式保存")


# 内部函数，用户不用关心，以及调用与使用
def _path_set(file: str):
    """基于 get_base_dir 获取资源绝对路径"""
    base_dir = get_base_dir()

    data_dir     = base_dir / "data"
    image_dir    = base_dir / "image"
    template_dir = base_dir / "my_template"
    project_dir  = base_dir / "project"

    if file.endswith(('.txt', '.csv', '.xlsx')):
        file_path = data_dir / file
    elif file.endswith('.png'):
        file_path = image_dir / file
    elif file.endswith('.otpu'):
        file_path = template_dir / file
    elif file.endswith('.opju'):
        file_path = project_dir / file
    else:
        file_path = None
        
    return str(file_path) if file_path is not None else None


# 暂定封装
def add_layer(Graph: op.GPage, location, type=0):

    layer = Graph.add_layer(type=type)

    op.lt_exec('legend')    

    return layer