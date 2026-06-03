#!/usr/bin/env python3
"""
Generate PDF for Delivery Status Enum Fix Documentation.
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
MD_PATH = DOCS_DIR / "DeliveryStatus-Enum-Fix-Documentation.md"
PDF_PATH = DOCS_DIR / "DeliveryStatus-Enum-Fix-Documentation.pdf"

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
            spaceBefore=16,
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
            leftIndent=10,
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
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
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
            ("FONTSIZE", (0, 0), (-1, 0), 9),
        ])
        style.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]))
    t.setStyle(TableStyle(style))
    return t


def pre(text):
    return Preformatted(text.strip(), build_styles()["code"])


def bullet_list(items, style):
    return ListFlowable(
        [ListItem(Paragraph(i, style), leftIndent=10) for i in items],
        bulletType="bullet",
        start="•",
    )


def build_document():
    s = build_styles()
    story = []

    # ---- COVER ----
    story.append(Spacer(1, 2.5 * cm))
    story.append(Paragraph("DELIVERY STATUS ENUM FIX", ParagraphStyle(
        "badge", fontName="Helvetica-Bold", fontSize=9, textColor=ACCENT, spaceAfter=12)))
    story.append(Paragraph("Comprehensive Documentation", s["cover_title"]))
    story.append(Paragraph(
        "Detailed explanation of the AVAILABLE enum fix, root cause analysis, "
        "and architecture implications for the delivery-partner-service",
        s["cover_sub"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "Microservices Architecture • Event-Driven Design • State Management",
        s["cover_sub"]))
    story.append(Spacer(1, 1.5 * cm))
    for line in [
        "<b>Issue:</b> Cannot resolve symbol 'AVAILABLE'",
        "<b>Service:</b> delivery-partner-service",
        "<b>Component:</b> DeliveryStatus enum (common-lib)",
        "<b>Date:</b> May 28, 2026",
    ]:
        story.append(Paragraph(line, s["cover_meta"]))
    story.append(PageBreak())

    # ---- TOC ----
    story.append(Paragraph("Table of Contents", s["h1"]))
    toc_items = [
        "1. Problem Overview",
        "2. Error Details",
        "3. Root Cause Analysis",
        "4. Solution Implementation",
        "5. Technical Context",
        "6. Delivery Partner Lifecycle",
        "7. Architecture Implications",
        "8. Best Practices",
        "9. Testing Considerations",
        "10. Related Patterns",
    ]
    for item in toc_items:
        story.append(Paragraph(item, s["toc"]))
    story.append(PageBreak())

    # ---- 1. PROBLEM OVERVIEW ----
    story.append(Paragraph("1. Problem Overview", s["h1"]))
    story.append(Paragraph(
        "A compilation error occurred in the delivery-partner-service when trying "
        "to use a non-existent enum value AVAILABLE from the DeliveryStatus enum.",
        s["body"]))
    
    story.append(Paragraph("Error Message", s["h2"]))
    story.append(pre("""Cannot resolve symbol 'AVAILABLE'
Location: delivery-partner-service/src/main/java/com/fooddelivery/
delivery/consumer/OrderEventConsumer.java:42"""))
    
    story.append(Paragraph("Impact", s["h2"]))
    story.append(bullet_list([
        "The OrderEventConsumer class could not compile",
        "Delivery partner status updates would fail after order delivery",
        "The messaging flow for marking partners as available was broken",
    ], s["bullet"]))

    # ---- 2. ERROR DETAILS ----
    story.append(Paragraph("2. Error Details", s["h1"]))
    story.append(Paragraph(
        "<b>File:</b> OrderEventConsumer.java", s["h3"]))
    story.append(Paragraph(
        "<b>Location:</b> delivery-partner-service/src/main/java/com/fooddelivery/"
        "delivery/consumer/OrderEventConsumer.java", s["body"]))
    
    story.append(Paragraph("Problematic Code (Line 42)", s["h2"]))
    story.append(pre("""case "ORDER_DELIVERED":
    log.info("Order delivered event received for order: {}, partner: {}", 
        event.getOrderId(), event.getDeliveryPartnerId());
    // Update delivery partner status to AVAILABLE after delivery
    updateDeliveryStatus(event.getDeliveryPartnerId(), 
        com.fooddelivery.common.enums.DeliveryStatus.AVAILABLE);
    break;"""))
    
    story.append(Paragraph("Error Context", s["h2"]))
    story.append(bullet_list([
        "The code was attempting to set a delivery partner's status to AVAILABLE "
        "after completing a delivery",
        "This is part of the event-driven architecture where order status changes "
        "trigger delivery partner status updates",
        "The enum constant AVAILABLE did not exist in the DeliveryStatus enum",
    ], s["bullet"]))

    # ---- 3. ROOT CAUSE ----
    story.append(Paragraph("3. Root Cause Analysis", s["h1"]))
    story.append(Paragraph("The Missing Enum Value", s["h2"]))
    story.append(Paragraph("Original DeliveryStatus Enum:", s["h3"]))
    story.append(pre("""package com.fooddelivery.common.enums;

