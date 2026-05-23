#!/usr/bin/env python3
"""Rebuild Rodriguez CV with Graphic Designer freelance role after Data Engineer."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

SRC = Path("/home/ubuntu/.cursor/projects/workspace/uploads/Rodriguez_DI_CV_8781.pdf")
OUT = Path("/workspace/Rodriguez_DI_CV_GraphicDesign.pdf")
OUT_LEGACY = Path("/workspace/Rodriguez_DI_CV_updated.pdf")
OUT_UPLOAD = SRC.parent / "Rodriguez_DI_CV_GraphicDesign.pdf"

PAGE_W = letter[0] - 1.1 * inch  # margins


def ps(name, **kw):
    defaults = dict(fontName="Times-Roman", fontSize=10, leading=11.5)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)


NAME = ps("Name", fontName="Times-Bold", fontSize=16, leading=18, alignment=1, spaceAfter=4)
CONTACT = ps("Contact", alignment=1, spaceAfter=8)
SECTION = ps("Section", fontName="Times-Bold", fontSize=11, leading=13, spaceBefore=6, spaceAfter=3)
BODY = ps("Body")
BULLET = ps("Bullet", leftIndent=12, bulletIndent=0, spaceAfter=0)
CERT = ps("Cert", fontSize=9.5, leading=10.5, spaceAfter=0)


def job_block(company, role, dates, bullets):
    rows = []
    company_p = Paragraph(f"<b>{company}</b>", ps("co", fontName="Times-Bold"))
    date_p = Paragraph(dates, ps("dt", alignment=2))
    rows.append([company_p, date_p])
    if role:
        rows.append([Paragraph(role, BODY), ""])
    t = Table(rows, colWidths=[PAGE_W * 0.72, PAGE_W * 0.28])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ]
        )
    )
    flow = [t]
    for b in bullets:
        flow.append(Paragraph(f"&bull; {b}", BULLET))
    flow.append(Spacer(1, 3))
    return flow


def cert_row(title, date):
    t = Table(
        [[Paragraph(title, CERT), Paragraph(date, ps("cd", fontSize=9.5, alignment=2))]],
        colWidths=[PAGE_W * 0.72, PAGE_W * 0.28],
    )
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return t


def build_story():
    story = [
        Paragraph("DANIEL IVAN S. RODRIGUEZ", NAME),
        Paragraph(
            "Pasay City, Metro Manila | +63 9158915925 | rodriguezdaniel.ivan@outlook.com",
            CONTACT,
        ),
        Paragraph("WORK EXPERIENCE", SECTION),
    ]

    story.extend(
        job_block(
            "Starbucks Philippines",
            "Data Engineer",
            "September 2025 - Present",
            [
                "Built and automated data ingestion and ETL pipelines using Azure Data Factory and Azure Databricks",
                "Orchestrated and scheduled Databricks jobs to process and transform 20+ billion data using PySpark and SQL",
                "Implemented data quality, validation, and reconciliation checks using SQL and PySpark",
                "Optimized data pipelines and Delta Lake tables to improve data accuracy, performance, and reliability",
                "Migrated datasets from on-premise data warehouse systems into Azure Databricks and Azure Data Lake",
            ],
        )
    )
    story.extend(
        job_block(
            "Freelance",
            "Graphic Designer",
            "2024 - Present",
            [
                "Designed social media graphics and pubmats for Sangguniang Kabataan (SK) and school events (Facebook, Instagram)",
                "Created layouts with photo compositing, retouching, and brand-consistent typography using Canva",
            ],
        )
    )
    story.extend(
        job_block(
            "Department of Public Works and Highways - Central Office, IMS",
            "Web Developer, Intern",
            "February 2025 - May 2025",
            [
                "Developed a web application for processing and retrieving BIR Form 2316 for DPWH employees",
                "Integrated external API services and handled testing via Postman",
                "Coded backend logic using .NET (C#) and frontend views using Visual Studio Code",
            ],
        )
    )
    story.extend(
        job_block(
            "Developed Ordering System, Part time",
            "",
            "April 2024 - May 2024",
            [
                "Developed an Android-based Ordering System for Fred's Pastries using B4A",
                "Created a user-friendly interface for browsing and ordering pastries",
                "Integrated basic order management",
            ],
        )
    )

    story.append(Paragraph("TECHNICAL SKILLS", SECTION))
    for line in [
        "<b>Data Engineering &amp; Cloud:</b> Azure Databricks, Azure Data Factory, Azure Data Lake, Azure Logic Apps, Microsoft Azure, Data Warehousing, Big Data",
        "<b>Programming &amp; Scripting:</b> Python, PySpark, SQL",
        "<b>ETL &amp; Data Operations:</b> ETL Development, Data Pipelines, Data Quality Checks, Data Validation, Data Reconciliation.",
        "<b>Design &amp; Creative:</b> Canva, Social Media Graphics, Photo Compositing, Brand Layout, Typography, Pubmat Design",
        "<b>Developer Tools:</b> Git, Visual Studio, VS Code, PyCharm, SQL Server Management Studio (SSMS)",
    ]:
        story.append(Paragraph(line, BODY))

    story.append(Paragraph("EDUCATION", SECTION))
    story.extend(
        job_block(
            "ROMBLON STATE UNIVERSITY",
            "● Bachelor of Science in Information Technology",
            "July 2025",
            [],
        )
    )

    story.append(Paragraph("UNIVERSITY PROJECTS", SECTION))
    story.extend(
        job_block(
            "Capstone Project – Romblon State University",
            "Development of Android-based Restaurant Table Booking",
            "September 2024 - March 2025",
            [
                "Developed an Android app for restaurant table bookings in Municipality of Odiongan using Flutter",
                "Integrated Firebase as the database for managing user and reservation data",
            ],
        )
    )
    story.extend(
        job_block(
            "Mini Project – Romblon State University",
            "ADK's Super Delivery (Android App)",
            "May 2024",
            [
                "Developed an Android app for ADK's Super Delivery, a food delivery service like Shakey's, using B4A",
            ],
        )
    )

    story.append(Paragraph("CERTIFICATIONS &amp; TRAINING", SECTION))
    for title, date in [
        ("Mastering Azure Databricks for Data Engineers-Packt", "December 2025"),
        ("Advanced Data Management in Azure Databricks-Packt", "December 2025"),
        ("Microsoft Data &amp; AI Solutions - Microsoft", "October 2025"),
        ("Build the Future with AWS: A Guide to GenerativeAI-TrainocatePHxAWS", "October 2025"),
        ("Foundations of Software Testing and Validation(UniversityofLeeds)-Coursera", "July 2025"),
        ("Automate tasks and processes with Jira (UnitedLatinoStudentsAssociation)-Coursera", "July 2025"),
        ("40-hour Python Essentials Course 1 - DICT", "October-November 2024"),
        ("Introduction to Machine Learning Using PythonandGoogleColab-RSUMainCampus", "November 2024"),
    ]:
        story.append(cert_row(title, date))

    return story


def main():
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.42 * inch,
        bottomMargin=0.38 * inch,
    )
    doc.build(build_story())
    OUT_LEGACY.write_bytes(OUT.read_bytes())
    OUT_UPLOAD.write_bytes(OUT.read_bytes())
    print(f"Wrote {OUT}")
    print(f"Wrote {OUT_LEGACY}")
    print(f"Wrote {OUT_UPLOAD}")


if __name__ == "__main__":
    main()
