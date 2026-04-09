import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TCM Herb Reference",
    page_icon="🌿",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@300;400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
    h1, h2, h3 { font-family: 'Lora', serif; }

    .app-header {
        background: linear-gradient(135deg, #2d4a3e 0%, #4a7c59 100%);
        padding: 2rem 2.5rem; border-radius: 12px; margin-bottom: 2rem; color: white;
    }
    .app-header h1 { color: white; margin: 0; font-size: 2rem; }
    .app-header p  { color: #b8d4c0; margin: 0.25rem 0 0; font-size: 1rem; }

    .stats-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
    .stat-chip {
        background: #f0f7f2; border: 1px solid #c8e0cc; border-radius: 20px;
        padding: 0.3rem 0.85rem; font-size: 0.85rem; color: #2d4a3e; font-weight: 600;
    }

    .herb-card {
        background: white; border: 1px solid #e0ebe3; border-radius: 10px;
        padding: 1.25rem 1.5rem; margin-bottom: 1rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05); transition: box-shadow 0.2s;
    }
    .herb-card:hover { box-shadow: 0 4px 14px rgba(45,74,62,0.12); }
    .herb-name {
        font-family: 'Lora', serif; font-size: 1.15rem; font-weight: 600;
        color: #1e3329; margin-bottom: 0.1rem;
    }
    .herb-pinyin { font-size: 0.9rem; color: #7aaa8a; font-style: italic; margin-bottom: 0.75rem; }
    .section-label {
        font-size: 0.72rem; font-weight: 600; letter-spacing: 0.08em;
        text-transform: uppercase; color: #4a7c59; margin-bottom: 0.25rem; margin-top: 0.6rem;
    }
    .tag {
        display: inline-block; background: #eef6f0; border: 1px solid #c0ddc8;
        border-radius: 4px; padding: 0.15rem 0.55rem; font-size: 0.8rem;
        color: #2d5c3f; margin: 0.15rem 0.2rem 0.15rem 0;
    }
    .tag.warm    { background: #fff4e6; border-color: #f5c97a; color: #7a4f00; }
    .tag.hot     { background: #ffe8e8; border-color: #f5a0a0; color: #7a0000; }
    .tag.cool    { background: #e8f0ff; border-color: #a0b8f5; color: #1a3a7a; }
    .tag.cold    { background: #e0f0ff; border-color: #80b8f5; color: #003a7a; }
    .tag.neutral { background: #f5f5f5; border-color: #c0c0c0; color: #444; }
    .indication-text { font-size: 0.9rem; color: #445; line-height: 1.5; }
    .no-results { text-align: center; padding: 3rem; color: #888; font-style: italic; }
    .sidebar-title { font-family: 'Lora', serif; font-weight: 600; color: #2d4a3e; }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
HERBS = [
    {
        "name": "Astragalus", "pinyin": "Huáng Qí", "category": "Tonifying",
        "temperature": "Warm", "taste": ["Sweet"], "meridians": ["Spleen", "Lung"],
        "properties": "Tonifies Wei Qi and consolidates the exterior; raises Spleen and Stomach Qi; promotes urination and reduces edema.",
        "indications": "Fatigue, shortness of breath, spontaneous sweating, frequent colds, prolapse of organs, edema, non-healing sores.",
    },
    {
        "name": "Ginseng", "pinyin": "Rén Shēn", "category": "Tonifying",
        "temperature": "Warm", "taste": ["Sweet", "Slightly bitter"], "meridians": ["Heart", "Lung", "Spleen"],
        "properties": "Strongly tonifies Yuan Qi; tonifies Lung and Spleen Qi; generates body fluids; calms the spirit.",
        "indications": "Extreme fatigue, cold limbs, poor appetite, chronic cough, palpitations, insomnia, diabetes.",
    },
    {
        "name": "Angelica Root", "pinyin": "Dāng Guī", "category": "Blood-Tonifying",
        "temperature": "Warm", "taste": ["Sweet", "Acrid"], "meridians": ["Heart", "Liver", "Spleen"],
        "properties": "Tonifies and invigorates Blood; regulates menstruation; moistens the intestines; reduces swelling.",
        "indications": "Blood deficiency, irregular menstruation, amenorrhea, dysmenorrhea, constipation, abscesses.",
    },
    {
        "name": "Rehmannia (Prepared)", "pinyin": "Shú Dì Huáng", "category": "Blood-Tonifying",
        "temperature": "Warm", "taste": ["Sweet"], "meridians": ["Heart", "Liver", "Kidney"],
        "properties": "Tonifies Blood and nourishes Yin; fills Essence and Marrow.",
        "indications": "Blood deficiency with pallor, dizziness, palpitations; Yin deficiency with night sweats, low-grade fever, tinnitus.",
    },
    {
        "name": "Coptis", "pinyin": "Huáng Lián", "category": "Heat-Clearing",
        "temperature": "Cold", "taste": ["Bitter"], "meridians": ["Heart", "Stomach", "Liver", "Large Intestine"],
        "properties": "Clears Heat and drains Damp; drains Fire and resolves toxicity; clears Heart fire.",
        "indications": "High fever, irritability, insomnia, vomiting, diarrhea from damp-heat, skin infections.",
    },
    {
        "name": "Poria", "pinyin": "Fú Líng", "category": "Damp-Draining",
        "temperature": "Neutral", "taste": ["Sweet", "Bland"], "meridians": ["Heart", "Spleen", "Kidney"],
        "properties": "Promotes urination and leaches Dampness; strengthens the Spleen; calms the Mind.",
        "indications": "Edema, difficult urination, diarrhea, insomnia, palpitations, forgetfulness.",
    },
    {
        "name": "Licorice Root", "pinyin": "Gān Cǎo", "category": "Tonifying",
        "temperature": "Neutral", "taste": ["Sweet"], "meridians": ["All 12 meridians"],
        "properties": "Tonifies Spleen Qi; moistens Lungs; moderates and harmonises other herbs; clears Heat.",
        "indications": "Fatigue, palpitations, cough, sore throat, spasms and pain. Widely used harmonising herb.",
    },
    {
        "name": "Cinnamon Bark", "pinyin": "Ròu Guì", "category": "Interior-Warming",
        "temperature": "Hot", "taste": ["Acrid", "Sweet"], "meridians": ["Kidney", "Spleen", "Heart", "Liver"],
        "properties": "Warms Kidney Yang and Ming Men Fire; disperses Cold; warms and unblocks the channels.",
        "indications": "Kidney Yang deficiency, cold limbs, impotence, abdominal coldness and pain, amenorrhea.",
    },
    {
        "name": "Chrysanthemum", "pinyin": "Jú Huā", "category": "Heat-Clearing",
        "temperature": "Cool", "taste": ["Sweet", "Bitter"], "meridians": ["Lung", "Liver"],
        "properties": "Disperses Wind-Heat; calms Liver and brightens eyes; clears Heat and resolves toxicity.",
        "indications": "Wind-heat fever, headache, red/painful eyes, blurred vision, Liver Yang rising.",
    },
    {
        "name": "Schisandra", "pinyin": "Wǔ Wèi Zǐ", "category": "Astringent",
        "temperature": "Warm", "taste": ["Sour", "Sweet"], "meridians": ["Heart", "Kidney", "Lung"],
        "properties": "Contains leakage of Lung Qi; tonifies Kidney; generates Body Fluids; calms the Mind.",
        "indications": "Chronic cough, asthma, night sweats, palpitations, insomnia, poor memory.",
    },
    {
        "name": "Salvia (Red Sage)", "pinyin": "Dān Shēn", "category": "Blood-Invigorating",
        "temperature": "Cool", "taste": ["Bitter"], "meridians": ["Heart", "Pericardium", "Liver"],
        "properties": "Invigorates Blood and dispels Stasis; clears Heat; nourishes Blood and calms the spirit.",
        "indications": "Chest pain, palpitations, amenorrhea, abdominal masses, insomnia, skin rashes.",
    },
    {
        "name": "Ginger (Dried)", "pinyin": "Gān Jiāng", "category": "Interior-Warming",
        "temperature": "Hot", "taste": ["Acrid"], "meridians": ["Heart", "Lung", "Spleen", "Stomach"],
        "properties": "Warms the Middle and dispels Cold; rescues Yang; warms Lungs and transforms Phlegm.",
        "indications": "Cold limbs and pulse, vomiting, diarrhea from Cold, cough with thin watery phlegm.",
    },
    {
        "name": "Codonopsis", "pinyin": "Dǎng Shēn", "category": "Tonifying",
        "temperature": "Neutral", "taste": ["Sweet"], "meridians": ["Lung", "Spleen"],
        "properties": "Tonifies Middle Jiao Qi; tonifies Lungs; nourishes Blood; promotes Body Fluids.",
        "indications": "Fatigue, poor appetite, loose stool, Lung deficiency cough. Milder substitute for Ginseng.",
    },
    {
        "name": "Peony Root (White)", "pinyin": "Bái Sháo", "category": "Blood-Tonifying",
        "temperature": "Cool", "taste": ["Bitter", "Sour"], "meridians": ["Liver", "Spleen"],
        "properties": "Nourishes Blood and regulates menstruation; softens Liver and alleviates pain; calms Liver Yang.",
        "indications": "Menstrual irregularity, dysmenorrhea, abdominal pain, limb spasms, dizziness.",
    },
    {
        "name": "Jujube (Red Date)", "pinyin": "Dà Zǎo", "category": "Tonifying",
        "temperature": "Warm", "taste": ["Sweet"], "meridians": ["Spleen", "Stomach"],
        "properties": "Tonifies Spleen and Stomach Qi; nourishes Blood; calms the spirit; moderates harsh herbs.",
        "indications": "Fatigue, poor appetite, irritability, palpitations, insomnia. Common harmonising herb.",
    },
]

CATEGORIES = sorted(set(h["category"] for h in HERBS))
TEMPERATURES = ["Warm", "Hot", "Cool", "Cold", "Neutral"]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-title">🌿 Filters</p>', unsafe_allow_html=True)
    search_query = st.text_input("Search herbs", placeholder="Name, indication, property…")
    selected_categories = st.multiselect("Category", options=CATEGORIES, default=[], placeholder="All categories")
    selected_temps = st.multiselect("Temperature", options=TEMPERATURES, default=[], placeholder="All temperatures")
    st.markdown("---")
    st.caption("For educational reference only — not medical advice.")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>🌿 TCM Herb Reference</h1>
    <p>Traditional Chinese Medicine — Materia Medica</p>
</div>
""", unsafe_allow_html=True)

# ── Filter logic ──────────────────────────────────────────────────────────────
def matches(herb):
    q = search_query.strip().lower()
    if q:
        blob = " ".join([
            herb["name"], herb["pinyin"], herb["category"],
            herb["properties"], herb["indications"],
            " ".join(herb["meridians"]), " ".join(herb["taste"]),
        ]).lower()
        if q not in blob:
            return False
    if selected_categories and herb["category"] not in selected_categories:
        return False
    if selected_temps and herb["temperature"] not in selected_temps:
        return False
    return True

filtered = [h for h in HERBS if matches(h)]

st.markdown(f"""
<div class="stats-row">
    <span class="stat-chip">📦 {len(HERBS)} total herbs</span>
    <span class="stat-chip">🔍 {len(filtered)} shown</span>
</div>
""", unsafe_allow_html=True)

# ── Cards ─────────────────────────────────────────────────────────────────────
if not filtered:
    st.markdown('<div class="no-results">No herbs match your search. Try different terms.</div>', unsafe_allow_html=True)
else:
    col1, col2 = st.columns(2, gap="medium")
    for i, herb in enumerate(filtered):
        col = col1 if i % 2 == 0 else col2
        temp_cls = herb["temperature"].lower()
        taste_tags    = "".join(f'<span class="tag">{t}</span>' for t in herb["taste"])
        meridian_tags = "".join(f'<span class="tag">{m}</span>' for m in herb["meridians"])
        with col:
            st.markdown(f"""
            <div class="herb-card">
                <div class="herb-name">{herb['name']}</div>
                <div class="herb-pinyin">{herb['pinyin']} &nbsp;·&nbsp; {herb['category']}</div>
                <div class="section-label">Temperature &amp; Taste</div>
                <span class="tag {temp_cls}">{herb['temperature']}</span>{taste_tags}
                <div class="section-label">Meridians</div>
                {meridian_tags}
                <div class="section-label">Properties</div>
                <div class="indication-text">{herb['properties']}</div>
                <div class="section-label">Indications</div>
                <div class="indication-text">{herb['indications']}</div>
            </div>
            """, unsafe_allow_html=True)