public enum DeliveryStatus {
    ASSIGNED,
    PICKED_UP,
    OUT_FOR_DELIVERY,
    DELIVERED
}"""))
    
    story.append(Paragraph("Analysis", s["h2"]))
    story.append(bullet_list([
        "The enum only defined statuses for active delivery states",
        "It was missing the initial state (AVAILABLE) for when partners are free",
        "The business logic required marking partners as available after delivery completion",
        "This created a gap in the delivery partner lifecycle management",
    ], s["bullet"]))
    
    story.append(Paragraph("Why This Was Missed", s["h2"]))
    story.append(bullet_list([
        "The enum was likely designed focusing only on the delivery process itself",
        "The partner availability state was not considered in the initial design",
        "As the system evolved, the need to track partner availability became apparent",
    ], s["bullet"]))

    # ---- 4. SOLUTION ----
    story.append(Paragraph("4. Solution Implementation", s["h1"]))
    story.append(Paragraph("Changes Made", s["h2"]))
    story.append(Paragraph(
        "<b>File:</b> common-lib/src/main/java/com/fooddelivery/common/enums/"
        "DeliveryStatus.java", s["body"]))
    
    story.append(Paragraph("Updated Enum", s["h2"]))
    story.append(pre("""package com.fooddelivery.common.enums;

public enum DeliveryStatus {
    AVAILABLE,        // NEW: Partner is available for new deliveries
    ASSIGNED,         // Partner has been assigned to an order
    PICKED_UP,        // Partner has picked up the order
    OUT_FOR_DELIVERY, // Partner is on the way to deliver
    DELIVERED         // Order has been delivered
}"""))
    
    story.append(Paragraph("What Changed", s["h2"]))
    story.append(bullet_list([
        "Added AVAILABLE as the first enum constant",
        "Positioned at the beginning to represent the initial/default state",
        "Maintains logical flow from available → assigned → picked up → "
        "out for delivery → delivered",
    ], s["bullet"]))
    
    story.append(Paragraph("Why This Position?", s["h2"]))
    story.append(bullet_list([
        "AVAILABLE represents the starting state in the partner lifecycle",
        "Partners start as available, get assigned, then progress through delivery states",
        "After delivery, they return to AVAILABLE for new assignments",
        "This creates a complete state machine for delivery partners",
    ], s["bullet"]))

    story.append(PageBreak())

    # ---- 5. TECHNICAL CONTEXT ----
    story.append(Paragraph("5. Technical Context", s["h1"]))
    story.append(Paragraph("Microservices Architecture", s["h2"]))
    story.append(Paragraph(
        "<b>Service Involved:</b> delivery-partner-service", s["h3"]))
    story.append(bullet_list([
        "Manages delivery partner information and status",
        "Receives events from order service via RabbitMQ",
        "Updates partner status based on order lifecycle events",
        "Communicates with other services through the common library",
    ], s["bullet"]))
    
    story.append(Paragraph("Common Library", s["h3"]))
    story.append(bullet_list([
        "common-lib contains shared enums, DTOs, and utilities",
        "DeliveryStatus enum is used across multiple services",
        "Changes to common enums affect all dependent services",
    ], s["bullet"]))
    
    story.append(Paragraph("Event-Driven Flow", s["h2"]))
    story.append(pre("""Order Service (ORDER_DELIVERED event)
    ↓
RabbitMQ (delivery.queue)
    ↓
OrderEventConsumer (delivery-partner-service)
    ↓
DeliveryPartnerService.updateStatus()
    ↓
