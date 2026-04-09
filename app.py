import streamlit as st

st.set_page_config(
    page_title="TCM Reference",
    page_icon="☯",
    layout="centered",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@300;400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
    h1, h2, h3 { font-family: 'Lora', serif; }

    .hero {
        background: linear-gradient(135deg, #2d4a3e 0%, #4a3a6a 100%);
        padding: 3rem 2.5rem 2.5rem;
        border-radius: 14px;
        margin-bottom: 2.5rem;
        text-align: center;
        color: white;
    }
    .hero h1 {
        font-family: 'Lora', serif;
        font-size: 2.4rem;
        color: white;
        margin: 0 0 0.5rem;
    }
    .hero p {
        color: #c8d8cf;
        font-size: 1.05rem;
        margin: 0;
    }

    .card-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.25rem;
        margin-bottom: 2rem;
    }
    .card {
        border-radius: 12px;
        padding: 2rem 1.75rem;
        text-decoration: none;
        display: block;
        transition: box-shadow 0.2s, transform 0.15s;
        cursor: pointer;
    }
    .card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.13);
        transform: translateY(-2px);
    }
    .card-herb {
        background: linear-gradient(145deg, #f0f7f2, #ddeee3);
        border: 1px solid #b8d8c4;
    }
    .card-formula {
        background: linear-gradient(145deg, #f3f0f8, #e8e0f4);
        border: 1px solid #c8b8e0;
    }
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
        display: block;
    }
    .card-title {
        font-family: 'Lora', serif;
        font-size: 1.35rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .card-herb .card-title  { color: #1e3329; }
    .card-formula .card-title { color: #1e1429; }
    .card-desc {
        font-size: 0.9rem;
        line-height: 1.55;
    }
    .card-herb .card-desc  { color: #3a5c4a; }
    .card-formula .card-desc { color: #4a3a6a; }
    .card-cta {
        display: inline-block;
        margin-top: 1.1rem;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        padding: 0.35rem 0.9rem;
        border-radius: 20px;
    }
    .card-herb .card-cta  { background: #2d4a3e; color: white; }
    .card-formula .card-cta { background: #3a2d52; color: white; }

    .footer-note {
        text-align: center;
        font-size: 0.82rem;
        color: #aaa;
        margin-top: 1rem;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>☯ TCM Reference</h1>
    <p>Traditional Chinese Medicine — Materia Medica &amp; Classical Formulas</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card-grid">
    <div class="card card-herb">
        <span class="card-icon">🌿</span>
        <div class="card-title">Herb Reference</div>
        <div class="card-desc">
            Browse individual herbs by category, temperature, taste, and meridian.
            Search by name, pinyin, properties, or indication.
        </div>
        <span class="card-cta">Open Herbs →</span>
    </div>
    <div class="card card-formula">
        <span class="card-icon">⚗️</span>
        <div class="card-title">Formula Reference</div>
        <div class="card-desc">
            Explore classical formulas with full ingredient breakdowns,
            functions, indications, and cautions.
        </div>
        <span class="card-cta">Open Formulas →</span>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.page_link("pages/1_Herbs.py", label="Open Herb Reference", icon="🌿", use_container_width=True)

with col2:
    st.page_link("pages/2_Formulas.py", label="Open Formula Reference", icon="⚗️", use_container_width=True)

st.markdown('<div class="footer-note">For educational reference only — not medical advice.</div>', unsafe_allow_html=True)
