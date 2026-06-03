#!/usr/bin/env python3
"""
Generate Circuit Breaker and Resilience Patterns PDF for FoodFlow Platform.
Focused documentation on resilience patterns, Circuit Breaker, and Resilience4j.
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
PDF_PATH = DOCS_DIR / "Circuit-Breaker-Resilience-Patterns.pdf"

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
    story.append(Paragraph("Circuit Breaker & Resilience Patterns", s["cover_title"]))
    story.append(Paragraph(
        "Comprehensive Guide to Building Fault-Tolerant Microservices",
        s["cover_sub"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "Spring Boot 3.x + Resilience4j Implementation Guide",
        s["cover_sub"]))
    story.append(Spacer(1, 2 * cm))
    for line in [
        "<b>Project:</b> FoodFlow — Food Delivery Backend",
        "<b>Architecture:</b> Microservices (Spring Cloud)",
        "<b>Focus:</b> Circuit Breaker, Retry, Bulkhead, Rate Limiter",
        "<b>Library:</b> Resilience4j 2.1.0",
        "<b>Framework:</b> Spring Boot 3.x",
    ]:
        story.append(Paragraph(line, s["cover_meta"]))
    story.append(PageBreak())

    # ---- TOC ----
    story.append(Paragraph("Table of Contents", s["h1"]))
    toc_items = [
        "1. What is Resilience in Microservices Architecture",
        "2. Problems Caused by Cascading Failures",
        "3. What Happens When a Dependent Service is Slow or Down",
        "4. Introduction to Circuit Breaker Pattern",
        "5. How Circuit Breaker Prevents System-Wide Failures",
        "6. States of Circuit Breaker: CLOSED, OPEN, HALF-OPEN",
        "7. Difference Between Retry and Circuit Breaker",
        "8. Introduction to Resilience4j",
        "9. Configuring Failure Threshold and Wait Duration",
        "10. Implementing Fallback Methods",
        "11. Monitoring Circuit Breaker Health",
        "12. Real-World Examples of Resilience Patterns",
        "13. Common Configuration Mistakes and Overuse of Retry",
    ]
    for item in toc_items:
        story.append(Paragraph(item, s["toc"]))
    story.append(PageBreak())

    # ---- 1. RESILIENCE ----
    story.append(Paragraph("1. What is Resilience in Microservices Architecture", s["h1"]))
    story.append(Paragraph(
        "Resilience is the ability of a system to continue functioning correctly even when "
        "some of its components fail or experience degraded performance. In microservices "
        "architecture, resilience is critical because services are distributed and communicate "
        "over the network.",
        s["body"]))
    
    story.append(Paragraph("<b>Why resilience matters in microservices:</b>", s["h3"]))
    story.append(bullet_list([
        "Services are distributed and communicate over the network",
        "Each service has its own failure domain",
        "A single service failure can cascade to dependent services",
        "Network latency and timeouts are inherent in distributed systems",
    ], s["bullet"]))

    story.append(Paragraph("<b>Resilience patterns protect the system from:</b>", s["h3"]))
    story.append(bullet_list([
        "Service unavailability (down services)",
        "High latency (slow services)",
        "Network failures",
        "Resource exhaustion (thread pools, connections)",
    ], s["bullet"]))

    # ---- 2. CASCADING FAILURES ----
    story.append(Paragraph("2. Problems Caused by Cascading Failures", s["h1"]))
    story.append(Paragraph(
        "Cascading failures occur when a failure in one service triggers failures in "
        "dependent services, creating a domino effect that can bring down the entire system.",
        s["body"]))

    story.append(Paragraph("<b>Example scenario:</b>", s["h3"]))
    story.append(pre("""
