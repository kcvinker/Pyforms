

from pyforms import (
    Form, Button, TextBox, Label, ComboBox, ListBox, 
    CheckBox, RadioButton, DateTimePicker, NumberPicker, 
    TrackBar, ListView, TreeView, TreeNode, ChannelStyle, 
    GroupBox, Color, ProgressBar, ProgressBarStyle, 
    MenuType, MenuBar, MenuItem, CalendarBox, Header, 
    ContextMenu, MenuState, FileOpenDialog, FileSaveDialog, 
    FolderBrowserDialog, TrayIcon, connect, ViewMode, 
    FormPosition, MenuStyle, trayBalloon)

from horology import Timing
import sys
import datetime as dt

# import sysconfig

is_main_module = __name__ == '__main__'

def loadtest(c, e):
    print("I am loaded")


frm = None
def main():
    global frm #, tk, pgb
    # def menu_click(m, e): print("Clicked menu - ", m._text)

    frm = Form("PyForms Window in Python", 800, 600)
    frm.createHandle()
    
    frm.createChilds = True
#     # frm.onLoad = loadtest
#     # frm.on_activate = lambda f, e: print("Activated ", f.text)
    frm.onMouseDown = lambda f, e: frm.printPoint(e)

#     tmr = frm.addTimer(1000, lambda f, e: print("Timer ticked..."))

    b1 = Button(frm, "Normal", 10, 10)
    b2 = Button(frm, "Flat Color", b1.right + 20, 10)
    b2.backColor = 0xee9b00
    b3 = Button(frm, "Gradient", b2.right + 20, 10)
    b3.setGradientColor(0x55a630, 0xeeef20)

#     # hdr = Header(frm, 340, 5)
#     # hdr.addItem("Manage", 70)
#     # hdr.addItem("Report", 70)
#     # hdr.addItem("Action", 70)

    cmb = ComboBox(frm, b3.right + 20, 10, items = ["Windows", "Linux", "ReactOS"])
    cmb.selectedIndex = 0

    dtp = DateTimePicker(frm, cmb.right + 20, 10)

    gb = GroupBox(frm, "Compiler Options", 10, b1.bottom + 10, width=170, height=170)
    gb.foreColor = 0x3a0ca3

    cb1 = CheckBox(frm, "Threads On", 20, gb.ypos + 32)
    cb2 = CheckBox(frm, "Hints Off", 20, cb1.bottom + 10)
    rb1 = RadioButton(frm, "Console App", 20, cb2.bottom + 20)
    rb2 = RadioButton(frm, "Gui App", 20, rb1.bottom + 10)
    rb1.foreColor = 0xFF2512

    gb2 = GroupBox(frm, "Project Details", 10, gb.bottom + 20, width=190, height=170)
    gb2.foreColor = 0xca6702

    lb1 = Label(frm, "Lines", 20, gb2.ypos + 32)
    np1 = NumberPicker(frm, lb1.right + 20, gb2.ypos + 32)

    lb2 = Label(frm, "Speed", 20, lb1.bottom + 20)
    np2 = NumberPicker(frm, lb2.right + 10, lb1.bottom + 20)
    np2.buttonOnLeft = True
    np2.decimalPlaces = 2
    np2.backColor = 0xffadad

    lv = ListView(frm, gb.right + 20, b1.bottom + 20, 330, 150, ["Windows", "MacOS", "Linux", 100, 130, 100])
    lv.addRow("XP", "Mountain Lion", "RedHat")
    lv.addRow("Vista", "Mavericks", "Mint")
    lv.addRow("Win7", "Monterey", "Ubuntu")
    lv.addRow("Win8", "Catalina", "Debian")
    lv.addRow("Win10", "Big Sur", "Kali")

    

    cal = CalendarBox(frm, gb.right + 20, lv.bottom + 20)

    tk = TrackBar(frm, cal.right + 30, 237, 60, 160, noCreate=True  )#20, np2.bottom + 10, 160, 40)
    tk.ticColor = 0xd90429
    tk.vertical = True
    tk.onMouseDown = lambda x, y: print(f"{y.xpos=}, {y.ypos=}")
    tk.createHandle()
    # tk.gettics()
    
    # tk.channelStyle = ChannelStyle.OUTLINE

    pgb = ProgressBar(frm, lv.right + 20, cmb.bottom + 20, 200, perc=True)


    cmenu = ContextMenu("Give Work", "Add Work", "Finish Work", "_", "Send Work")
    cmenu.menuItem("Give Work").enabled =  False
    cmenu.style = MenuStyle.CUSTOM
    lv.contextMenu = cmenu
    # cmenu.menus[0].onClick = lambda c, e: print("Add Work clicked ")



    tv = TreeView(frm, lv.right + 20, pgb.bottom + 10, 200, 175)
    tv.addNodeWithChilds("Windows", "Vista", "Win7", "Win8", "Win10", "Win11")
    tv.addNodeWithChilds("MacOS", "Mountain Lion", "Mavericks", "Catalina", "Big Sur", "Monterey")
    tv.addNodeWithChilds("Linux", "RedHat", "Mint", "Ubuntu", "Debian", "Kali")

    lbx = ListBox(frm, tk.right + 10, tv.bottom + 10, 200, 150)
    lbx.addItems("Windows", "Linux", "ReactOS")

    tb = TextBox(frm, gb2.right + 20, cal.bottom + 10, cal.width)
    tb.foreColor = 0x8338ec

    mbar = MenuBar(frm)
    fl = mbar.addMenu("File")
    edit = mbar.addMenu("Edit")
    helpm = mbar.addMenu("Help")

    stMenu = mbar.menus["File"].addMenu("Start")
    mbar.menus["File"].addSeperator()
    mbar.menus["File"].addMenu("Exit")

    fmt = mbar.menus["Edit"].addMenu("Format")

    dlt = mbar.menus["Edit"].addMenu("Delete")
    dlt.addMenu("Test")

    # stMenu.onClick = menu_click
    mbar.style = MenuStyle.CUSTOM
    fmt.state = MenuState.DISABLED
    # mbar.create()
    dlt.onFocus = lambda c, e: print("delete menu focused")

    ticon = TrayIcon("PyForms Tray")
    ticon.addContextMenu(["Windows", "Linux", "ReactOS"])


