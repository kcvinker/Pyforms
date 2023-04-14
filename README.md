# Pyforms
Window GUI lib for Python

# Screenshots

![image](https://user-images.githubusercontent.com/8840907/232149272-7eb7c3c7-21bf-4819-9b35-057210836e51.png)

## Code which created the window in above screenshot

```python
from pyforms import Form, Button, TextBox, Label, ComboBox, ListBox, CheckBox, RadioButton, DateTimePicker, NumberPicker
from pyforms import TrackBar, ListView, TreeView, TreeNode, ChannelStyle, GroupBox, Color, ProgressBar, ProgressBarStyle
from pyforms import MenuType, MenuBar, MenuItem, CalendarBox
from pyforms.colors import ButtonGradientColors
from pyforms.commons import Timing
from pyforms.control import connect
from pyforms.enums import ViewMode, FormPosition
from pyforms.messagebox import *

import sys
import datetime as dt
is_main_module = __name__ == '__main__'


def main():
    def menu_click(m, e): print("Clicked menu - ", m._text)

    frm = Form("PyForms Window in Python", 700, 500)
    frm.formPos = FormPosition.MID_RIGHT
    frm.createHandle()
    frm.onMouseDown = lambda f, e: frm.printPoint(e)

    cal = CalendarBox(frm, 330, 20, bCreate = True)
    
    cmb = ComboBox(frm, 252, 380, bCreate = True)
    cmb.addItems("Windows", "Linux", "ReactOS")

    btn = Button(frm, "Normal")
    btn.foreColor = 0xFF0000
    btn.createHandle()

    b2 = Button(frm, "Flat")
    b2.setPosition(20, 80)
    b2.backColor = 0xee9b00
    b2.createHandle()

    b3 = Button(frm, "Gradient")
    b3.setPosition(20, 140)
    b3.setGradientColor(0x55a630, 0xeeef20)
    b3.createHandle()

    cb = CheckBox(frm, "Option set", 20, 200)
    cb.foreColor = 0x0033cc
    cb.createHandle()

    rb = RadioButton(frm, "Select Python", 20, 235)
    rb2 = RadioButton(frm, "Select VB.Net", 20, 275)
    rb.foreColor = 0xFF2512
    rb.createHandle()
    rb2.createHandle()

    lv = ListView(frm, 250, 212, 290, 150)
    lv.addColumns(["Names", "Age", "Job"], [90, 50, 120])
    lv.createHandle()
    lv.addRow("Vinod", 40, "Translator")
    lv.addRow("Vinayak", 33, "DTP Operator")
    lv.addRow("Vineetha", 39, "Cashier")

    dtp = DateTimePicker(frm, 155, 170)
    dtp.backColor =0x80aaff
    dtp.foreColor = 0xcc0000
    dtp.createHandle()

    tv = TreeView(frm, 155, 20, 160, 100)
    tv.backColor = 0xddddbb
    tv.createHandle()
    n1 = TreeNode("Root One")
    n2 = TreeNode("Root Two")
    n3 = TreeNode("First Child")
    n4 = TreeNode("Second Child")
    tv.addNodes(n1, n2)
    tv.addChildNode(n3, n1)
    tv.addChildNode(n4, n1)

    n5 = TreeNode("Middle Node")
    tv.insertNode(n5, 1)
    n6 = TreeNode("Middle Child")
    tv.insertChildNode(n6, n1, 0)

    tb = TextBox(frm, 155, 133)
    tb.text = "Simple"
    tb.createHandle()

    # gb = GroupBox(frm, "My Group", 328, 20, height=100)
    # gb.foreColor = 0xFF0000
    # gb.backColor = Color.fromRGB(200, 200, 180)
    # gb.createHandle()

    tk = TrackBar(frm, 25, 352, 200, 40)
    tk.ticColor = 0xFF0012
    tk.channelStyle = ChannelStyle.OUTLINE
    tk.createHandle()

    pb = ProgressBar(frm, 10, 307)
    pb.step = 10
    pb.createHandle()

    np1 = NumberPicker(frm, 155, 210)
    np1.buttonOnLeft = True
    np1.createHandle()

    np2 = NumberPicker(frm, 155, 240)
    np2.backColor = 0xfaa307
    np2.createHandle()

    np3 = NumberPicker(frm, 155, 275)
    np3.foreColor = 0xe5383b
    np3.createHandle()

    mbar = MenuBar(frm)
    fl = mbar.addMenu("File")
    edit = mbar.addMenu("Edit")
    helpm = mbar.addMenu("Help")

    stMenu = mbar.menus["File"].addMenu("Start")
    exMenu = mbar.menus["File"].addMenu("Exit")

    formMenu = mbar.menus["Edit"].addMenu("Format")
    delMenu = mbar.menus["Edit"].addMenu("Delete")
    stMenu.onClick = menu_click
    exMenu.onClick = menu_click
    helpm.onClick = menu_click
    mbar.create()

    @connect(tk, "onValueChanged")
    def event_func(b, e):
        pb.value = tk.value

    @connect(btn, "onClick")
    def on_b1_click(b, e):
        # tb.text = "Sample"
        tk.backColor = 0xffb703
        print(dtp.value)

    frm.display()

if is_main_module :
    main()
    
```
