import os
import sys
import subprocess

# Ensure python-pptx is installed
try:
    import pptx
except ImportError:
    print("Installing python-pptx to generate PowerPoint file...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-pptx"])
    import pptx

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5) # 16:9 widescreen layout

    # Color Palette matching KPR template & modern CSDA theme
    C_NAVY_DARK = RGBColor(15, 23, 42)      # #0f172a
    C_BLUE_PRIMARY = RGBColor(14, 116, 144)  # #0e7490
    C_CYAN_ACCENT = RGBColor(6, 182, 212)   # #06b6d4
    C_TEXT_DARK = RGBColor(30, 41, 59)      # #1e293b
    C_TEXT_MUTED = RGBColor(71, 85, 105)    # #475569
    C_WHITE = RGBColor(255, 255, 255)
    C_CARD_BG = RGBColor(241, 245, 249)     # #f1f5f9
    C_BORDER = RGBColor(203, 213, 225)      # #cbd5e1

    def add_slide_background(slide, title_text=""):
        # Top decorative accent bar
        accent_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.4), Inches(7.5))
        accent_bar.fill.solid()
        accent_bar.fill.fore_color.rgb = C_BLUE_PRIMARY
        accent_bar.line.color.rgb = C_BLUE_PRIMARY

        accent_bar2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0), Inches(0.15), Inches(7.5))
        accent_bar2.fill.solid()
        accent_bar2.fill.fore_color.rgb = C_CYAN_ACCENT
        accent_bar2.line.color.rgb = C_CYAN_ACCENT

        if title_text:
            tb = slide.shapes.add_textbox(Inches(1.0), Inches(0.4), Inches(11.8), Inches(0.8))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title_text.upper()
            p.font.name = "Arial"
            p.font.size = Pt(24)
            p.font.bold = True
            p.font.color.rgb = C_NAVY_DARK

    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_slide_background(s1)

    # Institution Box
    tb_inst = s1.shapes.add_textbox(Inches(1.0), Inches(0.4), Inches(11.8), Inches(1.2))
    tf_inst = tb_inst.text_frame
    tf_inst.word_wrap = True
    
    p = tf_inst.paragraphs[0]
    p.text = "KPR COLLEGE OF ARTS SCIENCE AND RESEARCH"
    p.font.name = "Arial"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.alignment = PP_ALIGN.CENTER

    p2 = tf_inst.add_paragraph()
    p2.text = "(Affiliated to Bharathiar University, Coimbatore)\nAvinashi Road, Arasur, Coimbatore – 641 407"
    p2.font.name = "Arial"
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_TEXT_MUTED
    p2.alignment = PP_ALIGN.CENTER

    # Project Title Box
    title_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.8), Inches(11.4), Inches(1.1))
    title_box.fill.solid()
    title_box.fill.fore_color.rgb = C_NAVY_DARK
    title_box.line.color.rgb = C_BLUE_PRIMARY
    tf_t = title_box.text_frame
    tf_t.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_t.paragraphs[0]
    p.text = "STOCK MARKET TREND PREDICTION &\nTIME SERIES ANALYSIS SYSTEM"
    p.font.name = "Arial"
    p.font.size = Pt(21)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Student & Supervisor Box
    info_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(3.1), Inches(11.4), Inches(1.6))
    info_box.fill.solid()
    info_box.fill.fore_color.rgb = C_CARD_BG
    info_box.line.color.rgb = C_BORDER
    tf_info = info_box.text_frame
    tf_info.word_wrap = True

    p = tf_info.paragraphs[0]
    p.text = "Submitted by: [Your Name]   |   Reg. No: [Your Register Number]"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK
    p.alignment = PP_ALIGN.CENTER

    p2 = tf_info.add_paragraph()
    p2.text = "Degree: III B.Sc., Computer Science with Data Analytics (CSDA)"
    p2.font.name = "Arial"
    p2.font.size = Pt(13)
    p2.font.color.rgb = C_TEXT_DARK
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf_info.add_paragraph()
    p3.text = "Project Supervisor: Mr. M. Manoj MCA, M.Phil., (Ph.D.).,\nAssistant Professor, Department of Computer Science with Data Analytics"
    p3.font.name = "Arial"
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = C_BLUE_PRIMARY
    p3.alignment = PP_ALIGN.CENTER

    # Acknowledgement Box
    ack_box = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(4.9), Inches(11.4), Inches(2.1))
    ack_box.fill.solid()
    ack_box.fill.fore_color.rgb = C_WHITE
    ack_box.line.color.rgb = C_BORDER
    tf_ack = ack_box.text_frame
    tf_ack.word_wrap = True

    p = tf_ack.paragraphs[0]
    p.text = "Acknowledgement:"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY

    p2 = tf_ack.add_paragraph()
    p2.text = "I would like to express my heartfelt thanks to Dr. G. Satyavathy, Head of the Department of Computer Science with Data Analytics, and Dr. K. Jayanthi Vagini, Assistant Professor, Department of Computer Science with Data Analytics for being such incredible mentors throughout my academic journey. Finally, I'm extremely grateful to my supervisor Mr. M. Manoj, Assistant Professor, Department of Computer Science with Data Analytics for his valuable support and guidance."
    p2.font.name = "Arial"
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 2: PROJECT OVERVIEW (PROBLEM / SOLUTION / KEY FEATURES)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_slide_background(s2, "STOCKTREND AI - OVERVIEW & PROBLEM STATEMENT")

    # Column 1: Problem & Existing
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.3), Inches(5.6), Inches(5.7))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_CARD_BG
    c1.line.color.rgb = C_BORDER
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True

    p = tf_c1.paragraphs[0]
    p.text = "PROBLEM:"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = C_NAVY_DARK

    p = tf_c1.add_paragraph()
    p.text = "• Individual investors face significant challenges in accurately and quickly forecasting stock trends."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_DARK

    p = tf_c1.add_paragraph()
    p.text = "• Traditional manual charting methods are slow and subjective, leading to delays and severe financial losses."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_DARK

    p = tf_c1.add_paragraph()
    p.text = "\nEXISTING SYSTEM:"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = C_NAVY_DARK

    p = tf_c1.add_paragraph()
    p.text = "• Manual technical charting prone to emotional biases (fear, panic, greed).\n• Disconnected desktop tools lacking real-time data automation.\n• No statistical confidence bands or machine learning probability scoring."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_DARK

    # Column 2: Solution & Key Features
    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.3), Inches(5.8), Inches(5.7))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_CARD_BG
    c2.line.color.rgb = C_BORDER
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True

    p = tf_c2.paragraphs[0]
    p.text = "SOLUTION:"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = C_BLUE_PRIMARY

    p = tf_c2.add_paragraph()
    p.text = "• StockTrend AI is an intelligent financial analytics web platform designed to provide traders with a precise, automated tool for equity trend forecasting."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_DARK

    p = tf_c2.add_paragraph()
    p.text = "• Integrates statistical time-series forecasting (ARIMA) and supervised machine learning classification (Random Forest & Gradient Boosting) with interactive indicators."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_DARK

    p = tf_c2.add_paragraph()
    p.text = "\nKEY FEATURES:"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = C_BLUE_PRIMARY

    p = tf_c2.add_paragraph()
    p.text = "▪ Automated live data ingestion & 6-hour intelligent disk cache\n▪ Quantitative indicators (SMA 20/50, EMA 20, RSI 14, MACD)\n▪ 30-day ARIMA future price curves with 95% confidence bands\n▪ Next-day UP/DOWN direction classification & confidence %\n▪ Real-time hyperparameter tuning sandbox & Recharts dashboard"
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 3: INTRODUCTION
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_slide_background(s3, "INTRODUCTION")

    box_intro = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.3), Inches(11.7), Inches(5.7))
    box_intro.fill.solid()
    box_intro.fill.fore_color.rgb = C_WHITE
    box_intro.line.color.rgb = C_BORDER
    tf_i = box_intro.text_frame
    tf_i.word_wrap = True

    p = tf_i.paragraphs[0]
    p.text = "StockTrend AI is an advanced financial analytics and predictive modeling platform developed to address the critical challenges of market volatility and trend forecasting in modern financial equity markets. Leveraging cutting-edge artificial intelligence, specifically statistical time-series modeling and ensemble machine learning algorithms, StockTrend AI enables traders, investors, and quantitative researchers to accurately evaluate historical market behaviors and forecast next-day price trajectories."
    p.font.size = Pt(14)
    p.font.color.rgb = C_TEXT_DARK

    p2 = tf_i.add_paragraph()
    p2.text = "\nThe application integrates a high-performance Python FastAPI backend connected to real-time market data APIs (yfinance) and a robust 6-hour local disk cache, ensuring access to a comprehensive database of daily OHLCV trading records. Dynamic quantitative feature engineering algorithms autonomously extract rolling indicators—including Moving Averages (SMA/EMA), Relative Strength Index (RSI), and Moving Average Convergence Divergence (MACD)—to identify non-linear momentum patterns."
    p2.font.size = Pt(14)
    p2.font.color.rgb = C_TEXT_DARK

    p3 = tf_i.add_paragraph()
    p3.text = "\nBy combining statistical ARIMA forecasting (which provides 30-day projection curves bounded by 95% confidence limits) with supervised classification algorithms (Random Forest and Gradient Boosting for next-day UP/DOWN direction), StockTrend AI empowers users with actionable, evidence-based insights. The platform features an intuitive dark-mode React 18 and Recharts visual dashboard, an interactive hyperparameter sandbox, and diagnostic model evaluation metrics, ultimately contributing to disciplined, data-driven financial decision-making."
    p3.font.size = Pt(14)
    p3.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 4: TECHNICAL ARCHITECTURE: FRONTEND
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_slide_background(s4, "TECHNICAL ARCHITECTURE: FRONTEND (WEB APP)")

    fe_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.3), Inches(11.7), Inches(5.7))
    fe_box.fill.solid()
    fe_box.fill.fore_color.rgb = C_CARD_BG
    fe_box.line.color.rgb = C_BORDER
    tf_fe = fe_box.text_frame
    tf_fe.word_wrap = True

    p = tf_fe.paragraphs[0]
    p.text = "FRONTEND: SINGLE PAGE APPLICATION (SPA)"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = C_BLUE_PRIMARY

    items_fe = [
        ("FRAMEWORK & BUILD TOOL:", "React 18 (Single Page Application architecture) powered by Vite 8 for lightning-fast development, hot-module replacement (HMR), and optimized production builds."),
        ("INTERACTIVE DATA VISUALIZATION:", "Recharts charting engine (ComposedChart, ResponsiveContainer, Line, Area, Bar, Tooltip, Legend) rendering candlestick overlays, multi-timeframe curves, and confidence corridors."),
        ("API COMMUNICATION:", "Native Asynchronous JavaScript Fetch API, connecting seamlessly with the FastAPI backend endpoints via RESTful JSON schemas."),
        ("STATE MANAGEMENT:", "React Hooks (useState, useEffect, useCallback) managing dynamic stock ticker changes, time-series parameter adjustments, and real-time model evaluation results."),
        ("UI / UX DESIGN SYSTEM:", "Custom dark-mode glassmorphism with responsive CSS3 variables, flexible grid layouts, and Lucide-React icons (TrendingUp, Activity, Cpu, Search, CheckCircle2, AlertCircle).")
    ]

    for title, desc in items_fe:
        p = tf_fe.add_paragraph()
        p.text = f"\n▪ {title} "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = C_NAVY_DARK
        p2 = tf_fe.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(12)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 5: TECHNICAL ARCHITECTURE: BACKEND & DATABASE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_slide_background(s5, "TECHNICAL ARCHITECTURE: BACKEND (API & DATABASE)")

    be_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.3), Inches(11.7), Inches(5.7))
    be_box.fill.solid()
    be_box.fill.fore_color.rgb = C_CARD_BG
    be_box.line.color.rgb = C_BORDER
    tf_be = be_box.text_frame
    tf_be.word_wrap = True

    p = tf_be.paragraphs[0]
    p.text = "BACKEND (API, DATABASE & MACHINE LEARNING PIPELINE)"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = C_BLUE_PRIMARY

    items_be = [
        ("REST API & ASGI SERVER:", "Python 3.14 + FastAPI framework running on Uvicorn ASGI server with automatic OpenAPI/Swagger documentation and asynchronous request processing."),
        ("DATA INGESTION & PROCESSING:", "yfinance library for automated ingestion of Yahoo Finance market feeds; Pandas & NumPy for vectorized time-series wrangling and indicator calculation."),
        ("DATABASE & CACHE ENGINE:", "High-speed local file disk caching database located in backend/cache/ storing structured daily OHLCV CSV tables with automated 6-hour cache invalidation."),
        ("TIME-SERIES FORECASTING:", "Statsmodels ARIMA(p,d,q) implementation calculating out-of-sample error statistics (MAE, RMSE, MAPE) and 30-day projection curves with 95% confidence bands."),
        ("SUPERVISED ML CLASSIFIERS:", "Scikit-Learn ensemble models (RandomForestClassifier, GradientBoostingClassifier) generating next-day UP/DOWN direction, confidence %, and Gini feature importances.")
    ]

    for title, desc in items_be:
        p = tf_be.add_paragraph()
        p.text = f"\n▪ {title} "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = C_NAVY_DARK
        p2 = tf_be.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(12)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 6: MODULES
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_slide_background(s6, "SYSTEM MODULES")

    mods = [
        ("1. Stock Selection & Ticker Search Module", "Enables real-time lookup of global equity symbols or instant selection from blue-chip presets (AAPL, NVDA, TSLA, MSFT, GOOGL, AMZN)."),
        ("2. Market Overview & Equity Valuation Module", "Displays current stock quotes, market capitalization, P/E ratios, 52-week high/low boundaries, and interactive price trendlines."),
        ("3. Technical Indicators & Feature Engineering Module", "Computes and overlays Simple Moving Averages (SMA 20/50), Exponential Moving Averages (EMA 20), RSI (14), and MACD signal lines."),
        ("4. Statistical ARIMA Time-Series Forecasting Module", "Fits autoregressive integrated moving average equations to project 30-day future price trajectories with 95% statistical confidence corridors."),
        ("5. Ensemble ML Trend Predictor Module", "Trains supervised Random Forest and Gradient Boosting algorithms on return lags to predict next-day trend direction (UP/DOWN)."),
        ("6. Hyperparameter Tuning & Simulation Sandbox", "Allows users to adjust tree counts (n_estimators), tree depth (max_depth), lag counts, and ARIMA orders in real-time."),
        ("7. Model Evaluation & Explainability Module", "Computes out-of-sample confusion matrix metrics (Accuracy, Precision, Recall, F1-Score) and Gini feature importance rankings."),
        ("8. Data Ingestion & Intelligent Disk Caching Module", "Synchronizes external market feeds and automatically maintains an organized 6-hour local CSV cache in backend/cache/.")
    ]

    # Two columns for 8 modules
    for i, (m_title, m_desc) in enumerate(mods):
        col_x = Inches(1.0) if i < 4 else Inches(6.9)
        col_y = Inches(1.3) + Inches((i % 4) * 1.4)
        m_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col_x, col_y, Inches(5.6), Inches(1.25))
        m_box.fill.solid()
        m_box.fill.fore_color.rgb = C_WHITE
        m_box.line.color.rgb = C_BORDER
        tf_m = m_box.text_frame
        tf_m.word_wrap = True

        p = tf_m.paragraphs[0]
        p.text = m_title
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = C_BLUE_PRIMARY

        p2 = tf_m.add_paragraph()
        p2.text = m_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 7: FLOWCHART
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_slide_background(s7, "SYSTEM WORKFLOW & ARCHITECTURE FLOWCHART")

    # Workflow visual boxes
    steps = [
        ("USER OPENS APP", "Selects Ticker (AAPL/NVDA) & Timeframe", Inches(1.0), Inches(1.5), Inches(3.4), Inches(1.1), C_NAVY_DARK, C_WHITE),
        ("CACHE EVALUATION", "Checks backend/cache/{TICKER}.csv (< 6h)", Inches(5.0), Inches(1.5), Inches(3.4), Inches(1.1), C_BLUE_PRIMARY, C_WHITE),
        ("DATA ACQUISITION", "Read Local CSV or Fetch via yfinance API", Inches(9.0), Inches(1.5), Inches(3.4), Inches(1.1), C_CARD_BG, C_NAVY_DARK),

        ("FEATURE ENGINEERING", "Compute SMA 20/50, EMA 20, RSI, MACD & Lags", Inches(1.0), Inches(3.2), Inches(5.4), Inches(1.1), C_CARD_BG, C_NAVY_DARK),
        ("DUAL PREDICTIVE ENGINES", "Parallel Execution of ARIMA & Machine Learning", Inches(7.0), Inches(3.2), Inches(5.4), Inches(1.1), C_NAVY_DARK, C_WHITE),

        ("ARIMA FORECAST", "30-Day Trend Curve + 95% Confidence Bounds", Inches(1.0), Inches(4.8), Inches(3.6), Inches(1.8), C_CARD_BG, C_TEXT_DARK),
        ("SUPERVISED ML PREDICTION", "Random Forest / Gradient Boosting (UP/DOWN)", Inches(5.0), Inches(4.8), Inches(3.6), Inches(1.8), C_CARD_BG, C_TEXT_DARK),
        ("RECHARTS DASHBOARD", "Interactive Candlesticks, Gauges & Sandboxes", Inches(9.0), Inches(4.8), Inches(3.4), Inches(1.8), C_BLUE_PRIMARY, C_WHITE)
    ]

    for title, sub, x, y, w, h, bg, fg in steps:
        box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        box.fill.solid()
        box.fill.fore_color.rgb = bg
        box.line.color.rgb = C_BORDER
        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE

        p = tf.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = fg
        p.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(10)
        p2.font.color.rgb = fg
        p2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 8: THE PROCESS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_slide_background(s8, "THE PROCESS")

    proc_box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.3), Inches(11.7), Inches(5.7))
    proc_box.fill.solid()
    proc_box.fill.fore_color.rgb = C_WHITE
    proc_box.line.color.rgb = C_BORDER
    tf_proc = proc_box.text_frame
    tf_proc.word_wrap = True

    p = tf_proc.paragraphs[0]
    p.text = "END-TO-END EXECUTION PIPELINE:"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = C_BLUE_PRIMARY

    proc_steps = [
        "User selects or searches a stock symbol (e.g., AAPL, NVDA, TSLA) and timeframe (6M, 1Y, 2Y) on the interactive dashboard.",
        "The FastAPI backend checks the local cache (backend/cache/). If fresh data exists, it reads directly from the CSV; otherwise, it pulls real-time daily OHLCV trading records from Yahoo Finance and updates the disk cache.",
        "The quantitative engine calculates technical indicators (SMA, EMA, RSI, MACD), calculates daily return lags, and computes rolling volatility features.",
        "The dual analytics engine executes: Statsmodels fits the ARIMA(p,d,q) model to project a 30-day price curve with 95% confidence intervals, while Scikit-Learn trains Random Forest or Gradient Boosting classifiers to determine next-day trend direction (UP/DOWN).",
        "The predictions, model accuracy scorecard, and interactive visual charts are streamed as JSON to the React frontend and rendered instantly."
    ]

    for i, step in enumerate(proc_steps, 1):
        p = tf_proc.add_paragraph()
        p.text = f"\n• Step {i}: "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = C_NAVY_DARK
        p2 = tf_proc.add_paragraph()
        p2.text = f"   {step}"
        p2.font.size = Pt(12)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 9: BENEFITS FOR INVESTORS & TRADERS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_slide_background(s9, "BENEFITS FOR INVESTORS & TRADERS")

    ben_box = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.3), Inches(11.7), Inches(5.7))
    ben_box.fill.solid()
    ben_box.fill.fore_color.rgb = C_CARD_BG
    ben_box.line.color.rgb = C_BORDER
    tf_ben = ben_box.text_frame
    tf_ben.word_wrap = True

    p = tf_ben.paragraphs[0]
    p.text = "TRANSFORMING FINANCIAL DECISION-MAKING:"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = C_BLUE_PRIMARY

    bens = [
        ("Objective & Emotion-Free Trading:", "Eliminates cognitive biases, panic selling, and greedy over-leveraging by replacing subjective opinions with empirical probability scores and mathematical forecasts."),
        ("Downside Risk Mitigation:", "95% statistical confidence corridors provide clear upper and lower price boundaries, helping investors establish realistic stop-loss orders and protect capital."),
        ("High-Speed Sub-Second Analytics:", "Local disk caching eliminates slow API latencies and external rate-limiting, delivering instant charting and analytics without expensive subscriptions."),
        ("Transparent Algorithmic Explainability:", "Gini impurity feature importance rankings reveal exactly which technical indicators (RSI, Volatility, Moving Averages) drove the model's prediction."),
        ("Accessible Quantitative Education:", "Provides students, data analysts, and individual retail investors with an interactive sandbox to learn and experiment with machine learning and time series forecasting.")
    ]

    for title, desc in bens:
        p = tf_ben.add_paragraph()
        p.text = f"\n• {title} "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = C_NAVY_DARK
        p2 = tf_ben.add_paragraph()
        p2.text = f"   {desc}"
        p2.font.size = Pt(12)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 10: SAMPLE APPLICATION DASHBOARD
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_slide_background(s10, "SAMPLE APPLICATION DASHBOARD")

    screens = [
        ("1. Live Market Overview & Technical Charting", 
         "• Displays real-time stock metrics: Current Price ($347.32), Market Cap ($5.07T), P/E Ratio (39.8), and 52-Week Range ($243.42 - $351.73).\n• Multi-timeframe Recharts visualizer rendering primary price curves alongside SMA 20, SMA 50, EMA 20, RSI 14 sub-chart, and MACD histograms."),
        
        ("2. ARIMA Time-Series Forecast Screen",
         "• Visualizes historical equity data seamlessly transitioning into a 30-day future trajectory.\n• Shaded 95% confidence corridor highlights upper and lower statistical uncertainty boundaries.\n• Out-of-sample diagnostic error scorecard reporting MAE, RMSE, and MAPE."),

        ("3. Machine Learning Prediction Sandbox",
         "• Prominent directional callout: PREDICTED DIRECTION: UP / DOWN with calibrated Confidence %.\n• Interactive hyperparameter sliders for tuning tree depth, estimator counts, and lag variables.\n• Real-time model evaluation metrics: Accuracy, Precision, Recall, and F1-Score.")
    ]

    for i, (title, desc) in enumerate(screens):
        sc_box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.3 + i * 1.85), Inches(11.7), Inches(1.65))
        sc_box.fill.solid()
        sc_box.fill.fore_color.rgb = C_WHITE
        sc_box.line.color.rgb = C_BORDER
        tf_sc = sc_box.text_frame
        tf_sc.word_wrap = True

        p = tf_sc.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = C_BLUE_PRIMARY

        p2 = tf_sc.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 11: CONCLUSION & THANK YOU
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_slide_background(s11)

    # Conclusion Card
    conc_box = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(0.8), Inches(11.4), Inches(3.2))
    conc_box.fill.solid()
    conc_box.fill.fore_color.rgb = C_CARD_BG
    conc_box.line.color.rgb = C_BORDER
    tf_conc = conc_box.text_frame
    tf_conc.word_wrap = True

    p = tf_conc.paragraphs[0]
    p.text = "CONCLUSION:"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = C_NAVY_DARK

    p2 = tf_conc.add_paragraph()
    p2.text = "• StockTrend AI successfully demonstrates how full-stack web engineering, statistical time-series forecasting (ARIMA), and supervised machine learning (Random Forest & Gradient Boosting) can be unified into an accessible financial analytics tool."
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_TEXT_DARK

    p3 = tf_conc.add_paragraph()
    p3.text = "• By combining a high-performance FastAPI backend with an interactive React 18 & Recharts dashboard and 6-hour disk caching, the system delivers sub-second response times, empirical risk boundaries, and complete algorithmic transparency."
    p3.font.size = Pt(12)
    p3.font.color.rgb = C_TEXT_DARK

    p4 = tf_conc.add_paragraph()
    p4.text = "• The dual-engine methodology eliminates human emotional bias, providing investors with reliable quantitative evidence to make sound trading decisions."
    p4.font.size = Pt(12)
    p4.font.color.rgb = C_TEXT_DARK

    # Thank you box
    ty_box = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.3), Inches(11.4), Inches(2.7))
    ty_box.fill.solid()
    ty_box.fill.fore_color.rgb = C_NAVY_DARK
    ty_box.line.color.rgb = C_BLUE_PRIMARY
    tf_ty = ty_box.text_frame
    tf_ty.word_wrap = True
    tf_ty.vertical_anchor = MSO_ANCHOR.MIDDLE

    p = tf_ty.paragraphs[0]
    p.text = "THANK YOU"
    p.font.name = "Arial"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER

    p2 = tf_ty.add_paragraph()
    p2.text = "Questions & Discussion"
    p2.font.size = Pt(16)
    p2.font.color.rgb = C_CYAN_ACCENT
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf_ty.add_paragraph()
    p3.text = "\nPresenter: [Your Name]   |   Reg. No: [Your Register Number]"
    p3.font.size = Pt(13)
    p3.font.color.rgb = C_WHITE
    p3.alignment = PP_ALIGN.CENTER

    p4 = tf_ty.add_paragraph()
    p4.text = "Department of Computer Science with Data Analytics | KPR College of Arts Science and Research"
    p4.font.size = Pt(12)
    p4.font.color.rgb = C_BORDER
    p4.alignment = PP_ALIGN.CENTER

    # Save presentation
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "StockTrend_AI_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_deck()