DeliveryStatus.AVAILABLE"""))
    
    story.append(Paragraph("Idempotency Considerations", s["h2"]))
    story.append(Paragraph(
        "The OrderEventConsumer includes idempotency handling:", s["body"]))
    story.append(pre("""if (idempotencyHandler.isMessageProcessed(event.getMessageId())) {
    log.info("Skipping duplicate message: messageId={}", 
        event.getMessageId());
    return;
}"""))
    story.append(Paragraph(
        "This ensures that even if the same message is delivered multiple times, "
        "the partner status is only updated once, preventing race conditions.",
        s["body"]))

    # ---- 6. LIFECYCLE ----
    story.append(Paragraph("6. Delivery Partner Lifecycle", s["h1"]))
    story.append(Paragraph("State Machine", s["h2"]))
    story.append(pre("""┌─────────────┐
│  AVAILABLE  │ ← Initial state, after delivery completion
└──────┬──────┘
       │ Order assigned
       ↓
┌─────────────┐
│  ASSIGNED   │ ← Partner assigned to order
└──────┬──────┘
       │ Order picked up
       ↓
┌─────────────┐
│  PICKED_UP  │ ← Partner has the order
└──────┬──────┘
       │ En route to customer
       ↓
┌──────────────────┐
│ OUT_FOR_DELIVERY │ ← Partner delivering
└──────┬───────────┘
       │ Order delivered
       ↓
┌─────────────┐
│  DELIVERED  │ ← Order completed
└──────┬──────┘
       │ Return to pool
       ↓
