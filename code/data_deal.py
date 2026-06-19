import pandas as pd
import pyorigin as po

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


def parse_column(series, unit_dict):
    pat = r'([-+]?\d*\.?\d+(?:[eE][+-]?\d+)?)\s*([a-zA-Z]+)'
    extracted = series.str.extract(pat)
    values = pd.to_numeric(extracted[0], errors='coerce')
    units = extracted[1].map(unit_dict)
    return values * units

def clean(input_file:str, output_file:str):

    df = po.read_data(input_file)

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

    print("数据清洗完成")
    
    po.file_save(result,output_file)