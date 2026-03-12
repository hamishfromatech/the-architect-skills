# PowerPoint Generator

Create professional PowerPoint presentations programmatically using python-pptx.

## Overview

The PowerPoint Generator skill creates .pptx presentations from scratch, including slides, text, images, tables, and charts.

## Quick Start

### Trigger Phrases

Use these phrases to activate the skill:
- "create a PowerPoint"
- "make a presentation"
- "generate slides"
- "create slides"
- "build a slideshow"
- "make a pptx"

## Capabilities

- Create new presentations from scratch
- Add slides with various layouts (title, content, blank)
- Insert and format text (titles, body text, text boxes)
- Add images with precise positioning
- Create tables with customizable formatting
- Generate charts (bar, column, line, pie)
- Export to .pptx format

## Slide Layouts

| Index | Layout Type | Usage |
|-------|-------------|-------|
| 0 | Title Slide | Opening slide with title and subtitle |
| 1 | Title and Content | Title with bullet points or content |
| 2 | Section Header | Section divider |
| 5 | Title Only | Just a title, blank content area |
| 6 | Blank | Completely blank slide |

## Quick Example

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()

# Title slide
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "My Presentation"
slide.placeholders[1].text = "Subtitle here"

# Content slide
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Overview"
body = slide.placeholders[1].text_frame
body.text = "First point"
body.add_paragraph().text = "Second point"

prs.save('presentation.pptx')
```

## Examples

See [examples/presentation_examples.md](examples/presentation_examples.md) for complete examples including:
- Basic presentations
- Image galleries
- Data tables
- Charts
- Using the PresentationBuilder class

## Python Scripts

- `presentation_builder.py` - Build presentations from structured data

## References

See [references/python_pptx_guide.md](references/python_pptx_guide.md) for the complete API reference.

## Dependencies

```bash
pip install python-pptx
```

## License

MIT License - Part of The Architect Skills project.