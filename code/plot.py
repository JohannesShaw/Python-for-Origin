import pyorigin as po
import originpro as op
import pandas as pd


def fig4(input_file1,input_file2,input_file3,input_file4,output_file):

    # 读取数据
    df1 = po.read_data(input_file1)
    df2 = po.read_data(input_file2)
    df3 = po.read_data(input_file3)
    df4 = po.read_data(input_file4)

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
    
    time1 = df1['time'] * 1e9;
    time2 = df2['time'] * 1e9;
    time3 = df3['time'] * 1e9;
    time4 = df4['time'] * 1e9;

    #将数据加载到sheet里
    wks.from_df(pd.DataFrame({
        'Time(ns)1': time1,           
        'Voltage(V)1': df1['vout'],    
        'Current(A)1': df1['iout'],   

        'Time(ns)2': time2,           
        'Voltage(V)2': df2['vout'],    
        'Current(A)2': df2['iout'],

        'Time(ns)3': time3,           
        'Voltage(V)3': df3['vout'],    
        'Current(A)3': df3['iout'],

        'Time(ns)4': time4,           
        'Voltage(V)4': df4['vout'],    
        'Current(A)4': df4['iout'],

    }))


    gp = op.new_graph(template='MYPAN4.otpu')                # 新建一个图(该图默认只有一个图层)
    lay1 = gp[0]                       # 取该图的第一个图层绘图(默认只有一个图层)
    lay2 = gp[1]
    lay3 = gp[2]
    lay4 = gp[3]

    #------------------------参数设置------------------------

    po.plot_set(wks, lay1, colx='Time(ns)1', coly='Voltage(V)1', color='black', width=3, type='l')

    po.lay_set(gp,lay1,po.LayConfig(x_title='Time/ns',y_title='Vout/V',legend_title = ['Vout'],x_to=10,y_to=90,y_step=15))

    po.plot_set(wks, lay2, colx='Time(ns)2', coly='Voltage(V)2', color='black', width=3, type='l')

    po.lay_set(gp,lay2,po.LayConfig(x_title='Time/ns',y_title='Vout/V',legend_title = ['Vout'],x_to=10,y_to=90,y_step=15))

    po.plot_set(wks, lay3, colx='Time(ns)3', coly='Voltage(V)3', color='black', width=3, type='l')

    po.lay_set(gp,lay3,po.LayConfig(x_title='Time/ns',y_title='Vout/V',legend_title = ['Vout'],x_to=10,y_to=90,y_step=15))

    po.plot_set(wks, lay4, colx='Time(ns)4', coly='Voltage(V)4', color='black', width=3, type='l')

    po.lay_set(gp,lay4,po.LayConfig(x_title='Time/ns',y_title='Vout/V',legend_title = ['Vout'],x_to=10,y_to=90,y_step=15))
    
    #------------------------参数设置------------------------

    print("绘图完成")

    #------------------------保存设置------------------------

    po.graph_save(gp,output_file)
  
    po.project_save('template4.opju')
                          
def fig5(input_file1,input_file2,input_file3,input_file4,output_file):

    # 读取数据
    df1 = po.read_data(input_file1)
    df2 = po.read_data(input_file2)
    df3 = po.read_data(input_file3)
    df4 = po.read_data(input_file4)

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
    wks1 = wb.add_sheet()
    wks2 = wb.add_sheet()
    wks3 = wb.add_sheet()
    wks4 = wb.add_sheet()
    
    time1 = df1['time'] * 1e9;
    time2 = df2['time'] * 1e9;
    time3 = df3['time'] * 1e9;
    time4 = df4['time'] * 1e9;

    #将数据加载到sheet里
    wks1.from_df(pd.DataFrame({
        'Time(ns)': time1,           
        '5V': df1['vout'],       
    }))

    wks2.from_df(pd.DataFrame({
        'Time(ns)': time2,           
        '10V': df2['vout'],    
    }))

    wks3.from_df(pd.DataFrame({
        'Time(ns)': time3,           
        '20V': df3['vout'],    
    }))

    wks4.from_df(pd.DataFrame({
        'Time(ns)': time4,           
        '30V': df4['vout'],    
    }))

    gp = op.new_graph()                # 新建一个图(该图默认只有一个图层)
    lay1 = gp[0]                       # 取该图的第一个图层绘图(默认只有一个图层)

    po.plot_set(wks1, lay1, colx='Time(ns)', coly='5V', color='black', width=3, type='l')
    po.plot_set(wks2, lay1, colx='Time(ns)', coly='10V', color='red', width=3, type='l')
    po.plot_set(wks3, lay1, colx='Time(ns)', coly='20V', color='blue', width=3, type='l')
    po.plot_set(wks4, lay1, colx='Time(ns)', coly='30V', color='#F08228', width=3, type='l')

    po.lay_set(gp,lay1,po.LayConfig(x_title='Time/ns',y_title='Vout/V',x_to=10,y_to=90,y_step=15))

    print("绘图完成")
    
    po.graph_save(gp,output_file)

    po.project_save('template5.opju')