Payment Service slows down → Order Service threads block waiting
→ Order Service thread pool exhausts → API Gateway requests timeout
→ Customer retries → More requests flood the system
→ All services become unresponsive → System-wide outage
    """))

    story.append(Paragraph("<b>Common cascading failure patterns:</b>", s["h3"]))
    story.append(bullet_list([
        "Thread pool exhaustion from blocked calls",
        "Connection pool depletion from waiting connections",
        "Memory exhaustion from queued requests",
        "Database lock contention from long-running transactions",
        "Retry storms amplifying traffic to failing services",
    ], s["bullet"]))

    # ---- 3. DEPENDENT SERVICE ISSUES ----
    story.append(Paragraph("3. What Happens When a Dependent Service is Slow or Down", s["h1"]))

    story.append(Paragraph("<b>When a service is DOWN:</b>", s["h3"]))
    story.append(bullet_list([
        "Connection attempts timeout",
        "Feign clients throw ConnectException or SocketTimeoutException",
        "Calling service experiences increased latency",
        "If no timeout is set, threads block indefinitely",
        "Thread pool fills up, rejecting new requests",
    ], s["bullet"]))

    story.append(Paragraph("<b>When a service is SLOW:</b>", s["h3"]))
    story.append(bullet_list([
        "Requests complete but with high latency",
        "Response times exceed configured timeouts",
        "Backpressure builds up in calling services",
        "Resource pools (threads, connections) get exhausted",
        "User experience degrades across the system",
    ], s["bullet"]))

    story.append(Paragraph("<b>Impact on FoodFlow platform:</b>", s["h3"]))
    story.append(bullet_list([
        "Order Service calling slow Payment Service → orders hang",
        "Restaurant Service calling slow Menu Service → menu loading fails",
        "Delivery Service calling slow Notification Service → delivery updates delayed",
    ], s["bullet"]))

    story.append(PageBreak())

    # ---- 4. CIRCUIT BREAKER INTRO ----
    story.append(Paragraph("4. Introduction to Circuit Breaker Pattern", s["h1"]))
    story.append(Paragraph(
        "The Circuit Breaker pattern prevents cascading failures by detecting when a "
        "dependent service is failing and temporarily blocking calls to it, similar to "
        "an electrical circuit breaker that trips when there's a fault.",
        s["body"]))

    story.append(Paragraph("<b>Key benefits:</b>", s["h3"]))
    story.append(bullet_list([
        "Fast failure when a service is known to be down",
        "Prevents resource exhaustion on the calling side",
        "Allows the failing service time to recover",
        "Provides fallback behavior for users",
    ], s["bullet"]))

    story.append(Paragraph("<b>How it works:</b>", s["h3"]))
    story.append(bullet_list([
        "1. Monitor calls to a dependent service",
        "2. Count failures over a sliding time window",
        "3. When failure threshold is reached, trip the circuit (OPEN state)",
        "4. Block all calls immediately (fail fast)",
        "5. After a wait duration, attempt a single call (HALF-OPEN state)",
        "6. If successful, reset to CLOSED; if failed, stay OPEN",
    ], s["bullet"]))

    # ---- 5. PREVENTING FAILURES ----
    story.append(Paragraph("5. How Circuit Breaker Prevents System-Wide Failures", s["h1"]))

    story.append(Paragraph("<b>Without Circuit Breaker:</b>", s["h3"]))
    story.append(pre("""
Order Service → Payment Service (slow/down)
├─ Thread 1: waiting... (blocked)
├─ Thread 2: waiting... (blocked)
├─ Thread 3: waiting... (blocked)
└─ Thread pool exhausted → all new requests rejected
    """))

    story.append(Paragraph("<b>With Circuit Breaker:</b>", s["h3"]))
    story.append(pre("""
