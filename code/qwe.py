"""

此文件不要修改
此文件为底层实现,不可修改
用户可编辑的.py文件为plot.py main.py data_deal.py,在里面编辑自己的绘图函数

"""

import pandas as pd
import originpro as op
from pathlib import Path
from dataclasses import dataclass, field
from typing import ClassVar


"""坐标轴类"""
@dataclass
class AxisConfig:
    
    title: str                              = ''
    title_font: str                         = 'Times New Roman'
    title_color: str | tuple[int,int,int]   = 'black'
    title_bold: int                         = 1
    title_italic:int                        = 0
    title_font_size: int                    = 36

    axis_thickness: float                   = 3
    axis_bold: int                          = 1
    axis_pt: int                            = 26
    axis_font: str                          = 'Times New Roman'
    axis_color: str | tuple[int,int,int]    = 'black'      
    axis_ticks: str                         = 'inner'      

    begin: float | None                     = None       
    end: float | None                       = None
    step: float | None                      = None

    _FONT: ClassVar[dict]                   = {'inner': 5,'outer': 10}

    _strategy_map: ClassVar[dict] = {
        (True,True):  '_bold_italic',
        (True,False):  '_bold',
        (False,True):  '_italic',
        (False,False): '_default',
    }
    # 内部转换后的 ID (不对外暴露，不参与 repr 打印)
    _title_font_id: int   = field(init=False, repr=False)
    _title_color_id: int  = field(init=False, repr=False)
    _axis_font_id: int    = field(init=False, repr=False)
    _axis_color_id: int   = field(init=False, repr=False)
    _axis_ticks_id: int   = field(init=False, repr=False)

    def __post_init__(self):
        self._title_font_id  = op.lt_int(f'font({self.title_font})')
        self._title_color_id = op.lt_int(f'color({self.title_color})')

        self._axis_font_id   = op.lt_int(f'font({self.axis_font})')
        self._axis_color_id  = op.lt_int(f'color({self.axis_color})')
        
        self._axis_ticks_id  = self._FONT.get(self.axis_ticks, 5)


    # axis: X is the bottom X axis, X2 is the top X axis, Y is the left Y axis, Y2 is the right Y axis, Z is the front Z axis, Z2 is the back Z axis, Zh is the ZhX axis, Zh2 is the back ZhY axis, and Zh3 is the back ZhZ axis.
    def axis_set(self,axis:str,lay:op.GLayer):
        
        lay.axis(axis).title = self.title

        lay.set_float(f'{axis}.thickness', self.axis_thickness)
        
        # 坐标轴数字加粗
        lay.set_int(f'{axis}.label.bold', self.axis_bold)
        
        # 刻度数字大小
        lay.set_int(f'{axis}.label.pt', self.axis_pt)

        # 刻度数字字体
        lay.set_int(f'{axis}.label.font', self._axis_font_id)
    
        # 刻度朝向
        lay.set_int(f'{axis}.ticks', self._axis_ticks_id)
    
        # 自动设置坐标轴的范围
        lay.rescale()

        lay.axis(axis).set_limits(self.begin, self.end, self.step)

    def title_set(self,text:str,lay:op.GLayer):

        label = lay.label(text)
        label.set_int('font', self._title_font_id)
        label.set_int('fsize', self.title_font_size)
        label.set_int('color', self._title_color_id)

        # 加粗设置
        self._execute(text)

    def _execute(self,text):
        
        key = (bool(self.title_bold),bool(self.title_italic))
        
        strategy_name = self._strategy_map.get(key, '_default')
        formatter = getattr(self, strategy_name)
        
        # 获取格式化后的文本
        full_text = formatter()
        
        # 如果策略返回 None (如 default 状态)，则跳过执行
        if full_text is None:
            return

        op.lt_exec(f'{text}.text$="{full_text}"')


    def _bold(self) -> str:
       
        parts = [f"\\b({self.title})"]
        return "\n".join(parts)

    def _italic(self) -> str:

        parts = [f"\\i({self.title})"]
        return "\n".join(parts)
    
    def _bold_italic(self) -> str:

        parts = [f"\\b(\\i({self.title}))"]
        return "\n".join(parts)

    def _default(self) -> str | None:
        
        return None


