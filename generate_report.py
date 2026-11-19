from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

doc = Document()

style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)

for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

# ─── PAGE 1: TITLE PAGE ───

for _ in range(4):
    doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('Coffee Shop - AI Barista')
run.bold = True
run.font.size = Pt(28)
run.font.name = 'Times New Roman'
run.font.color.rgb = RGBColor(0x6F, 0x4E, 0x37)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run('Mini Project Synopsis')
run.font.size = Pt(18)
run.font.name = 'Times New Roman'
run.font.color.rgb = RGBColor(0x8B, 0x5E, 0x3C)

doc.add_paragraph()

dept = doc.add_paragraph()
dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = dept.add_run('Department of ____________________________')
run.font.size = Pt(14)
run.font.name = 'Times New Roman'

college = doc.add_paragraph()
college.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = college.add_run('____________________________')
run.font.size = Pt(14)
run.font.name = 'Times New Roman'

doc.add_paragraph()

team_heading = doc.add_paragraph()
team_heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = team_heading.add_run('Team Members')
run.bold = True
run.font.size = Pt(14)
run.font.name = 'Times New Roman'

table = doc.add_table(rows=5, cols=3)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.style = 'Table Grid'

headers = ['Sr. No.', 'Name', 'Roll No. / ID']
for i, header in enumerate(headers):
    cell = table.rows[0].cells[i]
    cell.text = header
    for paragraph in cell.paragraphs:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in paragraph.runs:
            run.bold = True
            run.font.size = Pt(12)
            run.font.name = 'Times New Roman'
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="D2B48C"/>')
    cell._tc.get_or_add_tcPr().append(shading)

for row_idx in range(1, 5):
    table.rows[row_idx].cells[0].text = str(row_idx)
    for col_idx in range(3):
        cell = table.rows[row_idx].cells[col_idx]
        for paragraph in cell.paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in paragraph.runs:
                run.font.size = Pt(12)
                run.font.name = 'Times New Roman'

table.columns[0].width = Inches(1.0)
table.columns[1].width = Inches(3.0)
table.columns[2].width = Inches(2.0)

doc.add_paragraph()

year = doc.add_paragraph()
year.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = year.add_run('Academic Year: 20__ - 20__')
run.font.size = Pt(13)
run.font.name = 'Times New Roman'

# ─── PAGE 2: INTRODUCTION & FEATURES ───

doc.add_page_break()

h1 = doc.add_heading('1. Introduction', level=1)
for run in h1.runs:
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0x6F, 0x4E, 0x37)

intro_text = (
    'Coffee Shop - AI Barista is a web-based application that uses GPT-3.5-turbo (via OpenRouter API) '
    'to simulate an AI barista. Users can chat in natural language to get drink/pastry recommendations, '
    'manage a shopping cart, and place orders. Built with Python and Streamlit.'
)
p = doc.add_paragraph(intro_text)
p.paragraph_format.space_after = Pt(6)
for run in p.runs:
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)

h2 = doc.add_heading('1.1 Problem Statement', level=2)
for run in h2.runs:
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0x6F, 0x4E, 0x37)

problem_text = (
    'Traditional ordering systems lack personalized interaction. Customers with dietary restrictions '
    'struggle to find suitable items. This project provides an AI conversational interface that '
    'understands preferences and dietary needs to recommend menu items intelligently.'
)
p = doc.add_paragraph(problem_text)
p.paragraph_format.space_after = Pt(6)
for run in p.runs:
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)

h2 = doc.add_heading('1.2 Features', level=2)
for run in h2.runs:
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0x6F, 0x4E, 0x37)

features = [
    ('AI-Powered Barista', 'Chat interface using GPT-3.5-turbo with conversation history tracking.'),
    ('Smart Menu Search', 'Scored search engine ranking items by name, tag, category, and description.'),
    ('Shopping Cart', 'Add, remove, adjust quantities, and checkout via sidebar or chat commands.'),
    ('Order History', 'Orders tracked with timestamps and unique IDs in session state.'),
    ('Allergen & Dietary Filtering', 'Items tagged with dietary labels and allergen info for safe recommendations.'),
    ('Hallucination Detection', 'Validates AI responses to prevent recommending off-menu items.'),
    ('Streamlit Web UI', 'Coffee-themed interface with sidebar menu, cart panel, and chat window.'),
]

for title, desc in features:
    p = doc.add_paragraph(style='List Bullet')
    run = p.add_run(f'{title}: ')
    run.bold = True
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run = p.add_run(desc)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)

# ─── PAGE 3: IMPLEMENTATION & ARCHITECTURE ───

doc.add_page_break()

h1 = doc.add_heading('2. Implementation', level=1)
for run in h1.runs:
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0x6F, 0x4E, 0x37)

h2 = doc.add_heading('2.1 Technology Stack', level=2)
for run in h2.runs:
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0x6F, 0x4E, 0x37)

tech_stack = [
    ('Language', 'Python 3.8+'),
    ('Web Framework', 'Streamlit (>=1.30.0)'),
    ('AI/LLM', 'OpenAI GPT-3.5-turbo via OpenRouter API'),
    ('AI SDK', 'OpenAI Python SDK (>=1.0.0)'),
    ('Configuration', 'python-dotenv (>=1.0.0)'),
    ('Data Storage', 'JSON files (menu.json, orders.json)'),
]