def fig6a(input_file1,input_file2,input_file3,output_file):
     # 读取数据
    df1 = po.read_data(input_file1)
    df2 = po.read_data(input_file2)
    df3 = po.read_data(input_file3)

    filtered = df2[df2['TLP'] == 500]

    df2 = filtered[['time', 'vout']]
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
    wks1 = wb.add_sheet()
    wks2 = wb.add_sheet()
    wks3 = wb.add_sheet()
    
    time1 = df1['#1_PESD18VF1BL_POS at 500 V_x'] * 1e9;
    time2 = df2['time'] * 1e9;
    time3 = df3['time'] * 1e9;

    #将数据加载到sheet里
    wks1.from_df(pd.DataFrame({
        'Time(ns)': time1,           
        'Measurement': df1['#1_PESD18VF1BL_POS at 500 V_y'],       
    }))

    wks2.from_df(pd.DataFrame({
        'Time(ns)': time2,           
        'Old simulation': df2['vout'],    
    }))

    wks3.from_df(pd.DataFrame({
        'Time(ns)': time3,           
        'New simulation': df3['vout'],    
    }))

    gp = op.new_graph()                # 新建一个图(该图默认只有一个图层)
    lay1 = gp[0]                       # 取该图的第一个图层绘图(默认只有一个图层)

    po.plot_set(wks1, lay1, colx='Time(ns)', coly='Measurement', color='black', width=3, type='l')
    po.plot_set(wks2, lay1, colx='Time(ns)', coly='Old simulation', color='red', width=3, type='l')
    po.plot_set(wks3, lay1, colx='Time(ns)', coly='New simulation', color='blue', width=3, type='l')

    po.lay_set(gp,lay1,po.LayConfig(x_title='Time/ns',y_title='Vout/V',x_to=10,y_to=90,y_step=15))

    print("绘图完成")

    po.graph_save(gp,output_file)

    po.project_save('template6a.opju')

def fig6b(input_file1,input_file2,input_file3,output_file):
     # 读取数据
    df1 = po.read_data(input_file1)
    df2 = po.read_data(input_file2)
    df3 = po.read_data(input_file3)

    filtered = df2[df2['TLP'] == 500]

    df2 = filtered[['time', 'vout']]
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
    wks1 = wb.add_sheet()
    wks2 = wb.add_sheet()
    wks3 = wb.add_sheet()
    
    time1 = df1['#1_PESD18VF1BL_POS at 200 V_x'] * 1e9;
    time2 = df2['time'] * 1e9;
    time3 = df3['time'] * 1e9;

    #将数据加载到sheet里
    wks1.from_df(pd.DataFrame({
        'Time(ns)': time1,           
        'Measurement': df1['#1_PESD18VF1BL_POS at 200 V_y'],       
    }))

    wks2.from_df(pd.DataFrame({
        'Time(ns)': time2,           
        'Old simulation': df2['vout'],    
    }))

    wks3.from_df(pd.DataFrame({
        'Time(ns)': time3,           
        'New simulation': df3['vout'],    
    }))

    gp = op.new_graph()                # 新建一个图(该图默认只有一个图层)
    lay1 = gp[0]                       # 取该图的第一个图层绘图(默认只有一个图层)

    po.plot_set(wks1, lay1, colx='Time(ns)', coly='Measurement', color='black', width=3, type='l')
    po.plot_set(wks2, lay1, colx='Time(ns)', coly='Old simulation', color='red', width=3, type='l')
    po.plot_set(wks3, lay1, colx='Time(ns)', coly='New simulation', color='blue', width=3, type='l')

    po.lay_set(gp,lay1,po.LayConfig(x_title='Time/ns',y_title='Vout/V',x_to=10,y_to=90,y_step=15))

    print("绘图完成")

    po.graph_save(gp,output_file)

    po.project_save('template6b.opju')

def fig6c(input_file1,input_file2,input_file3,output_file):
     # 读取数据
    df1 = po.read_data(input_file1)
    df2 = po.read_data(input_file2)
    df3 = po.read_data(input_file3)

    filtered = df2[df2['TLP'] == 500]

    df2 = filtered[['time', 'vout']]
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
    wks1 = wb.add_sheet()
    wks2 = wb.add_sheet()
    wks3 = wb.add_sheet()
    
    time1 = df1['#1_PESD18VF1BL_POS at 60 V_x'] * 1e9;
    time2 = df2['time'] * 1e9;
    time3 = df3['time'] * 1e9;

    #将数据加载到sheet里
    wks1.from_df(pd.DataFrame({
        'Time(ns)': time1,           
        'Measurement': df1['#1_PESD18VF1BL_POS at 60 V_y'],       
    }))

    wks2.from_df(pd.DataFrame({
        'Time(ns)': time2,           
        'Old simulation': df2['vout'],    
    }))

    wks3.from_df(pd.DataFrame({
        'Time(ns)': time3,           
        'New simulation': df3['vout'],    
    }))

    gp = op.new_graph()                # 新建一个图(该图默认只有一个图层)
    lay1 = gp[0]                       # 取该图的第一个图层绘图(默认只有一个图层)

    po.plot_set(wks1, lay1, colx='Time(ns)', coly='Measurement', color='black', width=3, type='l')
    po.plot_set(wks2, lay1, colx='Time(ns)', coly='Old simulation', color='red', width=3, type='l')
    po.plot_set(wks3, lay1, colx='Time(ns)', coly='New simulation', color='blue', width=3, type='l')

    po.lay_set(gp,lay1,po.LayConfig(x_title='Time/ns',y_title='Vout/V',x_to=10,y_to=90,y_step=15))

    print("绘图完成")

    po.graph_save(gp,output_file)

    po.project_save('template6c.opju')

