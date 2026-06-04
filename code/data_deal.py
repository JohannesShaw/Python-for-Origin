import pandas as pd
import os
import pyorigin as po

RENAME_MAP = {
    'sec': 'Time(s)',
    'A': 'Current(A)',
    'V': 'Voltage(V)',
    'TLP': 'TLP(V)'
}

# 时间单位转换
TIME_UNITS = {
    'sec': 1.0,
    'psec': 1e-12,
    'nsec': 1e-9,
    'fsec': 1e-15
}

# 电流单位转换
CURRENT_UNITS = {
    'A': 1.0,
    'mA': 1e-3,
    'uA': 1e-6,
    'nA': 1e-9,
    'pA': 1e-12,
    'fA': 1e-15
}

# 电压单位转换
VOLTAGE_UNITS = {
    'V': 1.0,
    'mV': 1e-3,
    'uV': 1e-6,
    'nV': 1e-9,
    'pV': 1e-12,
    'fV': 1e-15
}

# 解析列数据，提取数值和单位，并进行转换
def __parse_column(series, unit_dict):
    pat = r'([-+]?\d*\.?\d+(?:[eE][+-]?\d+)?)\s*([a-zA-Z]+)'
    extracted = series.str.extract(pat)
    values = pd.to_numeric(extracted[0], errors='coerce')
    units = extracted[1].map(unit_dict)
    return values * units


def clean(input_file, output_file):

    input_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file)   # 读：固定目录里的文件
    output_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', output_file) # 存：固定目录里的文件

    df = po.read_data(input_path)
        
    row = df.iloc[0];

    # 存储旧列名到新列名的映射
    rename_mapping = {}

    for col in df.columns:
        cell = str(row[col])         
        if 'sec' in cell:             
            rename_mapping[col] = RENAME_MAP['sec']
        elif 'A' in cell:             
            rename_mapping[col] = RENAME_MAP['A']
        elif 'V' in cell:             
            rename_mapping[col] = RENAME_MAP['V']
        else:
            rename_mapping[col] = RENAME_MAP['TLP']
    
    df.rename(columns=rename_mapping, inplace=True)

    time_clean    = __parse_column(df[RENAME_MAP['sec']], TIME_UNITS)
    current_clean = __parse_column(df[RENAME_MAP['A']], CURRENT_UNITS)
    voltage_clean = __parse_column(df[RENAME_MAP['V']], VOLTAGE_UNITS)
    #tlp_clean     = __parse_column(df[RENAME_MAP['TLP']], VOLTAGE_UNITS)

    # 5. 组装成固定格式输出：时间 + 电压 + 电流
    result = pd.DataFrame({
        RENAME_MAP['sec']: time_clean,
        RENAME_MAP['V']: voltage_clean,
        RENAME_MAP['A']: current_clean,
        #RENAME_MAP['TLP']:tlp_clean
    })

    result.to_csv(output_path, index=False, float_format='%.6e')
