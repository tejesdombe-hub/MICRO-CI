#!/usr/bin/env python3
"""Generate Microservices Learning PDF mapped to Food Delivery Platform project."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
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
PDF_PATH = DOCS_DIR / "Microservices-Learning-Guide.pdf"

NAVY = colors.HexColor("#0f3460")
ACCENT = colors.HexColor("#e94560")
LIGHT_BG = colors.HexColor("#f0f4f8")
TEXT = colors.HexColor("#1a1a2e")
MUTED = colors.HexColor("#4a5568")
GREEN_BG = colors.HexColor("#e8f5e9")


def build_styles():
    return {
        "cover_title": ParagraphStyle(
            "CoverTitle", fontName="Helvetica-Bold", fontSize=26, leading=32,
            textColor=NAVY, spaceAfter=14),
        "cover_sub": ParagraphStyle(
            "CoverSub", fontName="Helvetica", fontSize=12, leading=17,
            textColor=MUTED, spaceAfter=6),
        "h1": ParagraphStyle(
            "H1", fontName="Helvetica-Bold", fontSize=17, leading=21,
            textColor=NAVY, spaceBefore=18, spaceAfter=10),
        "h2": ParagraphStyle(
            "H2", fontName="Helvetica-Bold", fontSize=13, leading=17,
            textColor=NAVY, spaceBefore=12, spaceAfter=8),
        "h3": ParagraphStyle(
            "H3", fontName="Helvetica-Bold", fontSize=11, leading=14,
            textColor=TEXT, spaceBefore=8, spaceAfter=6),
        "body": ParagraphStyle(
            "Body", fontName="Helvetica", fontSize=10.5, leading=15,
            textColor=TEXT, alignment=TA_JUSTIFY, spaceAfter=8),
        "bullet": ParagraphStyle(
            "Bullet", fontName="Helvetica", fontSize=10, leading=14,
            textColor=TEXT, spaceAfter=4),
        "example": ParagraphStyle(
            "Example", fontName="Helvetica-Oblique", fontSize=10, leading=14,
            textColor=MUTED, leftIndent=10, spaceAfter=8),
        "code": ParagraphStyle(
            "Code", fontName="Courier", fontSize=8.5, leading=11,
            textColor=colors.HexColor("#2d3748"), backColor=LIGHT_BG,
            leftIndent=6, spaceBefore=4, spaceAfter=8),
        "toc": ParagraphStyle(
            "TOC", fontName="Helvetica", fontSize=11, leading=20, textColor=TEXT),
        "footer": ParagraphStyle(
            "Footer", fontName="Helvetica-Oblique", fontSize=9,
            textColor=MUTED, alignment=TA_CENTER),
    }


def table(data, col_widths=None):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (-1, -1), TEXT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
    ]))
    return t


def bullets(items, style):
    return ListFlowable(
        [ListItem(Paragraph(i, style), leftIndent=10) for i in items],
        bulletType="bullet", start="•")


def pre(text):
    return Preformatted(text.strip(), build_styles()["code"])


def project_box(text, s):
    return Paragraph(
        f'<font color="#0f3460"><b>In our project:</b></font> {text}',
        s["example"])


def build_story():
    s = build_styles()
    story = []

    # COVER
    story.append(Spacer(1, 2.5 * cm))
    story.append(Paragraph("MICROSERVICES LEARNING GUIDE", ParagraphStyle(
        "badge", fontName="Helvetica-Bold", fontSize=10, textColor=ACCENT, spaceAfter=14)))
    story.append(Paragraph("Concepts Explained Through the Food Delivery Platform", s["cover_title"]))
    story.append(Paragraph(
        "Theory + real examples from the Java 17 / Spring Boot 3 project you built "
        "(Zomato/Swiggy-style microservices)", s["cover_sub"]))
    story.append(Spacer(1, 1 * cm))
    for line in [
        "<b>Topics:</b> Monolith vs Microservices, Benefits, Challenges, Service Boundaries,",
        "Single Responsibility, Database per Service, Inter-Service Communication",
        "<b>Project:</b> food-delivery-platform — 11 microservices + API Gateway + Eureka + MySQL",
    ]:
        story.append(Paragraph(line, s["cover_sub"]))
    story.append(PageBreak())

    # TOC
    story.append(Paragraph("Table of Contents", s["h1"]))
    for i, t in enumerate([
        "1. What Are Microservices?",
        "2. Monolith vs Microservices",
        "3. Benefits of Microservices",
        "4. Challenges of Microservices",
        "5. Identifying Service Boundaries (Business Domains)",
        "6. Single Responsibility Principle in Service Design",
        "7. Database per Service",
        "8. Communication Between Services",
        "9. When NOT to Use Microservices",
        "10. Quick Reference — Our Project Map",
    ], 1):
        story.append(Paragraph(f"{i}. {t}", s["toc"]))
    story.append(PageBreak())

    # 1. WHAT ARE MICROSERVICES
    story.append(Paragraph("1. What Are Microservices?", s["h1"]))
    story.append(Paragraph(
        "<b>Microservices</b> is an architectural style where an application is built as a "
        "collection of <b>small, independent services</b>. Each service:",
        s["body"]))
    story.append(bullets([
        "Runs in its own process",
        "Owns a focused business capability",
        "Can be developed, deployed, and scaled independently",
        "Communicates with others over the network (usually HTTP/REST)",
    ], s["bullet"]))
    story.append(Paragraph("<b>Why are they used?</b>", s["h3"]))
    story.append(bullets([
        "Large systems become too big to maintain as one codebase (monolith)",
        "Different parts of the business change at different speeds",
        "Teams need to deploy without waiting for the entire application",
        "Scale only the busy parts (e.g. order service during peak hours)",
    ], s["bullet"]))
    story.append(project_box(
        "We split the food delivery app into 11 services: Auth, Customer, Restaurant, Menu, "
        "Order, Delivery Partner, Payment, Notification, plus Discovery, Config, and API Gateway. "
        "Each is a separate Spring Boot application with its own JAR and port.",
        s))

    # 2. MONOLITH VS MICROSERVICES
    story.append(Paragraph("2. Monolith vs Microservices", s["h1"]))
    story.append(table([
        ["Aspect", "Monolith (single app)", "Microservices (our project)"],
        ["Structure", "One codebase, one deployment", "Many repos/modules, many deployments"],
        ["Database", "Usually one shared database", "Database per service (8 MySQL DBs)"],
        ["Scaling", "Scale entire application", "Scale only order-service if orders spike"],
        ["Technology", "One stack for everything", "Can mix stacks per service (we use Java 17)"],
        ["Failure", "Bug can crash whole system", "Payment down; customers may still browse menus"],
        ["Complexity", "Simpler to start", "Needs Gateway, Eureka, Config, Feign"],
    ], col_widths=[3 * cm, 5 * cm, 5.5 * cm]))
    story.append(pre("""
    MONOLITH                         MICROSERVICES (Our Project)
    +------------------+             +----------+  +----------+
    |  One Big App     |             |  Auth    |  | Customer |
    |  - Auth          |             +----------+  +----------+
    |  - Orders        |                    \\         /
    |  - Payments      |             +---------------------+
    |  - Everything    |             |    API Gateway      |
    +------------------+             +---------------------+
         |  One DB                         | Feign / REST
         v                                 v
    [ single MySQL ]              [ auth_db | order_db | ... ]
    """))
    story.append(project_box(
        "If this were a monolith, all controllers would live in one project with one MySQL schema. "
        "Instead, OrderController is only in order-service, and Payment logic is only in payment-service.",
        s))

    story.append(PageBreak())

    # 3. BENEFITS
    story.append(Paragraph("3. Benefits of Microservices", s["h1"]))

    story.append(Paragraph("3.1 Scalability", s["h2"]))
    story.append(Paragraph(
        "You can run <b>more instances</b> of only the services under heavy load. "
        "Eureka registers multiple instances; the API Gateway load-balances requests.",
        s["body"]))
    story.append(project_box(
        "During lunch rush, you could run 5 instances of order-service and 1 instance of "
        "notification-service. Eureka + Gateway (lb://order-service) distribute traffic automatically.",
        s))

    story.append(Paragraph("3.2 Independent Deployment", s["h2"]))
    story.append(Paragraph(
        "Change payment logic and deploy <b>only payment-service</b> without redeploying "
        "customer, restaurant, or menu services.",
        s["body"]))
    story.append(project_box(
        "Docker: docker compose build payment-service && docker compose up -d payment-service. "
        "Other containers keep running. No full-system downtime.",
        s))

    story.append(Paragraph("3.3 Fault Isolation", s["h2"]))
    story.append(Paragraph(
        "If one service fails, others may continue working (if designed with fallbacks). "
        "A crash in notification-service should not take down customer registration.",
        s["body"]))
    story.append(project_box(
        "If notification-service is down, order placement might fail at the Feign call unless "
        "you add circuit breakers (Resilience4j — future improvement). Today, order-service "
        "depends on notification for success — a real trade-off to study.",
        s))

    story.append(Paragraph("3.4 Team Autonomy", s["h2"]))
    story.append(Paragraph(
        "Team A owns Restaurant + Menu; Team B owns Order + Delivery. Each team chooses "
        "release cycles, coding standards within shared rules, and owns their database.",
        s["body"]))
    story.append(project_box(
        "Folder structure mirrors ownership: restaurant-service/ and menu-service/ are separate "
        "Maven modules. Teams commit independently to the monorepo or separate repos.",
        s))

    # 4. CHALLENGES
    story.append(Paragraph("4. Challenges of Microservices", s["h1"]))

    story.append(Paragraph("4.1 Complexity", s["h2"]))
    story.append(Paragraph(
        "You manage many services, configs, deployments, and versions instead of one application.",
        s["body"]))
    story.append(project_box(
        "We need: Eureka (8761), Config Server (8888), API Gateway (8080), MySQL, Docker Compose, "
        "8 business services, JWT, Feign clients. A monolith would need only one application.yml.",
        s))

    story.append(Paragraph("4.2 Network Latency", s["h2"]))
    story.append(Paragraph(
        "Every call between services is an HTTP request over the network — slower than "
        "an in-process method call inside a monolith.",
        s["body"]))
    story.append(project_box(
        "POST /orders triggers 4+ Feign calls (customer, restaurant, payment, notification). "
        "Each adds milliseconds. Acceptable for most apps; problematic for ultra-low latency.",
        s))

    story.append(Paragraph("4.3 Data Consistency", s["h2"]))
    story.append(Paragraph(
        "No single database transaction across services. You cannot easily do "
        "ACID across order_db and payment_db. Patterns: Saga, eventual consistency, outbox.",
        s["body"]))
    story.append(project_box(
        "Order is saved, then payment is processed. If payment fails after order save, "
        "you need compensation logic (cancel order) — we simulate payment as always SUCCESS. "
        "Production needs Saga or two-phase patterns.",
        s))

    story.append(Paragraph("4.4 Monitoring", s["h2"]))
    story.append(Paragraph(
        "You must trace requests across services (correlation IDs, distributed tracing). "
        "Logs are scattered across 11 containers.",
        s["body"]))
    story.append(project_box(
        "docker compose logs order-service shows order flow; payment logs are separate. "
        "Tools like Zipkin, ELK, or Grafana Loki are added in production.",
        s))

    story.append(PageBreak())

    # 5. SERVICE BOUNDARIES
    story.append(Paragraph("5. Identifying Service Boundaries Using Business Domains", s["h1"]))
    story.append(Paragraph(
        "Split services by <b>business capability</b> (Domain-Driven Design), not by technical layers. "
        "Ask: \"What does the business do?\" not \"Where should controllers go?\"",
        s["body"]))
    story.append(table([
        ["Business Domain", "Service", "Why separate?"],
        ["Identity & login", "auth-service", "Security is a distinct concern"],
        ["Customer profiles", "customer-service", "User data lifecycle"],
        ["Restaurants", "restaurant-service", "Supply side of marketplace"],
        ["Menus", "menu-service", "Changes often; tied to restaurant but own data"],
        ["Orders", "order-service", "Core workflow; orchestrates others"],
        ["Delivery", "delivery-partner-service", "Logistics domain"],
        ["Payments", "payment-service", "PCI, refunds, gateways — isolate risk"],
        ["Notifications", "notification-service", "Email/SMS/push — cross-cutting"],
    ], col_widths=[3.5 * cm, 4 * cm, 5.5 * cm]))
    story.append(project_box(
        "Wrong boundary: \"database-service\" or \"controller-service\" (technical split). "
        "Right boundary: \"menu-service\" owns menu items because the business thinks in menus.",
        s))

    # 6. SRP
    story.append(Paragraph("6. Single Responsibility Principle in Service Design", s["h1"]))
    story.append(Paragraph(
        "<b>SRP:</b> A service should have only one reason to change. One cohesive business responsibility.",
        s["body"]))
    story.append(bullets([
        "payment-service changes when payment rules change — not when menu UI changes",
        "menu-service changes when menu fields change — not when JWT format changes",
        "auth-service only handles register, login, JWT — not order placement",
    ], s["bullet"]))
    story.append(project_box(
        "Each service has one main package job: CustomerServiceImpl only manages customers. "
        "OrderServiceImpl places orders but does NOT store payment rows — it calls payment-service.",
        s))

    # 7. DATABASE PER SERVICE
    story.append(Paragraph("7. Database per Service Concept", s["h1"]))
    story.append(Paragraph(
        "Each microservice has its <b>own private database</b>. No other service may access "
        "that database directly. Data is shared only via APIs (REST/Feign).",
        s["body"]))
    story.append(table([
        ["Service", "Database", "Tables (examples)"],
        ["auth-service", "auth_db", "users"],
        ["customer-service", "customer_db", "customers"],
        ["restaurant-service", "restaurant_db", "restaurants"],
        ["menu-service", "menu_db", "menu_items"],
        ["order-service", "order_db", "orders"],
        ["delivery-partner-service", "delivery_db", "delivery_partners"],
        ["payment-service", "payment_db", "payments"],
        ["notification-service", "notification_db", "notifications"],
    ], col_widths=[4 * cm, 3 * cm, 6.5 * cm]))
    story.append(Paragraph("<b>Config location in our project:</b>", s["h3"]))
    story.append(bullets([
        "config-repo/auth-service.yml — jdbc:mysql://.../auth_db",
        "config-repo/application.yml — shared username/password, JPA ddl-auto: update",
        "docker-compose.yml — SPRING_DATASOURCE_URL per service (Docker hostname mysql)",
        "docker/mysql/init-databases.sql — creates all 8 databases",
    ], s["bullet"]))
    story.append(project_box(
        "Access from your PC (Docker): localhost:3307, user root, password root. "
        "Services inside Docker use mysql:3306. You cannot JOIN customers table from order_db.",
        s))

    story.append(PageBreak())

    # 8. COMMUNICATION
    story.append(Paragraph("8. Communication Between Services (High-Level)", s["h1"]))
    story.append(Paragraph("<b>Types of communication:</b>", s["h3"]))
    story.append(table([
        ["Type", "Description", "In our project"],
        ["Synchronous", "Caller waits for response (HTTP)", "OpenFeign REST calls"],
        ["Asynchronous", "Message queue; caller does not wait", "Not used (could add Kafka)"],
        ["Client → Gateway", "Single entry point", "API Gateway :8080"],
        ["Service discovery", "Find service instances", "Eureka :8761"],
    ], col_widths=[3 * cm, 5 * cm, 5.5 * cm]))
    story.append(pre("""
    Client  -->  API Gateway (8080)  -->  customer-service
                                    -->  order-service
                                              |
                                              | Feign (HTTP + DTO only)
                                              v
                         +--------+--------+--------+--------+
                         |Customer|Restau- |Payment |Notifi- |
                         |Service |rant    |Service |cation  |
                         +--------+--------+--------+--------+

    Rules we follow:
    - No entity shared between services
    - Feign uses Request/Response DTOs only
    - No direct database access across services
    """))
    story.append(Paragraph("<b>Order placement — Feign chain:</b>", s["h3"]))
    story.append(bullets([
        "1. GET customer-service — validate customerId",
        "2. GET restaurant-service — validate restaurantId",
        "3. SAVE order in order_db",
        "4. POST payment-service — process payment",
        "5. POST notification-service — ORDER_PLACED, ORDER_ACCEPTED",
    ], s["bullet"]))
    story.append(project_box(
        "Feign interfaces live in order-service/client/: CustomerClient, RestaurantClient, "
        "PaymentClient, NotificationClient, DeliveryPartnerClient. @FeignClient(name = \"customer-service\").",
        s))

    # 9. WHEN NOT TO USE
    story.append(Paragraph("9. When NOT to Use Microservices", s["h1"]))
    story.append(bullets([
        "<b>Small project / startup MVP</b> — monolith is faster to build and deploy",
        "<b>Tiny team (1–3 developers)</b> — operational overhead of 11 services is too much",
        "<b>Simple CRUD app</b> — no need for distributed complexity",
        "<b>Strong ACID across everything</b> — bank transfer style transactions need one DB",
        "<b>No DevOps maturity</b> — Docker, monitoring, CI/CD not ready",
        "<b>Unclear domain boundaries</b> — you will split wrong and regret it",
    ], s["bullet"]))
    story.append(project_box(
        "A college assignment or food delivery prototype with 2 developers could start as a "
        "monolith. We chose microservices to <b>learn</b> enterprise patterns — that is a valid "
        "educational reason, even if a monolith would ship faster for production v1.",
        s))

    # 10. PROJECT MAP
    story.append(Paragraph("10. Quick Reference — Our Project Map", s["h1"]))
    story.append(table([
        ["Concept", "Where to see it in project"],
        ["Microservices", "11 modules in pom.xml &lt;modules&gt;"],
        ["API Gateway", "api-gateway/ — routes in application.yml"],
        ["Service Discovery", "discovery-server/ — Eureka UI :8761"],
        ["Config Server", "config-server/ + config-repo/"],
        ["Database per service", "config-repo/*-service.yml + 8 MySQL DBs"],
        ["Feign communication", "order-service/.../client/*.java"],
        ["DTO boundary", "*/dto/*RequestDto.java, *ResponseDto.java"],
        ["Layered architecture", "controller / service / repository per service"],
        ["JWT Security", "auth-service/security/"],
        ["Swagger testing", "http://localhost:8080/swagger-ui.html"],
        ["Docker run", "docker-compose.yml, DOCKER.md"],
    ], col_widths=[4.5 * cm, 9 * cm]))

    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph(
        "Study path: Read this PDF → Explore Eureka → Test Swagger (SWAGGER-TESTING.md) → "
        "Read OrderServiceImpl (Feign) → Connect MySQL on port 3307 and view tables.",
        s["body"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "Food Delivery Platform — Microservices Learning Guide",
        s["footer"]))

    return story


def main():
    doc = SimpleDocTemplate(
        str(PDF_PATH), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="Microservices Learning Guide",
    )

    def page_footer(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {canvas.getPageNumber()}")
        canvas.drawString(2 * cm, 1.2 * cm, "Microservices Learning Guide — Food Delivery Platform")
        canvas.restoreState()

    doc.build(build_story(), onFirstPage=page_footer, onLaterPages=page_footer)
    print(f"PDF generated: {PDF_PATH} ({PDF_PATH.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
