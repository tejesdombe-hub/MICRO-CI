#!/usr/bin/env python3
"""
Generate Service Communication Guide PDF using ReportLab.
Produces clean, text-selectable PDF for the Service Communication documentation.
"""

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
PDF_PATH = DOCS_DIR / "Service-Communication-Guide.pdf"

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
            fontSize=26,
            leading=32,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=12,
        ),
        "cover_sub": ParagraphStyle(
            "CoverSub",
            fontName="Helvetica",
            fontSize=12,
            leading=16,
            textColor=MUTED,
            alignment=TA_LEFT,
            spaceAfter=8,
        ),
        "cover_meta": ParagraphStyle(
            "CoverMeta",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=TEXT,
            alignment=TA_LEFT,
        ),
        "h1": ParagraphStyle(
            "H1",
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=NAVY,
            spaceBefore=18,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "H2",
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=NAVY,
            spaceBefore=12,
            spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "H3",
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=TEXT,
            spaceBefore=8,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "Body",
            fontName="Helvetica",
            fontSize=9.5,
            leading=14,
            textColor=TEXT,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=TEXT,
            leftIndent=12,
            spaceAfter=3,
        ),
        "code": ParagraphStyle(
            "Code",
            fontName="Courier",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#2d3748"),
            backColor=LIGHT_BG,
            leftIndent=6,
            rightIndent=6,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "toc": ParagraphStyle(
            "TOC",
            fontName="Helvetica",
            fontSize=10,
            leading=16,
            textColor=TEXT,
        ),
        "footer": ParagraphStyle(
            "Footer",
            fontName="Helvetica-Oblique",
            fontSize=8,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
    }


def table(data, col_widths=None, header=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style = [
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("TEXTCOLOR", (0, 0), (-1, -1), TEXT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
    ]
    if header and len(data) > 0:
        style.extend([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8.5),
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
    story.append(Paragraph("FOOD DELIVERY PLATFORM", ParagraphStyle(
        "badge", fontName="Helvetica-Bold", fontSize=9, textColor=ACCENT, spaceAfter=14)))
    story.append(Paragraph("Service Communication Guide", s["cover_title"]))
    story.append(Paragraph(
        "Comprehensive Guide to Inter-Service Communication in Microservices",
        s["cover_sub"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "REST, OpenFeign, Service Discovery, Resilience Patterns & Best Practices",
        s["cover_sub"]))
    story.append(Spacer(1, 2 * cm))
    for line in [
        "<b>Project:</b> food-delivery-platform (Maven Multi-Module)",
        "<b>Version:</b> 1.0.0-SNAPSHOT",
        "<b>Focus:</b> Service Communication Architecture",
        "<b>Technologies:</b> Spring Cloud, Eureka, OpenFeign, Resilience4j",
    ]:
        story.append(Paragraph(line, s["cover_meta"]))
    story.append(PageBreak())

    # ---- TOC ----
    story.append(Paragraph("Table of Contents", s["h1"]))
    toc_items = [
        "1. Introduction to Inter-Service Communication",
        "2. Why Microservices Need Inter-Service Communication",
        "3. Synchronous vs Asynchronous Communication",
        "4. REST-Based Service-to-Service Communication",
        "5. HTTP Clients in Spring Boot",
        "6. Service URL Management Challenges",
        "7. Handling Network Latency and Failures",
        "8. Timeout and Retry Considerations",
        "9. Designing Resilient Service Calls",
        "10. When Synchronous Communication is Appropriate",
        "11. Implementation in Food Delivery Platform",
        "12. Best Practices and Recommendations",
    ]
    for item in toc_items:
        story.append(Paragraph(item, s["toc"]))
    story.append(PageBreak())

    # ---- SECTION 1 ----
    story.append(Paragraph("1. Introduction to Inter-Service Communication", s["h1"]))
    story.append(Paragraph(
        "Inter-service communication refers to the mechanisms and protocols that allow "
        "microservices to exchange data and coordinate their actions. In a microservices "
        "architecture, applications are broken down into small, independent services that "
        "work together to deliver business functionality.",
        s["body"]))
    story.append(Paragraph("<b>The Communication Challenge:</b>", s["h3"]))
    story.append(bullet_list([
        "Network Latency: Calls take milliseconds instead of nanoseconds",
        "Partial Failures: One service may be down while others are running",
        "Data Serialization: Objects must be converted to wire format (JSON, XML, etc.)",
        "Service Discovery: Services need to find each other dynamically",
        "Security: Communication must be authenticated and authorized",
        "Observability: Calls must be traced and monitored",
    ], s["bullet"]))

    # ---- SECTION 2 ----
    story.append(Paragraph("2. Why Microservices Need Inter-Service Communication", s["h1"]))
    story.append(Paragraph("<b>Distributed Nature of Microservices</b>", s["h2"]))
    story.append(Paragraph(
        "Microservices are designed to be independently deployable and scalable units. "
        "Each service owns a specific business capability and its own data. To deliver "
        "complete business functionality, these services must collaborate.",
        s["body"]))
    story.append(Paragraph("<b>Business Process Orchestration</b>", s["h2"]))
    story.append(Paragraph(
        "Complex business processes often span multiple services. A single user action "
        "may trigger a chain of service calls.",
        s["body"]))
    story.append(pre("""
Customer places order
    ↓
Order Service validates customer (calls customer-service)
    ↓
Order Service validates restaurant (calls restaurant-service)
    ↓
Order Service processes payment (calls payment-service)
    ↓
Order Service sends notification (calls notification-service)
    ↓
Order Service assigns delivery partner (calls delivery-partner-service)
    """))

    # ---- SECTION 3 ----
    story.append(Paragraph("3. Synchronous vs Asynchronous Communication", s["h1"]))
    story.append(table([
        ["Aspect", "Synchronous", "Asynchronous"],
        ["Pattern", "Request-Response", "Event-Driven"],
        ["Blocking", "Yes", "No"],
        ["Coupling", "Temporal", "Loose"],
        ["Complexity", "Low", "High"],
        ["Feedback", "Immediate", "Delayed"],
        ["Scalability", "Limited", "High"],
        ["Use Case", "Real-time operations", "Background processing"],
    ], col_widths=[3 * cm, 4 * cm, 4 * cm]))

    # ---- SECTION 4 ----
    story.append(Paragraph("4. REST-Based Service-to-Service Communication", s["h1"]))
    story.append(Paragraph(
        "REST (Representational State Transfer) is an architectural style for distributed "
        "systems. It uses standard HTTP methods (GET, POST, PUT, DELETE) to operate on "
        "resources identified by URIs.",
        s["body"]))
    story.append(Paragraph("<b>REST Principles:</b>", s["h3"]))
    story.append(bullet_list([
        "Resource-Based: Everything is a resource with a unique URI",
        "Uniform Interface: Standard HTTP methods and status codes",
        "Stateless: Each request contains all necessary information",
        "Client-Server: Separation of concerns",
        "Cacheable: Responses can be cached to improve performance",
    ], s["bullet"]))

    # ---- SECTION 5 ----
    story.append(Paragraph("5. HTTP Clients in Spring Boot", s["h1"]))
    story.append(table([
        ["Feature", "RestTemplate", "WebClient", "OpenFeign"],
        ["Type", "Imperative", "Reactive", "Declarative"],
        ["Blocking", "Yes", "No", "Yes"],
        ["Status", "Maintenance", "Recommended", "Recommended"],
        ["Learning Curve", "Low", "High", "Low"],
        ["Service Discovery", "Manual", "Manual", "Built-in"],
        ["Load Balancing", "Manual", "Manual", "Built-in"],
        ["Best For", "Simple calls", "Reactive apps", "Microservices"],
    ], col_widths=[2.5 * cm, 3 * cm, 3 * cm, 3.5 * cm]))
    story.append(Paragraph("<b>OpenFeign Example:</b>", s["h2"]))
    story.append(pre("""
@FeignClient(name = "customer-service", path = "/customers")
public interface CustomerClient {
    @GetMapping("/{id}")
    CustomerResponseDto getCustomer(@PathVariable("id") Long id);
}
    """))

    # ---- SECTION 6 ----
    story.append(Paragraph("6. Service URL Management Challenges", s["h1"]))
    story.append(Paragraph("<b>The Hardcoded URL Problem:</b>", s["h2"]))
    story.append(Paragraph(
        "In traditional monolithic applications, service URLs are often hardcoded. This "
        "approach is fragile to environment changes and doesn't work in containerized "
        "deployments.",
        s["body"]))
    story.append(Paragraph("<b>Service Discovery Pattern:</b>", s["h2"]))
    story.append(Paragraph(
        "Service discovery allows services to dynamically find each other without hardcoded "
        "URLs. Services register with a service registry (Eureka, Consul), and clients "
        "query the registry for service locations.",
        s["body"]))
    story.append(Paragraph("<b>In Food Delivery Platform:</b>", s["h3"]))
    story.append(bullet_list([
        "Uses Netflix Eureka for service discovery",
        "Services register on startup via @EnableDiscoveryClient",
        "Feign clients use service names instead of URLs",
        "Automatic load balancing across instances",
    ], s["bullet"]))

    # ---- SECTION 7 ----
    story.append(Paragraph("7. Handling Network Latency and Failures", s["h1"]))
    story.append(Paragraph("<b>The Fallacies of Distributed Computing:</b>", s["h2"]))
    story.append(bullet_list([
        "The network is reliable - It's not. Networks fail.",
        "Latency is zero - It's not. Calls take time.",
        "Bandwidth is infinite - It's not. Networks have limits.",
        "The network is secure - It's not. Security must be added.",
        "Topology doesn't change - It does. Services move.",
    ], s["bullet"]))
    story.append(Paragraph("<b>Failure Handling Patterns:</b>", s["h2"]))
    story.append(bullet_list([
        "Try-Catch: Basic exception handling",
        "Fallback: Provide alternative behavior",
        "Circuit Breaker: Stop calling failing services",
        "Retry: Retry transient failures",
    ], s["bullet"]))

    # ---- SECTION 8 ----
    story.append(Paragraph("8. Timeout and Retry Considerations", s["h1"]))
    story.append(Paragraph("<b>Why Timeouts Matter:</b>", s["h2"]))
    story.append(Paragraph(
        "Without timeouts, a slow or unresponsive service can block threads indefinitely, "
        "cause thread pool exhaustion, cascade failures to other services, and create "
        "system-wide outages.",
        s["body"]))
    story.append(Paragraph("<b>Types of Timeouts:</b>", s["h3"]))
    story.append(bullet_list([
        "Connect Timeout: Time to establish connection",
        "Read Timeout: Time to receive response after connection",
        "Overall Timeout: Total time for the entire operation",
    ], s["bullet"]))
    story.append(Paragraph("<b>Retry Strategies:</b>", s["h2"]))
    story.append(bullet_list([
        "Fixed Delay: Retry after fixed time interval",
        "Exponential Backoff: Increase delay between retries",
        "Custom Retry: Configure max attempts and backoff strategy",
    ], s["bullet"]))

    # ---- SECTION 9 ----
    story.append(Paragraph("9. Designing Resilient Service Calls", s["h1"]))
    story.append(Paragraph("<b>The Resilience Patterns:</b>", s["h2"]))
    story.append(bullet_list([
        "Circuit Breaker: Stop calling failing services",
        "Retry: Retry transient failures",
        "Timeout: Don't wait forever",
        "Bulkhead: Limit resource usage",
        "Fallback: Provide alternative when service fails",
        "Cache: Reduce calls to services",
    ], s["bullet"]))
    story.append(Paragraph("<b>Circuit Breaker States:</b>", s["h3"]))
    story.append(pre("""
CLOSED (normal) → OPEN (tripped) → HALF_OPEN (testing) → CLOSED
    """))

    # ---- SECTION 10 ----
    story.append(Paragraph("10. When Synchronous Communication is Appropriate", s["h1"]))
    story.append(Paragraph("<b>Use Cases for Synchronous Communication:</b>", s["h2"]))
    story.append(bullet_list([
        "Immediate Response Required: Payment validation, authentication",
        "Simple Request-Response: Get customer details, fetch restaurant info",
        "Data Consistency Required: Operations that need immediate confirmation",
        "Low Latency Requirements: Real-time updates, interactive workflows",
    ], s["bullet"]))
    story.append(Paragraph("<b>When to Avoid Synchronous Communication:</b>", s["h2"]))
    story.append(bullet_list([
        "Long-Running Processes: Order processing, report generation",
        "High Throughput Requirements: Event ingestion, analytics",
        "Loose Coupling Needed: Independent service evolution",
        "Event-Driven Workflows: Order lifecycle events, notification triggers",
    ], s["bullet"]))

    # ---- SECTION 11 ----
    story.append(Paragraph("11. Implementation in Food Delivery Platform", s["h1"]))
    story.append(Paragraph(
        "The Food Delivery Platform uses synchronous REST-based communication with "
        "OpenFeign as the primary HTTP client. The order-service acts as an orchestrator, "
        "coordinating calls to multiple services.",
        s["body"]))
    story.append(Paragraph("<b>Feign Clients in Order Service:</b>", s["h2"]))
    story.append(table([
        ["Feign Client", "Target Service", "Endpoint"],
        ["CustomerClient", "customer-service", "GET /customers/{id}"],
        ["RestaurantClient", "restaurant-service", "GET /restaurants/{id}"],
        ["PaymentClient", "payment-service", "POST /payments/process"],
        ["NotificationClient", "notification-service", "POST /notifications"],
        ["DeliveryPartnerClient", "delivery-partner-service", "POST /delivery-partners/assign"],
    ], col_widths=[3.5 * cm, 3.5 * cm, 5.5 * cm]))
    story.append(Paragraph("<b>Enabling Feign Clients:</b>", s["h2"]))
    story.append(pre("""
@SpringBootApplication
@EnableDiscoveryClient
@EnableFeignClients
public class OrderServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderServiceApplication.class, args);
    }
}
    """))

    # ---- SECTION 12 ----
    story.append(Paragraph("12. Best Practices and Recommendations", s["h1"]))
    story.append(Paragraph("<b>General Best Practices:</b>", s["h2"]))
    story.append(bullet_list([
        "Use DTOs for Inter-Service Communication - Never expose entities directly",
        "Implement Service Discovery - Never hardcode service URLs",
        "Add Timeouts - Always configure connect and read timeouts",
        "Implement Retry with Backoff - Retry transient failures",
        "Use Circuit Breakers - Protect against cascading failures",
        "Add Logging and Monitoring - Track latency and error rates",
        "Use Idempotent Operations - Safe to retry without side effects",
    ], s["bullet"]))
    story.append(Paragraph("<b>OpenFeign Best Practices:</b>", s["h2"]))
    story.append(bullet_list([
        "Use Interfaces - Define Feign clients as interfaces",
        "Define Separate DTOs - Client-specific DTOs in calling service",
        "Use Path Variables Correctly - Match endpoint patterns",
        "Add Request Interceptors - For authentication headers",
        "Configure Timeouts per Service - Different timeouts for different services",
    ], s["bullet"]))
    story.append(Paragraph("<b>Resilience Best Practices:</b>", s["h2"]))
    story.append(bullet_list([
        "Combine Multiple Patterns - Circuit breaker + retry + timeout",
        "Implement Meaningful Fallbacks - Return cached data or default values",
        "Monitor Circuit Breaker States - Track open/close transitions",
        "Test Failure Scenarios - Chaos engineering and fault injection",
    ], s["bullet"]))

    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(
        "Service Communication Guide — Food Delivery Platform v1.0",
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
        title="Service Communication Guide",
        author="Food Delivery Platform",
    )

    def add_page_number(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {canvas.getPageNumber()}")
        canvas.drawString(2 * cm, 1.2 * cm, "Service Communication Guide — Food Delivery Platform")
        canvas.restoreState()

    doc.build(build_document(), onFirstPage=add_page_number, onLaterPages=add_page_number)
    size_kb = PDF_PATH.stat().st_size / 1024
    print(f"PDF generated: {PDF_PATH} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