Order Service → Payment Service (circuit OPEN)
├─ Thread 1: CircuitBreakerOpenException (immediate)
├─ Thread 2: CircuitBreakerOpenException (immediate)
├─ Thread 3: CircuitBreakerOpenException (immediate)
└─ Fallback: "Payment unavailable, try later" (graceful degradation)
    """))

    story.append(Paragraph("<b>Protection mechanisms:</b>", s["h3"]))
    story.append(bullet_list([
        "Immediate failure instead of waiting",
        "Resource conservation (threads, connections)",
        "Graceful degradation via fallbacks",
        "Automatic recovery detection",
    ], s["bullet"]))

    # ---- 6. CIRCUIT STATES ----
    story.append(Paragraph("6. States of Circuit Breaker: CLOSED, OPEN, HALF-OPEN", s["h1"]))

    story.append(Paragraph("<b>CLOSED State (Normal Operation):</b>", s["h3"]))
    story.append(bullet_list([
        "Circuit allows all requests to pass through",
        "Failure rate is monitored but below threshold",
        "Each failed request increments failure counter",
        "Successful requests reset failure counter",
        "Example: Payment Service responding normally",
    ], s["bullet"]))

    story.append(Paragraph("<b>OPEN State (Circuit Tripped):</b>", s["h3"]))
    story.append(bullet_list([
        "All requests are blocked immediately",
        "No actual calls to the dependent service",
        "CircuitBreakerOpenException thrown for each call",
        "Fallback methods are invoked",
        "Wait duration timer starts (e.g., 60 seconds)",
        "Example: Payment Service down, circuit tripped after 50% failure rate",
    ], s["bullet"]))

    story.append(Paragraph("<b>HALF-OPEN State (Recovery Attempt):</b>", s["h3"]))
    story.append(bullet_list([
        "After wait duration expires, circuit transitions to HALF-OPEN",
        "Allows a single request through to test if service recovered",
        "If request succeeds → transition to CLOSED (circuit reset)",
        "If request fails → transition back to OPEN (wait duration restarts)",
        "Example: Testing if Payment Service recovered after outage",
    ], s["bullet"]))

    story.append(PageBreak())

    # ---- 7. RETRY VS CIRCUIT BREAKER ----
    story.append(Paragraph("7. Difference Between Retry and Circuit Breaker", s["h1"]))

    story.append(table([
        ["Aspect", "Retry Pattern", "Circuit Breaker Pattern"],
        ["Purpose", "Handle transient failures", "Prevent cascading failures"],
        ["When to use", "Network glitches, temporary timeouts", "Service down, persistent failures"],
        ["Behavior", "Re-attempt the same request", "Block requests to failing service"],
        ["Resource usage", "Increases load (more requests)", "Decreases load (blocks requests)"],
        ["Failure handling", "Hope it works next time", "Accept failure, use fallback"],
        ["Example scenario", "Payment gateway timeout (retry once)", "Payment service down (stop calling)"],
    ], col_widths=[3 * cm, 4 * cm, 5.5 * cm]))

    story.append(Paragraph("<b>When to use together:</b>", s["h3"]))
    story.append(bullet_list([
        "Retry first for transient failures (1-3 attempts)",
        "Circuit Breaker trips if retries consistently fail",
        "This combination handles both temporary and persistent failures",
    ], s["bullet"]))

    # ---- 8. RESILIENCE4J ----
    story.append(Paragraph("8. Introduction to Resilience4j", s["h1"]))
    story.append(Paragraph(
        "Resilience4j is a fault tolerance library for Java that implements several "
        "resilience patterns. It is the recommended replacement for Hystrix, which is "
        "now in maintenance mode.",
        s["body"]))

    story.append(Paragraph("<b>Patterns provided by Resilience4j:</b>", s["h3"]))
    story.append(bullet_list([
        "<b>Circuit Breaker:</b> Prevent cascading failures",
        "<b>Retry:</b> Handle transient failures",
        "<b>Rate Limiter:</b> Control request rate",
        "<b>Bulkhead:</b> Limit concurrent calls",
        "<b>Time Limiter:</b> Cancel long-running operations",
        "<b>Cache:</b> Cache responses to reduce load",
    ], s["bullet"]))

    story.append(Paragraph("<b>Why Resilience4j over Hystrix:</b>", s["h3"]))
    story.append(bullet_list([
        "Active maintenance (Hystrix is in maintenance mode)",
        "Java 8+ compatibility",
        "Modular design (use only what you need)",
        "Better performance",
        "Reactive programming support",
    ], s["bullet"]))

    story.append(Paragraph("<b>Integration with Spring Boot:</b>", s["h3"]))
    story.append(pre("""
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-spring-boot3</artifactId>
    <version>2.1.0</version>
