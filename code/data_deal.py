import pandas as pd
import os
import pyorigin as po

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


def clean(input_file, output_file):

    df = po.read_data(input_file)
    
    # 重命名列
    rename_mapping = {

        df.columns[0]: 'Time(s)',
        df.columns[1]: 'Vout(V)',
        df.columns[2]: 'Iout(A)'

        }

    df.rename(columns=rename_mapping, inplace=True)

    # 清洗列
    time_clean    = po.parse_column(df[df.columns[0]], TIME_UNITS)
    voltage_clean = po.parse_column(df[df.columns[1]], VOLTAGE_UNITS)
    current_clean = po.parse_column(df[df.columns[2]], CURRENT_UNITS)

    # 5. 组装成固定格式输出：时间 + 电压 + 电流
    result = pd.DataFrame({

        df.columns[0]: time_clean,
        df.columns[1]: voltage_clean,
        df.columns[2]: current_clean,

    })

    print("数据清洗完成")
    
    po.file_save(result,output_file)

    
