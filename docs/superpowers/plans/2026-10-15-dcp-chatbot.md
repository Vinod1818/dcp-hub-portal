# DCP Knowledge Chatbot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a floating knowledge chatbot to the DCP Request Hub portal, powered by AWS Bedrock, with a team-editable knowledge base and admin analytics panel.

**Architecture:** Knowledge stored in `knowledge_base.json` (git-versioned). On each chat message, top-3 matching entries retrieved by keyword/tag scoring and passed as context to AWS Bedrock (Claude Sonnet). Chatbot UI is a floating bubble injected via HTML/JS into the existing Streamlit portal. Admin panel (separate password) allows CRUD on knowledge entries and views analytics/feedback.

**Tech Stack:** Python 3.13, Streamlit >=1.32.0, boto3 (AWS Bedrock), JSON file storage

## Global Constraints

- Branch: `feature/dcp-chatbot` — NO commits to `main`
- Streamlit Cloud deployment for preview testing before merge
- AWS Bedrock credentials stored in `.streamlit/secrets.toml` only — never committed to git
- `secrets.toml` is already in `.gitignore` — do not change this
- Admin password key in secrets: `ADMIN_PASSWORD`
- Portal password key in secrets: `APP_PASSWORD`
- AWS keys in secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
- Bedrock model: `anthropic.claude-sonnet-4-5` (available on Bedrock)
- No PII stored anywhere — chat history is session-only
- All new files go in repo root unless specified otherwise

---

## File Structure

```
dcp-hub-portal/
├── app.py                          ← MODIFY: add chatbot bubble + admin panel routing
├── chatbot.py                      ← CREATE: Bedrock call + knowledge retrieval logic
├── admin.py                        ← CREATE: admin panel UI (knowledge CRUD + analytics)
├── knowledge_base.json             ← CREATE: initial seed knowledge entries
├── analytics.json                  ← CREATE: anonymous question category counters
├── feedback.json                   ← CREATE: thumbs-down question log
├── requirements.txt                ← MODIFY: add boto3
└── .streamlit/
    └── secrets.toml                ← MODIFY locally only (never commit): add AWS + admin keys
```

---

### Task 1: Create feature branch and seed data files

**Files:**
- Create: `knowledge_base.json`
- Create: `analytics.json`
- Create: `feedback.json`
- Modify: `requirements.txt`

**Interfaces:**
- Produces: `knowledge_base.json` schema used by Tasks 2, 3, 4
- Produces: `analytics.json` schema used by Tasks 2, 4
- Produces: `feedback.json` schema used by Tasks 2, 4

- [ ] **Step 1: Create feature branch**

```bash
cd "C:/Users/e142143/dcp-hub-portal"
git checkout -b feature/dcp-chatbot
```

Expected: `Switched to a new branch 'feature/dcp-chatbot'`

- [ ] **Step 2: Create `knowledge_base.json` with seed entries**