def fig7a(input_file1,input_file2,output_file):
     # 读取数据
    df1 = po.read_data(input_file1)
    df2 = po.read_data(input_file2)

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
    wks1 = wb.add_sheet()
    wks2 = wb.add_sheet()
    
    time1 = df1['#1_PESD18VF1BL_POS at 500 V_x'] * 1e9;
    time2 = df2['time'] * 1e9;

    #将数据加载到sheet里
    wks1.from_df(pd.DataFrame({
        'Time(ns)': time1,           
        'Measurement': df1['#1_PESD18VF1BL_POS at 500 V_y'],       
    }))

    wks2.from_df(pd.DataFrame({
        'Time(ns)': time2,           
        'Simulation': df2['iout'],    
    }))

    gp = op.new_graph()                # 新建一个图(该图默认只有一个图层)
    lay1 = gp[0]                       # 取该图的第一个图层绘图(默认只有一个图层)

    po.plot_set(wks1, lay1, colx='Time(ns)', coly='Measurement', color='black', width=3, type='l')
    po.plot_set(wks2, lay1, colx='Time(ns)', coly='Simulation', color='red', width=3, type='l')

    po.lay_set(gp,lay1,po.LayConfig(x_title='Time/ns',y_title='Iout/A',x_to=10,y_to=10))

    print("绘图完成")

    po.graph_save(gp,output_file)

    po.project_save('template7a.opju')

def fig7b(input_file1,input_file2,output_file):
     # 读取数据
    df1 = po.read_data(input_file1)
    df2 = po.read_data(input_file2)

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
    wks1 = wb.add_sheet()
    wks2 = wb.add_sheet()
    wks3 = wb.add_sheet()
    
    #将数据加载到sheet里
    wks1.from_df(pd.DataFrame({
        'V': df1['vout'],           
        'Simulation': df1['iout'],       
    }))

    wks2.from_df(pd.DataFrame({
        'v': df2['Vwindow [V]'],         
        'Measurement': df2['Iwindow [A]'],    
    }))

    gp = op.new_graph()                # 新建一个图(该图默认只有一个图层)
    lay1 = gp[0]                       # 取该图的第一个图层绘图(默认只有一个图层)

    po.plot_set(wks2, lay1, colx='V', coly='Measurement', color='black', width=3, type='l')
    po.plot_set(wks1, lay1, colx='V', coly='Simulation', color='red', width=3, type='l')
    

    po.lay_set(gp,lay1,po.LayConfig(x_title='Iwindow/A',y_title='Vwindow/V',x_from = 0,x_to=45,x_step=5,y_to=10))

    print("绘图完成")

    po.graph_save(gp,output_file)

    po.project_save('template7b.opju')

def fig7c(input_file1,input_file2,output_file):
     # 读取数据
    df1 = po.read_data(input_file1)
    df2 = po.read_data(input_file2)

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
    wks1 = wb.add_sheet()
    wks2 = wb.add_sheet()
    wks3 = wb.add_sheet()
    
    #将数据加载到sheet里
    wks1.from_df(pd.DataFrame({
        'TLP': df1['TLP'],           
        'Simulation': df1['vout_max'],       
    }))

    wks2.from_df(pd.DataFrame({
        'v': df2['TLP'],         
        'Measurement': df2['Vpeak [V]'],    
    }))

    gp = op.new_graph()                # 新建一个图(该图默认只有一个图层)
    lay1 = gp[0]                       # 取该图的第一个图层绘图(默认只有一个图层)

    po.plot_set(wks2, lay1, colx='V', coly='Measurement', color='black', width=3, type='l')
    po.plot_set(wks1, lay1, colx='TLP', coly='Simulation', color='red', width=3, type='l')
    

    po.lay_set(gp,lay1,po.LayConfig(x_title='TLP/V',y_title='Vpeak/V',x_to=525,y_to=105,y_step=15,x_step=105))

    print("绘图完成")
    
    po.graph_save(gp,output_file)

    po.project_save('template7c.opju')