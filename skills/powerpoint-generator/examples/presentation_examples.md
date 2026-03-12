# PowerPoint Generator Examples

## Example 1: Basic Title Slide

```python
from pptx import Presentation

prs = Presentation()
title_slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide_layout)

title = slide.shapes.title
subtitle = slide.placeholders[1]

title.text = "Welcome to My Presentation"
subtitle.text = "Created with python-pptx"

prs.save('basic_title.pptx')
```

## Example 2: Content Slides with Bullets

```python
from pptx import Presentation

prs = Presentation()

# Title slide
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Project Overview"
slide.placeholders[1].text = "2024 Annual Report"

# Content slide
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Key Achievements"

# Add bullet points
body = slide.placeholders[1]
tf = body.text_frame
tf.text = "Launched 3 new products"

p = tf.add_paragraph()
p.text = "Increased market share by 20%"
p.level = 0

p = tf.add_paragraph()
p.text = "Expanded to 5 new markets"
p.level = 0

prs.save('project_overview.pptx')
```

## Example 3: Image Gallery Slide

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

slide.shapes.title.text = "Product Gallery"

# Add images in a grid layout
images = ['product1.jpg', 'product2.jpg', 'product3.jpg']
positions = [(0.5, 1), (3.5, 1), (6.5, 1)]

for img_path, (left, top) in zip(images, positions):
    slide.shapes.add_picture(
        img_path,
        Inches(left),
        Inches(top),
        width=Inches(2.5)
    )

prs.save('gallery.pptx')
```

## Example 4: Data Table Slide

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[5])

# Create table
rows, cols = 4, 3
left, top = Inches(2), Inches(2)
width, height = Inches(6), Inches(2)

shape = slide.shapes.add_table(rows, cols, left, top, width, height)
table = shape.table

# Headers
headers = ['Product', 'Q1 Sales', 'Q2 Sales']
for i, header in enumerate(headers):
    table.cell(0, i).text = header

# Data
data = [
    ['Widget A', '$10,000', '$12,000'],
    ['Widget B', '$8,000', '$9,500'],
    ['Widget C', '$5,000', '$6,200']
]

for row_idx, row_data in enumerate(data):
    for col_idx, value in enumerate(row_data):
        table.cell(row_idx + 1, col_idx).text = value

prs.save('sales_table.pptx')
```

## Example 5: Chart Slide

```python
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[5])

# Chart data
chart_data = CategoryChartData()
chart_data.categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
chart_data.add_series('Revenue', (15, 18, 22, 20, 25, 28))

# Add chart
x, y, cx, cy = Inches(2), Inches(2), Inches(6), Inches(4)
slide.shapes.add_chart(
    XL_CHART_TYPE.LINE,
    x, y, cx, cy,
    chart_data
)

prs.save('line_chart.pptx')
```

## Example 6: Multi-Series Bar Chart

```python
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[5])

chart_data = CategoryChartData()
chart_data.categories = ['2021', '2022', '2023', '2024']
chart_data.add_series('Revenue', (100, 120, 145, 180))
chart_data.add_series('Expenses', (80, 90, 95, 110))
chart_data.add_series('Profit', (20, 30, 50, 70))

x, y, cx, cy = Inches(1), Inches(1.5), Inches(8), Inches(5)
slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    x, y, cx, cy,
    chart_data
)

prs.save('multi_series_chart.pptx')
```

## Example 7: Using the PresentationBuilder

```python
from presentation_builder import PresentationBuilder, PresentationConfig, SlideContent

# Define slides
slides = [
    SlideContent(
        title="Company Overview",
        subtitle="Annual Report 2024"
    ),
    SlideContent(
        title="Key Highlights",
        content=[
            "Revenue growth of 25%",
            "Expanded to 10 new markets",
            "Launched 5 innovative products",
            "Customer satisfaction at 95%"
        ]
    ),
    SlideContent(
        title="Financial Summary",
        table_data={
            'headers': ['Quarter', 'Revenue', 'Expenses', 'Profit'],
            'rows': [
                ['Q1', '$2.5M', '$1.8M', '$0.7M'],
                ['Q2', '$2.8M', '$1.9M', '$0.9M'],
                ['Q3', '$3.1M', '$2.0M', '$1.1M'],
                ['Q4', '$3.5M', '$2.1M', '$1.4M']
            ],
            'left': 1.5,
            'top': 2
        }
    ),
    SlideContent(
        title="Growth Trajectory",
        chart_data={
            'categories': ['Q1', 'Q2', 'Q3', 'Q4'],
            'series': {
                'Revenue': (2.5, 2.8, 3.1, 3.5),
                'Profit': (0.7, 0.9, 1.1, 1.4)
            },
            'type': 'column'
        }
    )
]

# Create presentation
config = PresentationConfig(
    title="Annual Report",
    slides=slides,
    author="Finance Team"
)

builder = PresentationBuilder(config)
builder.build()
builder.save("annual_report.pptx")
```