┌─────────────┐
│  AVAILABLE  │ ← Ready for new orders
└─────────────┘"""))
    
    story.append(Paragraph("State Transitions", s["h2"]))
    story.append(table([
        ["Current State", "Event", "Next State", "Business Meaning"],
        ["AVAILABLE", "Order assigned", "ASSIGNED", "Partner gets a new delivery"],
        ["ASSIGNED", "Order picked up", "PICKED_UP", "Partner collects food"],
        ["PICKED_UP", "Start delivery", "OUT_FOR_DELIVERY", "Partner on the way"],
        ["OUT_FOR_DELIVERY", "Delivery complete", "DELIVERED", "Order delivered"],
        ["DELIVERED", "Return to pool", "AVAILABLE", "Partner free for new orders"],
    ], col_widths=[3.5*cm, 3*cm, 3*cm, 4.5*cm]))
    
    story.append(Paragraph("Business Logic", s["h2"]))
    story.append(Paragraph("<b>When Partner Becomes AVAILABLE:</b>", s["h3"]))
    story.append(bullet_list([
        "1. Order is marked as delivered in order service",
        "2. Order service publishes ORDER_DELIVERED event",
        "3. Delivery partner service receives event",
        "4. Partner status updated to AVAILABLE",
        "5. Partner becomes eligible for new order assignments",
    ], s["bullet"]))
    
    story.append(Paragraph("<b>Why This Matters:</b>", s["h3"]))
    story.append(bullet_list([
        "Ensures partners aren't assigned to multiple orders simultaneously",
        "Provides real-time visibility into partner availability",
        "Enables efficient order routing and dispatch",
        "Prevents overloading partners with too many deliveries",
    ], s["bullet"]))

    story.append(PageBreak())

    # ---- 7. ARCHITECTURE ----
    story.append(Paragraph("7. Architecture Implications", s["h1"]))
    story.append(Paragraph("Shared Enum Design", s["h2"]))
    story.append(Paragraph("<b>Principles:</b>", s["h3"]))
    story.append(bullet_list([
        "<b>Completeness:</b> Enums should represent all possible states in the lifecycle",
        "<b>Logical Ordering:</b> States should follow the natural flow of the business process",
        "<b>Cross-Service Consistency:</b> Shared enums ensure consistent state representation",
        "<b>Future-Proofing:</b> Design for evolution, anticipate new states",
    ], s["bullet"]))
    
    story.append(Paragraph("Common Library Impact", s["h3"]))
    story.append(bullet_list([
        "Changes to shared enums require careful consideration",
        "All services using the enum must be tested",
        "Database schemas may need updates if enum values are persisted",
        "API contracts may be affected if enum values are exposed",
    ], s["bullet"]))
    
    story.append(Paragraph("Service Boundaries", s["h2"]))
    story.append(Paragraph("<b>delivery-partner-service Responsibilities:</b>", s["h3"]))
    story.append(bullet_list([
        "Manage delivery partner CRUD operations",
        "Track partner status and availability",
        "Handle partner assignment logic",
        "Respond to order lifecycle events",
    ], s["bullet"]))
    
    story.append(Paragraph("<b>order-service Responsibilities:</b>", s["h3"]))
    story.append(bullet_list([
        "Manage order lifecycle",
        "Publish order status change events",
        "Coordinate with delivery service for assignments",
    ], s["bullet"]))
    
    story.append(Paragraph("<b>Separation of Concerns:</b>", s["h3"]))
    story.append(bullet_list([
        "Order service doesn't directly update partner status",
        "Uses event-driven communication to maintain loose coupling",
        "Each service owns its domain entities and state",
    ], s["bullet"]))
    
    story.append(Paragraph("Data Consistency", s["h2"]))
    story.append(Paragraph("<b>Eventual Consistency:</b>", s["h3"]))
    story.append(bullet_list([
        "Status updates are asynchronous via events",
        "There may be a brief delay between order delivery and partner availability",
        "Idempotency handlers prevent duplicate updates",
        "System is designed to handle temporary inconsistencies",
    ], s["bullet"]))

    # ---- 8. BEST PRACTICES ----
    story.append(Paragraph("8. Best Practices", s["h1"]))
    story.append(Paragraph("Enum Design Guidelines", s["h2"]))
    story.append(bullet_list([
        "<b>1. Represent Complete State Machine</b> - Include all possible states "
        "in the lifecycle, consider initial, intermediate, and final states",
        "<b>2. Logical Ordering</b> - Order enum values to reflect the natural flow, "
        "first value should be the initial/default state",
        "<b>3. Meaningful Names</b> - Use clear, descriptive names, avoid abbreviations, "
        "follow naming conventions (UPPER_SNAKE_CASE)",
        "<b>4. Documentation</b> - Document each enum value's purpose, explain state "
        "transitions, provide examples of usage",
    ], s["bullet"]))
    
    story.append(Paragraph("Event-Driven Architecture", s["h2"]))
    story.append(bullet_list([
        "<b>1. Idempotency</b> - Always handle duplicate messages, use message IDs "
        "for deduplication, design handlers to be safe for retries",
        "<b>2. Error Handling</b> - Log errors comprehensively, implement retry "
        "mechanisms, consider dead letter queues for failed messages",
        "<b>3. Event Design</b> - Include all necessary context in events, use "
        "consistent event naming, version events for backward compatibility",
    ], s["bullet"]))
    
    story.append(Paragraph("Microservices Communication", s["h2"]))
    story.append(bullet_list([
        "<b>1. Shared Libraries</b> - Use common-lib for shared types, keep common "
        "library stable, version shared libraries carefully",
        "<b>2. Loose Coupling</b> - Services communicate via events, not direct calls, "
        "each service owns its data, avoid shared databases",
        "<b>3. Resilience</b> - Handle service failures gracefully, implement "
        "circuit breakers, use timeouts and retries",
    ], s["bullet"]))

    story.append(PageBreak())

    # ---- 9. TESTING ----
    story.append(Paragraph("9. Testing Considerations", s["h1"]))
    story.append(Paragraph("Unit Tests", s["h2"]))
    story.append(Paragraph("Test Cases for DeliveryStatus Enum:", s["h3"]))
    story.append(pre("""@Test
void testDeliveryStatusValues() {
    assertEquals(5, DeliveryStatus.values().length);
    assertEquals("AVAILABLE", DeliveryStatus.values()[0].name());
    assertEquals("ASSIGNED", DeliveryStatus.values()[1].name());
    assertEquals("PICKED_UP", DeliveryStatus.values()[2].name());
    assertEquals("OUT_FOR_DELIVERY", DeliveryStatus.values()[3].name());
    assertEquals("DELIVERED", DeliveryStatus.values()[4].name());
}"""))
    
    story.append(Paragraph("Test Cases for OrderEventConsumer:", s["h3"]))
    story.append(pre("""@Test