```json
[
  {
    "id": "kb-001",
    "category": "Onboarding",
    "title": "How to onboard a new application to DCP",
    "content": "To onboard a new application to DCP: 1) Raise a DCP onboarding ticket in ServiceNow with app name, owner, and environment. 2) DCP SRE team reviews and assigns a port range. 3) Submit firewall rules request. 4) Configure app to use DCP proxy settings. 5) Validate connectivity via DCP health check endpoint. Contact DCP SRE team for assistance.",
    "tags": ["onboard", "app", "new", "DCP", "port", "firewall"],
    "added_by": "Vinod",
    "updated_at": "2026-10-15"
  },
  {
    "id": "kb-002",
    "category": "CRQ",
    "title": "What approvals does a CRQ need",
    "content": "A standard DCP CRQ requires: 1) Team lead approval. 2) Change Advisory Board (CAB) approval for major changes. 3) DCP SRE sign-off for infra changes. 4) Security review for any network or IAM changes. Minor CRQs (low risk) only need team lead approval. Submit CRQ at least 5 business days before planned change window.",
    "tags": ["CRQ", "approval", "CAB", "change", "sign-off"],
    "added_by": "Vinod",
    "updated_at": "2026-10-15"
  },
  {
    "id": "kb-003",
    "category": "Incident",
    "title": "DCP incident response procedure",
    "content": "DCP incident response: 1) Raise P1/P2 alert in Remedy immediately. 2) Page DCP SRE on-call via PagerDuty. 3) Create war room bridge. 4) Update Dynatrace incident ticket every 30 mins. 5) Post RCA within 48 hours of resolution. P1 = full outage, P2 = degraded service, P3 = minor issue.",
    "tags": ["incident", "P1", "P2", "response", "Remedy", "PagerDuty", "RCA"],
    "added_by": "Vinod",
    "updated_at": "2026-10-15"
  },
  {
    "id": "kb-004",
    "category": "Contacts",
    "title": "DCP SRE team contacts and on-call",
    "content": "DCP SRE Team Lead: Vinod Patil. On-call rotation: Check PagerDuty schedule for current on-call engineer. For urgent issues: page via PagerDuty. For non-urgent: raise ticket in ServiceNow DCP queue. Team channel: MS Teams - DCP SRE.",
    "tags": ["contact", "on-call", "team", "lead", "PagerDuty", "Teams"],
    "added_by": "Vinod",
    "updated_at": "2026-10-15"
  },
  {
    "id": "kb-005",
    "category": "SOP",
    "title": "DCP patching SOP",
    "content": "DCP patching follows a rolling update strategy: 1) Raise CRQ 5 days before patch window. 2) Patch non-prod first (DEV → STG → PROD). 3) Health check after each environment. 4) Rollback plan must be in CRQ. 5) Maintenance window: Sundays 2-6 AM IST. Emergency patches follow P1 incident process.",
    "tags": ["patch", "patching", "SOP", "maintenance", "window", "rollback"],
    "added_by": "Vinod",
    "updated_at": "2026-10-15"
  }
]
```

- [ ] **Step 3: Create `analytics.json`**

```json
{
  "Onboarding": 0,
  "CRQ": 0,
  "Incident": 0,
  "Contacts": 0,
  "SOP": 0,
  "General": 0
}
```

- [ ] **Step 4: Create `feedback.json`**

```json
[]
```

- [ ] **Step 5: Add boto3 to requirements.txt**

Replace contents of `requirements.txt` with:
```
streamlit>=1.32.0
boto3>=1.34.0
```

- [ ] **Step 6: Update secrets.toml locally with new keys**

Add to `.streamlit/secrets.toml` (do NOT commit this file):
```toml
APP_PASSWORD = "dcp-sre-2024"
ADMIN_PASSWORD = "dcp-admin-2024"
AWS_ACCESS_KEY_ID = "your-key-here"
AWS_SECRET_ACCESS_KEY = "your-secret-here"
AWS_REGION = "us-east-1"
```

- [ ] **Step 7: Commit seed files**

```bash
git add knowledge_base.json analytics.json feedback.json requirements.txt
git commit -m "feat: add knowledge base seed data and analytics/feedback stores"
```

---

### Task 2: Build knowledge retrieval and Bedrock chat engine

**Files:**
- Create: `chatbot.py`

**Interfaces:**
- Consumes: `knowledge_base.json` (list of objects with keys: `id`, `category`, `title`, `content`, `tags`)
- Consumes: `analytics.json`, `feedback.json`
- Produces:
  - `search_knowledge(query: str) -> list[dict]` — returns top-3 matching entries
  - `ask_bedrock(question: str, context_entries: list[dict]) -> str` — returns answer string
  - `record_analytics(category: str) -> None`
  - `record_feedback(question: str) -> None`
  - `SUGGESTED_QUESTIONS: list[str]` — 3 starter question strings

- [ ] **Step 1: Create `chatbot.py`**

