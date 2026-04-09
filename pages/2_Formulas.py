import streamlit as st
import re
import os

st.set_page_config(page_title='TCM Formula Reference', page_icon='⚗️', layout='wide')

st.markdown('\n<style>\n    @import url(\'https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Source+Sans+3:wght@300;400;600&display=swap\');\n    html, body, [class*="css"] { font-family: \'Source Sans 3\', sans-serif; }\n    h1, h2, h3 { font-family: \'Lora\', serif; }\n    .app-header { background: linear-gradient(135deg, #3a2d52 0%, #6b4f8c 100%);\n        padding: 2rem 2.5rem; border-radius: 12px; margin-bottom: 2rem; color: white; }\n    .app-header h1 { color: white; margin: 0; font-size: 2rem; }\n    .app-header p  { color: #cbbfe0; margin: 0.25rem 0 0; font-size: 1rem; }\n    .stats-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }\n    .stat-chip { background: #f3f0f8; border: 1px solid #d4c8e8; border-radius: 20px;\n        padding: 0.3rem 0.85rem; font-size: 0.85rem; color: #3a2d52; font-weight: 600; }\n    .formula-card { background: white; border: 1px solid #e4dff0; border-radius: 10px;\n        padding: 1.25rem 1.5rem; margin-bottom: 1rem;\n        box-shadow: 0 1px 4px rgba(0,0,0,0.05); transition: box-shadow 0.2s; }\n    .formula-card:hover { box-shadow: 0 4px 14px rgba(58,45,82,0.12); }\n    .formula-name { font-family: \'Lora\', serif; font-size: 1.15rem; font-weight: 600;\n        color: #1e1429; margin-bottom: 0.1rem; }\n    .formula-english { font-size: 0.9rem; color: #9b89b8; margin-bottom: 0.1rem; }\n    .formula-meta { font-size: 0.82rem; color: #a09cb8; font-style: italic; margin-bottom: 0.6rem; }\n    .section-label { font-size: 0.72rem; font-weight: 600; letter-spacing: 0.08em;\n        text-transform: uppercase; color: #6b4f8c; margin-bottom: 0.3rem; margin-top: 0.65rem; }\n    .body-text { font-size: 0.9rem; color: #334; line-height: 1.55; }\n    .category-badge { display: inline-block; background: #f3f0f8; border: 1px solid #c8bce0;\n        border-radius: 4px; padding: 0.12rem 0.5rem; font-size: 0.77rem;\n        color: #4a3a6a; font-weight: 600; margin-bottom: 0.5rem; }\n    .ing-grid { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.2rem; }\n    .ing-tag { display: inline-flex; align-items: center; gap: 0.3rem;\n        border-radius: 5px; padding: 0.2rem 0.55rem; font-size: 0.8rem; font-style: italic; }\n    .ing-monarch   { background:#fff0e8; border:1px solid #f5c09a; color:#7a3500; }\n    .ing-minister  { background:#f0f4ff; border:1px solid #a0b4f5; color:#1a2e7a; }\n    .ing-assistant { background:#f0fff4; border:1px solid #8fd4a8; color:#0a4a22; }\n    .ing-envoy     { background:#fdf0ff; border:1px solid #d4a8e8; color:#4a0a6a; }\n    .ing-ingredient{ background:#f5f5f5; border:1px solid #ccc;    color:#444; }\n    .role-dot { display:inline-block; width:7px; height:7px;\n        border-radius:50%; flex-shrink:0; margin-top:1px; }\n    .dot-monarch   { background:#e07030; }\n    .dot-minister  { background:#3060d0; }\n    .dot-assistant { background:#30a060; }\n    .dot-envoy     { background:#9030c0; }\n    .dot-ingredient{ background:#999; }\n    .caution-box { background:#fff8e8; border-left:3px solid #e8b44a;\n        padding:0.5rem 0.75rem; border-radius:0 6px 6px 0;\n        font-size:0.85rem; color:#5a4010; margin-top:0.3rem; line-height:1.5; }\n    .no-results { text-align:center; padding:3rem; color:#888; font-style:italic; }\n    .sidebar-title { font-family:\'Lora\',serif; font-weight:600; color:#3a2d52; }\n</style>\n', unsafe_allow_html=True)

