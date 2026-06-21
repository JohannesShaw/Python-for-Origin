"""
这个文件用于绘制交互界面
"""
import sys
import pandas as pd
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QFileDialog, QTextEdit,
    QGroupBox, QFormLayout, QSpinBox, QDoubleSpinBox, QComboBox,
    QCheckBox, QColorDialog, QMessageBox, QTabWidget, QSplitter
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QColor

# 尝试导入底层绘图库
try:
    import pyorigin as po
    import originpro as op
    ORIGIN_AVAILABLE = True
except ImportError:
    ORIGIN_AVAILABLE = False


class DropArea(QLabel):
    """支持拖拽和点击选择文件的区域"""
    file_dropped = Signal(str)

    def __init__(self):
        super().__init__("拖拽数据文件到此处\n或点击选择文件 (.csv, .txt, .xlsx)")
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa; 
                border-radius: 5px; 
                padding: 20px; 
                color: #666;
                background-color: #f9f9f9;
            }
            QLabel:hover {
                border: 2px dashed #4CAF50;
                background-color: #f1f8e9;
            }
        """)
        self.setMinimumHeight(100)
        self.file_path = None

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith(('.csv', '.txt', '.xlsx')):
                self.set_file(file_path)
            else:
                QMessageBox.warning(self, "格式错误", "仅支持 .csv, .txt, .xlsx 格式文件！")

    def mousePressEvent(self, event):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择数据文件", "", "Data Files (*.csv *.txt *.xlsx)"
        )
        if file_path:
            self.set_file(file_path)

    def set_file(self, file_path):
        self.file_path = file_path
        self.setText(f"已选择: {Path(file_path).name}")
        self.setStyleSheet("""
            QLabel {
                border: 2px solid #4CAF50; 
                border-radius: 5px; 
                padding: 20px; 
                color: #333; 
                background-color: #e8f5e9;
            }
        """)
        self.file_dropped.emit(file_path)


class AxisSettingsWidget(QWidget):
    """坐标轴参数设置组件 (对应 pyorigin.py 中的 AxisConfig)"""
    def __init__(self, title="Axis"):
        super().__init__()
        layout = QVBoxLayout()
        
        # ========== 标题设置 ==========
        title_group = QGroupBox(f"{title} 标题设置")
        title_form = QFormLayout()
        self.title_edit = QLineEdit("")
        self.title_font = QComboBox()
        self.title_font.addItems(['Times New Roman', 'Arial', 'Courier New', 'Helvetica'])
        self.title_color_btn = QPushButton("选择颜色")
        self.title_color_btn.clicked.connect(self.choose_title_color)
        self.title_color = (0, 0, 0) # 默认黑色
        
        self.title_bold = QCheckBox("加粗")
        self.title_bold.setChecked(True)
        self.title_italic = QCheckBox("斜体")
        self.title_underline = QCheckBox("下划线")
        self.title_size = QSpinBox()
        self.title_size.setRange(8, 100)
        self.title_size.setValue(36)

        title_form.addRow("标题文本:", self.title_edit)
        title_form.addRow("字体:", self.title_font)
        title_form.addRow("颜色:", self.title_color_btn)
        title_form.addRow("字号:", self.title_size)
        
        style_layout = QHBoxLayout()
        style_layout.addWidget(self.title_bold)
        style_layout.addWidget(self.title_italic)
        style_layout.addWidget(self.title_underline)
        title_form.addRow("样式:", style_layout)
        title_group.setLayout(title_form)
        layout.addWidget(title_group)

        # ========== 刻度与轴线设置 ==========
        axis_group = QGroupBox(f"{title} 刻度与轴线设置")
        axis_form = QFormLayout()
        self.axis_thickness = QDoubleSpinBox()
        self.axis_thickness.setRange(0.1, 10.0)
        self.axis_thickness.setValue(3.0)
        self.axis_bold = QCheckBox("刻度数字加粗")
        self.axis_bold.setChecked(True)
        self.axis_pt = QSpinBox()
        self.axis_pt.setRange(8, 100)
        self.axis_pt.setValue(26)
        self.axis_font = QComboBox()
        self.axis_font.addItems(['Times New Roman', 'Arial', 'Courier New', 'Helvetica'])
        self.axis_color_btn = QPushButton("选择颜色")
        self.axis_color_btn.clicked.connect(self.choose_axis_color)
        self.axis_color = (0, 0, 0)
        self.axis_ticks = QComboBox()
        self.axis_ticks.addItems(['inner', 'outer'])
        self.axis_show = QComboBox()
        self.axis_show.addItems(['0:不显示', '1:左下前', '2:右上后', '3:都显示'])
        self.axis_show.setCurrentIndex(3)

        axis_form.addRow("轴线粗细:", self.axis_thickness)
        axis_form.addRow("刻度数字字号:", self.axis_pt)
        axis_form.addRow("刻度数字字体:", self.axis_font)
        axis_form.addRow("轴线/刻度颜色:", self.axis_color_btn)
        axis_form.addRow("刻度朝向:", self.axis_ticks)
        axis_form.addRow("刻度显示:", self.axis_show)
        axis_form.addRow("", self.axis_bold)
        axis_group.setLayout(axis_form)
        layout.addWidget(axis_group)

        # ========== 范围设置 ==========
        range_group = QGroupBox(f"{title} 范围设置 (留空或0表示自动)")
        range_form = QFormLayout()
        self.begin_edit = QLineEdit("")
        self.begin_edit.setPlaceholderText("Auto")
        self.end_edit = QLineEdit("")
        self.end_edit.setPlaceholderText("Auto")
        self.step_edit = QLineEdit("")
        self.step_edit.setPlaceholderText("Auto")
        range_form.addRow("起始值 (Begin):", self.begin_edit)
        range_form.addRow("结束值 (End):", self.end_edit)
        range_form.addRow("步长 (Step):", self.step_edit)
        range_group.setLayout(range_form)
        layout.addWidget(range_group)

        layout.addStretch()
        self.setLayout(layout)

    def choose_title_color(self):
        color = QColorDialog.getColor(QColor(*self.title_color), self, "选择标题颜色")
        if color.isValid():
            self.title_color = (color.red(), color.green(), color.blue())
            self.title_color_btn.setStyleSheet(f"background-color: {color.name()}; color: white;")

    def choose_axis_color(self):
        color = QColorDialog.getColor(QColor(*self.axis_color), self, "选择轴线/刻度颜色")
        if color.isValid():
            self.axis_color = (color.red(), color.green(), color.blue())
            self.axis_color_btn.setStyleSheet(f"background-color: {color.name()}; color: white;")

    def get_config_params(self):
        """收集UI参数，返回用于实例化 AxisConfig 的字典"""
        def parse_float(text):
            try:
                return float(text) if text.strip() else None
            except ValueError:
                return None

        show_map = {0: 0, 1: 1, 2: 2, 3: 3}
        return {
            'title': self.title_edit.text(),
            'title_font': self.title_font.currentText(),
            'title_color': self.title_color,
            'title_bold': 1 if self.title_bold.isChecked() else 0,
            'title_italic': 1 if self.title_italic.isChecked() else 0,
            'title_underline': 1 if self.title_underline.isChecked() else 0,
            'title_font_size': self.title_size.value(),
            'axis_thickness': self.axis_thickness.value(),
            'axis_bold': 1 if self.axis_bold.isChecked() else 0,
            'axis_pt': self.axis_pt.value(),
            'axis_font': self.axis_font.currentText(),
            'axis_color': self.axis_color,
            'axis_ticks': self.axis_ticks.currentText(),
            'axis_show': show_map.get(self.axis_show.currentIndex(), 3),
            'begin': parse_float(self.begin_edit.text()),
            'end': parse_float(self.end_edit.text()),
            'step': parse_float(self.step_edit.text()),
        }


class LegendSettingsWidget(QWidget):
    """图例与图层设置组件 (对应 pyorigin.py 中的 TextConfig 和 LayConfig)"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # 图例设置
        legend_group = QGroupBox("图例 (Legend) 设置")
        legend_form = QFormLayout()
        self.legend_title = QLineEdit("")
        # 修改占位符提示
        self.legend_title.setPlaceholderText("留空则使用Y轴列名作为默认图例，多个图例用逗号分隔")
        self.legend_font = QComboBox()
        self.legend_font.addItems(['Times New Roman', 'Arial', 'Courier New', 'Helvetica'])
        self.legend_color_btn = QPushButton("选择颜色")
        self.legend_color_btn.clicked.connect(self.choose_color)
        self.legend_color = (0, 0, 0)
        self.legend_bold = QCheckBox("加粗")
        self.legend_bold.setChecked(True)
        self.legend_italic = QCheckBox("斜体")
        self.legend_underline = QCheckBox("下划线")
        self.legend_size = QSpinBox()
        self.legend_size.setRange(8, 100)
        self.legend_size.setValue(26)
        self.legend_bg = QComboBox()
        self.legend_bg.addItems(['0:透明', '1:白底', '2:灰底'])

        legend_form.addRow("图例文本:", self.legend_title)
        legend_form.addRow("字体:", self.legend_font)
        legend_form.addRow("颜色:", self.legend_color_btn)
        legend_form.addRow("字号:", self.legend_size)
        legend_form.addRow("背景:", self.legend_bg)
        
        style_layout = QHBoxLayout()
        style_layout.addWidget(self.legend_bold)
        style_layout.addWidget(self.legend_italic)
        style_layout.addWidget(self.legend_underline)
        legend_form.addRow("样式:", style_layout)
        legend_group.setLayout(legend_form)
        layout.addWidget(legend_group)

        # 图层设置
        layer_group = QGroupBox("图层 (Layer) 设置")
        layer_form = QFormLayout()
        self.frame_check = QCheckBox("显示边框 (Frame)")
        self.frame_check.setChecked(True)
        self.aa_check = QCheckBox("开启抗锯齿 (Anti-Aliasing)")
        self.aa_check.setChecked(True)
        layer_form.addRow("", self.frame_check)
        layer_form.addRow("", self.aa_check)
        layer_group.setLayout(layer_form)
        layout.addWidget(layer_group)

        layout.addStretch()
        self.setLayout(layout)

    def choose_color(self):
        color = QColorDialog.getColor(QColor(*self.legend_color), self, "选择图例颜色")
        if color.isValid():
            self.legend_color = (color.red(), color.green(), color.blue())
            self.legend_color_btn.setStyleSheet(f"background-color: {color.name()}; color: white;")

    def get_legend_params(self):
        title_text = self.legend_title.text().strip()
        title_list = [t.strip() for t in title_text.split(',')] if title_text else None
        
        return {
            'title': title_list,
            'font': self.legend_font.currentText(),
            'color': self.legend_color,
            'bold': 1 if self.legend_bold.isChecked() else 0,
            'italic': 1 if self.legend_italic.isChecked() else 0,
            'underline': 1 if self.legend_underline.isChecked() else 0,
            'font_size': self.legend_size.value(),
            'background': self.legend_bg.currentIndex(),
        }

    def get_layer_params(self):
        return {
            'frame': 1 if self.frame_check.isChecked() else 0,
            'aa': 1 if self.aa_check.isChecked() else 0,
        }