"""文本类"""
@dataclass
class TextConfig:
    title: str | list[str] | None       = None
    font: str                           = 'Times New Roman'
    color: str | tuple[int, int, int]   = 'black'
    bold: int                           = 1
    font_size: int                      = 26
    background: int                     = 0
    
    _font_id: int = field(init=False, repr=False)
    _color_id: int = field(init=False, repr=False)
    

    _strategy_map: ClassVar[dict] = {
        (True, True):  '_fmt_title_bold',
        (True, False): '_fmt_title_no',
        (False, True): '_fmt_no_bold',
        (False, False): '_fmt_default',
    }

    def __post_init__(self):
        self._font_id = op.lt_int(f'font({self.font})')
        self._color_id = op.lt_int(f'color({self.color})')

        # 检查self.title是否是字符串类型，如果是，将其转换成列表
        if isinstance(self.title, str):
            self.title = [self.title]

    def text_set(self, text: str, lay: op.GLayer):

        label = lay.label(text)
        label.set_int('font', self._font_id)
        label.set_int('fsize', self.font_size)
        label.set_int('color', self._color_id)
        label.set_int('background', self.background)
        self._execute(text)

    # ================= 核心执行引擎 (模板方法) =================

    def _execute(self,text:str):
        
        key = (bool(self.title), bool(self.bold))
        
        strategy_name = self._strategy_map.get(key, '_fmt_default')
        formatter = getattr(self, strategy_name)
        
        # 获取格式化后的文本
        full_text = formatter()
        
        # 如果策略返回 None (如 default 状态)，则跳过执行
        if full_text is None:
            return

        op.lt_exec(f'{text}.text$="{full_text}"')


    def _get_safe_title(self, index: int) -> str:
    
        if self.title and index < len(self.title):
            return self.title[index]
        return f"Data {index + 1}" # 越界时的安全降级默认值

    def _fmt_title_bold(self) -> str:
       
        op.lt_exec('layer -c;')
        count = op.lt_int('count')
        parts = [f"\\l({n+1}) \\b({self._get_safe_title(n)})" for n in range(count)]
        return "\n".join(parts)

    def _fmt_title_no(self) -> str:
        
        op.lt_exec('layer -c;')
        count = op.lt_int('count')
        parts = [f"\\l({n+1}) {self._get_safe_title(n)}" for n in range(count)]
        return "\n".join(parts)

    def _fmt_no_bold(self) -> str:
        
        op.lt_exec('layer -c;')
        count = op.lt_int('count')
        parts = [f"\\l({n+1}) \\b(%({n+1}))" for n in range(count)]
        return "\n".join(parts)

    def _fmt_default(self) -> str | None:
        
        return None

class LayConfig:
    
    def __init__(
        self,
        x: AxisConfig        = None,
        y: AxisConfig        = None,
        legend: TextConfig   = None,
        frame: int           = 1,
        aa: int              = 1,
    ):
        self.x          = x or AxisConfig(title='x')
        self.y          = y or AxisConfig(title='y')
        self.legend     = legend or TextConfig()
        
        self.frame      = frame
        self.aa         = aa


# 函数功能说明：配置一个图层的参数
def lay_set(Graph: op.GPage, lay: op.GLayer, config: LayConfig):

    lay.activate()
    
    config.x.axis_set('x',lay)
    config.x.title_set('xb',lay)
    config.y.axis_set('y',lay)
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
        print(f"图片文件保存成功😊,保存在{path}")
    else:
        print("不支持该图片文件格式保存")

# 备份原生方法，防止被污染
_original_new_graph = op.new_graph

def create_graph(*args, **kwargs) -> op.GPage:
    """
    创建图形对象。
    完美兼容 op.new_graph 的所有原生参数，并将 template 状态绑定到对象自身。
    """
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
        print(f"工程文件保存成功😊,保存在{path}")
    else:
        print("不支持该工程文件格式保存")


# 解析列数据，提取数值和单位，并进行转换
def parse_column(series, unit_dict):
    pat = r'([-+]?\d*\.?\d+(?:[eE][+-]?\d+)?)\s*([a-zA-Z]+)'
    extracted = series.str.extract(pat)
    values = pd.to_numeric(extracted[0], errors='coerce')
    units = extracted[1].map(unit_dict)
    return values * units


# 函数功能说明：读取数据
def read_data(
        name: str,           # 文件的名字
        path: str = None     # 文件的路径
        ):

    if not path:
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


# 函数功能说明：清洗数据
def clean(input_file: str, output_file: str):

    df = read_data(input_file)
    if df.empty:
        print("读取的数据为空，跳过清洗")
        return

    row = df.iloc[0]
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

    print("数据清洗完成")
    
    file_save(result, output_file)
    

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
        print(f"文件保存成功,保存在{path}")

    elif name.endswith('.csv'):

        dataframe.to_csv(path, index=index, float_format=float_format)
        print(f"文件保存成功,保存在{path}")

    else:
        print("不支持该文件格式保存")


# 内部函数，用户不用关心，以及调用与使用
def _path_set(file: str):

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
    else:
        file_path = None
    return str(file_path) if file_path is not None else None


# 暂定封装
def add_layer(Graph: op.GPage, location, type=0):

    layer = Graph.add_layer(type=type)

    op.lt_exec('legend')    

    return layer
