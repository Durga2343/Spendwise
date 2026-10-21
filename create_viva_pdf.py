import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Palette constants aligned with SpendWise Fintech Theme
C_FOREST = colors.HexColor("#123C32")
C_EMERALD = colors.HexColor("#10A878")
C_SAGE = colors.HexColor("#5A8C7A")
C_LIGHT_BG = colors.HexColor("#F7F9F8")
C_WARM_CREAM = colors.HexColor("#F7F5EF")
C_CARD_BG = colors.HexColor("#FFFFFF")
C_TEXT_MAIN = colors.HexColor("#183B35")
C_TEXT_MUTED = colors.HexColor("#556B65")
C_BORDER = colors.HexColor("#D8D2C5")
C_ACCENT_ROSE = colors.HexColor("#C85A6B")
C_ACCENT_ROSE_BG = colors.HexColor("#FDF2F3")
C_CALLOUT_BG = colors.HexColor("#EBF5F1")

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print total page numbers:
    'Page X of Y' along with header and footer rules.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress running header/footer on title cover page
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(C_SAGE)
        
        # Running Top Header
        self.drawString(54, 755, "SPENDWISE  |  MACHINE LEARNING EXPENSE ANALYZER")
        self.drawRightString(558, 755, "PROJECT VIVA & TECHNICAL REPORT")
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.6)
        self.line(54, 747, 558, 747)

        # Running Bottom Footer
        self.line(54, 45, 558, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(C_TEXT_MUTED)
        self.drawString(54, 32, "Confidential  *  Academic Project Defense & Viva Preparation Guide")
        self.drawRightString(558, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_pdf(filename="SpendWise_Complete_Viva_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=C_FOREST,
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=C_EMERALD,
        spaceAfter=25
    )
    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=C_TEXT_MUTED
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=22,
        textColor=C_FOREST,
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=17,
        textColor=C_SAGE,
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=C_TEXT_MAIN,
        spaceAfter=7
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    q_style = ParagraphStyle(
        'Question_Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=C_FOREST,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )
    ans_style = ParagraphStyle(
        'Answer_Style',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.3,
        leading=13.5,
        textColor=C_TEXT_MAIN,
        spaceAfter=7
    )
    callout_style = ParagraphStyle(
        'Callout_Style',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=C_FOREST
    )

    story = []

    # ─────────────────────────────────────────────────────────────
    # COVER / TITLE BANNER
    # ─────────────────────────────────────────────────────────────
    story.append(Spacer(1, 15))
    story.append(Paragraph("SPENDWISE", ParagraphStyle('Tag', fontName='Helvetica-Bold', fontSize=10, textColor=C_EMERALD, spaceAfter=8)))
    story.append(Paragraph("Smart Expense Analyzer & Machine Learning Anomaly Detection System", title_style))
    story.append(Paragraph("Comprehensive Technical Documentation, System Architecture, Algorithm Training Guide & Viva Voce Q&A Master Reference", subtitle_style))

    story.append(HRFlowable(width="100%", thickness=2, color=C_EMERALD, spaceAfter=18))

    meta_table_data = [
        [Paragraph("<b>Domain:</b> FinTech & Applied Machine Learning", meta_style), Paragraph("<b>Tech Stack:</b> Python, Streamlit, Scikit-Learn, Plotly", meta_style)],
        [Paragraph("<b>Primary ML Model:</b> Isolation Forest (Unsupervised)", meta_style), Paragraph("<b>Target Application:</b> Personal Finance Intelligence", meta_style)],
        [Paragraph("<b>Core Modules:</b> Ingestion, Analytics, Anomaly ML, Auth", meta_style), Paragraph("<b>Storage:</b> Local Flat-File CSV & JSON (Zero-Cloud Privacy)", meta_style)]
    ]
    t_meta = Table(meta_table_data, colWidths=[250, 250])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 20))

    # Executive Overview Box
    exec_summary_text = (
        "<b>Executive Project Summary:</b> SpendWise is an end-to-end, privacy-preserving financial management system "
        "designed to track personal expenditures, discover monthly patterns, and autonomously detect anomalous spending "
        "without requiring cloud-based APIs or third-party banking integrations. It implements a Scikit-Learn Isolation Forest "
        "ensemble model that isolates mathematical outliers in spending behavior, providing proactive warnings for budget overruns "
        "and unusual transactions."
    )
    t_exec = Table([[Paragraph(exec_summary_text, callout_style)]], colWidths=[504])
    t_exec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CALLOUT_BG),
        ('BOX', (0,0), (-1,-1), 1.2, C_EMERALD),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_exec)
    story.append(Spacer(1, 25))

    # Table of Contents
    story.append(Paragraph("DOCUMENT TABLE OF CONTENTS", h2_style))
    toc_data = [
        [Paragraph("<b>Section 1:</b> Project Overview & Problem Statement", body_style), Paragraph("<b>Section 4:</b> Isolation Forest ML: Training & Math", body_style)],
        [Paragraph("<b>Section 2:</b> System Architecture & Flow", body_style), Paragraph("<b>Section 5:</b> UI Performance & Optimization Fixes", body_style)],
        [Paragraph("<b>Section 3:</b> Data Pipeline & Schema", body_style), Paragraph("<b>Section 6:</b> Master Viva Voce Q&A (30 Questions)", body_style)]
    ]
    t_toc = Table(toc_data, colWidths=[250, 250])
    t_toc.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,-1), colors.white)
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 1: PROJECT OVERVIEW & MOTIVATION
    # ─────────────────────────────────────────────────────────────
    story.append(Paragraph("1. Project Overview & Motivation", h1_style))
    story.append(Paragraph(
        "Modern consumers face significant hurdles maintaining financial discipline. Conventional expense tracking tools "
        "suffer from severe operational limitations: (1) manual spreadsheets demand tedious manual formulas and lack intelligence; "
        "(2) mobile applications frequently require invasive bank SMS permissions or transmit sensitive financial data to cloud servers; "
        "(3) static budgets rely on rigid, hardcoded thresholds (e.g. 'flag if spend > 5,000') that fail to adapt to varied lifestyles.",
        body_style
    ))
    story.append(Paragraph("<b>Core Objectives of SpendWise:</b>", body_style))
    story.append(Paragraph("&bull; <b>Autonomous Anomaly Discovery:</b> Utilize machine learning to identify statistically improbable transactions rather than static rules.", bullet_style))
    story.append(Paragraph("&bull; <b>100% Privacy Guarantee:</b> Local file storage ensures financial data never leaves the user's host environment.", bullet_style))
    story.append(Paragraph("&bull; <b>Interactive Visual Synthesis:</b> Dynamic Plotly dashboards enable instant category breakdowns, trends, and daily rhythms.", bullet_style))
    story.append(Paragraph("&bull; <b>Low Friction Data Ingestion:</b> Supports flexible CSV imports with automated column aliasing, data type coercion, and manual entry forms.", bullet_style))

    # ─────────────────────────────────────────────────────────────
    # SECTION 2: SYSTEM ARCHITECTURE & MODULE DESIGN
    # ─────────────────────────────────────────────────────────────
    story.append(Paragraph("2. System Architecture & Module Design", h1_style))
    story.append(Paragraph(
        "SpendWise utilizes a layered modular architecture comprising a Presentation Layer, Business & Analytic Layer, "
        "Machine Learning Pipeline Layer, and Data Persistence Layer.",
        body_style
    ))

    arch_table_data = [
        [Paragraph("<b>Layer</b>", body_style), Paragraph("<b>Components & Libraries</b>", body_style), Paragraph("<b>Key Responsibilities</b>", body_style)],
        [Paragraph("<b>Presentation Layer</b>", body_style), Paragraph("Streamlit Multi-Page, BaseWeb UI, Custom CSS", body_style), Paragraph("Renders reactive UI, handles session states, form submission, and tab routing.", body_style)],
        [Paragraph("<b>Analytics Layer</b>", body_style), Paragraph("Plotly Graph Objects, Pandas GroupBy", body_style), Paragraph("Calculates metrics (daily burn, top categories) and builds interactive charts.", body_style)],
        [Paragraph("<b>Machine Learning Layer</b>", body_style), Paragraph("Scikit-Learn IsolationForest, NumPy", body_style), Paragraph("Performs Log1p transformations, fits 100 iTrees, predicts outlier flags.", body_style)],
        [Paragraph("<b>Data Layer</b>", body_style), Paragraph("CSV (`sample_expenses`, `user_expenses`), JSON", body_style), Paragraph("Stores raw transactions and user credentials locally on disk.", body_style)]
    ]
    t_arch = Table(arch_table_data, colWidths=[100, 150, 254])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_FOREST),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG])
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Application Pages & Workflow:</b>", body_style))
    story.append(Paragraph("&bull; <b>`app.py` (Dashboard Overview):</b> Aggregates high-level KPIs (Total Spend, Average Daily Spend, Top Category %, Anomalies Flagged), displays Donut chart, spline trend, and recent transaction feeds.", bullet_style))
    story.append(Paragraph("&bull; <b>`pages/1_Transactions.py`:</b> Interactive ledger with search filters, category multiselect, date range sliders, and manual transaction entry.", bullet_style))
    story.append(Paragraph("&bull; <b>`pages/2_Analytics.py`:</b> In-depth charts for daily expense distributions, category averages, and rule-based Pareto budget insights.", bullet_style))
    story.append(Paragraph("&bull; <b>`pages/3_ML_Insights.py`:</b> Displays ordinary vs. unusual histogram overlays, anomaly score cards, and Isolation Forest explanations.", bullet_style))
    story.append(Paragraph("&bull; <b>`pages/4_CSV_Upload.py`:</b> Secure drag-and-drop ingestion with header validation, automatic schema renaming, and sample template generator.", bullet_style))
    story.append(Paragraph("&bull; <b>`pages/5_Settings.py`:</b> Session termination, sample data reset, permanent data purge, and technical viva documentation download.", bullet_style))

    # ─────────────────────────────────────────────────────────────
    # SECTION 3: DATA PIPELINE & PREPROCESSING
    # ─────────────────────────────────────────────────────────────
    story.append(Paragraph("3. Data Pipeline & Schema Specification", h1_style))
    story.append(Paragraph(
        "The system operates on tabular expense records. To ensure compatibility with various bank export formats, "
        "the data ingestion engine implements flexible normalization.",
        body_style
    ))

    schema_data = [
        [Paragraph("<b>Field Name</b>", body_style), Paragraph("<b>Target Type</b>", body_style), Paragraph("<b>Accepted Aliases</b>", body_style), Paragraph("<b>Validation & Constraint</b>", body_style)],
        [Paragraph("`date`", body_style), Paragraph("datetime64[ns]", body_style), Paragraph("`transaction_date`, `date`", body_style), Paragraph("Parsed via pd.to_datetime; NaT dropped.", body_style)],
        [Paragraph("`description`", body_style), Paragraph("object / string", body_style), Paragraph("`merchant`, `description`", body_style), Paragraph("Non-empty text string identifying payee.", body_style)],
        [Paragraph("`category`", body_style), Paragraph("category / string", body_style), Paragraph("`type`, `category`", body_style), Paragraph("Categorical label (Food, Transport, Rent, etc.).", body_style)],
        [Paragraph("`amount`", body_style), Paragraph("float64", body_style), Paragraph("`transaction_amount`, `amount`", body_style), Paragraph("Numeric value. Inward cash is negative; outward is positive.", body_style)]
    ]
    t_schema = Table(schema_data, colWidths=[80, 80, 150, 194])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_SAGE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG])
    ]))
    story.append(t_schema)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Ingestion Cleaning Protocol:</b>", body_style))
    story.append(Paragraph("1. Column headers are normalized using `.str.lower().str.strip()`.", bullet_style))
    story.append(Paragraph("2. Header aliases are renamed into standard canonical forms via dictionary mapping.", bullet_style))
    story.append(Paragraph("3. Missing dates or amounts are coerced to NaT/NaN and pruned via `dropna()`.", bullet_style))
    story.append(Paragraph("4. Clean data is serialized to `data/user_expenses.csv`, triggering cache invalidation.", bullet_style))

    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 4: MACHINE LEARNING DEEP DIVE (TRAINING & MATH)
    # ─────────────────────────────────────────────────────────────
    story.append(Paragraph("4. Machine Learning Deep Dive: Isolation Forest Algorithm", h1_style))
    story.append(Paragraph(
        "The core intelligence of SpendWise is powered by the <b>Isolation Forest</b> (iForest) algorithm, "
        "developed by Fei Tony Liu, Kai Ming Ting, and Zhi-Hua Zhou (2008). Unlike traditional outlier detection algorithms "
        "that construct profiles of normal points, Isolation Forest explicitly isolates anomalies.",
        body_style
    ))

    story.append(Paragraph("Why Unsupervised Learning?", h2_style))
    story.append(Paragraph(
        "Personal expense records lack labeled 'ground truth' indicating fraud or budgetary infractions. "
        "Supervised classifiers (Random Forest, Logistic Regression, XGBoost) are unusable because there is no target label column `y`. "
        "Isolation Forest requires no prior labels, discovering statistical deviations organically from the unlabeled dataset.",
        body_style
    ))

    story.append(Paragraph("Why Isolation Forest over Alternative Outlier Algorithms?", h2_style))
    comp_data = [
        [Paragraph("<b>Algorithm</b>", body_style), Paragraph("<b>Computational Complexity</b>", body_style), Paragraph("<b>Operational Mechanism</b>", body_style), Paragraph("<b>Verdict for Personal Finance</b>", body_style)],
        [Paragraph("<b>Isolation Forest</b>", body_style), Paragraph("<b>O(t &middot; &psi; &middot; log &psi;) &approx; O(n)</b>", body_style), Paragraph("Partitions space randomly; anomalies isolate in fewer tree splits.", body_style), Paragraph("<b>Optimal:</b> Linear complexity, fast, no distance calculations.", body_style)],
        [Paragraph("<b>One-Class SVM</b>", body_style), Paragraph("O(n&sup2;) to O(n&sup3;)", body_style), Paragraph("Fits a max-margin hyperplane enclosing normal points in kernel space.", body_style), Paragraph("Poor scalability; quadratic memory consumption.", body_style)],
        [Paragraph("<b>DBSCAN</b>", body_style), Paragraph("O(n&sup2;)", body_style), Paragraph("Density clustering; marks unclustered points as noise.", body_style), Paragraph("Fails when expense distributions have variable densities.", body_style)],
        [Paragraph("<b>K-Means Distance</b>", body_style), Paragraph("O(n &middot; k &middot; i)", body_style), Paragraph("Measures Euclidean distance to cluster centroids.", body_style), Paragraph("Assumes spherical clusters; requires guessing cluster count k.", body_style)],
        [Paragraph("<b>LOF (Local Outlier)</b>", body_style), Paragraph("O(n&sup2;)", body_style), Paragraph("Compares local density of a point to its k-nearest neighbors.", body_style), Paragraph("Distance calculations slow down drastically as data grows.", body_style)]
    ]
    t_comp = Table(comp_data, colWidths=[80, 100, 174, 150])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_FOREST),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG])
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Mathematical Theory & Scoring Formulae", h2_style))
    story.append(Paragraph(
        "<b>1. Tree Construction (iTree):</b> Given a dataset sample X, an isolation tree recursively splits the data. "
        "At each node, an attribute q is selected randomly, and a split value p is chosen uniformly between [min(q), max(q)]. "
        "Splitting continues until either: (a) tree depth reaches h_max = ceil(log2(&psi;)), (b) |X| &le; 1, or (c) all samples have equal values.<br/>"
        "<b>2. Path Length h(x):</b> The path length h(x) is the number of edges traversed from the root node to the terminating leaf node.<br/>"
        "<b>3. Average Path Length Baseline c(n):</b> Because iTrees have an equivalent structure to Binary Search Trees (BST), "
        "the average path length of an unsuccessful search in a BST over n samples serves as the mathematical normalizer:",
        body_style
    ))

    eq_box_text = (
        "<b>Formula 1: Normalizing Constant c(n)</b><br/>"
        "c(n) = 2 * (ln(n - 1) + 0.5772156649) - (2 * (n - 1) / n)<br/>"
        "<i>where 0.5772156649 is the Euler-Mascheroni constant (&gamma;).</i><br/><br/>"
        "<b>Formula 2: Anomaly Score s(x, n)</b><br/>"
        "s(x, n) = 2 ^ (- ( E(h(x)) / c(n) ) )<br/>"
        "<i>where E(h(x)) is the mean path length across all 100 trees in the ensemble.</i>"
    )
    t_eq = Table([[Paragraph(eq_box_text, body_style)]], colWidths=[504])
    t_eq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, C_EMERALD),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_eq)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Score Interpretation:</b>", body_style))
    story.append(Paragraph("&bull; <b>When s &rarr; 1 (E(h(x)) &rarr; 0):</b> The observation is isolated in very few splits. It is a definite anomaly.", bullet_style))
    story.append(Paragraph("&bull; <b>When s &lt; 0.5 (E(h(x)) &rarr; c(n)):</b> The observation requires typical search depth. It is marked as normal.", bullet_style))
    story.append(Paragraph("&bull; <b>When all s &approx; 0.5:</b> The entire dataset exhibits uniform density without distinct outliers.", bullet_style))

    story.append(Paragraph("Feature Engineering: Why Log1p Transformation is Mandatory", h2_style))
    story.append(Paragraph(
        "Financial expenditures follow a heavy-tailed, power-law distribution (Pareto distribution). "
        "A typical user might have ninety expenses between Rs 100 - Rs 1,500, and one house rent transaction of Rs 25,000. "
        "If raw amounts are used directly, the split range [min, max] is dominated by the single extreme value [100, 25000]. "
        "Random splits will overwhelmingly fall in the large empty interval [1500, 25000], causing ordinary mid-range anomalies "
        "(e.g. an unexpected Rs 6,500 gadget purchase) to be lumped together with normal expenses.<br/>"
        "To resolve this, we apply the natural log transformation: <b>X = ln(1 + amount)</b> via `np.log1p()`. "
        "This compresses the monetary scale, stabilizes variance, and ensures uniform partition density across order-of-magnitude changes.",
        body_style
    ))

    story.append(Paragraph("Hyperparameters in SpendWise:", h2_style))
    story.append(Paragraph("&bull; <b>`contamination = 0.05`:</b> Pre-specifies that approximately 5% of expenditure records are expected to be unusual. This tunes the decision threshold.", bullet_style))
    story.append(Paragraph("&bull; <b>`n_estimators = 100`:</b> Creates 100 distinct random iTrees, ensuring low variance in average path length E(h(x)).", bullet_style))
    story.append(Paragraph("&bull; <b>`random_state = 42`:</b> Ensures reproducible trees and deterministic output.", bullet_style))
    story.append(Paragraph("&bull; <b>`n_jobs = -1`:</b> Distributes tree construction across all available CPU cores for high execution throughput.", bullet_style))
    story.append(Paragraph("&bull; <b>Minimum Data Threshold (N &ge; 20):</b> With fewer than 20 points, tree partitioning lacks statistical power. The app automatically disables ML until at least 20 records exist.", bullet_style))

    story.append(PageBreak())

    # ─────────────────────────────────────────────────────────────
    # SECTION 5: PERFORMANCE OPTIMIZATIONS & UI FIXES
    # ─────────────────────────────────────────────────────────────
    story.append(Paragraph("5. Performance Profiling & UI Optimization Fixes", h1_style))
    story.append(Paragraph(
        "During testing, two major system bugs were diagnosed and resolved: an input field invisibility glitch and slow page transition times. "
        "Understanding these engineering fixes is frequently examined during technical viva evaluations.",
        body_style
    ))

    story.append(Paragraph("Bug 1: The 'Dark-on-Dark' Input Visibility Defect", h2_style))
    story.append(Paragraph(
        "<b>Root Cause:</b> In `.streamlit/config.toml`, `secondaryBackgroundColor` was improperly set to `#123C32` (dark forest green). "
        "Streamlit's internal BaseWeb design system applies this secondary color to the container wrappers of `st.date_input` and `st.number_input`. "
        "Because `base = 'light'`, text was set to `#183B35` (dark green). Consequently, dark green text rendered inside a dark green container, "
        "rendering Date and Amount completely invisible.<br/>"
        "<b>Engineering Fix:</b> Neutralized `secondaryBackgroundColor` in `config.toml` to `#EFECE6` (light warm cream). "
        "In `assets/styles.css`, implemented robust explicit CSS selectors targeting `div[data-baseweb='input']`, `input`, calendar dialogs, "
        "and stepper control buttons (`+` and `-`) with solid white backgrounds and high-contrast dark forest typography.",
        body_style
    ))

    story.append(Paragraph("Bug 2: High Latency & Slow Execution Times", h2_style))
    story.append(Paragraph(
        "<b>Root Cause:</b> Streamlit executes Python scripts sequentially from top-to-bottom on every user click or widget interaction. "
        "Without caching: (1) `load_data()` read CSVs from disk and parsed string timestamps on every frame; (2) `detect_anomalies()` "
        "re-trained all 100 Isolation Forest trees on every UI rerun; (3) `assets/styles.css` was repeatedly read from disk.<br/>"
        "<b>Engineering Fix:</b> Decorated `load_data()`, `detect_anomalies()`, and `get_css()` with `@st.cache_data`. "
        "Subsequent page reruns return cached computations in under 1 millisecond. Implemented explicit cache clearing via "
        "`clear_data_cache()` and `detect_anomalies.clear()` whenever a transaction is added, uploaded, or deleted.",
        body_style
    ))

    story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceBefore=12, spaceAfter=14))

    # ─────────────────────────────────────────────────────────────
    # SECTION 6: MASTER VIVA VOCE QUESTIONS & ANSWERS (30 Q&A)
    # ─────────────────────────────────────────────────────────────
    story.append(Paragraph("6. Master Viva Voce Q&A Reference (30 Questions)", h1_style))
    story.append(Paragraph(
        "This section compiles the exact conceptual, technical, and mathematical questions frequently asked by project examiners.",
        body_style
    ))

    viva_qa = [
        # Part A
        ("Q1: What is SpendWise and what real-world problem does it solve?",
         "SpendWise is a privacy-first, machine learning-powered personal expense analyzer. It solves the problem of passive expense tracking by autonomously flagging unusual or anomalous transactions using an Isolation Forest model, while guaranteeing 100% data privacy by keeping all storage and processing strictly local on the user's computer without cloud servers."),

        ("Q2: What is the technology stack used in this project?",
         "The project is built entirely in Python. The front-end user interface is developed with Streamlit and styled with Vanilla CSS tokens. Data manipulation is handled by Pandas and NumPy. Visualizations are rendered via Plotly Graph Objects. Machine learning anomaly detection is powered by Scikit-Learn's Isolation Forest."),

        ("Q3: Why did you choose Streamlit instead of React or Django?",
         "Streamlit allows rapid prototyping of reactive, data-centric web applications entirely in Python. It seamlessly bridges Python data structures (Pandas DataFrames, NumPy arrays, Plotly figures) with web components, eliminating the need for separate REST API middleware, JSON serialization layers, and JavaScript state sync."),

        ("Q4: How does the application guarantee user privacy?",
         "All transactions and credentials are stored strictly in local flat files (CSV and JSON) on the host machine's disk. There are no outbound network calls, no cloud databases (like Firebase or AWS), and no external API integrations. Data remains entirely within the user's control."),

        ("Q5: What are the main functional modules of the system?",
         "The system comprises five core modules: (1) Overview Dashboard (KPIs, Donut chart, Trend line), (2) Transaction History (filtering and manual entry), (3) Deep-Dive Analytics (Pareto rules, category burn), (4) Machine Learning Insights (anomaly distributions), (5) CSV Upload Engine, and (6) User Authentication."),

        # Part B
        ("Q6: How does the application ingest and validate uploaded CSV files?",
         "When a CSV is uploaded, Pandas reads the buffer. The columns are stripped and lowercased. A dictionary maps common bank aliases (e.g. 'merchant' -> 'description', 'transaction_amount' -> 'amount'). The app verifies that the four required columns exist, converts types with `pd.to_datetime` and `pd.to_numeric`, drops invalid NaNs, and saves the clean file to disk."),

        ("Q7: How are income and expense records distinguished in the dataset?",
         "Outward expenditures are stored as positive float values (e.g., +Rs 1,500 for groceries). Inward income or refunds are represented as negative values (e.g., -Rs 50,000 for salary). This standard financial convention allows easy filtering via `df['amount'] > 0` for expense analytics."),

        ("Q8: What feature engineering was applied before feeding data to the ML model?",
         "Two essential transformations: First, we filter out all income records (`amount <= 0`) so inward earnings do not skew spending outlier detection. Second, we apply a Log1p transformation: X = ln(1 + amount) using `np.log1p()`. This normalizes the extreme positive skewness characteristic of monetary expenditures."),

        ("Q9: What happens if an uploaded CSV file contains invalid or corrupted rows?",
         "The pipeline uses safe type conversion: `pd.to_datetime(..., errors='coerce')` and `pd.to_numeric(..., errors='coerce')`. Any unparseable string is turned into `NaT` or `NaN`. Then `df.dropna(subset=['date', 'amount'])` removes those damaged rows without crashing the application."),

        ("Q10: How does the app handle cold-start when a new user has no transaction history?",
         "If no user dataset is detected, SpendWise automatically falls back to a generated synthetic dataset (`sample_expenses.csv`) containing 100 representative transactions with pre-seeded anomalies. If a user uploads an empty dataset with fewer than 20 rows, the ML model gracefully disables itself to prevent invalid predictions."),

        # Part C: Machine Learning
        ("Q11: Why is anomaly detection in SpendWise formulated as an unsupervised problem?",
         "Personal expense histories do not come with pre-existing labels indicating whether a transaction was 'normal' or 'unusual'. Because ground-truth target labels y do not exist, supervised learning cannot be used. Unsupervised learning identifies anomalies strictly based on intrinsic data properties and distribution geometry."),

        ("Q12: How does the Isolation Forest algorithm work fundamentally?",
         "Isolation Forest isolates anomalies instead of modeling normal data. It constructs an ensemble of random binary trees (iTrees). In each tree, features and split values are chosen randomly. Because anomalies are 'few and different', they are isolated near the root of the tree with very short path lengths, whereas normal points require many splits to isolate."),

        ("Q13: What is the mathematical definition of path length h(x)?",
         "Path length h(x) is the number of edges an observation x traverses from the root node of an isolation tree to a terminating leaf node. Shorter path lengths correspond to higher anomaly probabilities."),

        ("Q14: What is c(n) and why is it needed in the anomaly score formula?",
         "c(n) is the average path length of an unsuccessful search in a Binary Search Tree (BST) built over n observations. It acts as an objective mathematical normalizer so that path lengths across trees and sample sizes can be transformed into a standardized scale between 0 and 1."),

        ("Q15: State the formula for the Isolation Forest anomaly score s(x, n).",
         "s(x, n) = 2^(-(E(h(x)) / c(n))), where E(h(x)) is the expected (mean) path length of instance x across all isolation trees in the forest, and c(n) is the average path length normalizer."),

        ("Q16: How do you interpret an anomaly score s?",
         "If s is close to 1 (path length much shorter than average), the instance is an anomaly. If s is significantly less than 0.5, the instance is normal. If all instances have s approx 0.5, the dataset does not have distinctly discernible anomalies."),

        ("Q17: What does the hyperparameter 'contamination' mean?",
         "Contamination specifies the expected proportion of outliers in the dataset. In SpendWise, it is set to 0.05 (5%). The algorithm uses this parameter to calculate the threshold anomaly score: any transaction with a score in the top 5% is labeled as an anomaly (-1)."),

        ("Q18: What is n_estimators and what value is used in your project?",
         "n_estimators is the number of isolation trees grown in the ensemble. We set `n_estimators = 100`. Research by Liu et al. demonstrates that 100 trees is the optimal convergence point where path length variance stabilizes with minimal computational overhead."),

        ("Q19: Why is an unusual expense NOT necessarily fraudulent?",
         "An anomaly in Isolation Forest simply means mathematical deviation from historical spend patterns. A legitimate rare event—such as paying annual college tuition, booking flight tickets, or buying a new laptop—is mathematically unusual but completely valid. We clearly label flagged transactions as 'Unusual' rather than 'Fraudulent'."),

        ("Q20: What is the computational time complexity of training an Isolation Forest?",
         "The training time complexity of Isolation Forest is linear: O(t * psi * log(psi)), where t is the number of trees (100) and psi is the subsampling size. This makes it substantially faster than O(n^2) or O(n^3) distance-based algorithms like DBSCAN or One-Class SVM."),

        ("Q21: Why not use K-Means clustering for anomaly detection here?",
         "K-Means requires specifying the number of clusters k in advance, assumes spherical clusters of equal variance, and is severely distorted by outliers because centroids are pulled toward extreme values. Isolation Forest requires no cluster assumption and is explicitly built for outlier isolation."),

        ("Q22: Why did you set random_state=42?",
         "Isolation Forest relies on random feature selection and random split choices. Setting a fixed seed (`random_state=42`) ensures determinism and reproducibility, meaning the model produces the exact same anomaly scores on the same dataset across different runs."),

        # Part D: Architecture & Web
        ("Q23: How does Streamlit handle state across multiple page navigations?",
         "Streamlit provides the `st.session_state` dictionary, which persists across page switches and user interactions within the same browser tab session. We store user authentication status (`logged_in: True/False`) and username in `st.session_state` so the login barrier is enforced across all sub-pages."),

        ("Q24: What was the cause of the slow page loading and how did you resolve it?",
         "The slowness was caused by re-reading CSV files from disk and re-training the 100-tree Isolation Forest model on every single user click. We resolved this by wrapping `load_data()` and `detect_anomalies()` in `@st.cache_data`. This caches the output in memory, reducing rerun time from over 1 second to under 1 millisecond."),

        ("Q25: What is cache invalidation and how is it handled in SpendWise?",
         "Cache invalidation ensures that stale in-memory cached data is refreshed when underlying records change. In SpendWise, whenever a user adds a manual transaction, uploads a new CSV, or deletes data, we explicitly execute `clear_data_cache()` and `detect_anomalies.clear()`, forcing the app to re-fetch and re-fit on the updated dataset."),

        ("Q26: What was the Date and Amount input visibility bug and how was it fixed?",
         "Streamlit's `.streamlit/config.toml` had `secondaryBackgroundColor` set to dark green `#123C32`. Streamlit applied this color to the containers of `st.date_input` and `st.number_input`, while text color was also dark green `#183B35`. The dark-on-dark contrast made inputs invisible. We fixed it by changing `secondaryBackgroundColor` to light `#EFECE6` and enforcing CSS white backgrounds with dark text on all `data-baseweb='input'` containers."),

        ("Q27: How is Indian Rupee (INR) formatting implemented?",
         "Standard western currency formatting places commas every 3 digits (1,000,000). The Indian numbering system uses the Lakh and Crore system (10,00,000). In `utils/formatting.py`, the `format_inr()` function slices the string: taking the last 3 digits, and then grouping remaining digits in pairs of 2, prepending the 'Rs' symbol."),

        ("Q28: How do Plotly charts communicate with the Streamlit frontend?",
         "Plotly creates JSON-serialized declarative figure dictionaries (`go.Figure`). Streamlit renders them using `st.plotly_chart(fig, use_container_width=True)` using the Plotly.js client-side library, allowing tooltips, zooms, and interactive hovering."),

        # Part E: Limitations & Future Scope
        ("Q29: What are the current limitations of this project?",
         "Current limitations include: (1) The ML model evaluates anomaly status primarily on expenditure magnitude rather than multidimensional time-series periodicity; (2) Authentication uses a local JSON dictionary rather than hashed database records (like bcrypt); (3) It currently analyzes single-user data rather than multi-tenant household budgeting."),

        ("Q30: What future enhancements would you propose for SpendWise?",
         "Future scope includes: (1) Multi-feature anomaly detection incorporating category frequency, merchant novelty, and day-of-week timing; (2) Time-series expenditure forecasting using Facebook Prophet or ARIMA; (3) OCR receipt scanning using Tesseract to automatically ingest paper bills; (4) Automated budget alert emails or Telegram push notifications.")
    ]

    for q_text, ans_text in viva_qa:
        # Keep each Q&A block together to prevent page breaks between question and answer
        story.append(KeepTogether([
            Paragraph(q_text, q_style),
            Paragraph(ans_text, ans_style),
            Spacer(1, 3)
        ]))

    # Final wrap-up note
    story.append(Spacer(1, 10))
    t_end = Table([[Paragraph("<b>End of Viva Defense Guide.</b> Prepared for academic project submission and oral examination.", callout_style)]], colWidths=[504])
    t_end.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_WARM_CREAM),
        ('BOX', (0,0), (-1,-1), 1, C_SAGE),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_end)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built at: {os.path.abspath(filename)}")


if __name__ == "__main__":
    out_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SpendWise_Complete_Viva_Guide.pdf")
    build_pdf(out_pdf)