</dependency>
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-feign</artifactId>
    <version>2.1.0</version>
</dependency>
    """))

    # ---- 9. CONFIGURATION ----
    story.append(Paragraph("9. Configuring Failure Threshold and Wait Duration", s["h1"]))

    story.append(Paragraph("<b>Configuration in application.yml (from config-server):</b>", s["h3"]))
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
        recordExceptions:
          - java.util.concurrent.TimeoutException
          - java.io.IOException
        ignoreExceptions:
          - com.foodflow.order.exception.BusinessException
    """))

    story.append(Paragraph("<b>Key parameters explained:</b>", s["h3"]))
    story.append(table([
        ["Parameter", "Description"],
        ["slidingWindowSize", "Window size for failure rate calculation (count-based or time-based)"],
        ["failureRateThreshold", "Percentage of failures that triggers OPEN state"],
        ["waitDurationInOpenState", "How long to stay OPEN before attempting recovery"],
        ["slowCallRateThreshold", "Trip if calls are consistently slow (even if they succeed)"],
        ["permittedNumberOfCallsInHalfOpenState", "How many test calls to allow in recovery"],
    ], col_widths=[4 * cm, 9 * cm]))

    story.append(Paragraph("<b>Applying to Feign client:</b>", s["h3"]))
    story.append(pre("""
@FeignClient(
    name = "payment-service",
    fallback = PaymentServiceClientFallback.class,
    configuration = FeignCircuitBreakerConfig.class
)
public interface PaymentServiceClient {
    @PostMapping("/api/v1/payments")
    ApiResponse<PaymentResponseDto> createPayment(@RequestBody PaymentRequestDto dto);
}
    """))

    story.append(PageBreak())

    # ---- 10. FALLBACK METHODS ----
    story.append(Paragraph("10. Implementing Fallback Methods", s["h1"]))

    story.append(Paragraph("<b>Fallback class for Feign client:</b>", s["h3"]))
    story.append(pre("""
@Component
@Slf4j
public class PaymentServiceClientFallback implements PaymentServiceClient {

    @Override
    public ApiResponse<PaymentResponseDto> createPayment(PaymentRequestDto dto) {
        log.error("Payment service unavailable, using fallback for order: {}", dto.getOrderId());
        
        // Return a graceful response indicating payment service is down
        return ApiResponse.<PaymentResponseDto>error(
            "Payment service temporarily unavailable. Please try again later.",
            List.of("PAYMENT_SERVICE_UNAVAILABLE")
        );
    }
}
    """))

    story.append(Paragraph("<b>Fallback strategies:</b>", s["h3"]))
    story.append(bullet_list([
        "<b>Return cached data:</b> Use last known good value",
        "<b>Return default value:</b> Provide sensible defaults",
        "<b>Return error message:</b> Inform user of unavailability",
        "<b>Queue for later processing:</b> Store request, process when service recovers",
        "<b>Call alternative service:</b> Use backup provider",
    ], s["bullet"]))

    story.append(Paragraph("<b>Programmatic Circuit Breaker with fallback:</b>", s["h3"]))
    story.append(pre("""
@CircuitBreaker(
    name = "paymentService",
    fallbackMethod = "createPaymentFallback"
)
public PaymentResponseDto createPayment(PaymentRequestDto dto) {
    return paymentServiceClient.createPayment(dto).getData();
}

private PaymentResponseDto createPaymentFallback(PaymentRequestDto dto, Exception ex) {
    log.error("Circuit breaker triggered for payment service", ex);
    
    // Create a pending payment record to process later
    PaymentResponseDto fallback = new PaymentResponseDto();
    fallback.setOrderId(dto.getOrderId());
    fallback.setStatus("PENDING_RETRY");
    fallback.setMessage("Payment queued for retry");
    
    return fallback;
}
    """))

    # ---- 11. MONITORING ----
    story.append(Paragraph("11. Monitoring Circuit Breaker Health", s["h1"]))

    story.append(Paragraph("<b>Metrics exposed by Resilience4j:</b>", s["h3"]))
    story.append(bullet_list([
        "Circuit state (CLOSED, OPEN, HALF-OPEN)",
        "Failure rate",
        "Success rate",
        "Number of buffered calls",
        "Number of failed calls",
        "Number of slow calls",
    ], s["bullet"]))

    story.append(Paragraph("<b>Actuator endpoint integration:</b>", s["h3"]))
    story.append(pre("""
management:
  endpoints:
    web:
      exposure:
        include: health,metrics,circuitbreakers
  endpoint:
    health:
      show-details: always
  metrics:
    export:
      prometheus:
        enabled: true
    """))

    story.append(Paragraph("<b>Accessing metrics:</b>", s["h3"]))
    story.append(pre("""
GET /actuator/circuitbreakers
GET /actuator/metrics/resilience4j.circuitbreaker.state
GET /actuator/metrics/resilience4j.circuitbreaker.failure.rate
GET /actuator/prometheus
    """))

    story.append(Paragraph("<b>Sample Prometheus queries:</b>", s["h3"]))
    story.append(pre("""
# Circuit breaker state (0=CLOSED, 1=OPEN, 2=HALF_OPEN)
resilience4j_circuitbreaker_state{name="paymentService"}

# Failure rate percentage
resilience4j_circuitbreaker_failure_rate{name="paymentService"}

# Number of successful calls
rate(resilience4j_circuitbreaker_successful_calls{name="paymentService"}[5m])
    """))

    story.append(Paragraph("<b>Logging circuit state changes:</b>", s["h3"]))
    story.append(pre("""
@Component
@Slf4j
public class CircuitBreakerEventListener {

    @EventListener
    public void onCircuitBreakerEvent(CircuitBreakerOnStateTransitionEvent event) {
        log.warn("Circuit breaker state transition: {} from {} to {}",
            event.getCircuitBreakerName(),
            event.getStateTransition().getFromState(),
            event.getStateTransition().getToState());
    }
}
    """))

    story.append(PageBreak())

    # ---- 12. REAL-WORLD EXAMPLES ----
    story.append(Paragraph("12. Real-World Examples of Resilience Patterns", s["h1"]))

    story.append(Paragraph("<b>Example 1: Order Service calling Payment Service</b>", s["h3"]))
    story.append(pre("""
@CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")
@Retry(name = "paymentService", fallbackMethod = "paymentFallback")
@TimeLimiter(name = "paymentService")
public CompletableFuture<PaymentResponseDto> processPayment(PaymentRequestDto dto) {
    return CompletableFuture.supplyAsync(() -> 
        paymentServiceClient.createPayment(dto).getData()
    );
}

private CompletableFuture<PaymentResponseDto> paymentFallback(PaymentRequestDto dto, Exception ex) {
    // Queue payment for async processing
    paymentQueueService.enqueueForRetry(dto);
    
    return CompletableFuture.completedFuture(
        PaymentResponseDto.builder()
            .status("QUEUED")
            .message("Payment queued for processing")
            .build()
    );
}
    """))

    story.append(Paragraph("<b>Example 2: Menu Service with Bulkhead (limit concurrent calls)</b>", s["h3"]))
    story.append(pre("""
@Bulkhead(name = "menuService", type = Bulkhead.Type.THREADPOOL)
public List<MenuItemResponseDto> getMenuItems(Long restaurantId) {
    return menuServiceClient.getMenuByRestaurant(restaurantId).getData();
}
    """))

    story.append(Paragraph("<b>Example 3: Rate Limiter on public API</b>", s["h3"]))
    story.append(pre("""
@RateLimiter(name = "publicApi", fallbackMethod = "rateLimitFallback")
public ResponseEntity<ApiResponse<RestaurantResponseDto>> getRestaurant(Long id) {
    return ResponseEntity.ok(restaurantService.getRestaurantById(id));
}

private ResponseEntity<ApiResponse<RestaurantResponseDto>> rateLimitFallback(Long id, Exception ex) {
    return ResponseEntity.status(429).body(
        ApiResponse.error("Too many requests, please try again later", null)
    );
}
    """))

    story.append(Paragraph("<b>Example 4: Cache with Circuit Breaker</b>", s["h3"]))
    story.append(pre("""
@Cacheable(value = "restaurants", key = "#id")
@CircuitBreaker(name = "restaurantService", fallbackMethod = "restaurantFallback")
public RestaurantResponseDto getRestaurant(Long id) {
    return restaurantServiceClient.getRestaurantById(id).getData();
}

private RestaurantResponseDto restaurantFallback(Long id, Exception ex) {
    // Try to get from cache even if circuit is open
    return cacheManager.getCache("restaurants").get(id, RestaurantResponseDto.class);
}
    """))

    # ---- 13. MISTAKES ----
    story.append(Paragraph("13. Common Configuration Mistakes and Overuse of Retry", s["h1"]))

    story.append(Paragraph("<b>Common mistakes:</b>", s["h3"]))
    story.append(table([
        ["Mistake", "Impact", "Fix"],
        ["Setting failure threshold too high", "Too many failures before circuit opens", "Use 50-60% threshold"],
        ["Wait duration too short", "Circuit flips rapidly, doesn't give service time to recover", "Use 30-60 seconds minimum"],
        ["No timeout on Feign clients", "Threads block indefinitely on slow services", "Always set connect and read timeouts"],
        ["Retry without exponential backoff", "Retry storms overwhelm failing service", "Use exponential backoff (1s, 2s, 4s, 8s)"],
        ["Circuit breaker on non-critical paths", "Unnecessary complexity", "Use fallback only, no circuit breaker for non-critical services"],
        ["Ignoring specific exceptions", "Circuit never trips on real failures", "Only ignore business exceptions, not system exceptions"],
    ], col_widths=[4 * cm, 4 * cm, 5.5 * cm]))

    story.append(Paragraph("<b>Overuse of retry:</b>", s["h3"]))
    story.append(pre("""
# BAD: Excessive retry configuration
resilience4j:
  retry:
    instances:
      paymentService:
        maxAttempts: 10              # Too many retries
        waitDuration: 100ms         # Too fast between retries
        retryExceptions:
          - java.lang.Exception    # Retry on everything

# GOOD: Balanced retry configuration
resilience4j:
  retry:
    instances:
      paymentService:
        maxAttempts: 3              # Reasonable limit
        waitDuration: 1s           # Give service time
        exponentialBackoffMultiplier: 2  # Exponential backoff
        retryExceptions:
          - java.net.SocketTimeoutException
          - java.io.IOException
        ignoreExceptions:
          - com.foodflow.payment.exception.InsufficientFundsException
    """))

    story.append(Paragraph("<b>When NOT to use retry:</b>", s["h3"]))
    story.append(bullet_list([
        "Non-idempotent operations (POST without idempotency key)",
        "Business logic failures (insufficient funds, invalid data)",
        "Authentication failures (wrong password)",
        "Rate limit exceeded (429 status)",
        "Validation errors (400 status)",
    ], s["bullet"]))

    story.append(Paragraph("<b>Best practices summary:</b>", s["h3"]))
    story.append(bullet_list([
        "Use Circuit Breaker for all cross-service calls",
        "Use Retry only for transient network failures",
        "Always configure timeouts on Feign clients",
        "Implement meaningful fallbacks (not just null returns)",
        "Monitor circuit state and metrics",
        "Test failure scenarios in integration tests",
        "Don't over-engineer for non-critical paths",
    ], s["bullet"]))

    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(
        "FoodFlow Platform — Circuit Breaker & Resilience Patterns Guide v1.0",
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
        title="Circuit Breaker and Resilience Patterns",
        author="FoodFlow Platform",
    )

    def add_page_number(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {canvas.getPageNumber()}")
        canvas.drawString(2 * cm, 1.2 * cm, "FoodFlow Platform — Circuit Breaker & Resilience Patterns")
        canvas.restoreState()

    doc.build(build_document(), onFirstPage=add_page_number, onLaterPages=add_page_number)
    size_kb = PDF_PATH.stat().st_size / 1024
    print(f"Circuit Breaker PDF generated: {PDF_PATH} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
