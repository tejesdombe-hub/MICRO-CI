#!/usr/bin/env python3
"""
Generate readable Food Delivery Platform documentation PDF using ReportLab.
Produces clean, text-selectable PDF without HTML/Chrome rendering issues.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

DOCS_DIR = Path(__file__).parent
PDF_PATH = DOCS_DIR / "Food-Delivery-Platform-Documentation.pdf"

# Colors
NAVY = colors.HexColor("#0f3460")
ACCENT = colors.HexColor("#e94560")
LIGHT_BG = colors.HexColor("#f0f4f8")
TEXT = colors.HexColor("#1a1a2e")
MUTED = colors.HexColor("#4a5568")


def build_styles():
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "CoverTitle",
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=34,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=12,
        ),
        "cover_sub": ParagraphStyle(
            "CoverSub",
            fontName="Helvetica",
            fontSize=13,
            leading=18,
            textColor=MUTED,
            alignment=TA_LEFT,
            spaceAfter=8,
        ),
        "cover_meta": ParagraphStyle(
            "CoverMeta",
            fontName="Helvetica",
            fontSize=11,
            leading=16,
            textColor=TEXT,
            alignment=TA_LEFT,
        ),
        "h1": ParagraphStyle(
            "H1",
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=NAVY,
            spaceBefore=20,
            spaceAfter=10,
            borderPadding=(0, 0, 4, 0),
        ),
        "h2": ParagraphStyle(
            "H2",
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=8,
        ),
        "h3": ParagraphStyle(
            "H3",
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=TEXT,
            spaceBefore=10,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "Body",
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=TEXT,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=TEXT,
            leftIndent=12,
            spaceAfter=4,
        ),
        "code": ParagraphStyle(
            "Code",
            fontName="Courier",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#2d3748"),
            backColor=LIGHT_BG,
            leftIndent=8,
            rightIndent=8,
            spaceBefore=6,
            spaceAfter=10,
        ),
        "toc": ParagraphStyle(
            "TOC",
            fontName="Helvetica",
            fontSize=11,
            leading=18,
            textColor=TEXT,
        ),
        "footer": ParagraphStyle(
            "Footer",
            fontName="Helvetica-Oblique",
            fontSize=9,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
    }


def table(data, col_widths=None, header=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style = [
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (-1, -1), TEXT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
    ]
    if header and len(data) > 0:
        style.extend([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9.5),
        ])
        style.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]))
    t.setStyle(TableStyle(style))
    return t


def pre(text):
    return Preformatted(text.strip(), build_styles()["code"])


def bullet_list(items, style):
    return ListFlowable(
        [ListItem(Paragraph(i, style), leftIndent=12) for i in items],
        bulletType="bullet",
        start="•",
    )


def build_document():
    s = build_styles()
    story = []

    # ---- COVER (light background, dark text) ----
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph("FOOD DELIVERY PLATFORM", ParagraphStyle(
        "badge", fontName="Helvetica-Bold", fontSize=10, textColor=ACCENT, spaceAfter=16)))
    story.append(Paragraph("Technical Documentation", s["cover_title"]))
    story.append(Paragraph(
        "Enterprise Microservices Backend — Architecture, APIs, Security &amp; Learning Guide",
        s["cover_sub"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "Zomato / Swiggy-style system built with Java 17 and Spring Boot 3",
        s["cover_sub"]))
    story.append(Spacer(1, 2 * cm))
    for line in [
        "<b>Project:</b> food-delivery-platform (Maven Multi-Module)",
        "<b>Version:</b> 1.0.0-SNAPSHOT",
        "<b>Modules:</b> 12 (11 microservices + common-lib)",
        "<b>Stack:</b> Spring Cloud, Eureka, JWT, MySQL, OpenFeign",
    ]:
        story.append(Paragraph(line, s["cover_meta"]))
    story.append(PageBreak())

    # ---- TOC ----
    story.append(Paragraph("Table of Contents", s["h1"]))
    toc_items = [
        "1. Executive Summary",
        "2. Technology Stack",
        "3. System Architecture",
        "4. Microservices Overview",
        "5. Layered Architecture",
        "6. Project Structure",
        "7. Security and JWT Authentication",
        "8. Domain Entities and DTOs",
        "9. Inter-Service Communication (Feign)",
        "10. Business Flows",
        "11. REST API Reference",
        "12. Exception Handling",
        "13. Setup and Deployment",
        "14. Learning Guide",
    ]
    for item in toc_items:
        story.append(Paragraph(item, s["toc"]))
    story.append(PageBreak())

    # ---- 1. EXECUTIVE SUMMARY ----
    story.append(Paragraph("1. Executive Summary", s["h1"]))
    story.append(Paragraph(
        "This project is an enterprise-grade Food Delivery Microservices Backend similar in "
        "concept to Zomato or Swiggy. It is organized as a Maven multi-module monorepo with "
        "eleven deployable Spring Boot applications plus a shared common library.",
        s["body"]))
    story.append(Paragraph("<b>Key design principles:</b>", s["h3"]))
    story.append(bullet_list([
        "Microservices architecture — each service owns its database.",
        "Layered architecture — controller, service, repository in every service.",
        "DTO-only APIs — JPA entities are never exposed over HTTP or Feign.",
        "Eureka service discovery and Spring Cloud Config for centralized settings.",
        "API Gateway as a single entry point with load-balanced routing.",
        "JWT authentication with role-based access control (RBAC).",
    ], s["bullet"]))

    # ---- 2. TECH STACK ----
    story.append(Paragraph("2. Technology Stack", s["h1"]))
    story.append(table([
        ["Category", "Technology", "Version"],
        ["Language", "Java", "17"],
        ["Framework", "Spring Boot", "3.3.5"],
        ["Cloud", "Spring Cloud", "2023.0.3"],
        ["Database", "MySQL + Spring Data JPA", "Per service"],
        ["Security", "Spring Security + JWT", "jjwt 0.12.6"],
        ["Inter-service", "OpenFeign", "order-service"],
        ["Discovery", "Netflix Eureka", "Port 8761"],
        ["Config", "Spring Cloud Config", "Port 8888"],
        ["Gateway", "Spring Cloud Gateway", "Port 8080"],
        ["API Docs", "SpringDoc OpenAPI", "Swagger UI"],
        ["Build", "Maven", "Multi-module"],
    ], col_widths=[3.5 * cm, 5 * cm, 4 * cm]))

    # ---- 3. ARCHITECTURE ----
    story.append(Paragraph("3. System Architecture", s["h1"]))
    story.append(Paragraph(
        "Clients connect only to the API Gateway (port 8080). The gateway uses Eureka to "
        "find service instances and routes requests. The Order Service orchestrates other "
        "services using OpenFeign when a customer places an order.",
        s["body"]))
    story.append(Paragraph("3.1 Architecture Diagram", s["h2"]))
    story.append(pre("""
    [ Client Apps ]
           |
           v
    +------------------+
    |  API Gateway     |  :8080
    +------------------+
           |
    +------+------+------+------+------+
    v      v      v      v      v      v
  Auth  Customer Rest.  Menu  Order  Payment ...
  :8081  :8082   :8083  :8084 :8085  :8087

    Order Service --Feign--> Customer, Restaurant,
                             Payment, Notification, Delivery

    All services --> Eureka (:8761)
    All services --> Config Server (:8888)
    """))

    story.append(Paragraph("3.2 Service Ports and Databases", s["h2"]))
    story.append(table([
        ["Service", "Port", "Database", "Role"],
        ["discovery-server", "8761", "-", "Eureka registry"],
        ["config-server", "8888", "-", "Central configuration"],
        ["api-gateway", "8080", "-", "API routing"],
        ["auth-service", "8081", "auth_db", "JWT login/register"],
        ["customer-service", "8082", "customer_db", "Customer CRUD"],
        ["restaurant-service", "8083", "restaurant_db", "Restaurants"],
        ["menu-service", "8084", "menu_db", "Menu items"],
        ["order-service", "8085", "order_db", "Order orchestration"],
        ["delivery-partner-service", "8086", "delivery_db", "Delivery"],
        ["payment-service", "8087", "payment_db", "Payments"],
        ["notification-service", "8088", "notification_db", "Alerts"],
    ], col_widths=[4.2 * cm, 1.5 * cm, 2.5 * cm, 4.3 * cm]))

    story.append(PageBreak())

    # ---- 4. MICROSERVICES ----
    story.append(Paragraph("4. Microservices Overview", s["h1"]))
    story.append(Paragraph("4.1 Infrastructure Services", s["h2"]))
    story.append(Paragraph(
        "<b>Discovery Server:</b> All services register on startup. Dashboard at "
        "http://localhost:8761", s["body"]))
    story.append(Paragraph(
        "<b>Config Server:</b> Reads YAML from config-repo/. Each service imports config "
        "via spring.config.import.", s["body"]))
    story.append(Paragraph(
        "<b>API Gateway:</b> Routes /api/customers/** to customer-service, etc. "
        "Uses StripPrefix=1 so /api/customers/1 becomes /customers/1 downstream.",
        s["body"]))

    story.append(Paragraph("4.2 Common Library (common-lib)", s["h2"]))
    story.append(bullet_list([
        "Enums: Role, OrderStatus, DeliveryStatus, PaymentStatus",
        "Exceptions: ResourceNotFoundException, InvalidRequestException, UnauthorizedException",
        "GlobalExceptionHandler with uniform ErrorResponseDto",
    ], s["bullet"]))

    # ---- 5. LAYERED ----
    story.append(Paragraph("5. Layered Architecture (Every Service)", s["h1"]))
    story.append(pre("""
    controller     -> REST endpoints, ResponseEntity, @Valid
         |
    service        -> Interface (business contract)
         |
    serviceImpl    -> Business logic implementation
         |
    repository     -> Spring Data JPA
         |
    entity         -> @Entity (NEVER exposed in API)

    Also: dto/, mapper/, config/, security/, exception/
    """))
    story.append(Paragraph(
        "<b>Rule:</b> Controllers use RequestDto and ResponseDto only. Mappers convert "
        "between Entity and DTO inside the service layer.",
        s["body"]))

    # ---- 6. STRUCTURE ----
    story.append(Paragraph("6. Project Structure", s["h1"]))
    story.append(pre("""
    food-delivery-platform/
    |-- pom.xml                 (parent)
    |-- common-lib/             (shared code)
    |-- config-repo/            (YAML configs)
    |-- discovery-server/
    |-- config-server/
    |-- api-gateway/
    |-- auth-service/
    |-- customer-service/
    |-- restaurant-service/
    |-- menu-service/
    |-- order-service/          (Feign clients in client/)
    |-- delivery-partner-service/
    |-- payment-service/
    |-- notification-service/
    |-- docker-compose.yml
    """))

    # ---- 7. SECURITY ----
    story.append(Paragraph("7. Security and JWT Authentication", s["h1"]))
    story.append(table([
        ["Role", "Purpose"],
        ["ADMIN", "Platform administration"],
        ["CUSTOMER", "Place orders (referenceId = customerId)"],
        ["RESTAURANT_OWNER", "Manage restaurants and menus"],
        ["DELIVERY_PARTNER", "Update delivery status"],
    ], col_widths=[4 * cm, 9.5 * cm]))

    story.append(Paragraph("7.1 Login Flow", s["h2"]))
    story.append(bullet_list([
        "POST /auth/register with email, password, role, referenceId",
        "Password stored with BCryptPasswordEncoder",
        "POST /auth/login returns JWT token",
        "Send header: Authorization: Bearer <token>",
        "JwtAuthenticationFilter validates token on each request",
    ], s["bullet"]))

    story.append(Paragraph("7.2 Sample Auth Response", s["h2"]))
    story.append(pre("""
    {
      "token": "eyJhbGciOiJIUzI1NiIs...",
      "tokenType": "Bearer",
      "userId": 1,
      "email": "john@mail.com",
      "role": "CUSTOMER",
      "referenceId": 1
    }
    """))

    story.append(PageBreak())

    # ---- 8. ENTITIES ----
    story.append(Paragraph("8. Domain Entities and DTOs", s["h1"]))
    story.append(table([
        ["Entity", "Service", "Main Fields"],
        ["User", "auth", "email, password, role, referenceId"],
        ["Customer", "customer", "name, email, phone, address"],
        ["Restaurant", "restaurant", "restaurantName, ownerName, address, rating"],
        ["MenuItem", "menu", "restaurantId, itemName, price, availability"],
        ["Order", "order", "customerId, restaurantId, totalAmount, orderStatus"],
        ["DeliveryPartner", "delivery", "name, phone, vehicleNumber, availabilityStatus"],
        ["Payment", "payment", "orderId, amount, paymentStatus, paymentMethod"],
        ["Notification", "notification", "userId, message, type, sentAt"],
    ], col_widths=[2.8 * cm, 2.5 * cm, 8.2 * cm]))

    story.append(Paragraph("8.1 Status Enums", s["h2"]))
    story.append(table([
        ["Enum", "Values"],
        ["OrderStatus", "PLACED, CONFIRMED, PREPARING, READY, OUT_FOR_DELIVERY, DELIVERED, CANCELLED"],
        ["DeliveryStatus", "ASSIGNED, PICKED_UP, OUT_FOR_DELIVERY, DELIVERED"],
        ["PaymentStatus", "PENDING, SUCCESS, FAILED, REFUNDED"],
    ], col_widths=[3.5 * cm, 10 * cm]))

    # ---- 9. FEIGN ----
    story.append(Paragraph("9. Inter-Service Communication (OpenFeign)", s["h1"]))
    story.append(Paragraph(
        "Only order-service calls other services. All calls use DTOs in package "
        "com.fooddelivery.order.client — never entities.",
        s["body"]))
    story.append(table([
        ["Feign Client", "Target", "Endpoint"],
        ["CustomerClient", "customer-service", "GET /customers/{id}"],
        ["RestaurantClient", "restaurant-service", "GET /restaurants/{id}"],
        ["PaymentClient", "payment-service", "POST /payments/process"],
        ["NotificationClient", "notification-service", "POST /notifications"],
        ["DeliveryPartnerClient", "delivery-partner-service", "POST /delivery-partners/assign"],
    ], col_widths=[3.5 * cm, 3.5 * cm, 6.5 * cm]))

    # ---- 10. FLOWS ----
    story.append(Paragraph("10. Business Flows", s["h1"]))

    story.append(Paragraph("10.1 Customer Registration and Login", s["h2"]))
    story.append(pre("""
    Step 1: POST /api/customers          -> Create customer (get id)
    Step 2: POST /api/auth/register      -> role=CUSTOMER, referenceId=<id>
    Step 3: POST /api/auth/login         -> Get JWT token
    Step 4: Use Bearer token on API calls
    """))

    story.append(Paragraph("10.2 Restaurant and Menu", s["h2"]))
    story.append(pre("""
    Step 1: Register RESTAURANT_OWNER in auth-service
    Step 2: POST /api/restaurants        -> Create restaurant
    Step 3: POST /api/menus              -> Add menu items
    Step 4: PUT /api/menus/{id}          -> Update availability
    """))

    story.append(Paragraph("10.3 Order Placement (Orchestration)", s["h2"]))
    story.append(pre("""
    POST /api/orders
      1. Feign: validate customer exists
      2. Feign: validate restaurant exists
      3. Save order (status = PLACED)
      4. Feign: process payment -> SUCCESS
      5. Update order (status = CONFIRMED)
      6. Feign: send ORDER_PLACED notification
      7. Feign: send ORDER_ACCEPTED notification
    """))

    story.append(Paragraph("10.4 Delivery Flow", s["h2"]))
    story.append(pre("""
    POST /api/orders/{id}/assign-delivery
      -> Assigns nearest available partner (status = ASSIGNED)
      -> Order status = OUT_FOR_DELIVERY

    PATCH /api/delivery-partners/{id}/status
      -> ASSIGNED -> PICKED_UP -> OUT_FOR_DELIVERY -> DELIVERED
    """))

    story.append(PageBreak())

    # ---- 11. APIs ----
    story.append(Paragraph("11. REST API Reference", s["h1"]))
    story.append(Paragraph(
        "Base URL (via Gateway): <b>http://localhost:8080/api</b>",
        s["body"]))

    story.append(Paragraph("11.1 Auth Service", s["h2"]))
    story.append(table([
        ["Method", "Endpoint", "Description"],
        ["POST", "/api/auth/register", "Register with role"],
        ["POST", "/api/auth/login", "Login, get JWT"],
    ], col_widths=[2 * cm, 5 * cm, 6.5 * cm]))

    story.append(Paragraph("11.2 Customer Service", s["h2"]))
    story.append(table([
        ["Method", "Endpoint", "Description"],
        ["POST", "/api/customers", "Create customer"],
        ["GET", "/api/customers/{id}", "Get by ID"],
        ["GET", "/api/customers", "List all"],
        ["PUT", "/api/customers/{id}", "Update"],
        ["DELETE", "/api/customers/{id}", "Delete"],
    ], col_widths=[2 * cm, 5 * cm, 6.5 * cm]))

    story.append(Paragraph("11.3 Restaurant Service", s["h2"]))
    story.append(table([
        ["Method", "Endpoint", "Description"],
        ["POST", "/api/restaurants", "Create"],
        ["GET", "/api/restaurants/{id}", "Get by ID"],
        ["GET", "/api/restaurants", "List all"],
        ["PUT", "/api/restaurants/{id}", "Update"],
        ["DELETE", "/api/restaurants/{id}", "Delete"],
    ], col_widths=[2 * cm, 5 * cm, 6.5 * cm]))

    story.append(Paragraph("11.4 Menu Service", s["h2"]))
    story.append(table([
        ["Method", "Endpoint", "Description"],
        ["POST", "/api/menus", "Create menu item"],
        ["GET", "/api/menus/{id}", "Get item"],
        ["GET", "/api/menus/restaurant/{id}", "Menu by restaurant"],
        ["PUT", "/api/menus/{id}", "Update"],
        ["DELETE", "/api/menus/{id}", "Delete"],
    ], col_widths=[2 * cm, 5.5 * cm, 6 * cm]))

    story.append(Paragraph("11.5 Order Service", s["h2"]))
    story.append(table([
        ["Method", "Endpoint", "Description"],
        ["POST", "/api/orders", "Place order"],
        ["GET", "/api/orders/{id}", "Get order"],
        ["GET", "/api/orders/customer/{id}", "By customer"],
        ["PATCH", "/api/orders/{id}/status", "Update status"],
        ["POST", "/api/orders/{id}/assign-delivery", "Assign partner"],
    ], col_widths=[2 * cm, 5.5 * cm, 6 * cm]))

    story.append(Paragraph("11.6 Other Services", s["h2"]))
    story.append(table([
        ["Method", "Endpoint", "Service"],
        ["POST", "/api/delivery-partners/assign", "Assign partner"],
        ["PATCH", "/api/delivery-partners/{id}/status", "Delivery status"],
        ["POST", "/api/payments/process", "Process payment"],
        ["POST", "/api/notifications", "Send notification"],
    ], col_widths=[2.2 * cm, 5.8 * cm, 5.5 * cm]))

    story.append(Paragraph("11.7 Sample Order Request", s["h2"]))
    story.append(pre("""
    POST http://localhost:8080/api/orders
    Content-Type: application/json

    {
      "customerId": 1,
      "restaurantId": 1,
      "totalAmount": 499.0,
      "paymentMethod": "UPI"
    }
    """))

    # ---- 12. EXCEPTIONS ----
    story.append(Paragraph("12. Exception Handling", s["h1"]))
    story.append(table([
        ["Exception", "HTTP Status"],
        ["ResourceNotFoundException", "404 Not Found"],
        ["InvalidRequestException", "400 Bad Request"],
        ["UnauthorizedException", "401 Unauthorized"],
        ["Validation errors", "400 with field map"],
    ], col_widths=[5.5 * cm, 8 * cm]))

    # ---- 13. DEPLOYMENT ----
    story.append(Paragraph("13. Setup and Deployment", s["h1"]))
    story.append(Paragraph("13.1 Prerequisites", s["h2"]))
    story.append(bullet_list([
        "Java 17+, Maven 3.8+, MySQL 8",
        "Optional: docker-compose up -d for MySQL (root/root)",
    ], s["bullet"]))

    story.append(Paragraph("13.2 Startup Order", s["h2"]))
    story.append(pre("""
    1. docker-compose up -d          (MySQL)
    2. discovery-server              (port 8761)
    3. config-server                 (port 8888)
    4. All business services
    5. api-gateway                   (port 8080)
    """))

    story.append(Paragraph("13.3 Build and Run", s["h2"]))
    story.append(pre("""
    ./mvnw clean install -DskipTests
    ./mvnw -pl order-service spring-boot:run
    """))

    story.append(Paragraph("13.4 Swagger UI", s["h2"]))
    story.append(Paragraph(
        "Each service: http://localhost:{port}/swagger-ui.html",
        s["body"]))

    # ---- 14. LEARNING ----
    story.append(Paragraph("14. Learning Guide", s["h1"]))
    story.append(Paragraph("Recommended study order:", s["h3"]))
    story.append(bullet_list([
        "1. common-lib — shared exceptions and enums",
        "2. customer-service — simplest CRUD layers",
        "3. auth-service — JWT and Spring Security",
        "4. discovery, config, gateway — infrastructure",
        "5. order-service — Feign orchestration",
        "6. delivery-partner-service — status workflow",
    ], s["bullet"]))

    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(
        "Food Delivery Microservices Platform — Documentation v1.0",
        s["footer"]))

    return story


def main():
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Food Delivery Platform Documentation",
        author="Food Delivery Platform",
    )

    def add_page_number(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {canvas.getPageNumber()}")
        canvas.drawString(2 * cm, 1.2 * cm, "Food Delivery Platform — Technical Documentation")
        canvas.restoreState()

    doc.build(build_document(), onFirstPage=add_page_number, onLaterPages=add_page_number)
    size_kb = PDF_PATH.stat().st_size / 1024
    print(f"Readable PDF generated: {PDF_PATH} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