```python
import json
import re
import boto3
import streamlit as st

SUGGESTED_QUESTIONS = [
    "How do I onboard a new app to DCP?",
    "What approvals does a CRQ need?",
    "Who is the DCP SRE on-call?",
]

KB_FILE = "knowledge_base.json"
ANALYTICS_FILE = "analytics.json"
FEEDBACK_FILE = "feedback.json"


def load_knowledge() -> list[dict]:
    try:
        with open(KB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def search_knowledge(query: str) -> list[dict]:
    """Return top-3 knowledge entries most relevant to query."""
    entries = load_knowledge()
    query_words = set(re.findall(r"\w+", query.lower()))
    scored = []
    for entry in entries:
        searchable = " ".join([
            entry.get("title", ""),
            entry.get("content", ""),
            " ".join(entry.get("tags", []))
        ]).lower()
        entry_words = set(re.findall(r"\w+", searchable))
        score = len(query_words & entry_words)
        if score > 0:
            scored.append((score, entry))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [entry for _, entry in scored[:3]]


def ask_bedrock(question: str, context_entries: list[dict]) -> str:
    """Send question + context to AWS Bedrock and return answer."""
    if not context_entries:
        return "I don't have information on that yet. Please contact the DCP SRE team directly via MS Teams - DCP SRE channel."

    context_text = "\n\n".join([
        f"**{e['title']}**\n{e['content']}"
        for e in context_entries
    ])

    system_prompt = (
        "You are the DCP SRE knowledge assistant. "
        "Answer questions using ONLY the knowledge provided below. "
        "Be concise and clear. If the answer is not in the knowledge provided, "
        "say: 'I don't have information on that yet. Please contact the DCP SRE team.' "
        "Do not make up information.\n\n"
        f"Knowledge Base:\n{context_text}"
    )

    try:
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name=st.secrets["AWS_REGION"],
            aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
        )
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "system": system_prompt,
            "messages": [{"role": "user", "content": question}],
        })
        response = client.invoke_model(
            modelId="anthropic.claude-sonnet-4-5",
            body=body,
            contentType="application/json",
            accept="application/json",
        )
        result = json.loads(response["body"].read())
        return result["content"][0]["text"]
    except Exception as e:
        return f"Unable to reach AI service. Please contact DCP SRE team. (Error: {str(e)})"


def record_analytics(category: str) -> None:
    """Increment category counter in analytics.json."""
    try:
        with open(ANALYTICS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data[category] = data.get(category, 0) + 1
        with open(ANALYTICS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def record_feedback(question: str) -> None:
    """Append thumbs-down question to feedback.json."""
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.append({"question": question, "logged_at": str(__import__("datetime").date.today())})
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass
```

- [ ] **Step 2: Verify imports work**

```bash
cd "C:/Users/e142143/dcp-hub-portal"
python -c "from chatbot import search_knowledge, ask_bedrock, SUGGESTED_QUESTIONS; print('OK')"
```

Expected output: `OK`

- [ ] **Step 3: Quick smoke test of search_knowledge**

```bash
python -c "
from chatbot import search_knowledge
results = search_knowledge('how to onboard app')
print(len(results), 'results')
print(results[0]['title'])
"
```

Expected: `1 results` (or more) and title containing "onboard"

- [ ] **Step 4: Commit**

```bash
git add chatbot.py
git commit -m "feat: add knowledge retrieval and Bedrock chat engine"
```

---

### Task 3: Build admin panel

**Files:**
- Create: `admin.py`

**Interfaces:**
- Consumes: `load_knowledge()` from `chatbot.py`
- Consumes: `knowledge_base.json`, `analytics.json`, `feedback.json` directly
- Produces: `render_admin_panel() -> None` — called from `app.py` when admin is authenticated

- [ ] **Step 1: Create `admin.py`**

