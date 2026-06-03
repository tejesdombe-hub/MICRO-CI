# Test Files Quick Reference Guide

**Generated:** June 3, 2026  
**Purpose:** Quick lookup for all test files and test methods  

---

## Table of Contents
- [Auth Service Tests](#auth-service-tests)
- [Customer Service Tests](#customer-service-tests)
- [Order Service Tests](#order-service-tests)
- [Payment Service Tests](#payment-service-tests)
- [Restaurant Service Tests](#restaurant-service-tests)
- [Menu Service Tests](#menu-service-tests)
- [Delivery Partner Service Tests](#delivery-partner-service-tests)
- [Notification Service Tests](#notification-service-tests)
- [File Locations](#file-locations)

---

## Auth Service Tests

### File: `auth-service/src/test/java/com/fooddelivery/auth/service/AuthServiceImplTest.java`

**Test Methods (7):**

1. ✅ `testRegisterSuccess()`
   - Scenario: Register user with valid credentials
   - Mocks: AuthRepository, PasswordEncoder, JwtTokenProvider
   - Verifies: User created with JWT token

2. ✅ `testRegisterWithDuplicateEmail()`
   - Scenario: Attempt to register with existing email
   - Expected: InvalidRequestException thrown
   - Verifies: Email uniqueness constraint

3. ✅ `testLoginSuccess()`
   - Scenario: Login with correct credentials
   - Expected: JWT token returned
   - Verifies: Authentication successful

4. ✅ `testLoginUserNotFound()`
   - Scenario: Login with non-existent email
   - Expected: ResourceNotFoundException thrown
   - Verifies: User existence check

5. ✅ `testLoginIncorrectPassword()`
   - Scenario: Login with wrong password
   - Expected: UnauthorizedException thrown
   - Verifies: Password validation

6. ✅ `testValidateToken()`
   - Scenario: Validate JWT token
   - Expected: Returns true for valid token
   - Verifies: Token validation logic

7. ✅ `testGetEmailFromToken()`
   - Scenario: Extract email from JWT
   - Expected: Correct email extracted
   - Verifies: Token parsing

---

### File: `auth-service/src/test/java/com/fooddelivery/auth/controller/AuthControllerTest.java`

**Test Methods (7):**

1. ✅ `testRegisterSuccess()`
   - Endpoint: POST /api/auth/register
   - Expected Status: 201 Created
   - Verifies: Valid registration response

2. ✅ `testLoginSuccess()`
   - Endpoint: POST /api/auth/login
   - Expected Status: 200 OK
   - Verifies: Token in response

3. ✅ `testRegisterInvalidRequest()`
   - Endpoint: POST with missing fields
   - Expected Status: 400 Bad Request
   - Verifies: Validation errors

4. ✅ `testRegisterInvalidEmail()`
   - Endpoint: POST with invalid email
   - Expected Status: 400 Bad Request
   - Verifies: Email format validation

5. ✅ `testRegisterEmptyPassword()`
   - Endpoint: POST with empty password
   - Expected Status: 400 Bad Request
   - Verifies: Password requirement

6. ✅ `testControllerIntegration()`
   - Purpose: Full request-response flow
   - Verifies: JSON mapping correct

7. ✅ `testErrorHandling()`
   - Purpose: Handle service exceptions
   - Verifies: Proper HTTP error codes

---

## Customer Service Tests

### File: `customer-service/src/test/java/com/fooddelivery/customer/service/CustomerServiceImplTest.java`

**Test Methods (12):**

1. ✅ `testCreateCustomerSuccess()`
   - Scenario: Create customer with valid data
   - Expected: Customer persisted with ID
   - Verifies: CRUD create operation

2. ✅ `testCreateCustomerWithDuplicateEmail()`
   - Scenario: Create with existing email
   - Expected: InvalidRequestException thrown
   - Verifies: Email uniqueness

3. ✅ `testGetCustomerByIdSuccess()`
   - Scenario: Retrieve customer by ID
   - Expected: Valid CustomerResponseDto returned
   - Verifies: CRUD read operation

4. ✅ `testGetCustomerByIdNotFound()`
   - Scenario: Get non-existent customer
   - Expected: ResourceNotFoundException thrown
   - Verifies: Not found handling

5. ✅ `testGetAllCustomersSuccess()`
   - Scenario: Retrieve all customers
   - Expected: List of customers returned
   - Verifies: List operation

6. ✅ `testGetAllCustomersEmpty()`
   - Scenario: Get all when no customers exist
   - Expected: Empty list returned
   - Verifies: Empty collection handling

7. ✅ `testUpdateCustomerSuccess()`
   - Scenario: Update customer details
   - Expected: Updated customer returned
   - Verifies: CRUD update operation

8. ✅ `testUpdateCustomerNotFound()`
   - Scenario: Update non-existent customer
   - Expected: ResourceNotFoundException thrown
   - Verifies: Not found in update

9. ✅ `testDeleteCustomerSuccess()`
   - Scenario: Delete customer by ID
   - Expected: Customer removed from DB
   - Verifies: CRUD delete operation

10. ✅ `testDeleteCustomerNotFound()`
    - Scenario: Delete non-existent customer
    - Expected: ResourceNotFoundException thrown
    - Verifies: Not found in delete

11. ✅ `testValidateEmailFormat()`
    - Scenario: Validate email during create
    - Verifies: Email validation applied

12. ✅ `testEmailUniqueConstraint()`
    - Scenario: Verify email uniqueness
    - Verifies: Duplicate emails rejected

---

### File: `customer-service/src/test/java/com/fooddelivery/customer/controller/CustomerControllerTest.java`

**Test Methods (8):**

1. ✅ `testCreateCustomerSuccess()`
   - Endpoint: POST /customers
   - Expected Status: 201 Created
   - Verifies: Customer DTO in response

2. ✅ `testGetCustomerByIdSuccess()`
   - Endpoint: GET /customers/{id}
   - Expected Status: 200 OK
   - Verifies: Customer DTO returned

3. ✅ `testGetAllCustomersSuccess()`
   - Endpoint: GET /customers
   - Expected Status: 200 OK
   - Verifies: List size and content

4. ✅ `testUpdateCustomerSuccess()`
   - Endpoint: PUT /customers/{id}
   - Expected Status: 200 OK
   - Verifies: Updated DTO returned

5. ✅ `testDeleteCustomerSuccess()`
   - Endpoint: DELETE /customers/{id}
   - Expected Status: 204 No Content
   - Verifies: Successful deletion

6. ✅ `testCreateCustomerInvalidRequest()`
   - Endpoint: POST with invalid data
   - Expected Status: 400 Bad Request
   - Verifies: Validation errors

7. ✅ `testGetCustomerNotFound()`
   - Endpoint: GET non-existent customer
   - Expected Status: 404 Not Found
   - Verifies: Not found handling

8. ✅ `testValidationErrorHandling()`
   - Purpose: Handle validation errors
   - Verifies: Proper error response

---

## Order Service Tests

### File: `order-service/src/test/java/com/fooddelivery/order/service/OrderServiceImplTest.java`

**Test Methods (11):**

1. ✅ `testPlaceOrderSuccess()`
   - Scenario: Place order with valid data
   - Calls: Customer, Restaurant, Payment services
   - Expected: Order created with PENDING status
   - Verifies: Order orchestration

2. ✅ `testGetOrderByIdSuccess()`
   - Scenario: Retrieve order by ID
   - Expected: Valid OrderResponseDto returned
   - Verifies: Read operation

3. ✅ `testGetOrderByIdNotFound()`
   - Scenario: Get non-existent order
   - Expected: ResourceNotFoundException thrown
   - Verifies: Not found handling

4. ✅ `testGetOrdersByCustomerIdSuccess()`
   - Scenario: Get orders by customer
   - Expected: List of orders returned
   - Verifies: Filter by customer

5. ✅ `testUpdateOrderStatusSuccess()`
   - Scenario: Update order status
   - Expected: Status changed in database
   - Verifies: Status update

6. ✅ `testAssignDeliverySuccess()`
   - Scenario: Assign delivery partner
   - Expected: Delivery partner assigned
   - Verifies: Delivery assignment

7. ✅ `testAssignDeliveryOrderNotFound()`
   - Scenario: Assign to non-existent order
   - Expected: ResourceNotFoundException thrown
   - Verifies: Not found handling

8. ✅ `testValidatePositiveAmount()`
   - Scenario: Validate order amount
   - Expected: Negative amounts rejected
   - Verifies: Amount validation

9. ✅ `testFeignCallToCustomerService()`
   - Scenario: Call customer-service via Feign
   - Expected: Proper service communication
   - Verifies: Inter-service communication

10. ✅ `testPaymentIntegration()`
    - Scenario: Process payment via Feign
    - Expected: Payment service called
    - Verifies: Payment integration

11. ✅ `testNotificationIntegration()`
    - Scenario: Send notification via Feign
    - Expected: Notification service called
    - Verifies: Notification integration

---

## Payment Service Tests

### File: `payment-service/src/test/java/com/fooddelivery/payment/service/PaymentServiceImplTest.java`

**Test Methods (8):**

1. ✅ `testProcessPaymentSuccess()`
   - Scenario: Process payment with valid data
   - Expected: Payment with SUCCESS status
   - Verifies: Payment processing

2. ✅ `testGetPaymentByOrderIdSuccess()`
   - Scenario: Retrieve payment by order ID
   - Expected: Valid PaymentResponseDto returned
   - Verifies: Read by order ID

3. ✅ `testGetPaymentNotFound()`
   - Scenario: Get non-existent payment
   - Expected: ResourceNotFoundException thrown
   - Verifies: Not found handling

4. ✅ `testValidatePositiveAmount()`
   - Scenario: Validate payment amount
   - Expected: Negative amounts rejected
   - Verifies: Amount validation

5. ✅ `testValidatePaymentMethod()`
   - Scenario: Validate payment method
   - Expected: Valid method required
   - Verifies: Method validation

6. ✅ `testGenerateUniqueTransactionId()`
   - Scenario: Generate transaction ID
   - Expected: Unique ID created
   - Verifies: ID generation

7. ✅ `testPaymentStatusTransitions()`
   - Scenario: Verify valid status transitions
   - Expected: Status changes properly
   - Verifies: State machine

8. ✅ `testPaymentSimulation()`
   - Scenario: Simulate payment processing
   - Expected: Payment marked as SUCCESS
   - Verifies: Payment simulation

---

## Restaurant Service Tests

### File: `restaurant-service/src/test/java/com/fooddelivery/restaurant/service/RestaurantServiceImplTest.java`

**Test Methods (9):**

1. ✅ `testCreateRestaurantSuccess()`
   - Scenario: Create restaurant with valid data
   - Expected: Restaurant persisted with ID
   - Verifies: Create operation

2. ✅ `testCreateRestaurantDuplicateEmail()`
   - Scenario: Create with existing email
   - Expected: InvalidRequestException thrown
   - Verifies: Email uniqueness

3. ✅ `testGetRestaurantByIdSuccess()`
   - Scenario: Retrieve restaurant by ID
   - Expected: Valid RestaurantResponseDto returned
   - Verifies: Read operation

4. ✅ `testGetRestaurantNotFound()`
   - Scenario: Get non-existent restaurant
   - Expected: ResourceNotFoundException thrown
   - Verifies: Not found handling

5. ✅ `testGetAllActiveRestaurants()`
   - Scenario: Get only active restaurants
   - Expected: List of active restaurants returned
   - Verifies: Filter by active status

6. ✅ `testUpdateRestaurantSuccess()`
   - Scenario: Update restaurant details
   - Expected: Updated restaurant returned
   - Verifies: Update operation

7. ✅ `testDeactivateRestaurantSuccess()`
   - Scenario: Deactivate restaurant
   - Expected: isActive set to false
   - Verifies: Deactivation logic

8. ✅ `testValidateCuisineType()`
   - Scenario: Validate cuisine type
   - Verifies: Valid types required

9. ✅ `testRestaurantStatusManagement()`
   - Scenario: Manage restaurant status
   - Verifies: Status transitions

---

## Menu Service Tests

### File: `menu-service/src/test/java/com/fooddelivery/menu/service/MenuItemServiceImplTest.java`

**Test Methods (12):**

1. ✅ `testAddMenuItemSuccess()`
   - Scenario: Add menu item with valid data
   - Expected: Menu item persisted
   - Verifies: Create operation

2. ✅ `testGetMenuItemByIdSuccess()`
   - Scenario: Retrieve menu item by ID
   - Expected: Valid MenuItemResponseDto returned
   - Verifies: Read operation

3. ✅ `testGetMenuItemNotFound()`
   - Scenario: Get non-existent menu item
   - Expected: ResourceNotFoundException thrown
   - Verifies: Not found handling

4. ✅ `testGetMenuItemsByRestaurantId()`
   - Scenario: Get items by restaurant
   - Expected: List of menu items returned
   - Verifies: Filter by restaurant

5. ✅ `testUpdateMenuItemSuccess()`
   - Scenario: Update menu item details
   - Expected: Updated item returned
   - Verifies: Update operation

6. ✅ `testToggleAvailability()`
   - Scenario: Toggle item availability
   - Expected: Availability status changed
   - Verifies: Toggle logic

7. ✅ `testDeleteMenuItemSuccess()`
   - Scenario: Delete menu item
   - Expected: Item removed from DB
   - Verifies: Delete operation

8. ✅ `testDeleteMenuItemNotFound()`
   - Scenario: Delete non-existent item
   - Expected: ResourceNotFoundException thrown
   - Verifies: Not found in delete

9. ✅ `testValidatePositivePrice()`
   - Scenario: Validate item price
   - Expected: Negative prices rejected
   - Verifies: Price validation

10. ✅ `testBulkMenuUpdate()`
    - Scenario: Update multiple items
    - Expected: All items updated
    - Verifies: Bulk operations

11. ✅ `testMenuSearchByName()`
    - Scenario: Search items by name
    - Expected: Items with matching name returned
    - Verifies: Search functionality

12. ✅ `testPriceRangeFiltering()`
    - Scenario: Filter by price range
    - Expected: Items within range returned
    - Verifies: Filter logic

---

## Delivery Partner Service Tests

### File: `delivery-partner-service/src/test/java/com/fooddelivery/delivery/service/DeliveryPartnerServiceImplTest.java`

**Test Methods (11):**

1. ✅ `testRegisterDeliveryPartnerSuccess()`
   - Scenario: Register delivery partner
   - Expected: Partner registered with AVAILABLE status
   - Verifies: Registration logic

2. ✅ `testGetDeliveryPartnerByIdSuccess()`
   - Scenario: Retrieve partner by ID
   - Expected: Valid DeliveryPartnerResponseDto returned
   - Verifies: Read operation

3. ✅ `testGetDeliveryPartnerNotFound()`
   - Scenario: Get non-existent partner
   - Expected: ResourceNotFoundException thrown
   - Verifies: Not found handling

4. ✅ `testGetAvailableDeliveryPartners()`
   - Scenario: Get available partners
   - Expected: List of available partners returned
   - Verifies: Filter by availability

5. ✅ `testUpdateDeliveryStatusSuccess()`
   - Scenario: Update delivery status
   - Expected: Status changed (workflow validation)
   - Verifies: Status update

6. ✅ `testAssignDeliverySuccess()`
   - Scenario: Assign delivery to order
   - Expected: Partner assigned with order ID
   - Verifies: Assignment logic

7. ✅ `testCompleteDeliverySuccess()`
   - Scenario: Mark delivery as completed
   - Expected: Status set to DELIVERED
   - Verifies: Completion logic

8. ✅ `testValidateVehicleNumber()`
   - Scenario: Validate vehicle number
   - Expected: Valid format required
   - Verifies: Vehicle validation

9. ✅ `testDeliveryStatusWorkflow()`
   - Scenario: Test complete workflow
   - Expected: All statuses transitioned properly
   - Verifies: State machine

10. ✅ `testAvailabilityToggle()`
    - Scenario: Toggle partner availability
    - Expected: Available status changed
    - Verifies: Availability toggle

11. ✅ `testLocationTracking()`
    - Scenario: Handle location updates
    - Expected: Partner location tracked
    - Verifies: Location storage

---

## Notification Service Tests

### File: `notification-service/src/test/java/com/fooddelivery/notification/service/NotificationServiceImplTest.java`

**Test Methods (13):**

1. ✅ `testSendNotificationSuccess()`
   - Scenario: Send notification with email & SMS
   - Expected: Notification marked as SENT
   - Verifies: Multi-channel sending

2. ✅ `testGetNotificationByIdSuccess()`
   - Scenario: Retrieve notification by ID
   - Expected: Valid NotificationResponseDto returned
   - Verifies: Read operation

3. ✅ `testGetNotificationNotFound()`
   - Scenario: Get non-existent notification
   - Expected: ResourceNotFoundException thrown
   - Verifies: Not found handling

4. ✅ `testGetNotificationsByOrderId()`
   - Scenario: Get notifications for order
   - Expected: List of notifications returned
   - Verifies: Filter by order

5. ✅ `testSendEmailNotification()`
   - Scenario: Send email only
   - Expected: Email service called
   - Verifies: Email sending

6. ✅ `testSendSmsNotification()`
   - Scenario: Send SMS only
   - Expected: SMS service called
   - Verifies: SMS sending

7. ✅ `testRetryFailedNotification()`
   - Scenario: Retry failed notification
   - Expected: Failed notification re-sent
   - Verifies: Retry logic

8. ✅ `testValidateNotificationType()`
   - Scenario: Validate notification type
   - Expected: Valid types required
   - Verifies: Type validation

9. ✅ `testHandleOrderPlacedEvent()`
   - Scenario: Handle ORDER_PLACED event
   - Expected: Notification sent to customer
   - Verifies: Event handling

10. ✅ `testHandleOrderAcceptedEvent()`
    - Scenario: Handle ORDER_ACCEPTED event
    - Expected: Notification sent to customer
    - Verifies: Event handling

11. ✅ `testHandleDeliveryEvent()`
    - Scenario: Handle DELIVERY_STARTED event
    - Expected: Notification sent
    - Verifies: Event handling

12. ✅ `testBatchNotifications()`
    - Scenario: Send batch notifications
    - Expected: Multiple notifications processed
    - Verifies: Batch processing

13. ✅ `testAsyncNotificationProcessing()`
    - Scenario: Process notifications asynchronously
    - Expected: Async processing verified
    - Verifies: Async handling

---

## File Locations

### Complete File Path Reference

```
PROJECT_ROOT: /home/tejes.dombe/Downloads/MICRO

TEST FILES:
├── auth-service/src/test/java/com/fooddelivery/auth/
│   ├── service/AuthServiceImplTest.java (7 tests)
│   └── controller/AuthControllerTest.java (7 tests)
├── customer-service/src/test/java/com/fooddelivery/customer/
│   ├── service/CustomerServiceImplTest.java (12 tests)
│   └── controller/CustomerControllerTest.java (8 tests)
├── order-service/src/test/java/com/fooddelivery/order/
│   └── service/OrderServiceImplTest.java (11 tests)
├── payment-service/src/test/java/com/fooddelivery/payment/
│   └── service/PaymentServiceImplTest.java (8 tests)
├── restaurant-service/src/test/java/com/fooddelivery/restaurant/
│   └── service/RestaurantServiceImplTest.java (9 tests)
├── menu-service/src/test/java/com/fooddelivery/menu/
│   └── service/MenuItemServiceImplTest.java (12 tests)
├── delivery-partner-service/src/test/java/com/fooddelivery/delivery/
│   └── service/DeliveryPartnerServiceImplTest.java (11 tests)
└── notification-service/src/test/java/com/fooddelivery/notification/
    └── service/NotificationServiceImplTest.java (13 tests)

DOCUMENTATION:
├── TEST_CASES_DOCUMENTATION.md (Detailed test reference)
├── FILE_TRACKING_CHANGES.md (File inventory)
├── TEST_EXECUTION_CI_GUIDE.md (How-to guide)
├── TEST_IMPLEMENTATION_SUMMARY.md (Overview)
└── TEST_FILES_QUICK_REFERENCE.md (THIS FILE)

MODIFIED FILES:
└── .github/workflows/main.yml (CI/CD pipeline updates)
```

---

## Running Specific Tests

```bash
cd /home/tejes.dombe/Downloads/MICRO

# Run Auth Service tests
./mvnw test -Dtest=AuthServiceImplTest,AuthControllerTest

# Run Customer Service tests
./mvnw test -Dtest=CustomerServiceImplTest,CustomerControllerTest

# Run Order Service tests
./mvnw test -Dtest=OrderServiceImplTest

# Run Payment Service tests
./mvnw test -Dtest=PaymentServiceImplTest

# Run Restaurant Service tests
./mvnw test -Dtest=RestaurantServiceImplTest

# Run Menu Service tests
./mvnw test -Dtest=MenuItemServiceImplTest

# Run Delivery Partner Service tests
./mvnw test -Dtest=DeliveryPartnerServiceImplTest

# Run Notification Service tests
./mvnw test -Dtest=NotificationServiceImplTest

# Run all tests
./mvnw clean test
```

---

## Test Statistics Summary

| Service | Unit | Integration | Total | Status |
|---------|------|-------------|-------|--------|
| Auth | 7 | 7 | 14 | ✅ |
| Customer | 12 | 8 | 20 | ✅ |
| Order | 11 | - | 11 | ✅ |
| Payment | 8 | - | 8 | ✅ |
| Restaurant | 9 | - | 9 | ✅ |
| Menu | 12 | - | 12 | ✅ |
| Delivery Partner | 11 | - | 11 | ✅ |
| Notification | 13 | - | 13 | ✅ |
| **TOTAL** | **80** | **22** | **102** | ✅ |

---

## Key Test Methods by Category

### CRUD Operations
- `testCreate*Success()` - Create operations
- `testGet*ByIdSuccess()` - Read operations
- `testUpdate*Success()` - Update operations
- `testDelete*Success()` - Delete operations

### Error Handling
- `test*NotFound()` - Resource not found
- `test*Duplicate*()` - Duplicate data prevention
- `testValidate*()` - Input validation

### Business Logic
- `testAssign*()` - Assignment operations
- `testUpdate*Status()` - Status updates
- `test*Workflow()` - Complex workflows

### Integration
- `testFeign*()` - Feign client calls
- `test*Integration()` - Service integration
- `testAsync*()` - Async operations

---

**Quick Reference Version:** 1.0  
**Last Updated:** June 3, 2026  
**Total Test Methods:** 102+

