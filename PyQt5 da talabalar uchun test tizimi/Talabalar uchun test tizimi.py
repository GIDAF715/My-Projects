import sys
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QRadioButton,
    QButtonGroup, QStackedWidget, QTableWidget, QTableWidgetItem,
    QMessageBox, QInputDialog, QScrollArea, QFrame, QProgressBar,
    QComboBox, QSpinBox, QDialog, QDialogButtonBox, QGroupBox,
    QHeaderView, QSplitter
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap, QIcon, QPainter, QLinearGradient

# ===================== STYLES =====================
STYLE = """
QMainWindow {
    background-color: #0f1117;
}
QWidget {
    background-color: #0f1117;
    color: #e0e0e0;
    font-family: 'Segoe UI', Arial;
}
QPushButton {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #1d4ed8;
}
QPushButton:pressed {
    background-color: #1e40af;
}
QPushButton#danger {
    background-color: #dc2626;
}
QPushButton#danger:hover {
    background-color: #b91c1c;
}
QPushButton#success {
    background-color: #16a34a;
}
QPushButton#success:hover {
    background-color: #15803d;
}
QPushButton#secondary {
    background-color: #374151;
}
QPushButton#secondary:hover {
    background-color: #4b5563;
}
QLineEdit, QTextEdit, QComboBox, QSpinBox {
    background-color: #1e2130;
    border: 1px solid #374151;
    border-radius: 6px;
    padding: 8px 12px;
    color: #e0e0e0;
    font-size: 13px;
}
QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #2563eb;
}
QLabel#title {
    font-size: 28px;
    font-weight: bold;
    color: #60a5fa;
}
QLabel#subtitle {
    font-size: 16px;
    color: #9ca3af;
}
QLabel#section {
    font-size: 18px;
    font-weight: bold;
    color: #93c5fd;
}
QLabel#question_num {
    font-size: 15px;
    font-weight: bold;
    color: #fbbf24;
}
QTableWidget {
    background-color: #1e2130;
    border: 1px solid #374151;
    border-radius: 8px;
    gridline-color: #374151;
}
QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #2d3748;
}
QTableWidget::item:selected {
    background-color: #2563eb;
}
QHeaderView::section {
    background-color: #1a1f2e;
    color: #9ca3af;
    padding: 10px;
    border: none;
    border-right: 1px solid #374151;
    font-weight: bold;
}
QProgressBar {
    background-color: #1e2130;
    border: none;
    border-radius: 4px;
    height: 10px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #2563eb;
    border-radius: 4px;
}
QRadioButton {
    font-size: 14px;
    padding: 8px;
    color: #d1d5db;
}
QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 2px solid #4b5563;
    background: #1e2130;
}
QRadioButton::indicator:checked {
    background: #2563eb;
    border: 2px solid #2563eb;
}
QGroupBox {
    border: 1px solid #374151;
    border-radius: 8px;
    margin-top: 12px;
    padding: 10px;
    color: #9ca3af;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}
QScrollArea {
    border: none;
}
QScrollBar:vertical {
    background: #1e2130;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #4b5563;
    border-radius: 4px;
}
"""

DATA_FILE = "test_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"tests": [], "results": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ===================== DIALOG: SAVOL QO'SHISH =====================
class QuestionDialog(QDialog):
    def __init__(self, parent=None, question=None):
        super().__init__(parent)
        self.setWindowTitle("Savol qo'shish / tahrirlash")
        self.setMinimumSize(600, 500)
        self.setStyleSheet(STYLE)
        self.setup_ui()
        if question:
            self.load_question(question)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        lbl = QLabel("Savol matni:")
        lbl.setObjectName("section")
        layout.addWidget(lbl)

        self.question_text = QTextEdit()
        self.question_text.setPlaceholderText("Savol matnini kiriting...")
        self.question_text.setFixedHeight(100)
        layout.addWidget(self.question_text)

        lbl2 = QLabel("Javob variantlari (to'g'ri javobni belgilang):")
        lbl2.setObjectName("section")
        layout.addWidget(lbl2)

        self.options = []
        self.radio_group = QButtonGroup(self)
        for i in range(4):
            row = QHBoxLayout()
            rb = QRadioButton(f"{chr(65+i)})")
            self.radio_group.addButton(rb, i)
            le = QLineEdit()
            le.setPlaceholderText(f"{chr(65+i)} variantini kiriting")
            row.addWidget(rb)
            row.addWidget(le)
            layout.addLayout(row)
            self.options.append((rb, le))

        self.options[0][0].setChecked(True)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.Ok).setText("Saqlash")
        buttons.button(QDialogButtonBox.Cancel).setText("Bekor")
        layout.addWidget(buttons)

    def load_question(self, q):
        self.question_text.setPlainText(q["text"])
        for i, (rb, le) in enumerate(self.options):
            le.setText(q["options"][i] if i < len(q["options"]) else "")
        self.options[q.get("correct", 0)][0].setChecked(True)

    def get_question(self):
        opts = [le.text().strip() for _, le in self.options]
        correct = self.radio_group.checkedId()
        return {
            "text": self.question_text.toPlainText().strip(),
            "options": opts,
            "correct": correct
        }

    def validate(self):
        q = self.get_question()
        if not q["text"]:
            QMessageBox.warning(self, "Xato", "Savol matnini kiriting!")
            return False
        if any(o == "" for o in q["options"]):
            QMessageBox.warning(self, "Xato", "Barcha variantlarni to'ldiring!")
            return False
        return True

    def accept(self):
        if self.validate():
            super().accept()

