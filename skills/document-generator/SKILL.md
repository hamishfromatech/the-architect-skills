---
name: Document Generator
description: This skill should be used when the user asks to "create a document", "generate a document", "write a proposal", "create a contract", "draft an agreement", "make a report", "generate a letter", "create a memo", or mentions document creation, business documents, or document templates.
version: 1.0.0
---

# Document Generator Skill

Generate professional business documents including proposals, contracts, reports, memos, and letters.

## Supported Document Types

| Document Type | Description | Key Sections |
|--------------|-------------|--------------|
| Proposal | Business proposals for clients/partners | Executive summary, scope, timeline, pricing |
| Contract | Legal agreements | Parties, terms, conditions, signatures |
| Report | Business reports | Summary, findings, recommendations |
| Memo | Internal communications | Purpose, details, action items |
| Letter | Formal correspondence | Salutation, body, sign-off |
| Agreement | Non-binding agreements | Terms, responsibilities, duration |
| Invoice | Billing documents | Line items, amounts, payment terms |

## Process

1. **Identify Document Type**: Determine the appropriate document format
2. **Gather Requirements**: Collect necessary information and data
3. **Apply Template**: Use appropriate template structure
4. **Populate Content**: Fill in document sections
5. **Review & Format**: Ensure consistency and professionalism

## Document Structure Principles

### Proposals
```
1. Title Page
2. Executive Summary
3. Problem Statement / Background
4. Proposed Solution
5. Scope of Work
6. Timeline
7. Pricing / Investment
8. Terms & Conditions
9. Appendix (if needed)
```

### Contracts
```
1. Parties Identification
2. Recitals / Background
3. Terms and Conditions
4. Obligations
5. Payment Terms
6. Duration and Termination
7. Signatures
```

### Business Letters
```
1. Letterhead / Sender Info
2. Date
3. Recipient Address
4. Salutation
5. Body Paragraphs
6. Closing
7. Signature
8. Enclosures (if any)
```

## Formatting Standards

- **Font**: Professional fonts (Arial, Calibri, Times New Roman)
- **Size**: 11-12pt for body, 14-16pt for headings
- **Margins**: 1 inch standard, 0.5 inch minimum
- **Spacing**: Single or 1.15 for readability
- **Headers**: Clear hierarchy with consistent numbering

## Python Scripts

The `scripts/` directory contains:
- `document_builder.py` - Build documents from templates
- `pdf_generator.py` - Convert documents to PDF format
- `template_engine.py` - Template parsing and population
- `format_validator.py` - Validate document formatting

## Usage Examples

See `examples/` directory for:
- Sample proposals
- Contract templates
- Report formats
- Business letters

## References

See `references/` directory for:
- Document formatting standards
- Legal document guidelines
- Industry-specific conventions