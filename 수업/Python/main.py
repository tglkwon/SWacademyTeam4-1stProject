import os

def print_hi(name):
    print(f'Hi, {name}')


print_hi('PyCharm')

if __name__ == '__main__':
    print('활성화된 창입니다.')
    # import가 아니고 직접 실행시킬 때만 작동한다

print(os.__name__)

from PySide6.QtWidgets import QApplication, QWidget

app = QApplication()
widget = QWidget()
widget.show()
app.exec()