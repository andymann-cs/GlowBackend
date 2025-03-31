from moods import DB_CRUD
from PySide6.QtWidgets import QApplication, QMainWindow
import sys
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt

class testWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Piechart")
        self.setGeometry(100,100, 680, 500)

        self.create_piechart()
        self.show()


    def create_piechart(self):
        abc = DB_CRUD()
        a = abc.getMonthlyMood("67e373c2300f98be0a832ffc", 2, 2025)
        print(a)

        series = QPieSeries()

        for mood, count in a.items():
            series.append(mood, count)

        color_palette = [
            Qt.red, Qt.green, Qt.blue, Qt.yellow, Qt.cyan,
            Qt.magenta, Qt.darkRed, Qt.darkGreen, Qt.darkBlue
        ]

        for i, slice in enumerate(series.slices()):
            slice.setBrush(color_palette[i % len(color_palette)])
            slice.setLabelVisible(True) 


        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("How did you feel this month?")
      
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)


        self.setCentralWidget(chartview)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = testWindow()
    sys.exit(app.exec())