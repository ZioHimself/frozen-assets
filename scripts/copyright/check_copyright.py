#!/usr/bin/env python3
"""
Copyright and Usage Permissions Checker for Document URLs
Analyzes each document URL to determine if it can be legally quoted/used.
"""

import json
from urllib.parse import urlparse
from typing import Dict, List

def load_documents(file_path: str) -> List[Dict]:
    """Load and filter documents with valid links."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return [d for d in data if d.get('link') and d.get('link').strip() and d.get('title') and d.get('title').strip()]

def categorize_source(url: str, authority: str) -> Dict[str, str]:
    """
    Categorize the source and determine usage rights based on URL and authority.
    
    Returns a dict with:
    - category: Type of source
    - usage_status: allowed/restricted/check_required
    - reasoning: Explanation
    - license_info: Known license information
    """
    domain = urlparse(url).netloc.lower()
    
    # Government and Official Sources - Generally Public Domain or Open Access
    government_sources = {
        'consilium.europa.eu': {
            'category': 'EU Official',
            'usage_status': 'allowed',
            'reasoning': 'EU Council documents are public and can be freely quoted with attribution',
            'license_info': 'EU institutions policy: documents can be reused for commercial/non-commercial purposes'
        },
        'congress.gov': {
            'category': 'US Government',
            'usage_status': 'allowed',
            'reasoning': 'US federal government documents are in the public domain',
            'license_info': 'Public Domain (17 U.S.C. § 105)'
        },
        'europarl.europa.eu': {
            'category': 'European Parliament',
            'usage_status': 'allowed',
            'reasoning': 'European Parliament documents are publicly accessible and quotable',
            'license_info': 'EU institutions reuse policy applies'
        },
        'worldbank.org': {
            'category': 'International Organization',
            'usage_status': 'allowed',
            'reasoning': 'World Bank publications use Creative Commons licenses',
            'license_info': 'Typically CC BY 3.0 IGO license'
        },
        'g7.org': {
            'category': 'International Summit',
            'usage_status': 'allowed',
            'reasoning': 'Official G7 statements and documents are public and quotable',
            'license_info': 'Official government communications'
        }
    }
    
    # Academic and Research Institutions
    academic_sources = {
        'iiss.org': {
            'category': 'Think Tank',
            'usage_status': 'allowed',
            'reasoning': 'International Institute for Strategic Studies - research intended for educational/policy use, fair use applies',
            'license_info': 'Academic fair use for quotation with citation'
        },
        'petersoninstitute.org': {
            'category': 'Think Tank',
            'usage_status': 'allowed',
            'reasoning': 'Peterson Institute research is intended for public policy discourse, quotable with attribution',
            'license_info': 'Fair use for educational and informational purposes'
        },
        'internationallaw.org': {
            'category': 'Professional Association',
            'usage_status': 'allowed',
            'reasoning': 'International Law Association publishes for legal scholarship and discussion',
            'license_info': 'Academic fair use with proper citation'
        }
    }
    
    # News and Media Organizations
    news_sources = {
        'euobserver.com': {
            'category': 'News Media',
            'usage_status': 'allowed',
            'reasoning': 'News articles can be quoted under fair use with proper attribution',
            'license_info': 'Fair use for quotation and commentary'
        },
        'euractiv.com': {
            'category': 'News Media',
            'usage_status': 'allowed',
            'reasoning': 'EU news platform, articles quotable under fair use',
            'license_info': 'Fair use for quotation with attribution'
        },
        'eutoday.net': {
            'category': 'News Media',
            'usage_status': 'allowed',
            'reasoning': 'News content quotable under fair use doctrine',
            'license_info': 'Fair use applies to news quotation'
        },
        'tijd.be': {
            'category': 'News Media (Belgian)',
            'usage_status': 'allowed',
            'reasoning': 'Belgian newspaper, fair use applies for quotation',
            'license_info': 'Fair use with proper attribution'
        }
    }
    
    # Corporate/Financial
    corporate_sources = {
        'euroclear.com': {
            'category': 'Financial Institution',
            'usage_status': 'allowed',
            'reasoning': 'Public annual reports and investor relations documents can be quoted',
            'license_info': 'Public disclosure documents, quotable with attribution'
        }
    }
    
    # Advocacy/NGO
    advocacy_sources = {
        'ukrainianvictory.org': {
            'category': 'Advocacy Organization',
            'usage_status': 'allowed',
            'reasoning': 'International Centre for Ukrainian Victory publishes advocacy materials intended for public dissemination',
            'license_info': 'Public advocacy materials, quotable with attribution'
        }
    }
    
    # Check all categories
    all_sources = {
        **government_sources,
        **academic_sources,
        **news_sources,
        **corporate_sources,
        **advocacy_sources
    }
    
    # Check exact domain match first
    if domain in all_sources:
        return all_sources[domain]
    
    # Check domain patterns for partial matches
    # EU Official domains
    if 'consilium.europa.eu' in domain or 'europarl.europa.eu' in domain or 'europa.eu' in domain:
        return {
            'category': 'EU Official',
            'usage_status': 'allowed',
            'reasoning': 'EU institutional documents are public and can be freely quoted with attribution under EU reuse policy',
            'license_info': 'EU institutions allow reuse of documents for commercial/non-commercial purposes with attribution'
        }
    
    # US Government
    if 'congress.gov' in domain or '.gov' in domain:
        return {
            'category': 'US Government',
            'usage_status': 'allowed',
            'reasoning': 'US federal government documents are in the public domain',
            'license_info': 'Public Domain (17 U.S.C. § 105)'
        }
    
    # International Organizations
    if 'worldbank.org' in domain or 'g7.org' in domain:
        return {
            'category': 'International Organization',
            'usage_status': 'allowed',
            'reasoning': 'International organization publications are intended for public policy use',
            'license_info': 'Typically CC BY 3.0 IGO or similar open license'
        }
    
    # Think Tanks and Research Institutes
    if any(pattern in domain for pattern in ['institute', 'iiss.org', 'petersoninstitute', 'kse.ua', 'gmfus.org']):
        return {
            'category': 'Think Tank / Research Institute',
            'usage_status': 'allowed',
            'reasoning': 'Research publications intended for policy discourse and education, quotable under fair use',
            'license_info': 'Academic fair use with proper citation'
        }
    
    # News and Media
    if any(pattern in domain for pattern in ['euractiv', 'euobserver', 'eutoday', 'tijd.be']):
        return {
            'category': 'News Media',
            'usage_status': 'allowed',
            'reasoning': 'News articles can be quoted under fair use/fair dealing with proper attribution',
            'license_info': 'Fair use for quotation and commentary'
        }
    
    # Financial Institutions (public reports)
    if 'euroclear' in domain:
        return {
            'category': 'Financial Institution',
            'usage_status': 'allowed',
            'reasoning': 'Public annual reports and investor relations documents can be quoted',
            'license_info': 'Public disclosure documents, quotable with attribution'
        }
    
    # Academic/Professional Associations
    if 'internationallaw.org' in domain or '.edu' in domain or 'academic' in domain:
        return {
            'category': 'Academic / Professional Association',
            'usage_status': 'allowed',
            'reasoning': 'Academic and professional publications are intended for scholarly discourse',
            'license_info': 'Academic fair use with proper citation'
        }
    
    # Default for unknown sources
    return {
        'category': 'Unknown/Other',
        'usage_status': 'check_required',
        'reasoning': 'Source not in known database, manual review recommended',
        'license_info': 'Review specific website terms of use'
    }

def analyze_documents(documents: List[Dict]) -> List[Dict]:
    """Analyze all documents for copyright and usage permissions."""
    results = []
    
    for doc in documents:
        url = doc.get('link', '')
        authority = doc.get('authority', '')
        title = doc.get('title', '')
        doc_type = doc.get('type', '')
        
        analysis = categorize_source(url, authority)
        
        results.append({
            'title': title,
            'url': url,
            'authority': authority,
            'type': doc_type,
            **analysis
        })
    
    return results

def generate_report(results: List[Dict]) -> str:
    """Generate a formatted report of the analysis."""
    report = []
    report.append("=" * 100)
    report.append("COPYRIGHT AND USAGE PERMISSIONS ANALYSIS")
    report.append("Frozen Assets Document Database")
    report.append("=" * 100)
    report.append("")
    
    # Summary statistics
    total = len(results)
    allowed = sum(1 for r in results if r['usage_status'] == 'allowed')
    check_required = sum(1 for r in results if r['usage_status'] == 'check_required')
    
    report.append(f"SUMMARY:")
    report.append(f"  Total documents analyzed: {total}")
    report.append(f"  ✓ Allowed for quotation: {allowed} ({allowed/total*100:.1f}%)")
    report.append(f"  ⚠ Manual check required: {check_required}")
    report.append("")
    report.append("=" * 100)
    report.append("")
    
    # Group by usage status
    allowed_docs = [r for r in results if r['usage_status'] == 'allowed']
    check_docs = [r for r in results if r['usage_status'] == 'check_required']
    
    # Allowed documents
    if allowed_docs:
        report.append("✓ DOCUMENTS ALLOWED FOR QUOTATION/USE")
        report.append("-" * 100)
        report.append("")
        
        # Group by category
        categories = {}
        for doc in allowed_docs:
            cat = doc['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(doc)
        
        for category, docs in sorted(categories.items()):
            report.append(f"\n{category.upper()} ({len(docs)} documents)")
            report.append("-" * 100)
            
            for i, doc in enumerate(docs, 1):
                report.append(f"\n{i}. {doc['title']}")
                report.append(f"   Authority: {doc['authority']}")
                report.append(f"   URL: {doc['url']}")
                report.append(f"   License/Usage: {doc['license_info']}")
                report.append(f"   Reasoning: {doc['reasoning']}")
    
    # Documents requiring manual check
    if check_docs:
        report.append("\n\n")
        report.append("=" * 100)
        report.append("⚠ DOCUMENTS REQUIRING MANUAL REVIEW")
        report.append("-" * 100)
        report.append("")
        
        for i, doc in enumerate(check_docs, 1):
            report.append(f"\n{i}. {doc['title']}")
            report.append(f"   Authority: {doc['authority']}")
            report.append(f"   URL: {doc['url']}")
            report.append(f"   Reasoning: {doc['reasoning']}")
    
    report.append("\n\n")
    report.append("=" * 100)
    report.append("GENERAL LEGAL NOTES:")
    report.append("=" * 100)
    report.append("""
