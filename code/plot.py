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
    
    time1 = df1['Time(s)'] * 1e9;
    time2 = df2['Time(s)'] * 1e9;
    time3 = df3['Time(s)'] * 1e9;
    time4 = df4['Time(s)'] * 1e9;

    #将数据加载到sheet里
    wks.from_df(pd.DataFrame({
        'Time(ns)1': time1,           
        'Voltage(V)1': df1['Voltage(V)'],    
        'Current(A)1': df1['Current(A)'],   

        'Time(ns)2': time2,           
        'Voltage(V)2': df2['Voltage(V)'],    
        'Current(A)2': df2['Current(A)'],

        'Time(ns)3': time3,           
        'Voltage(V)3': df3['Voltage(V)'],    
        'Current(A)3': df3['Current(A)'],

        'Time(ns)4': time4,           
        'Voltage(V)4': df4['Voltage(V)'],    
        'Current(A)4': df4['Current(A)'],

    }))

    gp = po.create_graph()              
    lay = gp[0]                      

    #------------------------参数设置------------------------

    po.plot_set(wks, lay, colx='Time(ns)4', coly='Voltage(V)4', color="black", width=3, type='l')

    po.plot_set(wks, lay, colx='Time(ns)1', coly='Voltage(V)1', color='red', width=3, type='l')

    po.plot_set(wks, lay, colx='Time(ns)2', coly='Voltage(V)2', color='blue', width=3, type='l')

    po.plot_set(wks, lay, colx='Time(ns)3', coly='Voltage(V)3', color="#EB7114", width=3, type='l')


    po.lay_set(gp, lay, po.LayConfig())
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

    gp = po.create_graph()                # 新建一个图(该图默认只有一个图层)
    lay = gp[0]                       # 取该图的第一个图层绘图(默认只有一个图层)

    po.plot_set(wks1, lay, colx='Time(ns)', coly='5V', color='black', width=3, type='l')
    po.plot_set(wks2, lay, colx='Time(ns)', coly='10V', color='red', width=3, type='l')
    po.plot_set(wks3, lay, colx='Time(ns)', coly='20V', color='blue', width=3, type='l')
    po.plot_set(wks4, lay, colx='Time(ns)', coly='30V', color='#F08228', width=3, type='l')

    po.lay_set(gp,lay,po.LayConfig())

    print("绘图完成")
    
    po.graph_save(gp,output_file)

    po.project_save('template5.opju')