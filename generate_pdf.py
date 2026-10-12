import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print footer with title and page number.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_footer(num_pages)
            super().showPage()
        super().save()

    def draw_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        # Draw centered footer
        footer_text = f"Student Management System | Mini Project    (Page {self._pageNumber} of {page_count})"
        self.drawCentredString(A4[0] / 2.0, 30, footer_text)
        self.restoreState()

def build_pdf(filename="Student_Management_System_Documentation.pdf"):
    margin = 40  # approx 14mm
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin + 10
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        alignment=1, # Centered
        textColor=colors.HexColor('#111111'),
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.HexColor('#333333'),
        spaceAfter=3
    )

    credit_style = ParagraphStyle(
        'DocCredit',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        alignment=1,
        textColor=colors.HexColor('#111111'),
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor('#1a365d'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyJustify',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        alignment=4, # Justified
        textColor=colors.HexColor('#222222'),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        alignment=4,
        textColor=colors.HexColor('#222222'),
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=2.5
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#222222')
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#1e3a8a')
    )

    table_badge = ParagraphStyle(
        'TableBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#15803d')
    )

    arch_style = ParagraphStyle(
        'ArchText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        alignment=1,
        textColor=colors.HexColor('#1e293b')
    )

    story = []

    # ==================== PAGE 1 ====================
    story.append(Paragraph("STUDENT MANAGEMENT SYSTEM", title_style))
    story.append(Paragraph("Simple Web-Based Student Information and CRUD Management System", subtitle_style))
    story.append(Paragraph("Mini Project – 1 Credit", credit_style))

    story.append(Paragraph("1. Abstract", h2_style))
    story.append(Paragraph(
        "The Student Management System is a simple web-based application designed to help educational institutions "
        "and administrators manage student records efficiently. The system allows users to perform complete CRUD "
        "(Create, Read, Update, Delete) operations on student details including registration, profile search, "
        "information updates, and record removal. The application uses Streamlit for an interactive user interface "
        "and FastAPI for the backend REST API, with SQLite used to store student records persistently. The project "
        "demonstrates how a lightweight frontend and backend can work together to provide a practical, service-oriented "
        "academic management solution.",
        body_style
    ))

    story.append(Paragraph("2. Problem Statement", h2_style))
    story.append(Paragraph(
        "Educational institutions and department staff often experience difficulties maintaining student records "
        "through traditional paper registers or unstructured spreadsheets, leading to errors, duplicate entries, data loss, "
        "and slow lookups. A simple digital management assistant can provide centralized data entry, instant search by "
        "student ID, unique email validation, and streamlined updates before more complex ERP systems are implemented.",
        body_style
    ))

    story.append(Paragraph("3. Objectives", h2_style))
    objectives = [
        "Develop a simple web application for streamlined student record management.",
        "Allow users to register new students with name, age, department, and email address.",
        "Provide complete CRUD functionality to view, search, modify, and delete student records.",
        "Implement automated validation to ensure positive IDs, valid age boundaries, and unique emails.",
        "Use FastAPI to provide backend REST APIs and Streamlit to create the interactive frontend.",
        "Store student details in SQLite database using SQLAlchemy ORM for reliable local persistence."
    ]
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", bullet_style))

    story.append(Paragraph("4. Technologies Used", h2_style))
    tech_data = [
        [Paragraph("Technology", table_header), Paragraph("Purpose", table_header)],
        [Paragraph("Python 3", table_cell), Paragraph("Core programming language and application business logic", table_cell)],
        [Paragraph("FastAPI", table_cell), Paragraph("Backend REST API framework and request/response handling", table_cell)],
        [Paragraph("Streamlit", table_cell), Paragraph("Interactive web frontend for user interaction", table_cell)],
        [Paragraph("SQLite", table_cell), Paragraph("Storage of student records (<code>students.db</code>)", table_cell)],
        [Paragraph("SQLAlchemy", table_cell), Paragraph("Object Relational Mapping (ORM) and database session management", table_cell)],
        [Paragraph("Pydantic", table_cell), Paragraph("Validation of API request and response data schemas", table_cell)],
        [Paragraph("Requests", table_cell), Paragraph("HTTP communication between Streamlit frontend and FastAPI backend", table_cell)],
        [Paragraph("Uvicorn", table_cell), Paragraph("Asynchronous ASGI server running the FastAPI backend", table_cell)],
    ]
    t1 = Table(tech_data, colWidths=[130, 385])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dbeafe')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(t1)

    story.append(PageBreak())

    # ==================== PAGE 2 ====================
    story.append(Paragraph("5. System Architecture", h2_style))
    story.append(Paragraph(
        "The application follows a simple three-layer flow. The user interacts with the Streamlit frontend. Streamlit "
        "sends the student management request to the FastAPI backend through HTTP. FastAPI validates the payload against "
        "Pydantic schemas and passes the request to the CRUD database layer, which interacts with the SQLite database via "
        "SQLAlchemy ORM. The result is returned to Streamlit and displayed to the user. All student records are stored in SQLite.",
        body_style
    ))

    arch_table_data = [[Paragraph("User  &rarr;  Streamlit Frontend  &rarr;  FastAPI Backend  &rarr;  CRUD Logic / SQLAlchemy  &rarr;  SQLite", arch_style)]]
    arch_t = Table(arch_table_data, colWidths=[515])
    arch_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f1f5f9')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(arch_t)
    story.append(Spacer(1, 4))

    story.append(Paragraph("6. Main Features", h2_style))
    features = [
        "Home dashboard with student summary statistics and system overview.",
        "Student registration form capturing name, age, department, and email address.",
        "Real-time duplicate email validation preventing duplicate student admissions.",
        "Interactive student directory displaying all enrolled students in a clean table.",
        "Targeted student search by entering a unique Student ID.",
        "Student detail modification form for updating name, age, department, or email.",
        "Safe deletion module to remove obsolete records with confirmation.",
        "FastAPI Swagger interactive documentation available through /docs.",
        "Backend root health-check endpoint confirming API server availability.",
        "Modern, responsive user interface with clear success and error notifications."
    ]
    for feat in features:
        story.append(Paragraph(f"• {feat}", bullet_style))

    story.append(Paragraph("7. Database Schema & Core Entities", h2_style))
    story.append(Paragraph(
        "The system maintains a relational database model for student records. Each record represents an enrolled student "
        "with essential academic and personal details:",
        body_style
    ))

    schema_points = [
        "<b>Student ID:</b> Unique auto-incrementing integer identifier (Primary Key).",
        "<b>Student Name:</b> String field representing the full legal name of the student.",
        "<b>Student Age:</b> Positive integer representing the student's age (15 to 100).",
        "<b>Department:</b> String indicating academic branch (e.g., Computer Science, Mechanical, ECE).",
        "<b>Email Address:</b> Unique indexed string ensuring no two students share the same email."
    ]
    for sp in schema_points:
        story.append(Paragraph(f"• {sp}", bullet_style))

    schema_data = [
        [Paragraph("Field", table_header), Paragraph("Data Type", table_header), Paragraph("Constraints", table_header), Paragraph("Description", table_header)],
        [Paragraph("id", table_cell), Paragraph("Integer", table_cell), Paragraph("Primary Key, Auto-increment", table_cell), Paragraph("Unique student ID number", table_cell)],
        [Paragraph("name", table_cell), Paragraph("String(100)", table_cell), Paragraph("Not Null", table_cell), Paragraph("Full legal name of the student", table_cell)],
        [Paragraph("age", table_cell), Paragraph("Integer", table_cell), Paragraph("Not Null (15–100)", table_cell), Paragraph("Current age of the student", table_cell)],
        [Paragraph("department", table_cell), Paragraph("String(100)", table_cell), Paragraph("Not Null", table_cell), Paragraph("Academic department / branch", table_cell)],
        [Paragraph("email", table_cell), Paragraph("String(100)", table_cell), Paragraph("Unique, Indexed", table_cell), Paragraph("Student institutional email address", table_cell)],
    ]
    schema_t = Table(schema_data, colWidths=[70, 85, 150, 210])
    schema_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dbeafe')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(schema_t)

    story.append(PageBreak())

    # ==================== PAGE 3 ====================
    story.append(Paragraph("8. FastAPI Endpoints", h2_style))
    endpoint_data = [
        [Paragraph("Method", table_header), Paragraph("Endpoint", table_header), Paragraph("Purpose", table_header)],
        [Paragraph("GET", table_cell), Paragraph("/api/health or /", table_cell), Paragraph("Checks whether the backend server is running", table_cell)],
        [Paragraph("GET", table_cell), Paragraph("/students", table_cell), Paragraph("Retrieves list of all enrolled students from the database", table_cell)],
        [Paragraph("GET", table_cell), Paragraph("/students/{id}", table_cell), Paragraph("Retrieves a single student's details by their unique ID", table_cell)],
        [Paragraph("POST", table_cell), Paragraph("/students", table_cell), Paragraph("Creates a new student record after validating unique email", table_cell)],
        [Paragraph("PUT", table_cell), Paragraph("/students/{id}", table_cell), Paragraph("Updates an existing student's name, age, department, or email", table_cell)],
        [Paragraph("DELETE", table_cell), Paragraph("/students/{id}", table_cell), Paragraph("Deletes a student record permanently by ID", table_cell)],
    ]
    end_t = Table(endpoint_data, colWidths=[65, 140, 310])
    end_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dbeafe')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(end_t)

    story.append(Paragraph("9. Working of the System", h2_style))
    steps = [
        "The user launches the Streamlit frontend and FastAPI backend applications.",
        "The user opens the Streamlit web dashboard in their browser.",
        "To add a student, the user fills in the name, age, department, and email, then clicks Submit.",
        "Streamlit transmits the payload via an HTTP POST request to the FastAPI /students endpoint.",
        "FastAPI validates data types with Pydantic and checks SQLite to ensure the email is not already registered.",
        "The CRUD module inserts the student into SQLite via SQLAlchemy and generates a unique ID.",
        "The updated student profile is returned as a JSON response and rendered as a confirmation in Streamlit.",
        "The user can view all students in the interactive directory, look up records by ID, update fields, or delete entries."
    ]
    for idx, s in enumerate(steps, 1):
        story.append(Paragraph(f"<b>{idx}.</b> {s}", bullet_style))

    story.append(Paragraph("10. Testing and Results", h2_style))
    story.append(Paragraph(
        "The application was thoroughly verified through the Streamlit interface and FastAPI Swagger documentation. "
        "The backend health endpoint responded successfully, all CRUD endpoints processed requests accurately, and student "
        "records were successfully stored and managed in SQLite.",
        body_style
    ))

    test_data = [
        [Paragraph("Test Case", table_header), Paragraph("Expected Result", table_header), Paragraph("Status", table_header)],
        [Paragraph("Backend health check", table_cell), Paragraph("API reports root welcome and running status", table_cell), Paragraph("Passed", table_badge)],
        [Paragraph("Student enrollment", table_cell), Paragraph("New student added with auto-increment ID and HTTP 201", table_cell), Paragraph("Passed", table_badge)],
        [Paragraph("Duplicate email check", table_cell), Paragraph("HTTP 400 Bad Request returned with error message", table_cell), Paragraph("Passed", table_badge)],
        [Paragraph("Retrieve student list", table_cell), Paragraph("All active records displayed in tabular format", table_cell), Paragraph("Passed", table_badge)],
        [Paragraph("Search student by ID", table_cell), Paragraph("Student record returned; HTTP 404 for nonexistent ID", table_cell), Paragraph("Passed", table_badge)],
        [Paragraph("Update student record", table_cell), Paragraph("Student fields updated and persisted in SQLite", table_cell), Paragraph("Passed", table_badge)],
        [Paragraph("Delete student record", table_cell), Paragraph("Record deleted; success message returned", table_cell), Paragraph("Passed", table_badge)],
        [Paragraph("Swagger documentation", table_cell), Paragraph("API endpoints and schemas interactive at /docs", table_cell), Paragraph("Passed", table_badge)],
    ]
    test_t = Table(test_data, colWidths=[140, 305, 70])
    test_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dbeafe')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(test_t)

    story.append(PageBreak())

    # ==================== PAGE 4 ====================
    story.append(Paragraph("11. Advantages", h2_style))
    advs = [
        "Simple and easy-to-use graphical interface with zero training required.",
        "Fast response times and high performance powered by FastAPI.",
        "Guaranteed data integrity with Pydantic validation and unique email constraints.",
        "Lightweight technologies perfectly suited for an academic mini project.",
        "Zero-configuration persistence with SQLite requiring no database server setup.",
        "Modular codebase making it straightforward to add more academic modules in the future."
    ]
    for adv in advs:
        story.append(Paragraph(f"• {adv}", bullet_style))

    story.append(Paragraph("12. Limitations", h2_style))
    story.append(Paragraph(
        "The application provides a centralized student record management system designed for single-node academic use. "
        "It does not include role-based multi-user authentication (Admin, Teacher, Student roles) or fine-grained access control. "
        "Additionally, it currently does not support bulk CSV file uploads for batch student enrollment.",
        body_style
    ))

    story.append(Paragraph("13. Future Enhancements", h2_style))
    enhancements = [
        "Add user authentication and role-based permissions (Admin, Faculty, Student).",
        "Implement bulk student import and export using Excel / CSV spreadsheets.",
        "Introduce course enrollment, semester grades, and attendance tracking modules.",
        "Add automated PDF report card and student ID card generation.",
        "Migrate SQLite to cloud PostgreSQL for large-scale multi-institution deployment."
    ]
    for enh in enhancements:
        story.append(Paragraph(f"• {enh}", bullet_style))

    story.append(Paragraph("14. Conclusion", h2_style))
    story.append(Paragraph(
        "The Student Management System successfully demonstrates a complete full-stack web application using Streamlit "
        "and FastAPI. It accepts student registration details, validates them with strict schema rules, performs complete "
        "CRUD operations via SQLAlchemy, and stores records securely in SQLite. The project provides a practical example "
        "of REST API communication, modern frontend development, backend request handling, and relational database management "
        "in a compact academic application.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully: {filename}")

if __name__ == '__main__':
    build_pdf()