void testOrderDeliveredEventUpdatesPartnerToAvailable() {
    OrderEvent event = new OrderEvent();
    event.setEventType("ORDER_DELIVERED");
    event.setDeliveryPartnerId(1L);
    
    consumer.handleOrderEvent(event);
    
    verify(deliveryPartnerService).updateStatus(eq(1L), 
        any(DeliveryStatusUpdateRequestDto.class));
    // Verify status is AVAILABLE
}"""))
    
    story.append(Paragraph("Integration Tests", s["h2"]))
    story.append(Paragraph("<b>Test Scenarios:</b>", s["h3"]))
    story.append(bullet_list([
        "Complete order flow from creation to delivery",
        "Partner status transitions through all states",
        "Duplicate message handling",
        "Service failure and recovery",
    ], s["bullet"]))
    
    story.append(Paragraph("Regression Tests", s["h2"]))
    story.append(Paragraph("<b>Areas to Verify:</b>", s["h3"]))
    story.append(bullet_list([
        "All services using DeliveryStatus enum",
        "Database queries filtering by status",
        "API responses including status",
        "Event payloads with status values",
    ], s["bullet"]))

    # ---- 10. RELATED PATTERNS ----
    story.append(Paragraph("10. Related Patterns", s["h1"]))
    story.append(Paragraph("<b>State Pattern</b>", s["h2"]))
    story.append(Paragraph(
        "The delivery partner status could be implemented using the State pattern "
        "for more complex behavior:",
        s["body"]))
    story.append(bullet_list([
        "Each state encapsulates specific behavior",
        "State transitions are managed explicitly",
        "Easy to add new states without modifying existing code",
    ], s["bullet"]))
    
    story.append(Paragraph("<b>Saga Pattern</b>", s["h2"]))
    story.append(Paragraph(
        "For complex multi-step processes:", s["body"]))
    story.append(bullet_list([
        "Coordinate state changes across services",
        "Implement compensating transactions",
        "Ensure consistency in distributed systems",
    ], s["bullet"]))
    
    story.append(Paragraph("<b>Event Sourcing</b>", s["h2"]))
    story.append(Paragraph(
        "Alternative approach for state management:", s["body"]))
    story.append(bullet_list([
        "Store all state changes as events",
        "Rebuild current state from event history",
        "Provides complete audit trail",
    ], s["bullet"]))
    
    story.append(Paragraph("<b>CQRS</b>", s["h2"]))
    story.append(Paragraph(
        "Separate read and write models:", s["body"]))
    story.append(bullet_list([
        "Optimized queries for partner availability",
        "Separate data stores for different access patterns",
        "Improved performance for read-heavy operations",
    ], s["bullet"]))

    # ---- SUMMARY ----
    story.append(PageBreak())
    story.append(Paragraph("Summary", s["h1"]))
    story.append(Paragraph("<b>Problem</b>", s["h2"]))
    story.append(bullet_list([
        "DeliveryStatus.AVAILABLE enum value was missing",
        "Caused compilation error in OrderEventConsumer",
        "Broke the delivery partner lifecycle",
    ], s["bullet"]))
    
    story.append(Paragraph("<b>Solution</b>", s["h2"]))
    story.append(bullet_list([
        "Added AVAILABLE to the DeliveryStatus enum",
        "Positioned as first value (initial state)",
        "Completed the partner state machine",
    ], s["bullet"]))
    
    story.append(Paragraph("<b>Lessons Learned</b>", s["h2"]))
    story.append(bullet_list([
        "Design enums to represent complete state machines",
        "Consider all lifecycle states during initial design",
        "Shared types require careful change management",
        "Event-driven architectures need idempotency",
    ], s["bullet"]))
    
    story.append(Paragraph("<b>Next Steps</b>", s["h2"]))
    story.append(bullet_list([
        "Update database schemas if status is persisted",
        "Add comprehensive unit and integration tests",
        "Update API documentation",
        "Verify all services using the enum",
        "Consider adding state transition validation",
    ], s["bullet"]))

    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(
        "Delivery Status Enum Fix — Documentation v1.0",
        s["footer"]))

    return story


def main():
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="Delivery Status Enum Fix Documentation",
        author="Food Delivery Platform",
    )

    def add_page_number(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(A4[0] - 1.8 * cm, 1 * cm, 
                             f"Page {canvas.getPageNumber()}")
        canvas.drawString(1.8 * cm, 1 * cm, 
                         "Delivery Status Enum Fix — Technical Documentation")
        canvas.restoreState()

    doc.build(build_document(), onFirstPage=add_page_number, onLaterPages=add_page_number)
    size_kb = PDF_PATH.stat().st_size / 1024
    print(f"PDF generated: {PDF_PATH} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