tech_table = doc.add_table(rows=len(tech_stack) + 1, cols=2)
tech_table.style = 'Table Grid'
tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER

tech_headers = ['Component', 'Technology']
for i, header in enumerate(tech_headers):
    cell = tech_table.rows[0].cells[i]
    cell.text = header
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.bold = True
            run.font.size = Pt(11)
            run.font.name = 'Times New Roman'
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="D2B48C"/>')
    cell._tc.get_or_add_tcPr().append(shading)

for idx, (component, tech) in enumerate(tech_stack):
    tech_table.rows[idx + 1].cells[0].text = component
    tech_table.rows[idx + 1].cells[1].text = tech
    for col in range(2):
        for paragraph in tech_table.rows[idx + 1].cells[col].paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(11)
                run.font.name = 'Times New Roman'

doc.add_paragraph()

h2 = doc.add_heading('2.2 Module Description', level=2)
for run in h2.runs:
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0x6F, 0x4E, 0x37)

modules = [
    ('app.py', 'Main Streamlit app. Renders UI, handles chat, parses cart action tags from AI responses.'),
    ('agent.py', 'BaristaAgent class. Manages OpenAI API calls, system prompt, conversation context, and response validation.'),
    ('menu_search.py', 'Menu loading, scored search, preference filtering (hot/cold, sweet/strong, dietary), and recommendations.'),
    ('cart_manager.py', 'Cart operations: add, remove, update quantity, clear, calculate totals, save orders.'),
    ('config.py', 'Environment variable loading and API key validation.'),
    ('data/menu.json', '8 menu items across 3 categories (coffee, bakery, specialty) with tags and allergens.'),
]

for title, desc in modules:
    p = doc.add_paragraph()
    run = p.add_run(f'{title}: ')
    run.bold = True
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    run = p.add_run(desc)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    p.paragraph_format.space_after = Pt(4)

h2 = doc.add_heading('2.3 System Architecture', level=2)
for run in h2.runs:
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0x6F, 0x4E, 0x37)

arch_text = (
    'The application follows a modular architecture with clear separation of concerns:\n\n'
    'User (Browser) \u2192 Streamlit Web UI (app.py) \u2192 BaristaAgent (agent.py) \u2192 OpenRouter API \u2192 GPT-3.5-turbo\n'
    '                              \u2193                              \u2193\n'
    '                    Menu Search (menu_search.py)    Response Validation\n'
    '                              \u2193                              \u2193\n'
    '                    Cart Manager (cart_manager.py)   Action Tag Parsing\n'
    '                              \u2193\n'
    '                    Data Layer (JSON files)'
)
p = doc.add_paragraph(arch_text)
for run in p.runs:
    run.font.name = 'Consolas'
    run.font.size = Pt(9)

# ─── PAGE 4: WORKING & CONCLUSION ───

doc.add_page_break()

h1 = doc.add_heading('3. Working', level=1)
for run in h1.runs:
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0x6F, 0x4E, 0x37)

working_text = 'The application operates through the following workflow:'
p = doc.add_paragraph(working_text)
for run in p.runs:
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)

steps = [
    'User runs "streamlit run app.py" to start the local web server on port 8501.',
    'App loads menu from data/menu.json and initializes BaristaAgent with the API key.',
    'User types natural language queries (e.g., "show me cold drinks", "I\'m lactose intolerant").',
    'BaristaAgent sends the system prompt, last 10 messages, and user query to GPT-3.5-turbo via OpenRouter.',
    'Response is validated for hallucinations and corrected if off-menu items are referenced.',
    'Cart action tags ([CART_ADD:id], [CHECKOUT]) are parsed from the response and executed. Tags are stripped before display.',
    'Users can also browse the sidebar menu, add items directly, and checkout via the cart panel.',
    'On checkout, the order is saved with a unique ID and timestamp. Cart is cleared.',
]

for i, step in enumerate(steps, 1):
    p = doc.add_paragraph(style='List Number')
    run = p.add_run(step)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)

h1 = doc.add_heading('4. Future Enhancements', level=1)
for run in h1.runs:
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0x6F, 0x4E, 0x37)

enhancements = [
    'Order status tracking (Preparing \u2192 Ready \u2192 Picked Up)',
    'Customer accounts and loyalty points system',
    'Sales analytics dashboard',
    'Multiple language support',
    'PDF order receipt generation',
    'Voice input support for hands-free ordering',
]

for item in enhancements:
    p = doc.add_paragraph(style='List Bullet')
    run = p.add_run(item)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)

h1 = doc.add_heading('5. Conclusion', level=1)
for run in h1.runs:
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0x6F, 0x4E, 0x37)

conclusion_text = (
    'This project demonstrates practical LLM integration in a food-ordering scenario. It combines '
    'GPT-3.5-turbo with a structured menu, allergen filtering, and hallucination detection to deliver '
    'a safe, personalized experience. The modular architecture ensures easy maintainability and extensibility.'
)
p = doc.add_paragraph(conclusion_text)
for run in p.runs:
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)

output_path = r'C:\Projects\coffee-shop-ai-barista\Coffee_Shop_AI_Barista_Synopsis.docx'
doc.save(output_path)
print(f'Document saved to: {output_path}')
