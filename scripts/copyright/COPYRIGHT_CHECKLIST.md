# Copyright Compliance Checklist
## Quick Reference for Frozen Assets Database

---

## ✅ Current Status: FULLY COMPLIANT

Last Review: November 21, 2025  
Documents Analyzed: 26  
Clearance Rate: 100%

---

## When Adding New Documents

Use this checklist for each new source:

### 1. Source Type Classification

- [ ] **Government/Official** (EU, US, UN, etc.)
  - ✅ Generally public domain or open access
  - ✅ Freely quotable with attribution

- [ ] **International Organization** (World Bank, IMF, etc.)
  - ✅ Usually CC BY license or similar
  - ✅ Check specific organization's reuse policy

- [ ] **Academic/Research** (Universities, think tanks)
  - ✅ Fair use applies for quotation
  - ⚠️ Check for specific license (often CC BY)

- [ ] **News/Media** (Newspapers, news sites)
  - ✅ Quotation allowed under fair use
  - ⚠️ Keep excerpts brief, always attribute

- [ ] **NGO/Advocacy** (Non-profits, advocacy groups)
  - ✅ Usually intended for public sharing
  - ✅ Verify no restrictive copyright notice

- [ ] **Corporate** (Annual reports, public disclosures)
  - ✅ Public reports are quotable
  - ⚠️ Avoid proprietary/confidential materials

---

## 2. Attribution Checklist

For EVERY document, include:

- [ ] **Title** (exact or abbreviated)
- [ ] **Author/Authority** (organization or government body)
- [ ] **Publication Date** (month/year minimum)
- [ ] **URL/Link** (direct link to source)
- [ ] **Description** (your own summary, not copy-paste)

---

## 3. Safe Use Guidelines

✅ **ALWAYS ALLOWED:**
- Linking to documents
- Brief descriptions (1-3 sentences)
- Factual summaries in your own words
- Statistics and data with citation
- Titles and metadata

✅ **ALLOWED WITH CARE:**
- Short quotations (< 250 words)
- Key excerpts for commentary
- Figures/tables with full attribution

❌ **AVOID:**
- Reproducing entire articles
- Copying lengthy passages without quotes
- Using paywalled content beyond fair use
- Removing copyright notices
- Using without attribution

---

## 4. Red Flags to Watch For

⚠️ **Check carefully if you see:**

- "All rights reserved" with no fair use exception
- Paywall or subscription requirement
- "No reproduction without permission"
- Corporate confidential materials
- Personal/private communications

**What to do:** 
- Still usually OK for brief quotation under fair use
- Just ensure you're not reproducing substantial portions
- When in doubt, link with minimal description

---

## 5. Documentation Template

When adding a document, use this format:

```json
{
  "title": "Document Title",
  "authority": "Issuing Organization",
  "type": "Legal|Financial|Political|Expert Opinion|News|Research",
  "date": "YYYY-MM-DD",
  "year": YYYY,
  "link": "https://full-url-to-source.com",
  "short description": "Your 1-2 sentence summary describing the document's main point or contribution"
}
```

---

## 6. Fair Use Four Factors (US)

When evaluating questionable sources, consider:

1. **Purpose & Character**
   - ✅ Educational/informational = favors fair use
   - ✅ Non-commercial = favors fair use
   - ✅ Transformative (database/aggregation) = favors fair use

2. **Nature of Work**
   - ✅ Factual/informational = favors fair use
   - ⚠️ Creative/artistic = less fair use protection

3. **Amount Used**
   - ✅ Brief excerpts = favors fair use
   - ✅ Titles, descriptions, links only = strong fair use
   - ❌ Entire work = against fair use

4. **Market Effect**
   - ✅ No competition with original = favors fair use
   - ✅ Drives traffic to original = favors fair use
   - ❌ Replaces need for original = against fair use

**Your database:** ✅✅✅✅ (Strong fair use on all factors)

---

## 7. EU Fair Dealing (Directive 2001/29/EC)

Quotations allowed for:
- ✅ Criticism and review
- ✅ News reporting  
- ✅ Teaching and research
- ✅ Information and commentary

**Requirements:**
- Source must be lawfully accessible
- Use must be proportionate
- Source must be acknowledged

**Your database:** ✅ Meets all requirements

---

## 8. Quick Decision Tree

```
New Document
    ↓
Is it from a government/official source?
    YES → ✅ Safe to use
    NO  → Continue
    ↓
Is it from a research institution/think tank?
    YES → ✅ Safe to use (cite properly)
    NO  → Continue
    ↓
Is it a news article?
    YES → ✅ Safe to quote briefly
    NO  → Continue
    ↓
Is it publicly available advocacy/educational material?
    YES → ✅ Safe to use
    NO  → ⚠️ Review carefully
    ↓
Are you only linking + brief description?
    YES → ✅ Almost always safe
    NO  → ⚠️ Reconsider approach
```

---

## 9. Source-Specific Quick Reference

| Source | Status | Notes |
|--------|--------|-------|
| EU institutions (europa.eu) | ✅ Open | Reuse policy applies |
| US Gov (.gov) | ✅ Public Domain | No restrictions |
| World Bank / UN | ✅ Open | Usually CC BY |
| Academic journals | ✅ Fair Use | Cite properly |
| News sites | ✅ Fair Use | Brief quotes only |
| Think tanks | ✅ Fair Use | Intended for public use |
| Company reports (public) | ✅ OK | Public disclosures |
| Paywalled academic | ⚠️ Careful | Limited fair use OK |
| Subscription news | ⚠️ Careful | Brief quotes OK |

---

## 10. Monthly Review Checklist

- [ ] Review any new documents added
- [ ] Verify all links still work
- [ ] Check attribution is complete
- [ ] Confirm no full-text reproduction
- [ ] Update this checklist if needed

---

## Emergency Contact

If you receive a takedown notice or copyright complaint:

1. **Don't panic** - your use is likely protected
2. **Document everything** - save the complaint
3. **Review your use** - confirm it follows this checklist
4. **Respond professionally** - explain fair use if applicable
5. **Consult legal** - if it escalates

**Note:** Given your current implementation (links + descriptions), copyright complaints are highly unlikely.

---

## Resources

- Full Analysis: `COPYRIGHT_COMPLIANCE_SUMMARY.md`
- Detailed Report: `copyright_analysis_report.txt`
- JSON Data: `copyright_analysis.json`
- US Copyright Office: https://www.copyright.gov/fair-use/
- EU Copyright: https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32001L0029

---

**Remember:** Your current implementation is fully compliant. This checklist is for maintaining compliance as you add new documents.

✅ Keep using: Links + Attribution + Brief descriptions  
✅ You're doing it right!

