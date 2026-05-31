import pandas as pd
import os

# 时间单位转换
TIME_UNITS = {
    'sec': 1.0,
    'psec': 1e-12,
    'nsec': 1e-9,
    'fsec': 1e-15,
}

# 电流单位转换
CURRENT_UNITS = {
    'A': 1.0,
    'mA': 1e-3,
    'uA': 1e-6,
    'nA': 1e-9,
    'pA': 1e-12,
    'fA': 1e-15,
}

# 电压单位转换
VOLTAGE_UNITS = {
    'V': 1.0,
    'mV': 1e-3,
    'uV': 1e-6,
    'nV': 1e-9,
    'pV': 1e-12,
    'fV': 1e-15,
}

# 解析列数据，提取数值和单位，并进行转换
def parse_column(series, unit_dict):
    pat = r'([-+]?\d*\.?\d+(?:[eE][+-]?\d+)?)\s*([a-zA-Z]+)'
    extracted = series.str.extract(pat)
    values = pd.to_numeric(extracted[0], errors='coerce')
    units = extracted[1].map(unit_dict)
    return values * units

# 清洗CSV文件，提取数值并转换成统一单位
def clean(input_file, output_file):

    input_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file)   # 读：固定目录里的文件
    output_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', output_file) # 存：固定目录里的文件

    if 'csv' in input_file:
        df = pd.read_csv(input_path) 
    elif 'txt' in input_file:
        df = pd.read_csv(input_path,sep='\t')
    elif 'xlsx' in input_file:
        df = pd.read_excel(input_path)
        
    row = df.iloc[0];

    # 存储旧列名到新列名的映射
    rename_mapping = {}

    for col in df.columns:
        cell = str(row[col])         
        if 'sec' in cell:             
            rename_mapping[col] = 'Time(s)'
        elif 'A' in cell:             
            rename_mapping[col] = 'Current(A)'
        elif 'V' in cell:             
            rename_mapping[col] = 'Voltage(V)'
        else:
            rename_mapping[col] = 'TLP'
    
    df.rename(columns=rename_mapping, inplace=True)

    time_clean = parse_column(df['Time(s)'], TIME_UNITS)
    current_clean = parse_column(df['Current(A)'], CURRENT_UNITS)
    voltage_clean = parse_column(df['Voltage(V)'], VOLTAGE_UNITS)

    
    # 5. 组装成固定格式输出：时间 + 电压 + 电流
    result = pd.DataFrame({
        'Time(s)': time_clean,
        'Vout(V)': voltage_clean,
        'Iout(A)': current_clean
    })

    result.to_csv(output_path, index=False, float_format='%.6e')

# 计算平均电流默认时间为3ns到5ns之间的平均电流值，按TLP分组
def mean_current_per_tlp(input_file='cleaned.csv', start_time=3e-9, end_time=5e-9):

    input_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file)   # 读：固定目录里的文件
    # 1. 读取数据
    df = pd.read_csv(input_path)

    # 2. 筛选出 3ns 到 5ns 之间的数据
    mask = (df['Time(s)'] >= start_time) & (df['Time(s)'] <= end_time)
    filtered_df = df[mask]

    result_df = filtered_df.groupby('TLP(V)')['Iout(A)'].mean().reset_index()
    
    result_df.rename(columns={'Iout(A)': 'Mean_Iout(A)'}, inplace=True)

    return result_df

# 计算平均电压默认时间为3ns到5ns之间的平均电压值，按TLP分组
def mean_voltage_per_tlp(input_file='cleaned.csv', start_time=3e-9, end_time=5e-9):
    
    input_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file)   # 读：固定目录里的文件
    # 1. 读取数据
    df = pd.read_csv(input_path)

    # 2. 筛选出 3ns 到 5ns 之间的数据
    mask = (df['Time(s)'] >= start_time) & (df['Time(s)'] <= end_time)
    filtered_df = df[mask]

    result_df = filtered_df.groupby('TLP(V)')['Vout(V)'].mean().reset_index()
    
    result_df.rename(columns={'Vout(V)': 'Mean_Vout(V)'}, inplace=True)

    return result_df

def merge(input_file1='Vout.csv', input_file2='Iout.csv', output_file='merged_data.csv'):

    input_path1 = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file1)   # 读：固定目录里的文件
    input_path2 = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', input_file2)   # 读：固定目录里的文件
    output_path = os.path.join(r'D:\VsCode File\Python Code\data_analysis\data', output_file)   # 输出:固定路径

    mean_voltage = mean_voltage_per_tlp(input_path1)    #读电压数据，计算平均电压
    mean_current = mean_current_per_tlp(input_path2)    #读电流数据，计算平均电流

    df = pd.merge(mean_voltage, mean_current, on='TLP(V)')

    df.to_csv(output_path, index=False, float_format='%.6e')

    return df