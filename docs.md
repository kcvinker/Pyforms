
# Documentation for Pyforms GUI library

## **Index**
[Button](#button-class)

[CalendarBox](#calendarbox-class)

[CheckBox](#checkbox-class)

[Color](#color-class)

[ComboBox](#combobox-class)

[DateTimePicker](#datetimepicker-class)



[Font](#font-class)

[GroupBox](#groupbox-class)

[Label](#label-class)

[ListBox](#listbox-class)

[ListView](#listview-class)

[MenuBar](#menubar-class)

[NumberPicker](#numberpicker-class)

[ProgressBar](#progressbar-class)

[RadioButton](#radiobutton-class)

[TextBox](#textbox-class)

[TrackBar](#trackbar-class)

[TreeView](#treeview-class)

---

## **Button class**

### Constructor
```python
Button(self, parent, txt: str = "", xpos = 20, ypos = 20, width = 120, height = 40, bCreate = False)
```
####        Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|

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

---


## **CalendarBox class**

### Constructor
```python
CalendarBox(self, parent, xpos = 20, ypos = 20, bCreate = False)
```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|If this is true, you don't need to call createHandle|

---

### Functions
| Function Name      | Description |
|--------------------|-------------|
|createHandle()      | Creates the handle of button.

---

### Properties
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

---

## CheckBox class

### Constructor
```python
CheckBox(self, parent, xpos = 20, ypos = 20, bCreate = False)
```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|

### Functions
| Function Name      | Description |
|--------------------|-------------|
|createHandle()      | Creates the handle of button.

----

### Properties
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
|onCheckedChanged | [EventHandler](#event-handler-types)|

---

# Color class
### Constructor
```python
Color(self, clr) # You can use int/Color
Color.fromColor(clr: int, change_value: int) # Create a new Color from given int value and change it with given change_value. Returns a Color type
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

### Properties
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
```ComboBox(self, parent, txt: str = "", xpos = 20, ypos = 20, width = 120, height = 40, bCreate = False)```
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
```DateTimePicker(self, parent, xpos = 20, ypos = 20, bCreate = False)```
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
        Form(self, )
#### Parameters
        parent: Form
        bCreate: bool - if this is true, you don't need to call createHandle


# Form class
### Constructor
        Form(self, )
#### Parameters
        parent: Form
        bCreate: bool - if this is true, you don't need to call createHandle

## **GroupBox class**

### Constructor
```GroupBox(self, parent, xpos = 20, ypos = 20, bCreate = False)```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|

## **Label class**

### Constructor
```Label(self, parent, xpos = 20, ypos = 20, bCreate = False)```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|

## **ListBox class**

### Constructor
```ListBox(self, parent, xpos = 20, ypos = 20, bCreate = False)```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|

## **ListView class**

### Constructor
```ListView(self, parent, xpos = 20, ypos = 20, bCreate = False)```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|


## **MenuBar class**

### Constructor
```MenuBar(self, parent, xpos = 20, ypos = 20, bCreate = False)```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|If this is true, you don't need to call createHandle|


## **NumberPicker class**

### Constructor
```NumberPicker(self, parent, xpos = 20, ypos = 20, bCreate = False)```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|

## **ProgressBar class**

### Constructor
```ProgressBar(self, parent, xpos = 20, ypos = 20, bCreate = False)```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|


## **RadioButton class**

### Constructor
```RadioButton(self, parent, xpos = 20, ypos = 20, bCreate = False)```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|


## **TextBox class**

### Constructor
```TextBox(self, parent, xpos = 20, ypos = 20, bCreate = False)```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|


## **TrackBar class**

### Constructor
```TrackBar(self, parent, xpos = 20, ypos = 20, bCreate = False)```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|


## **TreeView class**

### Constructor
```TreeView(self, parent, xpos = 20, ypos = 20, bCreate = False)```
#### Parameters
| Name      |Type| Description |
|-----------|------|-------|
|parent| [Form](#form-class)| Parent of this control|
|bCreate| bool|if this is true, you don't need to call createHandle|





## Enums

### ChannelStyle Enum


### ControlType Enum

### DateFormat Enum

### FontWeight Enum

### FormPosition Enum

### FormState Enum

### FormStyle Enum

### Keys Enum

### LabelAlignment Enum

### LabelBorder Enum

### ListViewStyle Enum

### MouseButton Enum

### MouseButtonState Enum

### ProgressBarState Enum

### ProgressBarStyle Enum

### SizedPositions Enum

### TextAlignment Enum

### TextCase Enum

### TextType Enum

### TickPosition Enum

### TrackChange Enum

### ViewMode Enum


