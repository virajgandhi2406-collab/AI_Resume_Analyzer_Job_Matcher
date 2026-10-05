import io
from datetime import datetime

def generate_pdf_report(resume_data: dict, match_data: dict = None) -> io.BytesIO:
    """
    Generate a clean PDF ATS Scorecard & Analysis Summary Report.
    Uses ReportLab if installed, otherwise provides an HTML-to-PDF or binary buffer fallback.
    """
    buffer = io.BytesIO()
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#1E293B'),
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#64748B')
        )
        
        h2_style = ParagraphStyle(
            'Heading2Custom',
            parent=styles['Heading2'],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#0F172A'),
            spaceBefore=12,
            spaceAfter=6
        )
        
        body_style = ParagraphStyle(
            'BodyCustom',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#334155')
        )
        
        # Header
        story.append(Paragraph("AI Resume Analysis & ATS Scorecard", title_style))
        story.append(Paragraph(f"Candidate: <b>{resume_data.get('candidate_name') or 'Candidate'}</b> | Generated on {datetime.utcnow().strftime('%B %d, %Y')}", subtitle_style))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3B82F6'), spaceAfter=15))
        
        # Score Summary Table
        ats_score = resume_data.get('ats_score', 0.0)
        breakdown = resume_data.get('score_breakdown', {})
        
        score_data = [
            [
                Paragraph("<b>Overall ATS Score</b>", body_style),
                Paragraph(f"<b><font size='16' color='{'#10B981' if ats_score >= 80 else '#F59E0B' if ats_score >= 60 else '#EF4444'}'>{ats_score:.1f}%</font></b>", body_style),
                Paragraph("<b>Keywords Density:</b>", body_style),
                Paragraph(f"{breakdown.get('keywords', 0):.0f}%", body_style)
            ],
            [
                Paragraph("<b>Formatting & Structure:</b>", body_style),
                Paragraph(f"{breakdown.get('formatting', 0):.0f}%", body_style),
                Paragraph("<b>Impact & Metrics:</b>", body_style),
                Paragraph(f"{breakdown.get('impact_metrics', 0):.0f}%", body_style)
            ]
        ]
        
        score_table = Table(score_data, colWidths=[140, 110, 140, 110])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 15))
        
        # Skills Section
        hard_skills = resume_data.get('hard_skills', []) or resume_data.get('extracted_skills', [])
        soft_skills = resume_data.get('soft_skills', [])
        
        story.append(Paragraph("Identified Hard & Technical Skills", h2_style))
        story.append(Paragraph(", ".join(hard_skills[:20]) if hard_skills else "None identified", body_style))
        story.append(Spacer(1, 10))
        
        if soft_skills:
            story.append(Paragraph("Identified Soft Skills", h2_style))
            story.append(Paragraph(", ".join(soft_skills[:15]), body_style))
            story.append(Spacer(1, 10))
            
        # Strengths & Weaknesses
        strengths = resume_data.get('strengths', [])
        weaknesses = resume_data.get('weaknesses', [])
        
        if strengths:
            story.append(Paragraph("Key Strengths", h2_style))
            for s in strengths[:4]:
                story.append(Paragraph(f"• {s}", body_style))
            story.append(Spacer(1, 10))
            
        if weaknesses:
            story.append(Paragraph("Areas for ATS Optimization", h2_style))
            for w in weaknesses[:4]:
                story.append(Paragraph(f"• {w}", body_style))
            story.append(Spacer(1, 10))
            
        # Actionable Bullet Improvements
        bullets = resume_data.get('bullet_improvements', [])
        if bullets:
            story.append(Paragraph("Suggested Bullet Point Rewrites (XYZ Formula)", h2_style))
            for b in bullets[:3]:
                orig = b.get('original', '')
                imp = b.get('improved', '')
                story.append(Paragraph(f"<b>Original:</b> <i>\"{orig}\"</i>", body_style))
                story.append(Paragraph(f"<b>Improved:</b> <font color='#059669'><b>\"{imp}\"</b></font>", body_style))
                story.append(Spacer(1, 6))
                
        doc.build(story)
        buffer.seek(0)
        return buffer
        
    except ImportError:
        # Fallback text output formatted cleanly
        content = f"""AI RESUME AUDIT REPORT
====================================
Candidate: {resume_data.get('candidate_name', 'Candidate')}
Date: {datetime.utcnow().strftime('%Y-%m-%d')}
ATS Score: {resume_data.get('ats_score', 0)}%

Extracted Skills:
{', '.join(resume_data.get('extracted_skills', []))}

Strengths:
{chr(10).join(['- ' + s for s in resume_data.get('strengths', [])])}

Weaknesses:
{chr(10).join(['- ' + w for w in resume_data.get('weaknesses', [])])}
"""
        buffer.write(content.encode('utf-8'))
        buffer.seek(0)
        return buffer
