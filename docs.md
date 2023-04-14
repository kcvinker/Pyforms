
# Documentation for Pyforms GUI library

## **Index**
|Types |  |  |  |  |
|------|------|-------|-------|-------|
|[Area](#area-class)|[Button](#button-class)| [CalendarBox](#calendarbox-class)| [CheckBox](#checkbox-class)| [Color](#color-class)| [ComboBox](#combobox-class)|
|[DateTimePicker](#datetimepicker-class) |[EventArgs](#eventargs-class) |[Font](#font-class)|[GroupBox](#groupbox-class)| [KeyEventArgs](#keyeventargs-class)|  [KeyPressEventArgs](#keypresseventargs-class) |
|[Label](#label-class)|[ListBox](#listbox-class)| [ListView](#listview-class)|[ListViewColumn]()|[ListViewItem]()|
|[MenuBar](#menubar-class) | [MenuItem]() |[MouseEventArgs](#mouseeventargs-class) |[NumberPicker](#numberpicker-class) |[ProgressBar](#progressbar-class) |
|[RadioButton](#radiobutton-class) |[SizeEventArgs](#sizeeventargs-class) |[TextBox](#textbox-class) |[TrackBar](#trackbar-class) |[TreeNode]() |
|[TreeView](#treeview-class)|


---

## **Area class**
### Constructor
```python
Area(self, w, h)
```
### **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|width   |int     | |
|height | int ||

---------------

## **Button class**

### Constructor
```python
Button(self, parent, txt: str = "", xpos = 20, ypos = 20, width = 120, height = 40, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```

### Functions
```python
createHandle(self)  # Creates the handle of button.
```


### **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND[^1]     | Getter only.
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

([Go to index](#index))
---


## **CalendarBox class**

### Constructor
```python
CalendarBox(self, parent, xpos = 20, ypos = 20, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```

### Functions
```python
createHandle(self)  # Creates the handle of button.
```

### **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND[^1]     | Getter only.|
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

([Go to index](#index))
---

## CheckBox class

### Constructor
```python
CheckBox(self, parent, xpos = 20, ypos = 20, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```

### Functions
```python
createHandle(self)  # Creates the handle of button.
```

### **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND[^1]     | Getter only.|
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
|onCheckedChanged | [EventHandler](#event-handler-types)|

([Go to index](#index))
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
createHBrush(self, adj: float = 0) -> HBRUSH[^4] # Create an HBRUSH[^4] to use win api functions
createHPen(self, adj: float = 0) -> HPEN[^5] # Create HPEN[^5] to use in win api functions

changeToColorRef(self, adj: float) -> COLORREF[^2]
# Change the color with given value and returns COLORREF[^2]
# NOTE:  To make a  color lighter, use values greater than 1.0
#        To make color darker, use values lower than 1.0
```
----

### **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|value   |int     | Getter only.|
|ref| COLORREF[^2]| Getterr only|
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

### Functions
```python
createHandle(self)  # Creates the handle of button.
```

### Properties
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND[^1]     | Getter only.
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
|nLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|

([Go to index](#index))
-------------

## DateTimePicker class

### Constructor
```python
DateTimePicker(self, parent, xpos = 20, ypos = 20, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```
### Functions
```python
createHandle(self)  # Creates the handle of button.
```

### **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND[^1]     | Getter only.
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
|nLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|

([Go to index](#index))
--------------

## **EventArgs class**
#### Properties
| Name      |Type| Description |
|-----------|------|-------|
|handled    | bool   | |
-------------

## **Event handler types**
| Name      | Signature        |
|--------------------|-------------|
|EventHandler| func(Control, [EventArgs](#eventargs-class))|
|MouseEventHandler|func(Control, [MouseEventArgs](#mouseeventargs-class)) |
|KeyEventHandler| func(Control, [KeyEventArgs](#keyeventargs-class))|
|KeyPressEventHandler| func(Control, [KeyPressEventArgs](#keypresseventargs-class))|
|PaintEventHandler| func(Control, PaintEventArgs)|

([Go to index](#index))


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

([Go to index](#index))
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
|handle   |HWND[^1]     | Getter only.
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

([Go to index](#index))
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
|handle   |HWND[^1]     | Getter only.
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

([Go to index](#index))
--------------

## **KeyEventArgs class**
### Constructor
```python
KeyEventArgs(self, wp: WPARAM)
```
#### Properties
| Name      |Type| Description |
|-----------|------|-------|
|handled | bool ||
|keyCode | [Keys](#keys-enum)| |
|shiftPressed | bool| |
|modifier | [Keys](#keys-enum)| |
|ctrlPressed | bool||
|altPressed | bool||
|keyValue | int| |

([Go to index](#index))
---------------

## **KeyPressEventArgs class**
### Constructor
```python
KeyPressEventArgs(self, wp: WPARAM)
```
#### Properties
| Name      |Type| Description |
|-----------|------|-------|
|handled | bool ||
|keyChar | char| |

([Go to index](#index))
---------------



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
|handle   |HWND[^1]     | Getter only.
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

([Go to index](#index))
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
|handle   |HWND[^1]     | Getter only.
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

([Go to index](#index))
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
|handle   |HWND[^1]     | Getter only.
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

([Go to index](#index))
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

([Go to index](#index))

--------------

## **ListViewItem class**
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

([Go to index](#index))
----------------

## **MenuBar class**

### Constructor
```python
MenuBar(self, parent)
# parent : Form
```
### Functions
```python
addMenu(self, txt: str) -> MenuItem
create(self) # Creates menu handles
# txt - Menu text
```
### Properties
menus - list[[MenuItem](#menuitem-class)]

([Go to index](#index))
-----------

## **MenuItem class**
### Constructor
```python
MenuItem(self, txt: str, typ: MenuType, parent)
# txt - Menu text
# typ - MenuType
# parent : MenuItem/MenuBar
```
### Functions
```python
addMenu(self, txt: str) -> MenuItem
addPopupMenu(self, txt: str) -> MenuItem
addSeperator(self): -> MenuItem
# txt - Menu text
```
### Event
| Name      |Type| Description |
|-----------|------|-------|
|onClick | [EventHandler](#event-handler-types)| |

([Go to index](#index))
-----------


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
|handled    | bool   | |
|mouseButton | [MouseButtons](#mousebutton-enum)|

([Go to index](#index))
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
|handle   |HWND[^1]     | Getter only.
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
|decimalPlaces | int|  |
|minRange | int | |
|maxRange | int| |
|autoRotate | bool| |
|step | int/float| |
|value | int/float| |
|buttonOnLeft | bool| |
|hasSeperator | bool| |
|hideCaret | bool| |

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
|nLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|
|onValueChanged          | [EventHandler](#event-handler-types)|

([Go to index](#index))
-----------------

## **ProgressBar class**

### Constructor
```python
ProgressBar(self, parent, xpos: int = 10, ypos: int = 10, width: int = 180, height: int = 25, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```
## Functions
```python
createHandle(self) # Create window handle for this NumberPicker
increment(self)
startMarquee(self)
stopMarquee(self)
```
## **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND[^1]     | Getter only.
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
|value| int| |
|step | int | |
|state | [ProgressBarState](#progressbarstate-enum) | |
|style | [ProgressBarStyle](#progressbarstyle-enum) | |



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
|nLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|
|onValueChanged          | [EventHandler](#event-handler-types)|

([Go to index](#index))
-------------

## **RadioButton class**

### Constructor
```python
RadioButton(self, parent, txt: str, xpos: int = 10, ypos: int = 10, width: int = 120, height: int = 23, bCreate = False)
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
|handle   |HWND[^1]     | Getter only.
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
|checked | bool | |



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
|nLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|
|onCheckedChanged          | [EventHandler](#event-handler-types)|

([Go to index](#index))
-------------


## **SizeEventArgs class**
### Constructor
```python
SizeEventArgs(self, msg: UINT, wp: WPARAM, lp: LPARAM)
```
## **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handled | bool | |
|sizedOn   |[SizedPositions](#sizedpositions-enum)     | Getter only.
|formRect | RECT[^3]| Getter only|
|clientArea | [Area](#area-class)| Getter only

([Go to index](#index))
------------

## **TextBox class**

### Constructor
```python
TextBox(self, parent, xpos: int = 10, ypos: int = 10, width: int = 120, height: int = 23, bCreate = False)
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
|handle   |HWND[^1]     | Getter only.
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
|textAlign | [TextAlignment](#textalignment-enum)
|textCase | [TextCase](#textcase-enum)| |
|textType | [TextType](#texttype-enum)| |
|cueBanner | string| |
|multiLine | bool| |
|hideSelection | bool | |
|readOnly | bool | |



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
|nLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|
|onTextChanged    | [EventHandler](#event-handler-types)|

([Go to index](#index))
-------------



## **TrackBar class**

### Constructor
```python
TrackBar(self, parent, xpos: int = 10, ypos: int = 10, width: int = 150, height: int = 25, bCreate = False)
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```
## Functions
```python
createHandle(self) # Create window handle for this TrackBar
calsulateSize(self) # This will show you how many points needed to properly align all the tics.

setTicPos(self, pos:str)
"""A handy function to set the tic position. You can set it by passing a string.
So, you don't need to import the TickPosition Enum.
Accepted values are: {'both', 'up', 'down', 'left', 'right'}"""

```
## **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND[^1]     | Getter only.
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
|trackChange | [TrackChange](#trackchange-enum)| |
|ticLength | int| |
|vertical | bool | |
|largeChange | int| |
|smallChange | int| |
|showSelection | bool | |
|frequency | int| |
|minimum | int| |
|maximum | int| |
|ticPosition | [TickPosition](#tickposition-enum)| |
|tooltip | bool | |
|reverse | bool | |
|value | int| |
|selectionColor | [Color](#color-class) | |
|ticColor | [Color](#color-class)| |
|channelColor | [Color](#color-class)| |
|freeMove | bool | |
|ticWidth | int| |
|noTics | bool | |
|channelStyle | [ChannelStyle](#channelstyle-enum)| |
|customDraw | bool | |



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
|nLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|
|onValueChanged   | [EventHandler](#event-handler-types)|
|onDragging       | [EventHandler](#event-handler-types)|
|onDragged        | [EventHandler](#event-handler-types)|

([Go to index](#index))
--------------


## **TreeNode class**

### Constructor
```python
TreeNode(self, text: str)
```
## **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|imageIndex | int ||
|foreColor| [Color](#color-class)||
|backColor | [Color](#color-class)||
|text | string ||
|parentNode | [TreeNode](#treenode-class) | |
|nodes | list[[TreeNode](#treenode-class)] | |
|selImgIndex | int| |
|nodeCount | int| |
|checked | bool| |
|index | int| |
|nodeID | int| |
|treeHwnd | HWND[^1]| |

([Go to index](#index))

-----------

## **TreeView class**

### Constructor
```python
TreeView(self, parent, xpos: int = 10, ypos: int = 10, width: int = 80, height: int = 24, bCreate = False )
# parent : Form
# bCreate: bool - if this is true, you don't need to call createHandle
```

## Functions
```python
createHandle(self) # Create window handle for this TreeView
addNode(self, node)
addNodes(self, *nodes)
insertNode(self, node, pos: int) # pos = Index to insert
addChildNode(self, node, parent) # parent = Parent TreeNode
addChildNodes(self, parent, *nodes)
insertChildNode(self, node, parent, pos)
```
## **Properties**
| Property Name      | Type        | Description|
|--------------------|-------------|------------|
|handle   |HWND[^1]     | Getter only.
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
|nLostFocus       | [EventHandler](#event-handler-types)|
|onClick          | [EventHandler](#event-handler-types)|

([Go to index](#index))

--------------




## Enums ----------------

## ChannelStyle Enum
    Values - DEFAULT = 0, CLASSIC = 1, OUTLINE = 2

## ColumnAlign Enum
    Values - LEFT = 0, RIGHT = 1, CENTER = 2

## ControlType Enum
    Values - NONE = 0, BUTTON = 1, CALENDAR_BOX = 2, CHECK_BOX = 3, COMBO_BOX = 4, DATE_TIME_PICKER = 5, GROUP_BOX = 6, LABEL = 7, LIST_BOX = 8, LIST_VIEW = 9,NUM_PICKER = 10, PROGRESS_BAR = 11, RADIO_BUTTON = 12, TEXT_BOX = 13, TRACK_BAR = 14, TREE_VIEW = 15

## DateFormat Enum
    Vaues - LONG_DATE = 1, SHORT_DATE = 2, TIME_ONLY = 4, CUSTOM_DATE = 8

## FontWeight Enum
    Values - THIN = 100, EXTRA_LIGHT = 200, LIGHT = 300, NORMAL = 400, MEDIUM = 500, SEMI_BOLD = 600, BOLD = 700, EXTRA_BOLD = 800, THICK = 900

## FormPosition Enum

## FormState Enum
    Values - NORMAL = 0, MAXIMIZED = 1, MINIMIZED = 2

## FormStyle Enum
    Values - NONE = 0, FIXED_SINGLE = 1, FIXED_3D = 2, FIXED_DIALOG = 3, FIXED_TOOL = 4, SIZABLE = 5, SIZABLE_TOOL = 6, HIDDEN = 7

## Keys Enum
    Keys enum is too big to include this documentation. Please refer to [enums.py](https://github.com/kcvinker/Pyforms/blob/main/pyforms/enums.py#:~:text=class-,Keys,-(Enum)%3A) in source

## LabelAlignment Enum
    Values - TOPLEFT = 0, TOPCENTER = 1, TOPRIGHT = 2, MIDLEFT = 3, CENTER  = 4, MIDRIGHT = 5, BOTTOMLEFT = 6, BOTTOMCENTER = 7, BOTTOMRIGHT = 8

## LabelBorder Enum
    Values - NONE = 0, SINGLE = 1, SUNKEN = 2

## ListViewStyle Enum
    Values - LARGE_ICON = 0, REPORT_VIEW = 1, SMALL_ICON = 2, LIST_VIEW = 3, TILE_VIEW = 4

## MouseButton Enum
    Values - NONE = 0, RIGHT = 20_97_152, MIDDLE = 41_94_304, LEFT = 10_48_576, XBUTTON1 = 83_88_608, XBUTTON2 = 167_77_216

## MouseButtonState Enum
    Values - RELEASED, PRESSED

## ProgressBarState Enum
    Values - NORMAL = 1, ERROR = 2, PAUSED = 3

## ProgressBarStyle Enum
    Values - BLOCK_STYLE = 0, MARQUEE_STYLE = 1

## SizedPositions Enum
    Values - LEFT_EDGE = 1, RIGHT_EDGE = 2, TOP_EDGE = 3, TOP_LEFT_CORNER = 4, TOP_RIGHT_CORNER = 5, BOTTOM_EDGE = 6, BOTTOM_LEFT_CORNER = 7, BOTTOM_RIGHT_CORNER = 8

## TextAlignment Enum
    Values - LEFT = 0, CENTER = 1, RIGHT = 2

## TextCase Enum
    Values - NORMAL = 0, LOWER = 1, UPPER = 2

## TextType Enum
    Values - NORMAL = 0, NUM_ONLY = 1, PASSWORD = 2

## TickPosition Enum
    Values - DOWN = 1, UP = 2, LEFT = 3, RIGHT = 4, BOTH = 5

## TrackChange Enum
    Values - NONE = 0, ARROW_LOW = 1, ARROW_HIGH = 2, PAGE_LOW = 3, PAGE_HIGH = 4, MOUSE_CLICK = 5, MOUSE_DRAG = 6

## ViewMode Enum
    Values - MONTH_VIEW = 0, YEAR_VIEW = 1, DECADE_VIEW = 2, CENTUARY_VIEW = 3


[^1]: HWND - Windows api data type for a Window handle

[^2]: COLORREF - Windows api data type for a color. BGR is the format.

[^3]: RECT - Windows api struct.

*Declaration*
```python
class RECT[^3](Structure):
_fields_ = [
    ('left', LONG),
    ('top', LONG),
    ('right', LONG),
    ('bottom', LONG)
]
```
[^4]: HBRUSH - Windows api data type for a brush object.
[^5]: HPEN - Windows api data type for a pen object.