```python
import json
import uuid
import streamlit as st
from datetime import date

KB_FILE = "knowledge_base.json"
ANALYTICS_FILE = "analytics.json"
FEEDBACK_FILE = "feedback.json"
CATEGORIES = ["Onboarding", "CRQ", "Incident", "Contacts", "SOP", "General"]


def _load(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return [] if path != ANALYTICS_FILE else {}


def _save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def render_admin_panel():
    st.markdown("## Admin Panel")
    tab1, tab2, tab3 = st.tabs(["Knowledge Base", "Feedback Log", "Analytics"])

    # ── Tab 1: Knowledge Base CRUD ──
    with tab1:
        entries = _load(KB_FILE)

        with st.expander("Add New Entry", expanded=False):
            with st.form("add_entry"):
                title = st.text_input("Title")
                category = st.selectbox("Category", CATEGORIES)
                content = st.text_area("Content", height=150)
                tags = st.text_input("Tags (comma separated)")
                submitted = st.form_submit_button("Add Entry")
                if submitted and title and content:
                    new_entry = {
                        "id": f"kb-{uuid.uuid4().hex[:6]}",
                        "category": category,
                        "title": title,
                        "content": content,
                        "tags": [t.strip() for t in tags.split(",") if t.strip()],
                        "added_by": "Admin",
                        "updated_at": str(date.today()),
                    }
                    entries.append(new_entry)
                    _save(KB_FILE, entries)
                    st.success("Entry added.")
                    st.rerun()

        st.markdown(f"**{len(entries)} entries in knowledge base**")
        for i, entry in enumerate(entries):
            with st.expander(f"[{entry['category']}] {entry['title']}", expanded=False):
                with st.form(f"edit_{entry['id']}"):
                    new_title = st.text_input("Title", value=entry["title"])
                    new_cat = st.selectbox("Category", CATEGORIES, index=CATEGORIES.index(entry["category"]))
                    new_content = st.text_area("Content", value=entry["content"], height=120)
                    new_tags = st.text_input("Tags", value=", ".join(entry.get("tags", [])))
                    col1, col2 = st.columns(2)
                    save = col1.form_submit_button("Save Changes")
                    delete = col2.form_submit_button("Delete", type="secondary")
                    if save:
                        entries[i].update({
                            "title": new_title,
                            "category": new_cat,
                            "content": new_content,
                            "tags": [t.strip() for t in new_tags.split(",") if t.strip()],
                            "updated_at": str(date.today()),
                        })
                        _save(KB_FILE, entries)
                        st.success("Saved.")
                        st.rerun()
                    if delete:
                        entries.pop(i)
                        _save(KB_FILE, entries)
                        st.warning("Deleted.")
                        st.rerun()

    # ── Tab 2: Feedback Log ──
    with tab2:
        feedback = _load(FEEDBACK_FILE)
        if not feedback:
            st.info("No feedback logged yet.")
        else:
            st.markdown(f"**{len(feedback)} unanswered questions logged**")
            for item in reversed(feedback):
                st.markdown(f"- `{item['logged_at']}` — {item['question']}")

    # ── Tab 3: Analytics ──
    with tab3:
        analytics = _load(ANALYTICS_FILE)
        if not any(analytics.values()):
            st.info("No questions asked yet.")
        else:
            st.markdown("**Questions by category**")
            st.bar_chart(analytics)
```

- [ ] **Step 2: Verify import**

```bash
python -c "from admin import render_admin_panel; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add admin.py
git commit -m "feat: add admin panel with knowledge CRUD, feedback log, analytics"
```

---

### Task 4: Integrate chatbot bubble and admin panel into app.py

**Files:**
- Modify: `app.py`

**Interfaces:**
- Consumes: `ask_bedrock(question, context_entries)` from `chatbot.py`
- Consumes: `search_knowledge(query)` from `chatbot.py`
- Consumes: `record_analytics(category)` from `chatbot.py`
- Consumes: `record_feedback(question)` from `chatbot.py`
- Consumes: `SUGGESTED_QUESTIONS` from `chatbot.py`
- Consumes: `render_admin_panel()` from `admin.py`

- [ ] **Step 1: Add admin auth check function to app.py**

Add these imports at the top of `app.py` after existing imports:

```python
from chatbot import search_knowledge, ask_bedrock, record_analytics, record_feedback, SUGGESTED_QUESTIONS
from admin import render_admin_panel
```

- [ ] **Step 2: Add admin password check function to app.py**

Add this function after the `check_password()` function and before `if not check_password():`:

```python
def check_admin():
    if st.session_state.get("is_admin"):
        return True
    with st.sidebar:
        st.markdown("### Admin Access")
        with st.form("admin_login"):
            pwd = st.text_input("Admin password", type="password")
            submitted = st.form_submit_button("Login as Admin")
            if submitted:
                if hmac.compare_digest(pwd, st.secrets["ADMIN_PASSWORD"]):
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("Incorrect admin password.")
    return False
```

- [ ] **Step 3: Add admin panel route**

Add this block immediately after `if not check_password(): st.stop()`:

```python
# ===== ADMIN PANEL ROUTE =====
query_params = st.query_params
if query_params.get("admin") == "true":
    if check_admin():
        render_admin_panel()
    st.stop()
```

- [ ] **Step 4: Add chat state initialization**

Add this block after the admin panel route (before the hide CSS block):

```python
# ===== CHAT STATE =====
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None
```

- [ ] **Step 5: Add chat processing logic**

Add this block after chat state initialization:

```python
# ===== PROCESS CHAT MESSAGE =====
if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None
    with st.spinner(""):
        context = search_knowledge(question)
        answer = ask_bedrock(question, context)
        category = context[0]["category"] if context else "General"
        record_analytics(category)
    st.session_state.chat_history.append({
        "question": question,
        "answer": answer,
        "rated": None
    })
    st.rerun()
```

- [ ] **Step 6: Add feedback handler**

Add this block after the chat processing logic:

```python
# ===== PROCESS FEEDBACK =====
if "rate_down" in st.session_state and st.session_state.rate_down is not None:
    idx = st.session_state.rate_down
    if idx < len(st.session_state.chat_history):
        record_feedback(st.session_state.chat_history[idx]["question"])
        st.session_state.chat_history[idx]["rated"] = "down"
    st.session_state.rate_down = None
```

- [ ] **Step 7: Add floating chat bubble UI**

Add this block at the very end of `app.py`, after `st.iframe(build_portal(), height=950)`:

```python
# ===== FLOATING CHAT BUBBLE =====
st.markdown("---")
with st.container():
    # Toggle button
    col_spacer, col_btn = st.columns([6, 1])
    with col_btn:
        if st.button("💬 Ask DCP", key="chat_toggle", use_container_width=True):
            st.session_state.chat_open = not st.session_state.chat_open
            st.rerun()

if st.session_state.chat_open:
    st.markdown("""
    <style>
    .chat-panel {
        position: fixed; bottom: 80px; right: 24px; z-index: 99990;
        width: 370px; max-height: 520px;
        background: #fff; border-radius: 16px;
        box-shadow: 0 8px 40px rgba(0,0,0,0.18);
        display: flex; flex-direction: column;
        border: 1.5px solid #e2e8f0; overflow: hidden;
    }
    .chat-header {
        background: linear-gradient(135deg,#EB001B,#FF5F00);
        color: #fff; padding: 14px 18px;
        font-weight: 800; font-size: 15px;
        display: flex; align-items: center; gap: 8px;
    }
    .chat-messages {
        flex: 1; overflow-y: auto; padding: 14px;
        display: flex; flex-direction: column; gap: 10px;
        max-height: 320px;
    }
    .msg-user { background:#eff6ff; border-radius:10px; padding:8px 12px; align-self:flex-end; max-width:85%; font-size:13px; }
    .msg-bot { background:#f8fafc; border-radius:10px; padding:8px 12px; align-self:flex-start; max-width:90%; font-size:13px; border:1px solid #e2e8f0; }
    </style>
    <div class="chat-panel">
        <div class="chat-header">💬 Ask DCP &nbsp;<span style="font-weight:400;font-size:12px;opacity:.8;">DCP SRE Knowledge Bot</span></div>
        <div class="chat-messages" id="chat-messages">
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Suggested questions (show only if no history)
    if not st.session_state.chat_history:
        st.markdown("**Try asking:**")
        for q in SUGGESTED_QUESTIONS:
            if st.button(q, key=f"suggest_{q}"):
                st.session_state.pending_question = q
                st.rerun()

    # Chat history
    for i, msg in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.write(msg["question"])
        with st.chat_message("assistant"):
            st.write(msg["answer"])
            if msg["rated"] is None:
                col1, col2, col3 = st.columns([1, 1, 8])
                with col1:
                    if st.button("👍", key=f"up_{i}"):
                        st.session_state.chat_history[i]["rated"] = "up"
                        st.rerun()
                with col2:
                    if st.button("👎", key=f"down_{i}"):
                        st.session_state.rate_down = i
                        st.rerun()

    # Input box
    user_input = st.chat_input("Ask anything about DCP...")
    if user_input:
        st.session_state.pending_question = user_input
        st.rerun()
```