# ===================== DIALOG: TEST YARATISH =====================
class CreateTestDialog(QDialog):
    def __init__(self, parent=None, test=None):
        super().__init__(parent)
        self.setWindowTitle("Test yaratish")
        self.setMinimumSize(700, 600)
        self.setStyleSheet(STYLE)
        self.questions = []
        if test:
            self.questions = list(test.get("questions", []))
        self.setup_ui()
        if test:
            self.name_edit.setText(test.get("name", ""))
            self.time_spin.setValue(test.get("time_limit", 10))
            self.refresh_table()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Test ma'lumotlari")
        title.setObjectName("title")
        layout.addWidget(title)

        row = QHBoxLayout()
        row.addWidget(QLabel("Test nomi:"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Test nomini kiriting")
        row.addWidget(self.name_edit)
        layout.addLayout(row)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Vaqt chegarasi (daqiqa):"))
        self.time_spin = QSpinBox()
        self.time_spin.setRange(1, 120)
        self.time_spin.setValue(10)
        row2.addWidget(self.time_spin)
        row2.addStretch()
        layout.addLayout(row2)

        sec = QLabel("Savollar")
        sec.setObjectName("section")
        layout.addWidget(sec)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["#", "Savol", "To'g'ri javob"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(2, 120)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        btn_row = QHBoxLayout()
        btn_add = QPushButton("➕ Savol qo'shish")
        btn_add.setObjectName("success")
        btn_add.clicked.connect(self.add_question)

        btn_edit = QPushButton("✏️ Tahrirlash")
        btn_edit.setObjectName("secondary")
        btn_edit.clicked.connect(self.edit_question)

        btn_del = QPushButton("🗑️ O'chirish")
        btn_del.setObjectName("danger")
        btn_del.clicked.connect(self.delete_question)

        btn_row.addWidget(btn_add)
        btn_row.addWidget(btn_edit)
        btn_row.addWidget(btn_del)
        layout.addLayout(btn_row)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.Ok).setText("Saqlash")
        buttons.button(QDialogButtonBox.Cancel).setText("Bekor")
        layout.addWidget(buttons)

    def refresh_table(self):
        self.table.setRowCount(len(self.questions))
        for i, q in enumerate(self.questions):
            self.table.setItem(i, 0, QTableWidgetItem(str(i+1)))
            self.table.setItem(i, 1, QTableWidgetItem(q["text"][:60] + ("..." if len(q["text"]) > 60 else "")))
            correct_idx = q.get("correct", 0)
            opts = q.get("options", [])
            correct_text = opts[correct_idx] if correct_idx < len(opts) else ""
            self.table.setItem(i, 2, QTableWidgetItem(f"{chr(65+correct_idx)}) {correct_text[:20]}"))

    def add_question(self):
        dlg = QuestionDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            self.questions.append(dlg.get_question())
            self.refresh_table()

    def edit_question(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Info", "Savolni tanlang!")
            return
        dlg = QuestionDialog(self, self.questions[row])
        if dlg.exec_() == QDialog.Accepted:
            self.questions[row] = dlg.get_question()
            self.refresh_table()

    def delete_question(self):
        row = self.table.currentRow()
        if row < 0:
            return
        reply = QMessageBox.question(self, "O'chirish", "Savolni o'chirasizmi?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.questions.pop(row)
            self.refresh_table()

    def get_test(self):
        return {
            "name": self.name_edit.text().strip(),
            "time_limit": self.time_spin.value(),
            "questions": self.questions,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

    def accept(self):
        t = self.get_test()
        if not t["name"]:
            QMessageBox.warning(self, "Xato", "Test nomini kiriting!")
            return
        if not t["questions"]:
            QMessageBox.warning(self, "Xato", "Kamida bitta savol qo'shing!")
            return
        super().accept()

# ===================== TEST O'TKAZISH WIDGET =====================
class TestRunWidget(QWidget):
    finished = pyqtSignal(dict)

    def __init__(self, test, student_name, parent=None):
        super().__init__(parent)
        self.test = test
        self.student_name = student_name
        self.current = 0
        self.answers = {}
        self.time_left = test.get("time_limit", 10) * 60
        self.setup_ui()
        self.load_question()
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 20, 30, 20)

        # Header
        header = QHBoxLayout()
        self.test_name_lbl = QLabel(self.test["name"])
        self.test_name_lbl.setObjectName("title")
        header.addWidget(self.test_name_lbl)
        header.addStretch()

        self.timer_lbl = QLabel()
        self.timer_lbl.setStyleSheet("color: #fbbf24; font-size: 20px; font-weight: bold;")
        header.addWidget(self.timer_lbl)
        layout.addLayout(header)

        # Progress
        prog_row = QHBoxLayout()
        self.prog_lbl = QLabel()
        self.prog_lbl.setObjectName("question_num")
        prog_row.addWidget(self.prog_lbl)
        prog_row.addStretch()
        layout.addLayout(prog_row)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        # Question
        self.q_frame = QFrame()
        self.q_frame.setStyleSheet("background-color: #1e2130; border-radius: 12px; padding: 10px;")
        q_layout = QVBoxLayout(self.q_frame)

        self.q_lbl = QLabel()
        self.q_lbl.setWordWrap(True)
        self.q_lbl.setStyleSheet("font-size: 16px; color: #f0f0f0; padding: 10px;")
        q_layout.addWidget(self.q_lbl)

        self.btn_group = QButtonGroup(self)
        self.radio_btns = []
        for i in range(4):
            rb = QRadioButton()
            rb.setStyleSheet("font-size: 14px; padding: 8px; color: #d1d5db;")
            self.btn_group.addButton(rb, i)
            q_layout.addWidget(rb)
            self.radio_btns.append(rb)

        layout.addWidget(self.q_frame)
        layout.addStretch()

        # Navigation
        nav = QHBoxLayout()
        self.btn_prev = QPushButton("⬅ Oldingi")
        self.btn_prev.setObjectName("secondary")
        self.btn_prev.clicked.connect(self.prev_question)

        self.btn_next = QPushButton("Keyingi ➡")
        self.btn_next.clicked.connect(self.next_question)

        self.btn_finish = QPushButton("✅ Testni yakunlash")
        self.btn_finish.setObjectName("success")
        self.btn_finish.clicked.connect(self.finish_test)

        nav.addWidget(self.btn_prev)
        nav.addStretch()
        nav.addWidget(self.btn_next)
        nav.addWidget(self.btn_finish)
        layout.addLayout(nav)

    def tick(self):
        self.time_left -= 1
        mins = self.time_left // 60
        secs = self.time_left % 60
        self.timer_lbl.setText(f"⏱ {mins:02d}:{secs:02d}")
        if self.time_left <= 60:
            self.timer_lbl.setStyleSheet("color: #ef4444; font-size: 20px; font-weight: bold;")
        if self.time_left <= 0:
            self.timer.stop()
            QMessageBox.warning(self, "Vaqt tugadi!", "Vaqt tugadi! Test yakunlanadi.")
            self.finish_test()

    def load_question(self):
        total = len(self.test["questions"])
        q = self.test["questions"][self.current]
        self.prog_lbl.setText(f"Savol {self.current+1} / {total}")
        self.progress.setMaximum(total)
        self.progress.setValue(self.current + 1)
        self.q_lbl.setText(f"<b>{self.current+1}.</b> {q['text']}")

        for i, rb in enumerate(self.radio_btns):
            opt = q["options"][i] if i < len(q["options"]) else ""
            rb.setText(f"  {chr(65+i)})  {opt}")
            rb.setChecked(False)

        if self.current in self.answers:
            self.radio_btns[self.answers[self.current]].setChecked(True)

        self.btn_prev.setEnabled(self.current > 0)
        self.btn_next.setEnabled(self.current < total - 1)

    def save_answer(self):
        checked = self.btn_group.checkedId()
        if checked >= 0:
            self.answers[self.current] = checked

    def prev_question(self):
        self.save_answer()
        self.current -= 1
        self.load_question()

    def next_question(self):
        self.save_answer()
        self.current += 1
        self.load_question()

    def finish_test(self):
        self.save_answer()
        self.timer.stop()

        total = len(self.test["questions"])
        correct = 0
        for i, q in enumerate(self.test["questions"]):
            if self.answers.get(i) == q.get("correct"):
                correct += 1

        score = round(correct / total * 100) if total > 0 else 0
        result = {
            "student": self.student_name,
            "test_name": self.test["name"],
            "score": score,
            "correct": correct,
            "total": total,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "answers": self.answers
        }
        self.finished.emit(result)

# ===================== ASOSIY OYNA =====================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📚 Talabalar Test Tizimi")
        self.setMinimumSize(900, 650)
        self.data = load_data()
        self.setup_ui()
        self.show_home()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background-color: #0d1117; border-right: 1px solid #21262d;")
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(12, 20, 12, 20)
        sb_layout.setSpacing(8)

        logo = QLabel("📚 Test\nTizimi")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("font-size: 22px; font-weight: bold; color: #60a5fa; padding: 10px;")
        sb_layout.addWidget(logo)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #21262d;")
        sb_layout.addWidget(sep)
        sb_layout.addSpacing(10)

        self.nav_buttons = []
        nav_items = [
            ("🏠  Bosh sahifa", self.show_home),
            ("📝  Testlar", self.show_tests),
            ("▶️  Test boshlash", self.show_start_test),
            ("📊  Natijalar", self.show_results),
        ]
        for label, fn in nav_items:
            btn = QPushButton(label)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent; color: #9ca3af;
                    text-align: left; padding: 12px 16px;
                    border-radius: 8px; font-size: 14px;
                }
                QPushButton:hover { background: #1e2130; color: #e0e0e0; }
                QPushButton:checked { background: #1e3a5f; color: #60a5fa; }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(fn)
            sb_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sb_layout.addStretch()
        ver = QLabel("v1.0.0")
        ver.setStyleSheet("color: #4b5563; font-size: 11px;")
        ver.setAlignment(Qt.AlignCenter)
        sb_layout.addWidget(ver)

        main_layout.addWidget(sidebar)

        # Stack
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #0f1117;")
        main_layout.addWidget(self.stack)

        # Pages
        self.home_page = self._build_home()
        self.tests_page = self._build_tests()
        self.start_page = self._build_start()
        self.results_page = self._build_results()

        for p in [self.home_page, self.tests_page, self.start_page, self.results_page]:
            self.stack.addWidget(p)

    def set_nav(self, idx):
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == idx)

    # ---- HOME ----
    def _build_home(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel("Bosh sahifaga xush kelibsiz!")
        title.setObjectName("title")
        layout.addWidget(title)

        sub = QLabel("Talabalar uchun onlayn test tizimi")
        sub.setObjectName("subtitle")
        layout.addWidget(sub)

        layout.addSpacing(20)

        # Stats
        stats_row = QHBoxLayout()
        stats = [
            ("📝", "Testlar soni", len(self.data["tests"])),
            ("📊", "O'tkazilgan testlar", len(self.data["results"])),
            ("👥", "Talabalar", len(set(r["student"] for r in self.data["results"])) if self.data["results"] else 0),
        ]
        for icon, label, val in stats:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #1e2130;
                    border-radius: 12px;
                    border: 1px solid #374151;
                }
            """)
            cl = QVBoxLayout(card)
            cl.setContentsMargins(20, 20, 20, 20)
            il = QLabel(icon)
            il.setStyleSheet("font-size: 36px;")
            il.setAlignment(Qt.AlignCenter)
            vl = QLabel(str(val))
            vl.setStyleSheet("font-size: 28px; font-weight: bold; color: #60a5fa;")
            vl.setAlignment(Qt.AlignCenter)
            ll = QLabel(label)
            ll.setStyleSheet("color: #9ca3af; font-size: 13px;")
            ll.setAlignment(Qt.AlignCenter)
            cl.addWidget(il)
            cl.addWidget(vl)
            cl.addWidget(ll)
            stats_row.addWidget(card)

        layout.addLayout(stats_row)
        layout.addSpacing(20)

        quick = QLabel("Tezkor harakatlar")
        quick.setObjectName("section")
        layout.addWidget(quick)

        btns = QHBoxLayout()
        b1 = QPushButton("➕ Yangi test yaratish")
        b1.setObjectName("success")
        b1.clicked.connect(self.create_new_test)
        b2 = QPushButton("▶️ Test boshlash")
        b2.clicked.connect(self.show_start_test)
        b3 = QPushButton("📊 Natijalarni ko'rish")
        b3.setObjectName("secondary")
        b3.clicked.connect(self.show_results)
        btns.addWidget(b1)
        btns.addWidget(b2)
        btns.addWidget(b3)
        layout.addLayout(btns)

        layout.addStretch()
        return page

    # ---- TESTS ----
    def _build_tests(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        header = QHBoxLayout()
        t = QLabel("Testlar ro'yxati")
        t.setObjectName("title")
        header.addWidget(t)
        header.addStretch()
        btn_new = QPushButton("➕ Yangi test")
        btn_new.setObjectName("success")
        btn_new.clicked.connect(self.create_new_test)
        header.addWidget(btn_new)
        layout.addLayout(header)

        self.tests_table = QTableWidget(0, 4)
        self.tests_table.setHorizontalHeaderLabels(["Test nomi", "Savollar", "Vaqt (daq.)", "Yaratilgan"])
        self.tests_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tests_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tests_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.tests_table)

        btn_row = QHBoxLayout()
        btn_edit = QPushButton("✏️ Tahrirlash")
        btn_edit.setObjectName("secondary")
        btn_edit.clicked.connect(self.edit_test)
        btn_del = QPushButton("🗑️ O'chirish")
        btn_del.setObjectName("danger")
        btn_del.clicked.connect(self.delete_test)
        btn_row.addWidget(btn_edit)
        btn_row.addWidget(btn_del)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        return page

    def refresh_tests_table(self):
        tests = self.data["tests"]
        self.tests_table.setRowCount(len(tests))
        for i, t in enumerate(tests):
            self.tests_table.setItem(i, 0, QTableWidgetItem(t["name"]))
            self.tests_table.setItem(i, 1, QTableWidgetItem(str(len(t["questions"]))))
            self.tests_table.setItem(i, 2, QTableWidgetItem(str(t.get("time_limit", "-"))))
            self.tests_table.setItem(i, 3, QTableWidgetItem(t.get("created", "-")))

    # ---- START TEST ----
    def _build_start(self):
        page = QWidget()
        self.start_layout = QVBoxLayout(page)
        self.start_layout.setContentsMargins(40, 40, 40, 40)
        self.start_layout.setSpacing(15)
        self._show_start_form()
        return page

    def _show_start_form(self):
        # Clear layout
        while self.start_layout.count():
            item = self.start_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        t = QLabel("Test boshlash")
        t.setObjectName("title")
        self.start_layout.addWidget(t)

        form = QFrame()
        form.setStyleSheet("background-color: #1e2130; border-radius: 12px; padding: 5px;")
        fl = QVBoxLayout(form)
        fl.setContentsMargins(25, 25, 25, 25)
        fl.setSpacing(15)

        fl.addWidget(QLabel("Talaba ismi:"))
        self.student_name_edit = QLineEdit()
        self.student_name_edit.setPlaceholderText("Ismingizni kiriting")
        fl.addWidget(self.student_name_edit)

        fl.addWidget(QLabel("Testni tanlang:"))
        self.test_combo = QComboBox()
        self.test_combo.addItems([t["name"] for t in self.data["tests"]])
        fl.addWidget(self.test_combo)

        btn = QPushButton("▶️  Testni boshlash")
        btn.setObjectName("success")
        btn.clicked.connect(self.start_test)
        fl.addWidget(btn)

        self.start_layout.addWidget(form)
        self.start_layout.addStretch()

    def start_test(self):
        name = self.student_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Xato", "Ismingizni kiriting!")
            return
        idx = self.test_combo.currentIndex()
        if idx < 0 or idx >= len(self.data["tests"]):
            QMessageBox.warning(self, "Xato", "Test topilmadi!")
            return
        test = self.data["tests"][idx]

        # Clear and show test widget
        while self.start_layout.count():
            item = self.start_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.run_widget = TestRunWidget(test, name)
        self.run_widget.finished.connect(self.test_finished)
        self.start_layout.addWidget(self.run_widget)

    def test_finished(self, result):
        self.data["results"].append(result)
        save_data(self.data)

        score = result["score"]
        grade = "A'lo ✨" if score >= 86 else "Yaxshi 👍" if score >= 71 else "Qoniqarli 😐" if score >= 56 else "Qoniqarsiz ❌"

        msg = f"""
<b>Test yakunlandi!</b><br><br>
👤 Talaba: <b>{result['student']}</b><br>
📝 Test: <b>{result['test_name']}</b><br>
✅ To'g'ri javoblar: <b>{result['correct']} / {result['total']}</b><br>
🏆 Ball: <b>{score}%</b><br>
🎯 Baho: <b>{grade}</b>
        """
        QMessageBox.information(self, "Natija", msg)
        self._show_start_form()
        self.refresh_home()

    # ---- RESULTS ----
    def _build_results(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        header = QHBoxLayout()
        t = QLabel("Natijalar")
        t.setObjectName("title")
        header.addWidget(t)
        header.addStretch()
        btn_clear = QPushButton("🗑️ Tozalash")
        btn_clear.setObjectName("danger")
        btn_clear.clicked.connect(self.clear_results)
        header.addWidget(btn_clear)
        layout.addLayout(header)

        self.results_table = QTableWidget(0, 5)
        self.results_table.setHorizontalHeaderLabels(["Talaba", "Test nomi", "To'g'ri/Jami", "Ball", "Sana"])
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.results_table)

        return page

    def refresh_results_table(self):
        results = self.data["results"]
        self.results_table.setRowCount(len(results))
        for i, r in enumerate(results):
            self.results_table.setItem(i, 0, QTableWidgetItem(r["student"]))
            self.results_table.setItem(i, 1, QTableWidgetItem(r["test_name"]))
            self.results_table.setItem(i, 2, QTableWidgetItem(f"{r['correct']} / {r['total']}"))

            score_item = QTableWidgetItem(f"{r['score']}%")
            color = QColor("#16a34a") if r["score"] >= 86 else QColor("#d97706") if r["score"] >= 56 else QColor("#dc2626")
            score_item.setForeground(color)
            self.results_table.setItem(i, 3, score_item)
            self.results_table.setItem(i, 4, QTableWidgetItem(r.get("date", "-")))

    def clear_results(self):
        reply = QMessageBox.question(self, "Tozalash", "Barcha natijalarni o'chirasizmi?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.data["results"] = []
            save_data(self.data)
            self.refresh_results_table()
            self.refresh_home()

    # ---- NAVIGATION ----
    def show_home(self):
        self.refresh_home()
        self.stack.setCurrentIndex(0)
        self.set_nav(0)

    def refresh_home(self):
        # Rebuild home to refresh stats
        old = self.stack.widget(0)
        new = self._build_home()
        self.stack.insertWidget(0, new)
        self.stack.removeWidget(old)
        old.deleteLater()
        self.home_page = new

    def show_tests(self):
        self.refresh_tests_table()
        self.stack.setCurrentIndex(1)
        self.set_nav(1)

    def show_start_test(self):
        if not self.data["tests"]:
            QMessageBox.information(self, "Info", "Avval test yarating!")
            self.show_tests()
            return
        self._show_start_form()
        # Update combo
        self.test_combo.clear()
        self.test_combo.addItems([t["name"] for t in self.data["tests"]])
        self.stack.setCurrentIndex(2)
        self.set_nav(2)

    def show_results(self):
        self.refresh_results_table()
        self.stack.setCurrentIndex(3)
        self.set_nav(3)

    # ---- CRUD ----
    def create_new_test(self):
        dlg = CreateTestDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            self.data["tests"].append(dlg.get_test())
            save_data(self.data)
            self.refresh_tests_table()
            self.refresh_home()
            QMessageBox.information(self, "Muvaffaqiyat", "Test muvaffaqiyatli yaratildi!")

    def edit_test(self):
        row = self.tests_table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Info", "Testni tanlang!")
            return
        dlg = CreateTestDialog(self, self.data["tests"][row])
        if dlg.exec_() == QDialog.Accepted:
            self.data["tests"][row] = dlg.get_test()
            save_data(self.data)
            self.refresh_tests_table()

    def delete_test(self):
        row = self.tests_table.currentRow()
        if row < 0:
            return
        reply = QMessageBox.question(self, "O'chirish", "Testni o'chirasizmi?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.data["tests"].pop(row)
            save_data(self.data)
            self.refresh_tests_table()
            self.refresh_home()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()