# DCP Knowledge Chatbot — Design Spec
**Date:** 2026-10-15
**Author:** Vinod Patil (DCP SRE)
**Status:** Approved for implementation

---

## 1. Overview

A knowledge-driven chatbot embedded in the DCP Request Hub portal as a floating chat bubble. Powered by AWS Bedrock (Claude Sonnet). Enables DCP SRE team members to ask questions about onboarding, CRQ processes, incidents, SOPs, and contacts — and get instant answers grounded in team-maintained knowledge.

**Goal:** Reduce repetitive queries to the SRE team, onboard new members faster, and provide a single source of truth for DCP knowledge — accessible from anywhere via the portal.

---

## 2. Architecture

```
Streamlit Cloud (dcp-hub-portal)
│
├── app.py                  ← portal + chat engine + admin panel
├── knowledge_base.json     ← DCP knowledge entries (git versioned)
├── analytics.json          ← anonymous question category counters
├── feedback.json           ← thumbs-down questions (knowledge gaps)
└── .streamlit/
    └── secrets.toml        ← AWS creds + admin password (NOT in git)
        AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY
        AWS_REGION
        ADMIN_PASSWORD
        APP_PASSWORD
```

**Flow:**
```
User types question
      ↓
Keyword/tag search → top 3 matching knowledge entries
      ↓
Prompt built: [system instructions] + [knowledge context] + [user question]
      ↓
AWS Bedrock → Claude Sonnet (claude-sonnet-4-6)
      ↓
Answer streamed back to chat bubble
      ↓
User rates response 👍 👎
```

**Constraint:** All AI inference stays within AWS Bedrock — no external API calls, no data leaving the enterprise boundary.

---

## 3. Knowledge Base

**File:** `knowledge_base.json`

**Schema:**
```json
[
  {
    "id": "kb-001",
    "category": "Onboarding",
    "title": "How to onboard a new application to DCP",
    "content": "Full text of the answer...",
    "tags": ["onboard", "app", "DCP", "new"],
    "added_by": "Vinod",
    "updated_at": "2026-10-15"
  }
]
```

**Categories:** `Onboarding`, `CRQ`, `Incident`, `Contacts`, `SOP`, `General`

**Retrieval logic:** Keyword match against `title` + `content` + `tags`. Top 3 scoring entries passed as context to Bedrock. If no entries match with sufficient score, bot responds with: *"I don't have information on that yet. Please contact the DCP SRE team."* — no hallucination outside the knowledge base.

---

## 4. Chat Bubble UI

- **Trigger:** Floating button, bottom-right corner, Mastercard red/orange branded, always on top (z-index above portal content)
- **Open state:** Chat panel slides up, 380px wide, showing conversation history
- **Starter suggestions:** On first open, show 3 suggested questions pulled from the most common analytics categories
- **Thinking state:** Animated "Thinking..." indicator while awaiting Bedrock response
- **Feedback:** Each bot response shows 👍 👎 — thumbs up increments analytics counter, thumbs down logs the question to `feedback.json`
- **Session scope:** Chat history lives in `st.session_state` — clears on page refresh, no persistence, no PII stored

---

## 5. Admin Panel

**Access:** Separate admin password (`ADMIN_PASSWORD` in secrets). Admin panel is a hidden section — not visible in the normal portal nav.

**Features:**
| Feature | Description |
|---|---|
| View knowledge base | Full table of all entries with search/filter |
| Add entry | Form: title, category, content, tags |
| Edit entry | Inline edit of any field |
| Delete entry | Soft confirmation before delete |
| Feedback log | Table of thumbs-down questions — used to identify knowledge gaps |
| Analytics dashboard | Bar chart of question categories by volume |

---

## 6. Analytics

**File:** `analytics.json`

**Schema:**
```json
{
  "Onboarding": 42,
  "CRQ": 28,
  "Incident": 18,
  "Contacts": 7,
  "SOP": 3,
  "General": 12
}
```

- Incremented server-side on each chat message (category inferred from matched knowledge entry)
- No user identity stored — fully anonymous
- Visible only to admin in the admin panel as a bar chart

---

## 7. Security

| Layer | Control |
|---|---|
| Portal access | `APP_PASSWORD` in Streamlit secrets |
| Admin access | `ADMIN_PASSWORD` in Streamlit secrets (separate, stronger) |
| AWS Bedrock credentials | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` in Streamlit secrets only — never in GitHub |
| Knowledge base | Stored in GitHub (suitable for internal SOPs — no secrets, no PII) |
| Chat history | Session-only (`st.session_state`) — never persisted |
| Feedback/analytics | Anonymous — no user identity captured |

---

## 8. Git Workflow

- All implementation on branch: **`feature/dcp-chatbot`**
- **No direct commits to `main`**
- PR raised for review → Vinod tests on Streamlit Cloud preview → merge to `main` only after approval

---

## 9. Dependencies

| Package | Purpose |
|---|---|
| `boto3` | AWS Bedrock API calls |
| `streamlit` | Portal framework (already present) |

No additional packages required.

---

## 10. Out of Scope

- Voice input/output
- Multi-language support
- Integration with Remedy/Jira/ServiceNow (future phase)
- User login/identity tracking
- Email notifications