- [ ] **Step 8: Verify app starts without error**

```bash
cd "C:/Users/e142143/dcp-hub-portal"
python -c "import ast, sys; ast.parse(open('app.py').read()); print('Syntax OK')"
```

Expected: `Syntax OK`

- [ ] **Step 9: Commit**

```bash
git add app.py
git commit -m "feat: integrate floating chat bubble and admin panel into portal"
```

---

### Task 5: Push branch and deploy preview on Streamlit Cloud

**Files:** none (git/deployment operations only)

- [ ] **Step 1: Push feature branch to GitHub**

```bash
cd "C:/Users/e142143/dcp-hub-portal"
git push -u origin feature/dcp-chatbot
```

Expected: branch appears at `https://github.com/Vinod1818/dcp-hub-portal/tree/feature/dcp-chatbot`

- [ ] **Step 2: Deploy preview app on Streamlit Cloud**

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Repository: `Vinod1818/dcp-hub-portal`
4. Branch: `feature/dcp-chatbot`
5. Main file: `app.py`
6. Click **"Advanced settings"** → add secrets:
   ```toml
   APP_PASSWORD = "dcp-sre-2024"
   ADMIN_PASSWORD = "dcp-admin-2024"
   AWS_ACCESS_KEY_ID = "your-key"
   AWS_SECRET_ACCESS_KEY = "your-secret"
   AWS_REGION = "us-east-1"
   ```
7. Click **Deploy**

- [ ] **Step 3: Test portal password gate**

- Open preview URL → verify login screen appears
- Enter wrong password → verify error message
- Enter `dcp-sre-2024` → verify portal loads

- [ ] **Step 4: Test chat bubble**

- Click **💬 Ask DCP** → verify chat panel opens
- Verify 3 suggested questions appear
- Click a suggested question → verify "Thinking..." → verify answer appears
- Click 👍 → verify rating saved
- Type a question → verify answer
- Click 👎 → verify logged (check admin panel)

- [ ] **Step 5: Test admin panel**

- Navigate to `<preview-url>?admin=true`
- Enter admin password → verify admin panel loads
- Add a new knowledge entry → verify it appears in list
- Edit an entry → verify changes saved
- Check Analytics tab → verify question counts incremented
- Check Feedback tab → verify thumbs-down question logged

- [ ] **Step 6: Raise PR to main only after testing passes**

```bash
gh pr create \
  --title "feat: DCP knowledge chatbot with admin panel and AWS Bedrock" \
  --body "$(cat <<'EOF'
## Summary
- Floating Ask DCP chat bubble on all portal pages
- AWS Bedrock (Claude Sonnet) answers grounded in knowledge base only
- Team-editable knowledge base via admin panel (separate password)
- Anonymous analytics + feedback log for knowledge gap tracking
- 3 suggested starter questions on first open

## Test plan
- [ ] Portal password gate works
- [ ] Chat bubble opens/closes
- [ ] Suggested questions work
- [ ] Bedrock answers are grounded in knowledge base
- [ ] Thumbs up/down rating works
- [ ] Admin panel: add/edit/delete knowledge entries
- [ ] Admin panel: analytics bar chart shows question counts
- [ ] Admin panel: feedback log shows thumbs-down questions
- [ ] No Streamlit/GitHub branding visible
- [ ] Tested on WFH (external) network via Streamlit Cloud URL

🤖 Generated with Claude Code
EOF
)"
```

**Do NOT merge until Vinod approves after testing.**