CHAPTER_MAP = [
    (1223, 'Release the Exterior'),
    (2391, 'Drain Downward'),
    (3272, 'Harmonize'),
    (4282, 'Clear Heat'),
    (6574, 'Resolve Summer Heat'),
    (7157, 'Warm the Interior'),
    (8209, 'Tonify & Reinforce'),
    (10312, 'Secure & Astringe'),
    (11923, 'Open the Orifices'),
    (12645, 'Regulate Qi'),
    (14141, 'Regulate Blood'),
    (15985, 'Dispel or Stop Wind'),
    (17264, 'Treat Dryness'),
    (18154, 'Resolve Dampness'),
    (20634, 'Resolve Phlegm'),
    (21943, 'Promote Digestion'),
    (22630, 'Kill Parasites & Worms'),
    (22801, 'Induce Emesis'),
    (22960, 'Treat Sores & Abscesses'),
]


def get_category(lineno):
    cat = 'General'
    for start, name in CHAPTER_MAP:
        if lineno >= start: cat = name
        else: break
    return cat


# Single backslash character — used to build tag search strings safely
_BS = chr(92)
_INGR_TAG  = _BS + '[Ingredients'  + _BS + ']'
_END_TAGS  = [_BS+'[Explanations', _BS+'[Method', _BS+'[Functions', _BS+'[Actions']
_FUNC_TAG  = _BS + '[Functions'    + _BS + ']'
_IND_TAG   = _BS + '[Indications'  + _BS + ']'
_CAUT_KW   = 'Cautions & contraindications:'
_OPEN      = _BS + '['


