
# Documentation for Pyforms GUI library

## **Index**
|Type | Type | Type | Type |
|------|------|-------|-------|
|[Button](#button-class)| [CalendarBox](#calendarbox-class)| [CheckBox](#checkbox-class)| [Color](#color-class)|
|[ComboBox](#combobox-class)|[DateTimePicker](#datetimepicker-class)|[Font](#font-class)|[GroupBox](#groupbox-class)|
|[KeyEventArgs]()| [KeyPressEventArgs]() |[Label](#label-class)|[ListBox](#listbox-class)|
[ListView](#listview-class)|[ListViewColumn]()|[ListViewItem]()|[MenuBar](#menubar-class) |
[MenuItem]()|[MouseEventArgs](#mouseeventargs-class)|[NumberPicker](#numberpicker-class)|[ProgressBar](#progressbar-class)|[RadioButton](#radiobutton-class)
|[SizeEventArgs](#sizeeventargs-class)|[TextBox](#textbox-class)|[TrackBar](#trackbar-class)|[TreeNode]()|
[TreeView](#treeview-class)|


---

## **Button class**

### Constructor
```python
Button(self, parent, txt: str = "", xpos = 20, ypos = 20, width = 120, height = 40, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```

---

### Functions
| Function Name      | Description |
|--------------------|-------------|
|createHandle()      | Creates the handle of button.

---


### Properties
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND     | Getter only.
|parent   |[Form](#form-class)     | Getter Only
|font     |[Font](#font-class)     |
|text     |string   |
|xpos     |int      |
|xpos     |int      |
|ypos     |int      |
|width    |int      |
|height   |int      |
|visibile |bool     |
|backColor|[Color](#color-class)/int|
|foreColor|[Color](#color-class)/int|

----

### **Events**
| Property Name      | Type        |
|--------------------|-------------|
|onMouseEnter     | [EventHandler](#event-handler-types)|
|onMouseDown      | [MouseEventHandler](#event-handler-types)|
|onMouseUp        | [MouseEventHandler](#event-handler-types)|
|onRightMouseDown | [MouseEventHandler](#event-handler-types)|
|onRightMouseUp   | [MouseEventHandler](#event-handler-types)|
|onRightClick     | [EventHandler](#event-handler-types)|
|onMouseLeave     | [EventHandler](#event-handler-types)|
|onDoubleClick    | [EventHandler](#event-handler-types)|
|onMouseWheel     | [MouseEventHandler](#event-handler-types)|
|onMouseMove      | [MouseEventHandler](#event-handler-types)|
|onMouseHover     | [EventHandler](#event-handler-types)|
|onKeyDown        | [KeyEventHandler](#event-handler-types)|
|onKeyUp          | [KeyEventHandler](#event-handler-types)|
|onKeyPress       | [KeyPressEventHandler](#event-handler-types)|
|onPaint          | [PaintEventHandler](#event-handler-types)|
|onGotFocus       | [EventHandler](#event-handler-types)|
|onLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|

---


## **CalendarBox class**

### Constructor
```python
CalendarBox(self, parent, xpos = 20, ypos = 20, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```

---

### Functions
| Function Name      | Description |
|--------------------|-------------|
|createHandle()      | Creates the handle of button.

---

### **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND     | Getter only.|
|parent   |[Form](#form-class)     | Getter Only|
|font     |[Font](#font-class)     |
|text     |string   |
|xpos     |int      |
|xpos     |int      |
|ypos     |int      |
|width    |int      |
|height   |int      |
|visibile |bool     |
|backColor|[Color](#color-class)/int|
|foreColor|[Color](#color-class)/int|
|value| [datetime](https://docs.python.org/3/library/datetime.html)|
|viewMode| [ViewMode](#viewmode-enum)| |
|oldViewMode| [ViewMode](#viewmode-enum)|
|showWeekNumber|   bool|
|noTodayCircle   | bool |
|noToday         | bool |
|noTrailingDates | bool |
|shortDateNames  | bool |

### **Events**
| Property Name      | Type        |
|--------------------|-------------|
|onMouseEnter     | [EventHandler](#event-handler-types)|
|onMouseDown      | [MouseEventHandler](#event-handler-types)|
|onMouseUp        | [MouseEventHandler](#event-handler-types)|
|onRightMouseDown | [MouseEventHandler](#event-handler-types)|
|onRightMouseUp   | [MouseEventHandler](#event-handler-types)|
|onRightClick     | [EventHandler](#event-handler-types)|
|onMouseLeave     | [EventHandler](#event-handler-types)|
|onDoubleClick    | [EventHandler](#event-handler-types)|
|onMouseWheel     | [MouseEventHandler](#event-handler-types)|
|onMouseMove      | [MouseEventHandler](#event-handler-types)|
|onMouseHover     | [EventHandler](#event-handler-types)|
|onKeyDown        | [KeyEventHandler](#event-handler-types)|
|onKeyUp          | [KeyEventHandler](#event-handler-types)|
|onKeyPress       | [KeyPressEventHandler](#event-handler-types)|
|onPaint          | [PaintEventHandler](#event-handler-types)|
|onGotFocus       | [EventHandler](#event-handler-types)|
|onLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|

---

## CheckBox class

### Constructor
```python
CheckBox(self, parent, xpos = 20, ypos = 20, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```

### Functions
| Function Name      | Description |
|--------------------|-------------|
|createHandle()      | Creates the handle of button.

----

### **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND     | Getter only.|
|parent   |[Form](#form-class)     | Getter Only|
|font     |[Font](#font-class)     |
|text     |string   |
|xpos     |int      |
|xpos     |int      |
|ypos     |int      |
|width    |int      |
|height   |int      |
|visibile |bool     |
|backColor|[Color](#color-class)/int|
|foreColor|[Color](#color-class)/int|
|rightAlign| bool|
|checked| bool|

----


### **Events**
| Property Name      | Type        |
|--------------------|-------------|
|onMouseEnter     | [EventHandler](#event-handler-types)|
|onMouseDown      | [MouseEventHandler](#event-handler-types)|
|onMouseUp        | [MouseEventHandler](#event-handler-types)|
|onRightMouseDown | [MouseEventHandler](#event-handler-types)|
|onRightMouseUp   | [MouseEventHandler](#event-handler-types)|
|onRightClick     | [EventHandler](#event-handler-types)|
|onMouseLeave     | [EventHandler](#event-handler-types)|
|onDoubleClick    | [EventHandler](#event-handler-types)|
|onMouseWheel     | [MouseEventHandler](#event-handler-types)|
|onMouseMove      | [MouseEventHandler](#event-handler-types)|
|onMouseHover     | [EventHandler](#event-handler-types)|
|onKeyDown        | [KeyEventHandler](#event-handler-types)|
|onKeyUp          | [KeyEventHandler](#event-handler-types)|
|onKeyPress       | [KeyPressEventHandler](#event-handler-types)|
|onPaint          | [PaintEventHandler](#event-handler-types)|
|onGotFocus       | [EventHandler](#event-handler-types)|
|onLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|
|onCheckedChanged | [EventHandler](#event-handler-types)|

---

# Color class
### Constructor
```python
Color(self, clr) # You can use int/Color
Color.fromColor(clr: int, change_value: int)
# Create a new Color from given int value and change it with given change_value. Returns a Color type

Color.fromRGB(red, green, blue) # Create new Color from given values
```
---

### Functions
```python
updateColor(self, clr: int) -> Color # Updates the color with new value
createHBrush(self, adj: float = 0) -> HBRUSH # Create an HBRUSH to use win api functions
createHPen(self, adj: float = 0) -> HPEN # Create HPEN to use in win api functions

changeToColorRef(self, adj: float) -> COLORREF
# Change the color with given value and returns COLORREF
# NOTE:  To make a  color lighter, use values greater than 1.0
#        To make color darker, use values lower than 1.0
```
----

### **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|value   |int     | Getter only.|
|ref| COLORREF| Getterr only|
|red| int| Getterr only|
|green| int| Getterr only|
|blue| int| Getterr only|

---

## **ComboBox class**

### Constructor
```python
ComboBox(self, parent, xpos: int = 10, ypos: int = 10, width: int = 120, height: int = 30, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```
####        Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|

### Functions
| Function Name      | Description |
|--------------------|-------------|
|createHandle()      | Creates the handle of button.

### Properties
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND     | Getter only.
|parent   |[Form](#form-class)     | Getter Only
|font     |[Font](#font-class)     |
|text     |string   |
|xpos     |int      |
|xpos     |int      |
|ypos     |int      |
|width    |int      |
|height   |int      |
|visibile |bool     |
|backColor|[Color](#color-class)/int|
|foreColor|[Color](#color-class)/int|

### Events
| Property Name      | Type        |
|--------------------|-------------|
|onMouseEnter     | [EventHandler](#event-handler-types)|
|onMouseDown      | [MouseEventHandler](#event-handler-types)|
|onMouseUp        | [MouseEventHandler](#event-handler-types)|
|onRightMouseDown | [MouseEventHandler](#event-handler-types)|
|onRightMouseUp   | [MouseEventHandler](#event-handler-types)|
|onRightClick     | [EventHandler](#event-handler-types)|
|onMouseLeave     | [EventHandler](#event-handler-types)|
|onDoubleClick    | [EventHandler](#event-handler-types)|
|onMouseWheel     | [MouseEventHandler](#event-handler-types)|
|onMouseMove      | [MouseEventHandler](#event-handler-types)|
|onMouseHover     | [EventHandler](#event-handler-types)|
|onKeyDown        | [KeyEventHandler](#event-handler-types)|
|onKeyUp          | [KeyEventHandler](#event-handler-types)|
|onKeyPress       | [KeyPressEventHandler](#event-handler-types)|
|onPaint          | [PaintEventHandler](#event-handler-types)|
|onGotFocus       | [EventHandler](#event-handler-types)|
|nLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|


## DateTimePicker class

### Constructor
```python
DateTimePicker(self, parent, xpos = 20, ypos = 20, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|


## Event handler types
| Name      | Signature        |
|--------------------|-------------|
|EventHandler| func(Control, EventArgs)|
|MouseEventHandler|func(Control, MouseEventArgs) |
|KeyEventHandler| func(Control, KeyEventArgs)|
|KeyPressEventHandler| func(Control, KeyPressEventArgs)|
|PaintEventHandler| func(Control, PaintEventArgs)|


# **Font class**
### Constructor
```python
Font(self, name: str = "Tahoma", size: int = 11, weight: FontWeight = FontWeight.NORMAL, italics: bool = False, underLine: bool = False)
```

----
#### Properties
| Name      |Type| Description |
|-----------|------|-------|
|name | string||
|size | int ||
|weight | [FontWeight](#fontweight-enum)||
|italics| bool ||
|underLine| bool ||

----



# Form class
### Constructor
```python
Form(self, txt = "", width = 500, height = 400, bCreate = False)
# bCreate: bool - if this is true, you don't need to call createHandle
```
-------------

## Functions
```python
createHandle(self)
printPoint(self, me: [MouseEventArgs]())
setGradientColor(self, clr1, clr2, top2btm = True)
display(self)
```

### Properties
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND     | Getter only.
|parent   |[Form](#form-class)     | Getter Only
|font     |[Font](#font-class)     |
|text     |string   |
|xpos     |int      |
|xpos     |int      |
|ypos     |int      |
|width    |int      |
|height   |int      |
|visibile |bool     |
|backColor|[Color](#color-class)/int|
|foreColor|[Color](#color-class)/int|
|formID | int| Uniqe id for a form(Read only)|
|formPos | [FormPosition](#formposition-enum)| |
|formStyle | [FormStyle](#formstyle-enum)| |
|formState | [FormState](#formstate-enum)| |

----

### **Events**
| Event Name      | Type        |
|--------------------|-------------|
|onMouseEnter     | [EventHandler](#event-handler-types)|
|onMouseDown      | [MouseEventHandler](#event-handler-types)|
|onMouseUp        | [MouseEventHandler](#event-handler-types)|
|onRightMouseDown | [MouseEventHandler](#event-handler-types)|
|onRightMouseUp   | [MouseEventHandler](#event-handler-types)|
|onRightClick     | [EventHandler](#event-handler-types)|
|onMouseLeave     | [EventHandler](#event-handler-types)|
|onDoubleClick    | [EventHandler](#event-handler-types)|
|onMouseWheel     | [MouseEventHandler](#event-handler-types)|
|onMouseMove      | [MouseEventHandler](#event-handler-types)|
|onMouseHover     | [EventHandler](#event-handler-types)|
|onKeyDown        | [KeyEventHandler](#event-handler-types)|
|onKeyUp          | [KeyEventHandler](#event-handler-types)|
|onKeyPress       | [KeyPressEventHandler](#event-handler-types)|
|onPaint          | [PaintEventHandler](#event-handler-types)|
|onGotFocus       | [EventHandler](#event-handler-types)|
|onLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|
|onLoad | [EventHandler](#event-handler-types)|
|onMinimized | [EventHandler](#event-handler-types)|
|onMaximized | [EventHandler](#event-handler-types)|
|onRestored | [EventHandler](#event-handler-types)|
|onClosing | [EventHandler](#event-handler-types)|
|onClosed | [EventHandler](#event-handler-types)|
|onActivate | [EventHandler](#event-handler-types)|
|onDeActivate | [EventHandler](#event-handler-types)|
|onMoving | [EventHandler](#event-handler-types)|
|onMoved | [EventHandler](#event-handler-types)|
|onSizing | [SizeEventArgs](#sizeeventargs-class)|
|onSized | [SizeEventArgs](#sizeeventargs-class)|

----



## **GroupBox class**
### Constructor
```python
GroupBox(self, parent, txt: str = "", xpos: int = 10, ypos: int = 10, width: int = 300, height: int = 300, bCreate = False )
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```
## Functions
```python
createHandle(self)
```

### Properties
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND     | Getter only.
|parent   |[Form](#form-class)     | Getter Only
|font     |[Font](#font-class)     |
|text     |string   |
|xpos     |int      |
|xpos     |int      |
|ypos     |int      |
|width    |int      |
|height   |int      |
|visibile |bool     |
|backColor|[Color](#color-class)/int|
|foreColor|[Color](#color-class)/int|

----

### **Events**
| Event Name      | Type        |
|--------------------|-------------|
|onMouseEnter     | [EventHandler](#event-handler-types)|
|onMouseDown      | [MouseEventHandler](#event-handler-types)|
|onMouseUp        | [MouseEventHandler](#event-handler-types)|
|onRightMouseDown | [MouseEventHandler](#event-handler-types)|
|onRightMouseUp   | [MouseEventHandler](#event-handler-types)|
|onRightClick     | [EventHandler](#event-handler-types)|
|onMouseLeave     | [EventHandler](#event-handler-types)|
|onDoubleClick    | [EventHandler](#event-handler-types)|
|onMouseWheel     | [MouseEventHandler](#event-handler-types)|
|onMouseMove      | [MouseEventHandler](#event-handler-types)|
|onMouseHover     | [EventHandler](#event-handler-types)|
|onKeyDown        | [KeyEventHandler](#event-handler-types)|
|onKeyUp          | [KeyEventHandler](#event-handler-types)|
|onKeyPress       | [KeyPressEventHandler](#event-handler-types)|
|onPaint          | [PaintEventHandler](#event-handler-types)|
|onGotFocus       | [EventHandler](#event-handler-types)|
|onLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|

--------------


## **Label class**

### Constructor
```python
Label(self, parent, txt: str = "", xpos: int = 10, ypos: int = 10, width: int = 120, height: int = 30, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```
## Functions
```python
createHandle(self)
```

### Properties
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND     | Getter only.
|parent   |[Form](#form-class)     | Getter Only
|font     |[Font](#font-class)     |
|text     |string   |
|xpos     |int      |
|xpos     |int      |
|ypos     |int      |
|width    |int      |
|height   |int      |
|visibile |bool     |
|backColor|[Color](#color-class)/int|
|foreColor|[Color](#color-class)/int|
|autoSize | bool | |
|multiLine | bool | |
|textAlign | [TextAlignment](#textalignment-enum) | |
|borderStyle | [LabelBorder](#labelborder-enum) | |

----

### **Events**
| Event Name      | Type        |
|--------------------|-------------|
|onMouseEnter     | [EventHandler](#event-handler-types)|
|onMouseDown      | [MouseEventHandler](#event-handler-types)|
|onMouseUp        | [MouseEventHandler](#event-handler-types)|
|onRightMouseDown | [MouseEventHandler](#event-handler-types)|
|onRightMouseUp   | [MouseEventHandler](#event-handler-types)|
|onRightClick     | [EventHandler](#event-handler-types)|
|onMouseLeave     | [EventHandler](#event-handler-types)|
|onDoubleClick    | [EventHandler](#event-handler-types)|
|onMouseWheel     | [MouseEventHandler](#event-handler-types)|
|onMouseMove      | [MouseEventHandler](#event-handler-types)|
|onMouseHover     | [EventHandler](#event-handler-types)|
|onKeyDown        | [KeyEventHandler](#event-handler-types)|
|onKeyUp          | [KeyEventHandler](#event-handler-types)|
|onKeyPress       | [KeyPressEventHandler](#event-handler-types)|
|onPaint          | [PaintEventHandler](#event-handler-types)|
|onGotFocus       | [EventHandler](#event-handler-types)|
|onLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|

------------

## **ListBox class**
### Constructor
```python
ListBox(self, parent, xpos: int = 10, ypos: int = 10, width: int = 150, height: int = 200, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```
## Functions
```python
createHandle(self)
selectAll(self)
clearSelection(self)
insertItem(self, item: string, index: int)
removeItem(self, index: int)
removeAll(self)
```

### Properties
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND     | Getter only.
|parent   |[Form](#form-class)     | Getter Only
|font     |[Font](#font-class)     |
|text     |string   |
|xpos     |int      |
|xpos     |int      |
|ypos     |int      |
|width    |int      |
|height   |int      |
|visibile |bool     |
|backColor|[Color](#color-class)/int|
|foreColor|[Color](#color-class)/int|
|items| list[string] | Getter only|
|hasHScroll | bool | |
|hasHScroll | bool | |
|hasVScroll | bool | |
|selectedIndex | int | |
|selectedIndices | list[int] | Getter only |
|multiSelection | bool | |
|selectedItem | string | |
|hotIndex | int | Getter only|
|selectedItems | list[string] | Getter only|
|hotItem | string | Getter only|

----

### **Events**
| Event Name      | Type        |
|--------------------|-------------|
|onMouseEnter     | [EventHandler](#event-handler-types)|
|onMouseDown      | [MouseEventHandler](#event-handler-types)|
|onMouseUp        | [MouseEventHandler](#event-handler-types)|
|onRightMouseDown | [MouseEventHandler](#event-handler-types)|
|onRightMouseUp   | [MouseEventHandler](#event-handler-types)|
|onRightClick     | [EventHandler](#event-handler-types)|
|onMouseLeave     | [EventHandler](#event-handler-types)|
|onDoubleClick    | [EventHandler](#event-handler-types)|
|onMouseWheel     | [MouseEventHandler](#event-handler-types)|
|onMouseMove      | [MouseEventHandler](#event-handler-types)|
|onMouseHover     | [EventHandler](#event-handler-types)|
|onKeyDown        | [KeyEventHandler](#event-handler-types)|
|onKeyUp          | [KeyEventHandler](#event-handler-types)|
|onKeyPress       | [KeyPressEventHandler](#event-handler-types)|
|onPaint          | [PaintEventHandler](#event-handler-types)|
|onGotFocus       | [EventHandler](#event-handler-types)|
|onLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|
|onSelectionChanged | [EventHandler](#event-handler-types)|

-----


## **ListView class**

### Constructor
```python
ListView(self, parent, xpos: int = 10, ypos: int = 10, width: int = 250, height: int = 200, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```

## Functions
```python
createHandle(self)
addColumn(self, txt: str, width: int = 100, image_index: int = -1)
addColumnEx(self, lvc: ListViewColumn)
addColumns(self, col_names: list[str], col_widths: list[int])
addRow(self, *items)
# selectAll(self)
# clearSelection(self)
# insertItem(self, item: string, index: int)
# removeItem(self, index: int)
# removeAll(self)
```

### **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND     | Getter only.
|parent   |[Form](#form-class)     | Getter Only
|font     |[Font](#font-class)     |
|text     |string   |
|xpos     |int      |
|xpos     |int      |
|ypos     |int      |
|width    |int      |
|height   |int      |
|visibile |bool     |
|backColor|[Color](#color-class)/int|
|foreColor|[Color](#color-class)/int|
|items    | list[[ListViewItem](#listviewcolumn-class)] | Getter only|
|selectedIndex | int | |
|checked | bool | |
|columns | list[[ListViewColumn](#listviewcolumn-class)] | |
|headerVisualStyle | bool | |
|headerHeight | int | |
|editLabel | bool | |
|hideSelection | bool | |
|multiSelection | bool | |
|hasCheckBox | bool | |
|fullRowSelection | bool | |
|showGrid | bool | |
|oneClickActivate | bool | |
|hotTrackSelection | bool | |
|headerClickable | bool | |
|checkBoxLast | bool | |
|headerBackColor | [Color](#color-class)/int | |
|headerForeColor | [Color](#color-class)/int | |
|headerFont | [Font](#font-class) | |
|selectedItem | [ListViewItem](#listviewitem-class) | |
|viewStyle | [ListViewStyle](#listviewstyle-enum) | |

----

### **Events**
| Event Name      | Type        |
|--------------------|-------------|
|onMouseEnter     | [EventHandler](#event-handler-types)|
|onMouseDown      | [MouseEventHandler](#event-handler-types)|
|onMouseUp        | [MouseEventHandler](#event-handler-types)|
|onRightMouseDown | [MouseEventHandler](#event-handler-types)|
|onRightMouseUp   | [MouseEventHandler](#event-handler-types)|
|onRightClick     | [EventHandler](#event-handler-types)|
|onMouseLeave     | [EventHandler](#event-handler-types)|
|onDoubleClick    | [EventHandler](#event-handler-types)|
|onMouseWheel     | [MouseEventHandler](#event-handler-types)|
|onMouseMove      | [MouseEventHandler](#event-handler-types)|
|onMouseHover     | [EventHandler](#event-handler-types)|
|onKeyDown        | [KeyEventHandler](#event-handler-types)|
|onKeyUp          | [KeyEventHandler](#event-handler-types)|
|onKeyPress       | [KeyPressEventHandler](#event-handler-types)|
|onPaint          | [PaintEventHandler](#event-handler-types)|
|onGotFocus       | [EventHandler](#event-handler-types)|
|onLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|
|onSelectionChanged | [EventHandler](#event-handler-types)|

--------------

## ListViewColumn class
### Constructor
```python
ListViewColumn(self, hdr_txt: str, width: int, img:int = -1, img_right: bool = False)
```
#### Properties
| Name      |Type| Description |
|-----------|------|-------|
|text | string | |
|width | int | |
|index | int | |
|imageIndex | int | |
|imageOnRight | bool | |
|textAlign |  [ColumnAlign](#columnalign-enum) | |
|hasImage | bool | |
|headerTextAlign | [TextAlignment](#textalignment-enum) | |
|backColor | [Color](#color-class)/int | |
|foreColor | [Color](#color-class)/int | |

--------------

## ListViewItem class
### Constructor
```python
ListViewItem(self, txt: str, bg_color: int = 0xFFFFFF, fg_color: int = 0x000000, imageIndex: int = -1)
```
#### Properties
| Name      |Type| Description |
|-----------|------|-------|
|text | string | |
|index | int | |
|imageIndex | int | |
|subItems | list[string] | |
| font | [Font](#font-class) | |
|backColor | [Color](#color-class)/int | |
|foreColor | [Color](#color-class)/int | |

----------------

## **MenuBar class**

### Constructor
```python
MenuBar(self, parent, xpos = 20, ypos = 20, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|If this is true, you don't need to call createHandle|

## **MouseEventArgs class**

### Constructor
```python
MouseEventArgs(self, msg: UINT, wp: WPARAM, lp: LPARAM)
```
#### Properties
| Name      |Type| Description |
|-----------|------|-------|
|x| int||
|y|int||
|delta|int||
|shiftPressed| bool ||
|ctrlPressed| bool||
|mouseButton | [MouseButtons](#mousebutton-enum)|

----



## **NumberPicker class**

### Constructor
```python
NumberPicker(self, parent, xpos: int = 10, ypos: int = 10, width: int = 80, height: int = 24, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```
## Functions
```python
createHandle(self) # Create window handle for this NumberPicker
```
## **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND     | Getter only.
|parent   |[Form](#form-class)     | Getter Only
|font     |[Font](#font-class)     |
|text     |string   |
|xpos     |int      |
|xpos     |int      |
|ypos     |int      |
|width    |int      |
|height   |int      |
|visibile |bool     |
|backColor|[Color](#color-class)/int|
|foreColor|[Color](#color-class)/int|

----

### **Events**
| Property Name      | Type        |
|--------------------|-------------|
|onMouseEnter     | [EventHandler](#event-handler-types)|
|onMouseDown      | [MouseEventHandler](#event-handler-types)|
|onMouseUp        | [MouseEventHandler](#event-handler-types)|
|onRightMouseDown | [MouseEventHandler](#event-handler-types)|
|onRightMouseUp   | [MouseEventHandler](#event-handler-types)|
|onRightClick     | [EventHandler](#event-handler-types)|
|onMouseLeave     | [EventHandler](#event-handler-types)|
|onDoubleClick    | [EventHandler](#event-handler-types)|
|onMouseWheel     | [MouseEventHandler](#event-handler-types)|
|onMouseMove      | [MouseEventHandler](#event-handler-types)|
|onMouseHover     | [EventHandler](#event-handler-types)|
|onKeyDown        | [KeyEventHandler](#event-handler-types)|
|onKeyUp          | [KeyEventHandler](#event-handler-types)|
|onKeyPress       | [KeyPressEventHandler](#event-handler-types)|
|onPaint          | [PaintEventHandler](#event-handler-types)|
|onGotFocus       | [EventHandler](#event-handler-types)|
|nLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|


## **ProgressBar class**

### Constructor
```python
ProgressBar(self, parent, xpos = 20, ypos = 20, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|


## **RadioButton class**

### Constructor
```python
RadioButton(self, parent, xpos = 20, ypos = 20, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|

## **SizeEventArgs class**
### Constructor
```python
SizeEventArgs(self, msg: UINT, wp: WPARAM, lp: LPARAM)
```
## **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|sizedOn   |[SizedPositions](#sizedpositions-enum)     | Getter only.
|formRect | RECT| Getter only|
|clientArea | [Area](#area-class)| Getter only

------------

## **TextBox class**

### Constructor
```python
TextBox(self, parent, xpos = 20, ypos = 20, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|


## **TrackBar class**

### Constructor
```python
TrackBar(self, parent, xpos = 20, ypos = 20, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|


## **TreeView class**

### Constructor
```python
TreeView(self, parent, xpos = 20, ypos = 20, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|





## Enums

## ChannelStyle Enum

## ColumnAlign Enum

## ControlType Enum

## DateFormat Enum

## FontWeight Enum

## FormPosition Enum

## FormState Enum

## FormStyle Enum

## Keys Enum

## LabelAlignment Enum

## LabelBorder Enum

## ListViewStyle Enum

## MouseButton Enum

## MouseButtonState Enum

## ProgressBarState Enum

## ProgressBarStyle Enum

## SizedPositions Enum

## TextAlignment Enum

## TextCase Enum

## TextType Enum

## TickPosition Enum

## TrackChange Enum

## ViewMode Enum


