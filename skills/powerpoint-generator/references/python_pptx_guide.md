# python-pptx Reference Guide

## Installation

```bash
pip install python-pptx
```

## Core Classes

### Presentation

The main class for creating and manipulating presentations.

```python
from pptx import Presentation

# Create new presentation
prs = Presentation()

# Open existing presentation
prs = Presentation('existing.pptx')
```

### Slide Layouts

Available slide layouts (index-based):

| Index | Name | Description |
|-------|------|-------------|
| 0 | Title | Title with subtitle |
| 1 | Title and Content | Title with content placeholder |
| 2 | Section Header | Section divider |
| 3 | Two Content | Title with two content areas |
| 4 | Comparison | Title with comparison layout |
| 5 | Title Only | Title with blank area |
| 6 | Blank | No placeholders |

### Slide Object

```python
# Access slide
slide = prs.slides[0]

# Add slide
slide = prs.slides.add_slide(layout)

# Count slides
total = len(prs.slides)

# Iterate slides
for slide in prs.slides:
    print(slide.slide_id)
```

## Shapes

### Text Shapes

```python
# Title (available on most layouts)
title = slide.shapes.title
title.text = "My Title"

# Text frame
text_frame = shape.text_frame
text_frame.text = "Paragraph 1"

# Add paragraph
p = text_frame.add_paragraph()
p.text = "Paragraph 2"

# Set font
from pptx.util import Pt
run = text_frame.paragraphs[0].runs[0]
run.font.size = Pt(24)
run.font.bold = True
```

### Picture Shapes

```python
from pptx.util import Inches

# Add image
pic = slide.shapes.add_picture('image.jpg', left, top)

# With explicit width
pic = slide.shapes.add_picture('image.jpg', left, top, width=Inches(4))

# With explicit height
pic = slide.shapes.add_picture('image.jpg', left, top, height=Inches(3))

# Position and size
pic.left = Inches(1)
pic.top = Inches(2)
pic.width = Inches(4)
pic.height = Inches(3)
```

### Table Shapes

```python
# Create table
shape = slide.shapes.add_table(rows, cols, left, top, width, height)
table = shape.table

# Access cells
cell = table.cell(row, col)
cell.text = "Value"

# Set column width
from pptx.util import Inches
table.columns[0].width = Inches(2)

# Merge cells
table.cell(0, 0).merge(table.cell(0, 2))
```

### Chart Shapes

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

# Prepare data
chart_data = CategoryChartData()
chart_data.categories = ['A', 'B', 'C']
chart_data.add_series('Series 1', (10, 20, 30))

# Add chart
chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    left, top, width, height,
    chart_data
)
```

## Available Chart Types

| Type | Enum | Description |
|------|------|-------------|
| Column | `COLUMN_CLUSTERED` | Vertical bars |
| Bar | `BAR_CLUSTERED` | Horizontal bars |
| Line | `LINE` | Line chart |
| Pie | `PIE` | Pie chart |
| Area | `AREA` | Area chart |
| Scatter | `XY_SCATTER` | Scatter plot |
| Doughnut | `DOUGHNUT` | Doughnut chart |
| Radar | `RADAR` | Radar/spider chart |

## Units and Measurements

```python
from pptx.util import Inches, Pt, Emu

# Inches (most common)
width = Inches(4)

# Points (for font sizes)
font_size = Pt(14)

# EMUs (English Metric Units)
# 1 inch = 914400 EMUs
position = Emu(914400)  # 1 inch
```

## Text Formatting

```python
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Paragraph formatting
p = text_frame.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
p.level = 1  # Indent level

# Font formatting
run = p.runs[0]
run.font.size = Pt(18)
run.font.bold = True
run.font.italic = True
run.font.color.rgb = RGBColor(0x42, 0x24, 0xE9)
```

## Shape Types

```python
from pptx.enum.shapes import MSO_SHAPE

# Auto shapes
shape = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE,
    left, top, width, height
)

# Available shapes
MSO_SHAPE.RECTANGLE
MSO_SHAPE.ROUNDED_RECTANGLE
MSO_SHAPE.OVAL
MSO_SHAPE.DIAMOND
MSO_SHAPE.STAR_5_POINT
MSO_SHAPE.HEART
# ... and many more
```

## Best Practices

1. **Use Context Managers**: When working with files
   ```python
   # Not necessary for simple cases, but good practice
   prs = Presentation()
   prs.save('output.pptx')
   ```

2. **Position with Inches**: Use `Inches()` for intuitive positioning
   ```python
   # Good
   slide.shapes.add_picture('img.jpg', Inches(1), Inches(2))

   # Avoid raw EMUs
   slide.shapes.add_picture('img.jpg', 914400, 1828800)
   ```

3. **Check Placeholder Index**: Always verify placeholder exists
   ```python
   if len(slide.placeholders) > 1:
       slide.placeholders[1].text = "Subtitle"
   ```

4. **Clean Up**: Close presentations after use in scripts
   ```python
   # python-pptx handles this automatically
   # but explicit is good for long-running processes
   prs.save('output.pptx')
   ```

## Common Patterns

### Iterate All Shapes

```python
for shape in slide.shapes:
    if shape.has_text_frame:
        print(shape.text_frame.text)
```

### Find Shape by Name

```python
for shape in slide.shapes:
    if shape.name == "Title 1":
        shape.text_frame.text = "New Title"
```

### Copy Slide

```python
def copy_slide(prs, index):
    """Copy slide at index to new slide."""
    source = prs.slides[index]
    slide_layout = source.slide_layout
    new_slide = prs.slides.add_slide(slide_layout)
    # Copy shapes...
    return new_slide
```

## Error Handling

```python
from pptx.exc import PythonPptxError

try:
    prs = Presentation('missing.pptx')
except PythonPptxError as e:
    print(f"Error: {e}")
```