def _clean(text):
    text = re.sub(r'[\\]+', '', text)
    text = re.sub(r'[\[\]]', '', text)
    text = re.sub(r'[*]+', '', text)
    text = re.sub(r'\{[^}]+\}', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def _grab_field(section_text, tag_str):
    """Return text after tag_str up to the next \\[tag or end."""
    idx = section_text.find(tag_str)
    if idx < 0:
        return ''
    start = idx + len(tag_str)
    # skip ** or * and spaces after the tag
    while start < len(section_text) and section_text[start] in '* ':
        start += 1
    # find next opening tag
    next_idx = section_text.find(_OPEN, start)
    chunk = section_text[start: next_idx if next_idx > start else start + 600]
    chunk = re.sub(r'\s*\n\s*', ' ', chunk).strip()
    return _clean(chunk)


def _cautions(section_text):
    idx = section_text.find(_CAUT_KW)
    if idx < 0:
        return ''
    start = idx + len(_CAUT_KW)
    while start < len(section_text) and section_text[start] == ' ':
        start += 1
    next_idx = section_text.find(_OPEN, start)
    # also stop at next bold formula header
    m = re.search(r'[*]{2,3}[A-Z]', section_text[start:start+600])
    if m:
        alt = start + m.start()
        next_idx = min(next_idx, alt) if next_idx > start else alt
    chunk = section_text[start: next_idx if next_idx > start else start + 400]
    chunk = re.sub(r'\s*\n\s*', ' ', chunk).strip()
    return _clean(chunk)


def _parse_ingredients(section_lines):
    role_map = {'monarch':'Monarch','minister':'Minister',
                'assistant':'Assistant','envoy':'Envoy'}
    start = end = None
    for i, l in enumerate(section_lines):
        if _INGR_TAG in l:
            start = i
        if start is not None and end is None and i > start:
            if any(t in l for t in _END_TAGS):
                end = i
                break
    if start is None:
        return []
    block = section_lines[start: end or start + 50]
    table_rows = [l for l in block if '|' in l and not l.startswith('+')]
    if not table_rows:
        return []
    groups, current = [], []
    for row in table_rows:
        cells = [c.strip() for c in row.split('|')]
        first = next((c for c in cells[1:3] if c.strip()), '')
        fc = re.sub('[^a-z]', '', first.lower())
        is_start = any(kw.startswith(fc) and len(fc) >= 2 for kw in role_map)
        if is_start or not current:
            if current:
                groups.append(current)
            current = [row]
        else:
            current.append(row)
    if current:
        groups.append(current)
    herbs = []
    for group in groups:
        parsed = [[c.strip() for c in r.split('|')] for r in group]
        max_cols = max(len(r) for r in parsed)
        merged = [
            ' '.join(r[col] if col < len(r) else '' for r in parsed).strip()
            for col in range(max_cols)
        ]
        role = None
        for c in merged[1:3]:
            fc = re.sub('[^a-z]', '', c.lower())
            for kw, r in role_map.items():
                if kw.startswith(fc) and len(fc) >= 2:
                    role = r
                    break
            if role:
                break
        for p in re.findall(r'[*](.+?)[*]', ' '.join(merged)):
            p = p.strip()
            if p and 1 <= len(p.split()) <= 5 and len(p) < 40:
                herbs.append({'name': p, 'role': role or 'Ingredient'})
    return herbs


SKIP_WORDS = [
    'chapter', 'review question', 'table ', 'annex formula',
    'envoy:', 'minister:', 'monarch:', 'assistant:',
    'general introduction', 'treatment method', 'formula and',
    'basic structure', 'variation', 'dosage form', 'preparation method',
    'administration', 'appendix', 'textual research',
    'synergetic', 'extension of', 'alleviation',
    'explanations of the formula',
    '1.1 ', '1.2 ', '1.3 ', '2.1 ', '2.2 ', '2.3 ',
    'pungent and warm', 'pungent and cold', 'release the exterior with',
    'formulas that ', 'typical formula',
]
TCM_SUFFIXES = ['tang','san','wan','yin','jian','dan','ye','gao','yin zi','pian','lu','ji']


def _find_headers(lines):
    N = len(lines)
    positions = []
    i = 0
    while i < N:
        line = lines[i].rstrip()
        combined = None
        if (re.match(r'^[*]{2,3}[A-Z]', line) and
                not re.search(r'[*]{1,3}\s*$', line) and i + 1 < N):
            nxt = lines[i + 1].rstrip()
            if re.search(r'[*]{1,3}\s*$', nxt):
                combined = line + ' ' + nxt.strip()
        for candidate in ([combined] if combined else []) + [line]:
            if not candidate:
                continue
            m = re.match(r'^[*]{2,3}(.+?)[*]{1,3}\s*$', candidate)
            if not m:
                continue
            raw = m.group(1)
            if any(s in raw.lower() for s in SKIP_WORDS):
                continue
            stripped = re.sub(r'[*]|\([^)]*\)', '', raw).strip().lower()
            words = stripped.split()
            if (any(stripped.endswith(s) for s in TCM_SUFFIXES) or
                    (len(words) >= 3 and
                     words[-1] not in {'formula','decoction','pill','powder','method'})):
                positions.append((i + 1, raw))
                break
        i += 1
    return positions


@st.cache_data
def load_formulas():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(script_dir, '..', 'formulas.md')
    with open(md_path, encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    N = len(lines)
    positions = _find_headers(lines)
    formulas = []
    seen = set()
    for idx, (lineno, raw_name) in enumerate(positions):
        next_lineno = positions[idx + 1][0] if idx + 1 < len(positions) else N
        end = min(lineno + 300, next_lineno)
        section_lines = lines[lineno - 1: end]
        section_text = '\n'.join(section_lines)
        pinyin = re.sub(r'\([^)]*\)', '', raw_name)
        pinyin = re.sub(r'[*]+', '', pinyin).strip().strip('., ')
        eng_m = re.search(r'\(([^*()]{4,60})\)', raw_name)
        english = eng_m.group(1).strip() if eng_m else ''
        category = get_category(lineno)
        source = ''
        bs_ = chr(92)
        for sl in section_lines[1:6]:
            sl = sl.strip()
            if (sl.startswith('*') and not sl.startswith('**')
                    and len(sl) < 150 and bs_+'[' not in sl):
                source = _clean(sl)
                break
        ingredients = _parse_ingredients(section_lines)
        functions   = _grab_field(section_text, _FUNC_TAG)
        indications = _grab_field(section_text, _IND_TAG)
        cautions    = _cautions(section_text)
        if pinyin and len(pinyin) > 2 and (functions or indications) and pinyin not in seen:
            seen.add(pinyin)
            formulas.append({
                'name': pinyin, 'english': english, 'source': source,
                'category': category, 'ingredients': ingredients,
                'functions': functions, 'indications': indications,
                'cautions': cautions,
            })
    return formulas


FORMULAS = load_formulas()
ALL_CATS = sorted(set(f['category'] for f in FORMULAS))

with st.sidebar:
    st.markdown('<p class="sidebar-title">⚗️ Filters</p>', unsafe_allow_html=True)
    search_query  = st.text_input('Search formulas', placeholder='Name, herb, indication…')
    selected_cats = st.multiselect('Category', options=ALL_CATS, default=[],
                                   placeholder='All categories')
    st.markdown('---')
    st.markdown('''
**Ingredient roles**  
🟠 **Monarch** — chief therapeutic action  
🔵 **Minister** — supports & strengthens  
🟢 **Assistant** — moderates, aids, or corrects  
🟣 **Envoy** — guides to target organ / harmonises
''')
    st.markdown('---')
    st.caption('For educational reference only — not medical advice.')

st.markdown('''
<div class="app-header">
    <h1>⚗️ TCM Formula Reference</h1>
    <p>Traditional Chinese Medicine — Classical Formulas (方剂学)</p>
</div>
''', unsafe_allow_html=True)


def matches(f):
    q = search_query.strip().lower()
    if q:
        herb_blob = ' '.join(i['name'] for i in f['ingredients']).lower()
        blob = ' '.join([f['name'], f['english'], f['category'],
                         f['functions'], f['indications'], f['source'], herb_blob]).lower()
        if q not in blob:
            return False
    if selected_cats and f['category'] not in selected_cats:
        return False
    return True


filtered = [f for f in FORMULAS if matches(f)]

st.markdown(f'''
<div class="stats-row">
    <span class="stat-chip">📦 {len(FORMULAS)} total formulas</span>
    <span class="stat-chip">🔍 {len(filtered)} shown</span>
    <span class="stat-chip">📚 {len(ALL_CATS)} categories</span>
</div>
''', unsafe_allow_html=True)

ROLE_CSS = {
    'Monarch':    ('ing-monarch',    'dot-monarch'),
    'Minister':   ('ing-minister',   'dot-minister'),
    'Assistant':  ('ing-assistant',  'dot-assistant'),
    'Envoy':      ('ing-envoy',      'dot-envoy'),
    'Ingredient': ('ing-ingredient', 'dot-ingredient'),
}


def ingredient_html(ingredients):
    if not ingredients:
        return '<span style="color:#aaa;font-size:0.85rem;font-style:italic;">—</span>'
    parts = []
    for ing in ingredients:
        role = ing['role']
        name = ing['name']
        css_tag, css_dot = ROLE_CSS.get(role, ROLE_CSS['Ingredient'])
        parts.append(
            f'<span class="ing-tag {css_tag}">'
            f'<span class="role-dot {css_dot}"></span>'
            f'{name}</span>'
        )
    return '<div class="ing-grid">' + ''.join(parts) + '</div>'


if not filtered:
    st.markdown('<div class="no-results">No formulas match your search.</div>',
                unsafe_allow_html=True)
else:
    col1, col2 = st.columns(2, gap='medium')
    for i, f in enumerate(filtered):
        col = col1 if i % 2 == 0 else col2
        name     = f['name']
        english  = f['english']
        source   = f['source']
        category = f['category']
        functions   = f['functions']
        indications = f['indications']
        cautions    = f['cautions']
        eng  = f'<div class="formula-english">{english}</div>' if english else ''
        src  = f'<div class="formula-meta">{source}</div>'     if source  else ''
        caut = (f'<div class="section-label">⚠ Cautions</div>'
                f'<div class="caution-box">{cautions}</div>') if cautions else ''
        ingr_html = ingredient_html(f['ingredients'])
        with col:
            st.markdown(f'''
<div class="formula-card">
  <div class="formula-name">{name}</div>
  {eng}{src}
  <span class="category-badge">{category}</span>
  <div class="section-label">Ingredients</div>
  {ingr_html}
  <div class="section-label">Functions</div>
  <div class="body-text">{functions}</div>
  <div class="section-label">Indications</div>
  <div class="body-text">{indications}</div>
  {caut}
</div>
''', unsafe_allow_html=True)