1. FAIR USE DOCTRINE: In the US and similar doctrines globally allow quotation of copyrighted 
   materials for purposes of commentary, criticism, research, and education.

2. EU COPYRIGHT: Under EU Directive 2001/29/EC and national implementations, quotations are 
   permitted for purposes such as criticism, review, and illustration for teaching/research.

3. GOVERNMENT WORKS: Most government documents (EU, US federal) are in public domain or 
   under permissive licenses allowing reuse.

4. NEWS ARTICLES: Can be quoted under fair use/fair dealing with proper attribution, especially 
   for informational and commentary purposes.

5. RESEARCH PUBLICATIONS: Academic and think tank publications are intended for scholarly 
   discourse and can be quoted with proper citation.

6. BEST PRACTICES:
   - Always provide proper attribution
   - Include title, author/organization, publication date, and URL
   - Quote only necessary portions (not entire articles)
   - Use for informational, educational, or commentary purposes
   - Add your own analysis/commentary

7. YOUR USE CASE: Creating a database with links, titles, and brief descriptions with 
   proper attribution falls well within fair use/fair dealing exceptions.
""")
    
    return "\n".join(report)

def main():
    """Main execution function."""
    # Load documents
    documents = load_documents('/tmp/documents_data.json')
    print(f"Loaded {len(documents)} documents with valid links\n")
    
    # Analyze documents
    results = analyze_documents(documents)
    
    # Generate and save report
    report = generate_report(results)
    
    # Save to file
    output_file = '/tmp/copyright_analysis_report.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"\n\nReport saved to: {output_file}")
    
    # Also save JSON version
    json_output = '/tmp/copyright_analysis.json'
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"JSON data saved to: {json_output}")

if __name__ == '__main__':
    main()