#     @b1.connect("onClick")
#     def on_b1_click(b, e):
#         trayBalloon("PyForms Balloon", "You have activated TrayIcon Balloon", 10)
#         # # tb.text = "Sample"
#         # # fod = FolderBrowserDialog("Open a folder", initDir="D:\\Work\\Shashikumar\\2023\\Jack Ryan")
#         # fod = FileOpenDialog("Select files", initDir="D:\\Work\\Shashikumar\\2023\\Jack Ryan", filterStr= "PDF files\0*.pdf\0")
#         # # fod = FileSaveDialog("Open a folder", initDir="D:\\Work\\Shashikumar\\2023\\Jack Ryan")
#         # # fod.filter = ".pdf"
#         # fod.multiSelection = True
#         # fod.showDialog(frm.handle)
#         # # print(fod.selectedFile)
#         # print(fod.fileNames)
#         # # print(fod._extStart)

#     @b2.connect("onClick")
#     def onB2Click(b, e):
#         print("Timer is going to start")
#         tmr.start()

#     def KeyDownfunc(f, e):
#         print(f"{e.keyCode} key down: {e.shiftPressed = }, {e.ctrlPressed = }, {e.altPressed = } ")
#     def KeyUpfunc(f, e):
#         print(f"{e.keyCode} key up: {e.shiftPressed = }, {e.ctrlPressed = }, {e.altPressed = } ")

#     frm.onKeyDown = KeyDownfunc
#     frm.onKeyUp = KeyUpfunc

    



# def on_form_display(f, e):
#     print(f.text)

if is_main_module :
    with Timing("Total time for forms and controls: "):
        main()

    frm.display()
#         # print(sysconfig.get_config_var("CC"))
#     @tk.connect("onValueChanged")
#     def onTrackChanged(c, e):
#         pgb.value = tk.value
    
    
    
    
    


#
#
# Use this function for combo, listbox & listview items.
# We can mimic dot net's data bound container controls with this.
def extract_field(objects, field):
    extracted_field = []
    for obj in objects:
        if hasattr(obj, field):
            extracted_field.append(getattr(obj, field))
        else:
            raise AttributeError(f"Object does not have attribute: {field}")
    return extracted_field
