#!/usr/bin/env python3
"""
Generate comprehensive Food Delivery Platform documentation PDF including
Skill Specification, README, Docker Guide, and Resilience Patterns.
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
PROJECT_DIR = DOCS_DIR.parent
PDF_PATH = DOCS_DIR / "FoodFlow-Platform-Comprehensive-Documentation.pdf"

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

    # ---- COVER ----
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph("FOODFLOW PLATFORM", ParagraphStyle(
        "badge", fontName="Helvetica-Bold", fontSize=10, textColor=ACCENT, spaceAfter=16)))
    story.append(Paragraph("Comprehensive Technical Documentation", s["cover_title"]))
    story.append(Paragraph(
        "Enterprise Microservices Backend — Architecture, APIs, Security, Resilience Patterns & Deployment",
        s["cover_sub"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "Zomato / Swiggy-style system built with Java 17 and Spring Boot 3",
        s["cover_sub"]))
    story.append(Spacer(1, 2 * cm))
    for line in [
        "<b>Project:</b> FoodFlow — Food Delivery Backend",
        "<b>Architecture:</b> Microservices (Spring Cloud)",
        "<b>Language:</b> Java 17",
        "<b>Framework:</b> Spring Boot 3.x",
        "<b>Services:</b> 12 (11 microservices + common-lib)",
        "<b>Stack:</b> Spring Cloud, Eureka, JWT, MySQL, OpenFeign, Resilience4j",
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
        "13. Docker Deployment",
        "14. Resilience Patterns in Microservices",
        "15. Circuit Breaker Pattern",
        "16. Resilience4j Configuration",
        "17. Monitoring and Best Practices",
        "18. Setup and Deployment Guide",
    ]
    for item in toc_items:
        story.append(Paragraph(item, s["toc"]))
    story.append(PageBreak())

    # ---- 1. EXECUTIVE SUMMARY ----
    story.append(Paragraph("1. Executive Summary", s["h1"]))
    story.append(Paragraph(
        "FoodFlow is an enterprise-grade Food Delivery Microservices Backend similar in "
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
        "Resilience patterns using Resilience4j for fault tolerance.",
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
        ["Resilience", "Resilience4j", "2.1.0"],
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
  Auth  Customer Rest.  Menu  Order  Payment
  :8081  :8082   :8083  :8084 :8085  :8087
    |      |       |      |      |      |
    +------+------+------+------+------+
           |
    +------+------+------+
    v      v      v
  Eureka Config MySQL
  :8761  :8888  :3306
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
        "GlobalExceptionHandler with uniform ApiResponse<T>",
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

    Also: dto/, mapper/, config/, security/, exception/, client/
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
    |-- Dockerfile
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

    story.append(Paragraph("7.2 JWT Token Contract", s["h2"]))
    story.append(pre("""
    Claims:
      sub         = user email (String)
      role        = "ROLE_CUSTOMER" | "ROLE_ADMIN" | "ROLE_RESTAURANT_OWNER" | "ROLE_DELIVERY_PARTNER"
      userId      = Long (maps to auth_users table)
      referenceId = Long (customerId / restaurantId / partnerId — 0 for ADMIN)
      iat         = issued at
      exp         = expiry (configurable, default 24h)

    Header forwarded by Gateway:
      X-Auth-User-Id       : userId value
      X-Auth-User-Role     : role value
      X-Auth-Reference-Id  : referenceId value
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
        ["OrderStatus", "PLACED, CONFIRMED, PREPARING, READY_FOR_PICKUP, PICKED_UP, OUT_FOR_DELIVERY, DELIVERED, DELIVERY_FAILED, CANCELLED"],
        ["DeliveryStatus", "ASSIGNED, PICKED_UP, OUT_FOR_DELIVERY, DELIVERED, DELIVERY_FAILED, REASSIGNED"],
        ["PaymentStatus", "PENDING, SUCCESS, FAILED, REFUNDED"],
    ], col_widths=[3.5 * cm, 10 * cm]))

    # ---- 9. FEIGN ----
    story.append(Paragraph("9. Inter-Service Communication (OpenFeign)", s["h1"]))
    story.append(Paragraph(
        "Order service orchestrates other services using Feign. All calls use DTOs in package "
        "client/ — never entities.",
        s["body"]))
    story.append(table([
        ["Feign Client", "Target", "Endpoint"],
        ["CustomerServiceClient", "customer-service", "GET /api/v1/customers/{id}"],
        ["RestaurantServiceClient", "restaurant-service", "GET /api/v1/restaurants/{id}"],
        ["MenuServiceClient", "menu-service", "POST /api/v1/menu/validate"],
        ["PaymentServiceClient", "payment-service", "POST /api/v1/payments"],
        ["NotificationServiceClient", "notification-service", "POST /api/v1/notifications"],
        ["DeliveryServiceClient", "delivery-partner-service", "POST /api/v1/delivery-partners/assign"],
    ], col_widths=[4 * cm, 3.5 * cm, 6.5 * cm]))

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
      1. Feign: validate customer exists (customer-service)
      2. Feign: validate restaurant exists (restaurant-service)
      3. Feign: validate menu items (menu-service)
      4. Save order (status = PLACED)
      5. Feign: process payment (payment-service) -> SUCCESS/FAILED
      6. On SUCCESS: keep status PLACED, trigger notification
      7. On FAILED: set status CANCELLED, trigger notification
      8. Feign: send notification (notification-service)
    """))

    story.append(Paragraph("10.4 Delivery Flow", s["h2"]))
    story.append(pre("""
    POST /api/orders/{id}/assign-delivery
      -> Assigns nearest available partner (status = ASSIGNED)
      -> Order status = OUT_FOR_DELIVERY

    PATCH /api/delivery-partners/{id}/status
      -> ASSIGNED -> PICKED_UP -> OUT_FOR_DELIVERY -> DELIVERED
      -> Or DELIVERY_FAILED -> REASSIGNED
    """))

    story.append(PageBreak())

    # ---- 11. APIs ----
    story.append(Paragraph("11. REST API Reference", s["h1"]))
    story.append(Paragraph(
        "Base URL (via Gateway): <b>http://localhost:8080/api/v1</b>",
        s["body"]))

    story.append(Paragraph("11.1 Auth Service", s["h2"]))
    story.append(table([
        ["Method", "Endpoint", "Description"],
        ["POST", "/api/v1/auth/register", "Register with role"],
        ["POST", "/api/v1/auth/login", "Login, get JWT"],
    ], col_widths=[2 * cm, 5 * cm, 6.5 * cm]))

    story.append(Paragraph("11.2 Customer Service", s["h2"]))
    story.append(table([
        ["Method", "Endpoint", "Description"],
        ["POST", "/api/v1/customers", "Create customer"],
        ["GET", "/api/v1/customers/{id}", "Get by ID"],
        ["GET", "/api/v1/customers", "List all (paginated)"],
        ["PUT", "/api/v1/customers/{id}", "Update"],
        ["DELETE", "/api/v1/customers/{id}", "Delete"],
    ], col_widths=[2 * cm, 5 * cm, 6.5 * cm]))

    story.append(Paragraph("11.3 Restaurant Service", s["h2"]))
    story.append(table([
        ["Method", "Endpoint", "Description"],
        ["POST", "/api/v1/restaurants", "Create"],
        ["GET", "/api/v1/restaurants/{id}", "Get by ID"],
        ["GET", "/api/v1/restaurants", "List all"],
        ["PUT", "/api/v1/restaurants/{id}", "Update"],
        ["DELETE", "/api/v1/restaurants/{id}", "Delete"],
    ], col_widths=[2 * cm, 5 * cm, 6.5 * cm]))

    story.append(Paragraph("11.4 Menu Service", s["h2"]))
    story.append(table([
        ["Method", "Endpoint", "Description"],
        ["POST", "/api/v1/menus", "Create menu item"],
        ["GET", "/api/v1/menus/{id}", "Get item"],
        ["GET", "/api/v1/menus/restaurant/{id}", "Menu by restaurant"],
        ["PUT", "/api/v1/menus/{id}", "Update"],
        ["DELETE", "/api/v1/menus/{id}", "Delete"],
    ], col_widths=[2 * cm, 5.5 * cm, 6 * cm]))

    story.append(Paragraph("11.5 Order Service", s["h2"]))
    story.append(table([
        ["Method", "Endpoint", "Description"],
        ["POST", "/api/v1/orders", "Place order"],
        ["GET", "/api/v1/orders/{id}", "Get order"],
        ["GET", "/api/v1/orders/customer/{id}", "By customer"],
        ["PATCH", "/api/v1/orders/{id}/status", "Update status"],
        ["POST", "/api/v1/orders/{id}/assign-delivery", "Assign partner"],
    ], col_widths=[2 * cm, 5.5 * cm, 6 * cm]))

    story.append(Paragraph("11.6 Universal Response Envelope", s["h2"]))
    story.append(pre("""
    // Success
    {
      "success": true,
      "message": "Customer retrieved successfully",
      "data": { ... },
      "timestamp": "2024-01-15T10:30:00Z"
    }

    // Error
    {
      "success": false,
      "message": "Customer not found with id: 42",
      "data": null,
      "timestamp": "2024-01-15T10:30:00Z",
      "errors": ["field: validation message"]
    }
    """))

    # ---- 12. EXCEPTIONS ----
    story.append(Paragraph("12. Exception Handling", s["h1"]))
    story.append(table([
        ["Exception", "HTTP Status"],
        ["ResourceNotFoundException", "404 Not Found"],
        ["InvalidRequestException", "400 Bad Request"],
        ["UnauthorizedException", "403 Forbidden"],
        ["MethodArgumentNotValidException", "400 with field errors"],
        ["Exception (catch-all)", "500 Internal Server Error"],
    ], col_widths=[5.5 * cm, 8 * cm]))

    story.append(PageBreak())

    # ---- 13. DOCKER ----
    story.append(Paragraph("13. Docker Deployment", s["h1"]))
    story.append(Paragraph(
        "Docker Compose runs the entire platform in containers, avoiding port conflicts. "
        "Only ports 8080, 8761, 8888, and 3307 are exposed on the host.",
        s["body"]))

    story.append(Paragraph("13.1 Container Overview", s["h2"]))
    story.append(table([
        ["Container", "Host Port", "Internal Only"],
        ["fd-mysql", "3307", "No"],
        ["fd-discovery", "8761", "No"],
        ["fd-config", "8888", "No"],
        ["fd-gateway", "8080", "No"],
        ["fd-auth", "-", "Yes"],
        ["fd-customer", "-", "Yes"],
        ["fd-restaurant", "-", "Yes"],
        ["fd-menu", "-", "Yes"],
        ["fd-order", "-", "Yes"],
        ["fd-delivery", "-", "Yes"],
        ["fd-payment", "-", "Yes"],
        ["fd-notification", "-", "Yes"],
    ], col_widths=[3.5 * cm, 2.5 * cm, 5.5 * cm]))

    story.append(Paragraph("13.2 Quick Start", s["h2"]))
    story.append(pre("""
    chmod +x docker-start.sh
    ./docker-start.sh

    Or manually:
    docker compose build
    docker compose up -d
    """))

    story.append(Paragraph("13.3 Startup Order", s["h2"]))
    story.append(bullet_list([
        "MySQL (healthy check)",
        "Eureka discovery-server (healthy)",
        "Config server (healthy, mounts config-repo/)",
        "All business services (parallel)",
        "API Gateway (last)",
    ], s["bullet"]))

    story.append(Paragraph("13.4 Useful Commands", s["h2"]))
    story.append(pre("""
    docker compose ps                    # Status of all containers
    docker compose logs -f order-service # Logs for one service
    docker compose restart order-service # Restart one service
    docker compose down                  # Stop everything
    docker compose down -v               # Stop and remove database volume
    """))

    # ---- 14. RESILIENCE PATTERNS ----
    story.append(Paragraph("14. Resilience Patterns in Microservices", s["h1"]))
    story.append(Paragraph(
        "Resilience is the ability of a system to continue functioning correctly even when "
        "some of its components fail or experience degraded performance.",
        s["body"]))

    story.append(Paragraph("14.1 What is Resilience", s["h2"]))
    story.append(bullet_list([
        "Services are distributed and communicate over the network",
        "Each service has its own failure domain",
        "A single service failure can cascade to dependent services",
        "Network latency and timeouts are inherent in distributed systems",
    ], s["bullet"]))

    story.append(Paragraph("14.2 Problems Caused by Cascading Failures", s["h2"]))
    story.append(Paragraph(
        "Cascading failures occur when a failure in one service triggers failures in "
        "dependent services, creating a domino effect that can bring down the entire system.",
        s["body"]))
    story.append(pre("""
    Example Scenario:
    Payment Service slows down → Order Service threads block waiting
    → Order Service thread pool exhausts → API Gateway requests timeout
    → Customer retries → More requests flood the system
    → All services become unresponsive → System-wide outage
    """))

    story.append(Paragraph("14.3 When a Dependent Service is Slow or Down", s["h2"]))
    story.append(table([
        ["Condition", "Impact"],
        ["Service DOWN", "Connection timeouts, Feign throws ConnectException, threads block indefinitely"],
        ["Service SLOW", "High latency, backpressure builds up, resource pools exhausted"],
    ], col_widths=[3 * cm, 10 * cm]))

    story.append(PageBreak())

    # ---- 15. CIRCUIT BREAKER ----
    story.append(Paragraph("15. Circuit Breaker Pattern", s["h1"]))
    story.append(Paragraph(
        "The Circuit Breaker pattern prevents cascading failures by detecting when a dependent "
        "service is failing and temporarily blocking calls to it.",
        s["body"]))

    story.append(Paragraph("15.1 How It Works", s["h2"]))
    story.append(bullet_list([
        "Monitor calls to a dependent service",
        "Count failures over a sliding time window",
        "When failure threshold is reached, trip the circuit (OPEN state)",
        "Block all calls immediately (fail fast)",
        "After wait duration, attempt a single call (HALF-OPEN state)",
        "If successful, reset to CLOSED; if failed, stay OPEN",
    ], s["bullet"]))

    story.append(Paragraph("15.2 Circuit Breaker States", s["h2"]))
    story.append(table([
        ["State", "Description"],
        ["CLOSED", "Normal operation - all requests pass through, failure rate monitored"],
        ["OPEN", "Circuit tripped - all requests blocked, fallback invoked, wait timer starts"],
        ["HALF-OPEN", "Recovery attempt - single test call allowed to check if service recovered"],
    ], col_widths=[3 * cm, 10 * cm]))

    story.append(Paragraph("15.3 Retry vs Circuit Breaker", s["h2"]))
    story.append(table([
        ["Aspect", "Retry Pattern", "Circuit Breaker Pattern"],
        ["Purpose", "Handle transient failures", "Prevent cascading failures"],
        ["When to use", "Network glitches, temporary timeouts", "Service down, persistent failures"],
        ["Behavior", "Re-attempt the same request", "Block requests to failing service"],
        ["Resource usage", "Increases load (more requests)", "Decreases load (blocks requests)"],
    ], col_widths=[3 * cm, 4.5 * cm, 5.5 * cm]))

    # ---- 16. RESILIENCE4J ----
    story.append(Paragraph("16. Resilience4j Configuration", s["h1"]))
    story.append(Paragraph(
        "Resilience4j is a fault tolerance library for Java that implements several resilience patterns.",
        s["body"]))

    story.append(Paragraph("16.1 Patterns Provided", s["h2"]))
    story.append(bullet_list([
        "Circuit Breaker: Prevent cascading failures",
        "Retry: Handle transient failures",
        "Rate Limiter: Control request rate",
        "Bulkhead: Limit concurrent calls",
        "Time Limiter: Cancel long-running operations",
        "Cache: Cache responses to reduce load",
    ], s["bullet"]))

    story.append(Paragraph("16.2 Circuit Breaker Configuration", s["h2"]))
    story.append(pre("""
    resilience4j:
      circuitbreaker:
        instances:
          paymentService:
            slidingWindowSize: 10              # Number of calls in sliding window
            minimumNumberOfCalls: 5            # Minimum calls before calculating rate
            failureRateThreshold: 50           # Failure percentage to trip (50%)
            waitDurationInOpenState: 60s      # Time in OPEN before HALF-OPEN
            permittedNumberOfCallsInHalfOpenState: 3  # Test calls in HALF-OPEN
            slowCallRateThreshold: 100         # Slow call rate threshold
            slowCallDurationThreshold: 2s      # What qualifies as "slow"
    """))

    story.append(Paragraph("16.3 Implementing Fallback Methods", s["h2"]))
    story.append(pre("""
    @Component
    @Slf4j
    public class PaymentServiceClientFallback implements PaymentServiceClient {
        @Override
        public ApiResponse<PaymentResponseDto> createPayment(PaymentRequestDto dto) {
            log.error("Payment service unavailable, using fallback");
            return ApiResponse.<PaymentResponseDto>error(
                "Payment service temporarily unavailable. Please try again later.",
                List.of("PAYMENT_SERVICE_UNAVAILABLE")
            );
        }
    }
    """))

    story.append(PageBreak())

    # ---- 17. MONITORING ----
    story.append(Paragraph("17. Monitoring and Best Practices", s["h1"]))

    story.append(Paragraph("17.1 Circuit Breaker Metrics", s["h2"]))
    story.append(bullet_list([
        "Circuit state (CLOSED, OPEN, HALF-OPEN)",
        "Failure rate",
        "Success rate",
        "Number of buffered calls",
        "Number of failed calls",
        "Number of slow calls",
    ], s["bullet"]))

    story.append(Paragraph("17.2 Actuator Endpoints", s["h2"]))
    story.append(pre("""
    GET /actuator/circuitbreakers
    GET /actuator/metrics/resilience4j.circuitbreaker.state
    GET /actuator/metrics/resilience4j.circuitbreaker.failure.rate
    GET /actuator/prometheus
    """))

    story.append(Paragraph("17.3 Common Configuration Mistakes", s["h2"]))
    story.append(table([
        ["Mistake", "Impact", "Fix"],
        ["Failure threshold too high (90%)", "Too many failures before circuit opens", "Use 50-60% threshold"],
        ["Wait duration too short (5s)", "Circuit flips rapidly", "Use 30-60 seconds minimum"],
        ["No timeout on Feign clients", "Threads block indefinitely", "Always set connect and read timeouts"],
        ["Retry without exponential backoff", "Retry storms overwhelm service", "Use exponential backoff"],
        ["Circuit breaker on non-critical paths", "Unnecessary complexity", "Use fallback only"],
    ], col_widths=[4 * cm, 4 * cm, 5.5 * cm]))

    story.append(Paragraph("17.4 When NOT to Use Retry", s["h2"]))
    story.append(bullet_list([
        "Non-idempotent operations (POST without idempotency key)",
        "Business logic failures (insufficient funds, invalid data)",
        "Authentication failures (wrong password)",
        "Rate limit exceeded (429 status)",
        "Validation errors (400 status)",
    ], s["bullet"]))

    story.append(Paragraph("17.5 Best Practices Summary", s["h2"]))
    story.append(bullet_list([
        "Use Circuit Breaker for all cross-service calls",
        "Use Retry only for transient network failures",
        "Always configure timeouts on Feign clients",
        "Implement meaningful fallbacks (not just null returns)",
        "Monitor circuit state and metrics",
        "Test failure scenarios in integration tests",
        "Don't over-engineer for non-critical paths",
    ], s["bullet"]))

    # ---- 18. SETUP ----
    story.append(Paragraph("18. Setup and Deployment Guide", s["h1"]))

    story.append(Paragraph("18.1 Prerequisites", s["h2"]))
    story.append(bullet_list([
        "Java 17+, Maven 3.8+, MySQL 8",
        "Docker Engine 20+, Docker Compose v2 (for Docker deployment)",
        "8 GB+ RAM recommended (11 JVMs for Docker)",
    ], s["bullet"]))

    story.append(Paragraph("18.2 Local Maven Startup", s["h2"]))
    story.append(pre("""
    # Start MySQL
    docker compose up -d mysql

    # Build project
    ./mvnw clean install -DskipTests

    # Start services (order matters)
    ./mvnw -pl discovery-server spring-boot:run
    ./mvnw -pl config-server spring-boot:run
    ./mvnw -pl auth-service,customer-service,restaurant-service,menu-service,payment-service,notification-service,delivery-partner-service,order-service spring-boot:run
    ./mvnw -pl api-gateway spring-boot:run
    """))

    story.append(Paragraph("18.3 Access Points", s["h2"]))
    story.append(table([
        ["Service", "URL"],
        ["API Gateway", "http://localhost:8080"],
        ["Eureka Dashboard", "http://localhost:8761"],
        ["Config Server", "http://localhost:8888"],
        ["Swagger UI (per service)", "http://localhost:{port}/swagger-ui.html"],
    ], col_widths=[4 * cm, 9 * cm]))

    story.append(Paragraph("18.4 Sample cURL Commands", s["h2"]))
    story.append(pre("""
    # Create customer
    curl -X POST http://localhost:8080/api/v1/customers \\
      -H "Content-Type: application/json" \\
      -d '{"name":"John","email":"john@mail.com","phone":"9876543210","address":"Mumbai"}'

    # Register auth
    curl -X POST http://localhost:8080/api/v1/auth/register \\
      -H "Content-Type: application/json" \\
      -d '{"email":"john@mail.com","password":"secret1","role":"CUSTOMER","referenceId":1}'

    # Place order
    curl -X POST http://localhost:8080/api/v1/orders \\
      -H "Content-Type: application/json" \\
      -d '{"customerId":1,"restaurantId":1,"totalAmount":499.0,"paymentMethod":"UPI"}'
    """))

    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(
        "FoodFlow Platform — Comprehensive Technical Documentation v1.0",
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
        title="FoodFlow Platform Comprehensive Documentation",
        author="FoodFlow Platform",
    )

    def add_page_number(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {canvas.getPageNumber()}")
        canvas.drawString(2 * cm, 1.2 * cm, "FoodFlow Platform — Comprehensive Documentation")
        canvas.restoreState()

    doc.build(build_document(), onFirstPage=add_page_number, onLaterPages=add_page_number)
    size_kb = PDF_PATH.stat().st_size / 1024
    print(f"Comprehensive PDF generated: {PDF_PATH} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
