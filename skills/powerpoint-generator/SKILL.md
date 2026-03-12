---
name: PowerPoint Generator
description: This skill should be used when the user asks to "create a PowerPoint", "make a presentation", "generate slides", "create slides", "build a slideshow", "make a pptx", or mentions PowerPoint, slides, presentations, or python-pptx.
version: 1.0.0
---

# PowerPoint Generator

Generate professional PowerPoint presentations programmatically using python-pptx.

## Capabilities

- Create new presentations from scratch
- Add slides with various layouts (title, content, blank, etc.)
- Insert and format text (titles, body text, text boxes)
- Add images with precise positioning
- Create tables with customizable formatting
- Generate charts (bar, column, line, pie, etc.)
- Apply shapes and visual elements
- Save presentations as .pptx files

## Process

1. **Create Presentation**: Initialize a new `Presentation()` object
2. **Choose Layout**: Select from available slide layouts (0-5 typically)
3. **Add Slides**: Use `prs.slides.add_slide(layout)` to add new slides
4. **Add Content**: Insert text, images, tables, charts, or shapes
5. **Save File**: Export with `prs.save('filename.pptx')`

## Slide Layouts

| Index | Layout Type | Usage |
|-------|-------------|-------|
| 0 | Title Slide | Opening slide with title and subtitle |
| 1 | Title and Content | Title with bullet points or content |
| 2 | Section Header | Section divider |
| 5 | Title Only | Just a title, blank content area |
| 6 | Blank | Completely blank slide |

## Common Operations

### Create Basic Presentation
```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
title_slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "Presentation Title"
subtitle.text = "Subtitle here"
prs.save('presentation.pptx')
```

### Add Image to Slide
```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

# Add image with position and size
left = Inches(1)
top = Inches(1)
width = Inches(4)
pic = slide.shapes.add_picture('image.jpg', left, top, width=width)
prs.save('with_image.pptx')
```

### Add Table
```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[5])

# Create 3x3 table
x, y, cx, cy = Inches(2), Inches(2), Inches(4), Inches(1.5)
shape = slide.shapes.add_table(3, 3, x, y, cx, cy)
table = shape.table

# Populate cells
table.cell(0, 0).text = 'Header 1'
table.cell(0, 1).text = 'Header 2'
table.cell(1, 0).text = 'Data'
prs.save('with_table.pptx')
```

### Add Chart
```python
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[5])

# Define chart data
chart_data = CategoryChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('Revenue', (19.2, 21.4, 16.7, 25.0))

# Add chart to slide
x, y, cx, cy = Inches(2), Inches(2), Inches(6), Inches(4.5)
slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
)
prs.save('with_chart.pptx')
```

## Guidelines

- Use `Inches()` for positioning and sizing (most intuitive unit)
- Access existing shapes via `slide.shapes` collection
- Use `slide.placeholders[idx]` for layout placeholders
- Close files properly after manipulation
- Consider aspect ratio (16:9 or 4:3) when creating presentations

## Python Scripts

The `scripts/` directory contains:
- `presentation_builder.py` - Build presentations from structured data
- `slide_templates.py` - Pre-defined slide templates
- `chart_generator.py` - Generate various chart types
- `theme_utils.py` - Apply consistent themes and styling

## Usage Examples

See `examples/` directory for:
- Business presentation templates
- Data visualization examples
- Report generation samples

## References

See `references/` directory for:
- python-pptx documentation highlights
- Slide layout reference
- Shape and positioning guide