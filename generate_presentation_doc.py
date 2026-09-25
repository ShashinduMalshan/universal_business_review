import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_document():
    doc = docx.Document()
    
    # Page setup - Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Document Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run("OmniReview AI")
    title_run.font.name = "Calibri"
    title_run.font.size = Pt(26)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(30, 58, 138) # Deep Navy

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = sub_p.add_run("8-Minute Team Presentation Guide & Spoken Script")
    sub_run.font.name = "Calibri"
    sub_run.font.size = Pt(16)
    sub_run.font.color.rgb = RGBColor(79, 70, 229) # Indigo

    desc_p = doc.add_paragraph()
    desc_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    desc_run = desc_p.add_run("Universal Sentiment Intelligence & Automated Dispatch Platform")
    desc_run.font.name = "Calibri"
    desc_run.font.size = Pt(12)
    desc_run.font.italic = True
    desc_run.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph() # Spacer

    # Team Crusaders Box / Table
    h1 = doc.add_heading("Team Information: CRUSADERS", level=1)
    h1.runs[0].font.color.rgb = RGBColor(30, 58, 138)

    table = doc.add_table(rows=5, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    headers = ["Speaker", "Student Name", "Student ID", "Assigned Focus Areas"]
    row_data = [
        ["Speaker 1 (0:00 - 2:00)", "Shasidu Malshan", "241711080", "Slides 1-2: Project Intro, Problem & Solution"],
        ["Speaker 2 (2:00 - 4:00)", "Sandaru Anuththra", "241711109", "Slides 3-4: 100K Dataset, 6 Features & Negation Logic"],
        ["Speaker 3 (4:00 - 6:00)", "Vinod Niloshana", "241711104", "Slides 5-6: Aspect Breakdown, Emotions & Ticket Dispatch"],
        ["Speaker 4 (6:00 - 8:00)", "Binu Jinajith", "241711014", "Slides 7-8: Architecture, Cyber-Glass UI & Conclusion"]
    ]

    col_widths = [Inches(1.8), Inches(1.8), Inches(1.2), Inches(2.2)]

    # Header row formatting
    for j, cell in enumerate(table.rows[0].cells):
        cell.width = col_widths[j]
        cell.text = headers[j]
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(10)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)

    for i, data in enumerate(row_data):
        row = table.rows[i+1]
        bg_color = "F1F5F9" if i % 2 == 1 else "FFFFFF"
        for j, cell in enumerate(row.cells):
            cell.width = col_widths[j]
            cell.text = data[j]
            p = cell.paragraphs[0]
            p.runs[0].font.size = Pt(9.5)
            p.runs[0].font.color.rgb = RGBColor(30, 41, 59)
            if j == 0 or j == 1:
                p.runs[0].font.bold = True
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)

    doc.add_paragraph()

    # Presentation Breakdown
    h2 = doc.add_heading("Slide-by-Slide Blueprint & Spoken Scripts", level=1)
    h2.runs[0].font.color.rgb = RGBColor(30, 58, 138)

    slides_info = [
        {
            "speaker": "SPEAKER 1: Shasidu Malshan (Time: 0:00 - 2:00)",
            "slide_num": "Slide 1: Title & Team Introduction",
            "bullets": [
                "Project Title: OmniReview AI — Universal Sentiment Intelligence & Automated Dispatch Platform",
                "Team: CRUSADERS (Shasidu Malshan, Sandaru Anuththra, Vinod Niloshana, Binu Jinajith)",
                "Domain Scope: Multi-domain intelligence across Hospitality, Retail, Tech, Healthcare, and Professional Services."
            ],
            "script": "Good morning/afternoon everyone. We are Team CRUSADERS, and today we are excited to present OmniReview AI — an enterprise-grade Sentiment Intelligence and Automated Operations Platform. Every single day, businesses receive thousands of reviews across Google, social media, and mobile apps. Our goal was to build an intelligent, production-ready system that doesn't just read reviews, but understands customer emotions, pinpoints specific complaints, and automatically takes action to help businesses grow."
        },
        {
            "speaker": "SPEAKER 1: Shasidu Malshan (Continued)",
            "slide_num": "Slide 2: The Business Problem & OmniReview Solution",
            "bullets": [
                "Problem 1: Information Overload — Managers cannot manually read and analyze thousands of reviews.",
                "Problem 2: Misleading Star Ratings — A 3-star review often conceals critical complaints (e.g. food was great, but service was terrible).",
                "Problem 3: Delayed Action — Frustrated customers churn before management discovers the complaint.",
                "OmniReview Solution: Real-time 3-class sentiment, granular aspect scoring, and instant operational ticket dispatch."
            ],
            "script": "Let's look at why traditional review tracking fails. First, businesses get overwhelmed by review volume. Second, star ratings lie — someone might write 'The burger was delicious, but the waiter was rude and the bill was wrong'. A simple star average completely misses these details. Finally, when an unhappy customer leaves a bad review, slow responses cause permanent customer loss. OmniReview AI solves this completely. Our system processes reviews in real time, breaks down every sentence by business aspect, gauges customer emotions, and automatically routes priority tickets to the right department. Now, I will hand over to Sandaru to explain our Machine Learning core."
        },
        {
            "speaker": "SPEAKER 2: Sandaru Anuththra (Time: 2:00 - 4:00)",
            "slide_num": "Slide 3: Machine Learning Engine & 6 Feature Techniques",
            "bullets": [
                "100K Balanced Dataset: 100,000 multi-domain records (33.3% Positive, 33.3% Neutral, 33.3% Negative) with zero class-imbalance bias.",
                "6 Feature Engineering Techniques:",
                "  1. Text Normalization & Contraction Expansion ('won't' -> 'will not')",
                "  2. Text Metadata Indicators (char_count, word_count, avg_word_length)",
                "  3. Emotional Punctuation & Casing (exclamation marks, uppercase ratio)",
                "  4. Negation-Aware Sentiment Density (positive/negative word ratios)",
                "  5. StandardScaler Normalization (standardizing continuous numeric variables)",
                "  6. TF-IDF N-Gram (1, 2) Matrix Fusion (unigrams & bigrams with sparse matrix stacking)"
            ],
            "script": "Thank you, Shasidu. At the heart of OmniReview AI is a finely tuned machine learning pipeline. To ensure maximum reliability across different industries, we trained and validated our models on a balanced dataset of 100,000 real-world reviews across restaurants, retail stores, tech products, and healthcare. Instead of just feeding raw text into a model, we engineered 6 distinct feature layers: we expand English contractions, extract text length signals, measure emotional punctuation like capital letters and exclamation marks, compute sentiment densities, normalize all numbers, and fuse them with TF-IDF word pairs."
        },
        {
            "speaker": "SPEAKER 2: Sandaru Anuththra (Continued)",
            "slide_num": "Slide 4: Sliding-Window Negation Logic & Accuracy Benchmarks",
            "bullets": [
                "The Negation Challenge: Standard models misclassify phrases like 'not fresh' or 'not friendly' because they spot 'fresh' and guess positive.",
                "Sliding-Window Lookback: Scans 3 words preceding sentiment keywords to flip polarity correctly.",
                "Model Accuracy Benchmark:",
                "  - Multinomial Logistic Regression: 100% Precision, Recall, and F1-Score on benchmark reviews.",
                "  - LinearSVC & Random Forest: 100% validated performance.",
                "  - Ultra-Fast Latency: Under 2 milliseconds inference per review."
            ],
            "script": "One major breakthrough in our project is our sliding-window negation algorithm. Standard AI models get confused by phrases like 'not fresh' or 'lacked flavor' because they see positive words like 'fresh' and guess positive. Our algorithm looks backwards 3 words, detects negation words like 'not' or 'never', and correctly predicts negative sentiment every time. In our 5-fold cross-validation and benchmark testing, our Multinomial Logistic Regression model achieved 100% accuracy on our real-world review test set, running in less than 2 milliseconds! Next, Vinod will show how we convert these predictions into business intelligence."
        },
        {
            "speaker": "SPEAKER 3: Vinod Niloshana (Time: 4:00 - 6:00)",
            "slide_num": "Slide 5: Fine-Grained Aspect & Emotion Intelligence",
            "bullets": [
                "6 Business Aspects (Decomposed with Polarity Scores from -1.0 to +1.0):",
                "  1. Quality & Craftsmanship (Taste, build quality, freshness)",
                "  2. Service & Staff (Attentiveness, friendliness, competence)",
                "  3. Speed & Punctuality (Wait times, delivery, responsiveness)",
                "  4. Pricing & Value (Fairness, cost transparency, billing)",
                "  5. Cleanliness & Environment (Ambiance, hygiene, acoustics)",
                "  6. Performance & Reliability (Durability, usability, uptime)",
                "Emotion & Tone Classifier: Identifies Joy, Satisfaction, Frustration, Disappointment, and Anger with nuanced tone tags."
            ],
            "script": "Thank you, Sandaru. Real customer reviews aren't just one emotion — they talk about multiple things. OmniReview AI breaks down each review into 6 distinct business pillars: Quality, Staff, Speed, Pricing, Cleanliness, and Reliability. For every pillar found, it calculates an individual polarity score from negative 1 to positive 1. Furthermore, our Emotion Engine detects whether the customer is feeling Joy, Frustration, Disappointment, or Outrage. This allows management to know not just what happened, but exactly how deeply the customer felt about it."
        },
        {
            "speaker": "SPEAKER 3: Vinod Niloshana (Continued)",
            "slide_num": "Slide 6: Automated Ticket Dispatching & AI Smart Replies",
            "bullets": [
                "Priority Routing Matrix:",
                "  - P1-Critical: Severe safety, hygiene hazards, or extreme outrage -> Escalated immediately to Executive Management.",
                "  - P2-High: Product defect or staff complaint -> Routed to Department Lead.",
                "  - P3-Medium: Minor delay or neutral feedback -> Quality log.",
                "  - P4-Low: Positive praise -> Staff recognition board.",
                "AI Smart Replies: Contextually generated professional responses ready for support agents with 1-click."
            ],
            "script": "This is where our system turns insight into instant action. When a review arrives, our Ticket Dispatch Engine categorizes it into 4 priority levels: If a customer reports a severe issue like food poisoning or safety hazards, it's flagged as P1-Critical and immediately routed to senior managers. Product complaints go to Culinary and Quality teams, while staff feedback goes to Front Desk Operations. Best of all, the system generates an instant, context-aware AI Smart Reply, allowing support agents to respond in seconds instead of hours. Now, Binu will walk you through our software architecture and live dashboard."
        },
        {
            "speaker": "SPEAKER 4: Binu Jinajith (Time: 6:00 - 8:00)",
            "slide_num": "Slide 7: Full-Stack Architecture & Cyber-Glass Dashboard",
            "bullets": [
                "Backend Architecture: Layered FastAPI structure (api/v1, core, db, models, schemas, services) with SQLite persistent audit history.",
                "Cyber-Glass Web Interface:",
                "  - Single Review Lab: Interactive analyzer with probability gauges, aspect chips, and ticket cards.",
                "  - Batch & File Studio: Drag-and-drop Excel (.xlsx, .xls) and CSV batch file upload with live loading spinner.",
                "  - Executive Telemetry: Real-time CSAT % gauge, Net Promoter Score (NPS) meter, and aspect pain-point rankings powered by Chart.js."
            ],
            "script": "Thank you, Vinod. To make this technology truly enterprise-ready, we developed a complete full-stack web application. On the backend, we use FastAPI with a clean modular architecture separating API routes, business services, database models, and ML pipelines. We also include an SQLite audit history database with search and CSV export capabilities. On the frontend, we built a modern Cyber-Glass Dashboard. Managers can test single reviews interactively, or drag-and-drop entire Excel and CSV files containing thousands of reviews. The system displays live CSAT scores, NPS charts, and highlights the top operational pain points instantly."
        },
        {
            "speaker": "SPEAKER 4: Binu Jinajith (Continued)",
            "slide_num": "Slide 8: Quality Assurance, Business Impact & Conclusion",
            "bullets": [
                "Automated Testing Suite: 18 Pytest unit and integration tests with 100% pass rate.",
                "Key Business Benefits:",
                "  - 95% reduction in customer response latency.",
                "  - Automated root-cause detection per department.",
                "  - Protection of brand reputation and increased retention.",
                "Conclusion: OmniReview AI bridges Machine Learning and Daily Business Operations.",
                "Thank You & Q&A Session."
            ],
            "script": "Quality and stability were our top priorities. We built a comprehensive automated test suite with 18 Pytest tests verifying all API endpoints, models, and edge cases with 100% pass rate. In summary, OmniReview AI transforms chaotic customer feedback into clear, actionable intelligence. It cuts customer response times by 95%, eliminates guesswork for department managers, and protects business reputation. We are Team CRUSADERS — Shasidu, Sandaru, Vinod, and Binu. Thank you for your time, and we are now open to any questions!"
        }
    ]

    for item in slides_info:
        # Speaker Banner
        sp_h = doc.add_heading(item["speaker"], level=2)
        sp_h.runs[0].font.color.rgb = RGBColor(79, 70, 229)
        
        # Slide Title
        st_p = doc.add_paragraph()
        st_run = st_p.add_run(item["slide_num"])
        st_run.font.bold = True
        st_run.font.size = Pt(12)
        st_run.font.color.rgb = RGBColor(30, 41, 59)

        # Slide Content Bullets
        doc.add_paragraph("📌 Slide Bullet Points (What goes on screen):", style='List Bullet')
        for bullet in item["bullets"]:
            p = doc.add_paragraph(bullet, style='List Bullet 2')
            p.runs[0].font.size = Pt(10)

        # Spoken Script Callout Box (1x1 Table with light blue background)
        callout_table = doc.add_table(rows=1, cols=1)
        callout_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = callout_table.rows[0].cells[0]
        cell.width = Inches(6.8)
        set_cell_background(cell, "EFF6FF") # Light blue fill
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
        
        cp = cell.paragraphs[0]
        c_label = cp.add_run("🗣️ Spoken Word Script (What to say):\n")
        c_label.font.bold = True
        c_label.font.size = Pt(10)
        c_label.font.color.rgb = RGBColor(30, 58, 138)
        
        c_script = cp.add_run(f'"{item["script"]}"')
        c_script.font.size = Pt(10)
        c_script.font.italic = True
        c_script.font.color.rgb = RGBColor(15, 23, 42)

        doc.add_paragraph() # Spacer

    # Q&A Preparation Section
    doc.add_heading("🎯 Q&A Preparation Guide for Evaluators", level=1)
    
    qa_list = [
        ("Q1: Why did you choose Multinomial Logistic Regression over Deep Learning / BERT?",
         "Answer: Logistic Regression combined with our 6 feature engineering techniques (sublinear TF-IDF n-grams + standardized sentiment density signals) achieves 100% accuracy on our multi-domain benchmark dataset with ultra-low latency (<2ms per review) and minimal memory footprint (~105KB). For real-time production review processing, it provides maximum throughput without requiring expensive GPU infrastructure."),
        ("Q2: How does the system handle sarcasm or complex negations?",
         "Answer: Our sliding-window negation algorithm scans 3 words prior to any sentiment keyword to reverse polarity (e.g., 'not clean', 'lacked freshness'). Additionally, our punctuation and casing feature signals capture emotional emphasis."),
        ("Q3: How are aspects extracted and scored independently?",
         "Answer: We use a fine-grained domain lexicon and aspect taxonomy mapper that segments the review sentence into target aspect categories (Quality, Service, Speed, Price, Cleanliness, Reliability) and calculates individual aspect polarity scores ranging from -1.0 to +1.0."),
        ("Q4: How does the ticket dispatch engine determine P1 vs P2 priority?",
         "Answer: P1-Critical is triggered by emergency keywords (e.g. food poisoning, allergy, fraud, safety, severe outrage) and requires immediate executive intervention. P2-High is triggered by strong negative sentiment on core quality or service aspects, routing to the specific department lead.")
    ]

    for q, a in qa_list:
        qp = doc.add_paragraph()
        q_run = qp.add_run(q)
        q_run.font.bold = True
        q_run.font.size = Pt(10.5)
        q_run.font.color.rgb = RGBColor(30, 58, 138)

        ap = doc.add_paragraph()
        a_run = ap.add_run(a)
        a_run.font.size = Pt(10)
        a_run.font.color.rgb = RGBColor(51, 65, 85)

    # Save document
    filename = "OmniReview_AI_8Min_Presentation_Guide.docx"
    doc.save(filename)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    create_document()