class PlotWorker(QThread):
    """后台绘图线程，防止 Origin 调用阻塞 UI"""
    log_signal = Signal(str)
    finished_signal = Signal(bool, str)

    def __init__(self, file_path, col_x, col_y, plot_params, x_params, y_params, legend_params, layer_params, save_params):
        super().__init__()
        self.file_path = file_path
        self.col_x = col_x
        self.col_y = col_y
        self.plot_params = plot_params
        self.x_params = x_params
        self.y_params = y_params
        self.legend_params = legend_params
        self.layer_params = layer_params
        self.save_params = save_params

    def run(self):
        if not ORIGIN_AVAILABLE:
            self.finished_signal.emit(False, "未检测到 pyorigin 或 originpro 库，无法绘图！")
            return

        try:
            self.log_signal.emit("正在读取数据...")
            df1 = po.read_data(self.file_path)

            self.log_signal.emit("正在启动 Origin 软件...")
            op.set_show(True)
            op.new()

            wb = op.new_book('w', 'Data')
            wks = wb.add_sheet()
            
            self.log_signal.emit("正在加载数据到工作表...")
            wks.from_df(pd.DataFrame({
                self.col_x: df1[self.col_x],
                self.col_y: df1[self.col_y],
            }))

            self.log_signal.emit("正在创建图形并绘制曲线...")
            gp = po.create_graph()
            lay = gp[0]

            po.plot_set(
                wks, lay, 
                colx=self.col_x, 
                coly=self.col_y, 
                color=self.plot_params['color'], 
                width=self.plot_params['width'], 
                type=self.plot_params['type']
            )

            self.log_signal.emit("正在应用坐标轴与图例参数...")
            # 实例化 Config 类 (必须在 op.set_show 之后)
            x_config = po.AxisConfig(**self.x_params)
            y_config = po.AxisConfig(**self.y_params)
            legend_config = po.TextConfig(**self.legend_params)
            
            lay_config = po.LayConfig(
                x=x_config, 
                y=y_config, 
                legend=legend_config,
                **self.layer_params
            )
            
            po.lay_set(gp, lay, lay_config)

            self.log_signal.emit("正在保存图像和工程文件...")
            po.graph_save(gp, self.save_params['image_name'])
            po.project_save(self.save_params['project_name'])

            self.log_signal.emit("✅ 绘图流程全部完成！")
            self.finished_signal.emit(True, "绘图成功！")

        except Exception as e:
            self.log_signal.emit(f"❌ 发生错误: {str(e)}")
            self.finished_signal.emit(False, str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Origin 自动化绘图 GUI")
        self.resize(1000, 700)
        self.df_columns = []

        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 使用 Splitter 分割左右布局
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # ================= 左侧面板 =================
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # 1. 文件导入区
        self.drop_area = DropArea()
        self.drop_area.file_dropped.connect(self.on_file_loaded)
        left_layout.addWidget(self.drop_area)

        # 2. 数据列与曲线设置
        data_group = QGroupBox("数据与曲线设置")
        data_form = QFormLayout()
        self.combo_x = QComboBox()
        self.combo_y = QComboBox()
        
        # 绑定下拉框改变信号，用于自动更新默认标题和图例
        self.combo_x.currentTextChanged.connect(self.on_column_changed)
        self.combo_y.currentTextChanged.connect(self.on_column_changed)
        
        self.line_color_btn = QPushButton("选择颜色")
        self.line_color_btn.clicked.connect(self.choose_line_color)
        self.line_color = (0, 0, 0)
        self.line_width = QDoubleSpinBox()
        self.line_width.setRange(0.1, 10.0)
        self.line_width.setValue(3.0)
        self.line_type = QComboBox()
        self.line_type.addItems(['l (实线)', 's (散点)', 'ls (线+点)'])

        data_form.addRow("X 轴数据列:", self.combo_x)
        data_form.addRow("Y 轴数据列:", self.combo_y)
        data_form.addRow("曲线颜色:", self.line_color_btn)
        data_form.addRow("曲线线宽:", self.line_width)
        data_form.addRow("图表类型:", self.line_type)
        data_group.setLayout(data_form)
        left_layout.addWidget(data_group)

        # 3. 保存设置
        save_group = QGroupBox("保存设置")
        save_form = QFormLayout()
        self.image_name_edit = QLineEdit("output.png")
        self.project_name_edit = QLineEdit("template_gui.opju")
        save_form.addRow("图片名称:", self.image_name_edit)
        save_form.addRow("工程名称:", self.project_name_edit)
        save_group.setLayout(save_form)
        left_layout.addWidget(save_group)

        # 4. 执行按钮
        self.btn_plot = QPushButton("🚀 开始绘图")
        self.btn_plot.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; color: white; border: none;
                padding: 12px; font-size: 16px; border-radius: 5px; font-weight: bold;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:pressed { background-color: #3e8e41; }
            QPushButton:disabled { background-color: #cccccc; }
        """)
        self.btn_plot.clicked.connect(self.start_plotting)
        left_layout.addWidget(self.btn_plot)

        # ================= 右侧面板 =================
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        self.tabs = QTabWidget()
        self.x_settings = AxisSettingsWidget("X 轴")
        self.y_settings = AxisSettingsWidget("Y 轴")
        self.legend_settings = LegendSettingsWidget()

        self.tabs.addTab(self.x_settings, "X 轴设置")
        self.tabs.addTab(self.y_settings, "Y 轴设置")
        self.tabs.addTab(self.legend_settings, "图例与图层")
        right_layout.addWidget(self.tabs)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([350, 650])

        # ================= 底部日志区 =================
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setPlaceholderText("运行日志将显示在这里...")
        self.log_area.setMaximumHeight(150)
        main_layout.addWidget(self.log_area)

        self.worker = None

    def on_file_loaded(self, file_path):
        """文件加载后，读取列名填充 ComboBox"""
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, nrows=0)
            elif file_path.endswith('.txt'):
                df = pd.read_csv(file_path, sep='\t', nrows=0)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path, nrows=0)
            else:
                return

            self.df_columns = df.columns.tolist()
            self.combo_x.clear()
            self.combo_y.clear()
            self.combo_x.addItems(self.df_columns)
            self.combo_y.addItems(self.df_columns)
            
            if len(self.df_columns) >= 2:
                self.combo_y.setCurrentIndex(1)
                
            # 文件加载完毕后，主动触发一次默认值更新
            self.on_column_changed()
            self.log(f"成功加载文件，识别到 {len(self.df_columns)} 列数据。")
        except Exception as e:
            QMessageBox.critical(self, "读取错误", f"无法读取文件列名:\n{str(e)}")

    def on_column_changed(self):
        """当选择的X或Y列改变时，自动更新默认的轴标题和图例名称"""
        x_col = self.combo_x.currentText()
        y_col = self.combo_y.currentText()
        
        # 1. 给x轴标题的默认值为用于x轴绘图的表头
        if x_col:
            self.x_settings.title_edit.setText(x_col)
            
        # 2. 给y轴标题的默认值为用于y轴绘图的表头
        if y_col:
            self.y_settings.title_edit.setText(y_col)
            
        # 3. 图例的默认名字为y的表头
        if y_col:
            self.legend_settings.legend_title.setText(y_col)

    def choose_line_color(self):
        color = QColorDialog.getColor(QColor(*self.line_color), self, "选择曲线颜色")
        if color.isValid():
            self.line_color = (color.red(), color.green(), color.blue())
            self.line_color_btn.setStyleSheet(f"background-color: {color.name()}; color: white;")

    def log(self, message):
        self.log_area.append(message)
        QApplication.processEvents()

    def start_plotting(self):
        if not self.drop_area.file_path:
            QMessageBox.warning(self, "提示", "请先导入数据文件！")
            return
        if not self.combo_x.currentText() or not self.combo_y.currentText():
            QMessageBox.warning(self, "提示", "请选择 X 和 Y 数据列！")
            return

        self.btn_plot.setEnabled(False)
        self.btn_plot.setText("⏳ 正在绘图...")
        self.log_area.clear()
        self.log(">>> 开始执行绘图流程...")

        # 收集所有参数
        plot_params = {
            'color': self.line_color,
            'width': self.line_width.value(),
            'type': self.line_type.currentText().split(' ')[0] # 提取 'l', 's' 等
        }
        save_params = {
            'image_name': self.image_name_edit.text(),
            'project_name': self.project_name_edit.text()
        }

        # 启动后台线程
        self.worker = PlotWorker(
            file_path=self.drop_area.file_path,
            col_x=self.combo_x.currentText(),
            col_y=self.combo_y.currentText(),
            plot_params=plot_params,
            x_params=self.x_settings.get_config_params(),
            y_params=self.y_settings.get_config_params(),
            legend_params=self.legend_settings.get_legend_params(),
            layer_params=self.legend_settings.get_layer_params(),
            save_params=save_params
        )
        self.worker.log_signal.connect(self.log)
        self.worker.finished_signal.connect(self.on_plot_finished)
        self.worker.start()

    def on_plot_finished(self, success, message):
        self.btn_plot.setEnabled(True)
        self.btn_plot.setText("🚀 开始绘图")
        if success:
            self.log(f">>> 任务结束: {message}")
        else:
            self.log(f">>> 任务失败: {message}")
            QMessageBox.critical(self, "绘图失败", f"绘图过程中发生错误:\n{message}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置全局样式
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())