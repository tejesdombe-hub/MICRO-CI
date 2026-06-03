# Test Execution & CI/CD Integration Guide

**Date:** June 3, 2026  
**Updated For:** GitHub Actions CI/CD Pipeline  

---

## Quick Start

### Run All Tests Locally
```bash
cd /home/tejes.dombe/Downloads/MICRO
./mvnw clean test
```

### Run Tests with Coverage Report
```bash
./mvnw clean test jacoco:report
# Open target/site/jacoco/index.html in browser
```

### Run Specific Service Tests
```bash
# Auth Service tests
./mvnw test -Dtest=AuthServiceImplTest,AuthControllerTest

# Customer Service tests
./mvnw test -Dtest=CustomerServiceImplTest,CustomerControllerTest

# All tests for a service
./mvnw test -Dtest=*ServiceImpl*
```

---

## Test Execution Methods

### 1. Run Tests from IDE
- **IntelliJ IDEA/WebStorm:**
  - Right-click test file → "Run Tests"
  - Or use Ctrl+Shift+F10 (Windows/Linux) / Cmd+Shift+R (Mac)
  - Watch test execution in Run panel

- **VS Code:**
  - Use Test Explorer extension
  - Or run via terminal

### 2. Run Tests from Terminal
```bash
# Clean and run all tests
./mvnw clean test

# Run tests only (skip build)
./mvnw test

# Run with verbose output
./mvnw test -X

# Run with specific log level
./mvnw test -Dorg.slf4j.simpleLogger.defaultLogLevel=DEBUG

# Run tests in parallel
./mvnw test -T 1C
```

### 3. Run Tests from GitHub Actions
Push code to main branch:
```bash
git add .
git commit -m "Add test cases"
git push origin main
```

Monitor in GitHub → Actions → Workflow Run

### 4. Run Test Suite via Maven Surefire Plugin
```bash
# Generate test reports
./mvnw surefire:test

# View reports in browser
open target/site/surefire-report.html
```

---

## CI/CD Pipeline Integration

### Pipeline Overview
```
┌─────────────────────────────────────────────────────────────┐
│ GitHub Push to main / Pull Request                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│ Checkout Code                                               │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│ Setup Java 17 + Maven Cache                                │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│ Build Project (clean install)                               │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│ RUN ALL TESTS ⭐ (NEW)                                       │
│ • Unit Tests                                                │
│ • Integration Tests                                         │
│ • Service Tests (8 services)                                │
│ • Controller Tests                                          │
│ • Failure = Build Failure                                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│ GENERATE TEST REPORTS ⭐ (NEW)                               │
│ • Surefire reports HTML                                    │
│ • Test statistics                                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│ UPLOAD ARTIFACTS ⭐ (NEW)                                    │
│ • Store test results                                       │
│ • Downloadable from GitHub UI                              │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│ Build Docker Images (8 services) ← Only if tests pass      │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│ PUBLISH TEST REPORT ⭐ (NEW)                                 │
│ • GitHub Checks                                            │
│ • Summary annotation                                       │
│ • Test count display                                       │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│ Pipeline Complete ✅                                        │
│ • Tests passed: Proceed to Docker build                    │
│ • Tests failed: Notify developers                          │
└─────────────────────────────────────────────────────────────┘
```

### Workflow Configuration
**File:** `.github/workflows/main.yml`

**Key Test Steps:**

#### Step 1: Run Tests
```yaml
- name: Run All Unit & Integration Tests
  run: ./mvnw test -DfailIfNoTests=false
```
- Executes all tests in all services
- Fails build if any test fails
- Continues even if no tests found (safety flag)

#### Step 2: Generate Reports
```yaml
- name: Generate Test Report
  run: ./mvnw surefire-report:report
  if: always()
```
- Creates HTML test report
- Runs even if tests failed
- Located in `**/target/site/`

#### Step 3: Upload Artifacts
```yaml
- name: Upload Test Results Artifacts
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: test-results-${{ github.run_number }}
    path: |
      **/target/surefire-reports/
      **/target/site/
```
- Uploads test results to GitHub
- Downloadable from build summary
- Keep 30 days (GitHub default)

#### Step 4: Publish Test Report
```yaml
- name: Publish Test Report
  uses: dorny/test-reporter@v1
  if: always()
  with:
    name: Test Results
    path: '**/target/surefire-reports/TEST-*.xml'
    reporter: java-junit
    fail-on-error: false
```
- Parses JUnit XML format
- Shows in Checks tab
- Provides summary annotation

---

## Test Failure Handling

### When Tests Fail in CI/CD

1. **GitHub shows "Some checks failed"**
   - Click "Details" to view logs
   - Scroll to "Run All Tests" section
   - See failing test output

2. **Download Test Report**
   - Go to Artifacts section
   - Download `test-results-<number>` zip
   - Extract and open `index.html` in browser

3. **View in GitHub Checks**
   - View "Checks" tab
   - See "Test Results" annotation
   - Lists failed tests with details

4. **Fix and Retest**
   ```bash
   # Fix code locally
   vim src/main/java/com/fooddelivery/service/...
   
   # Run tests locally
   ./mvnw test -Dtest=FailingTestClass
   
   # Verify tests pass
   ./mvnw test
   
   # Push to trigger CI/CD
   git push origin main
   ```

### Common Test Failures

| Failure | Cause | Solution |
|---------|-------|----------|
| OutOfMemory | JVM heap too small | Increase in GitHub Actions or pom.xml |
| Connection Timeout | Network issues | Check Docker/DB startup |
| Mock Not Setup | Missing `when()` statement | Add mock setup in @BeforeEach |
| Assertion Failed | Logic error | Check test vs implementation |
| Class Not Found | Wrong package/import | Verify package structure |

---

## Test Reports Access

### Via GitHub Actions UI
1. Go to repository → Actions
2. Click on workflow run
3. Scroll to bottom → "Artifacts"
4. Download `test-results-<number>`

### Artifacts Content
```
test-results-<number>.zip/
├── surefire-reports/
│   ├── TEST-*.xml (JUnit format)
│   ├── TEST-*.txt (Plain text)
│   └── ...
├── site/
│   ├── surefire-report.html (Summary)
│   └── surefire-report.css
└── ...
```

### View Test Report Locally
```bash
# Generate locally
./mvnw clean test surefire-report:report

# Open in browser
open target/site/surefire-report.html
# or
firefox target/site/surefire-report.html
```

---

## Code Coverage Integration

### Local Coverage Report
```bash
# Generate coverage report
./mvnw clean test jacoco:report

# Open in browser
open target/site/jacoco/index.html
```

### Coverage Goals by Service
- Auth Service: > 85%
- Customer Service: > 80%
- Order Service: > 75%
- Payment Service: > 85%
- Restaurant Service: > 80%
- Menu Service: > 80%
- Delivery Partner Service: > 75%
- Notification Service: > 80%

### Add Coverage to CI/CD (Optional)
To add coverage reports to GitHub:
```yaml
- name: Generate Code Coverage Report
  run: ./mvnw jacoco:report

- name: Upload Coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    files: ./target/site/jacoco/jacoco.xml
    flags: unittests
    name: codecov-umbrella
```

---

## Test Debugging

### Debug a Single Test
```bash
# Run single test class
./mvnw test -Dtest=AuthServiceImplTest

# Run single test method
./mvnw test -Dtest=AuthServiceImplTest#testLoginSuccess

# Run with debugging output
./mvnw test -X -DenableAssertions=true
```

### Debug in IDE
- Set breakpoint in test or service code
- Right-click test → "Debug"
- Use Step Over/Into commands
- Inspect variables in Debug panel

### Add Debug Logging
```java
@Test
void testExample() {
    // Add logging
    log.debug("Test starting");
    
    // Set breakpoint here
    service.execute();
    
    log.debug("Test completed");
}
```

### View Full Test Output
```bash
# Quiet mode (less output)
./mvnw test -q

# Verbose mode (more output)
./mvnw test -X

# Show test names
./mvnw test -v
```

---

## Performance Optimization

### Run Tests in Parallel
```bash
# 4 parallel threads
./mvnw test -T 4

# 1 thread per core
./mvnw test -T 1C
```

### Skip Tests (Not Recommended)
```bash
# Skip tests (FOR DEVELOPMENT ONLY)
./mvnw clean install -DskipTests

# Skip security checks
./mvnw test -Dskip=true
```

### Test Execution Time
Expected execution times:
- Unit Tests: ~2-3 seconds total
- Integration Tests: ~1-2 seconds each
- Full Suite: ~30-60 seconds (service dependent)

### Optimize Slow Tests
1. Use `@ExtendWith(MockitoExtension.class)` for unit tests (faster)
2. Avoid real Spring context when possible
3. Cache spring context between tests
4. Use in-memory H2 database

---

## Continuous Integration Best Practices

### Pre-Push Checklist
Before pushing code:

```bash
# 1. Run all tests locally
./mvnw test

# 2. Check for compilation errors
./mvnw clean compile

# 3. Run code quality checks
./mvnw checkstyle:check

# 4. Generate coverage report
./mvnw jacoco:report

# 5. Verify coverage is acceptable
# (Open target/site/jacoco/index.html)

# 6. Push to main
git push origin main
```

### Git Workflow for Tests
```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes
vim src/main/java/...

# Add tests
vim src/test/java/...

# Run tests locally
./mvnw test

# Commit
git add .
git commit -m "Add feature with tests"

# Push and create PR
git push origin feature/my-feature
# Create Pull Request on GitHub

# GitHub Actions validates automatically
# If tests pass → Merge PR
# If tests fail → Fix and push again
```

---

## GitHub Actions Configuration Summary

### Build Agent
- **OS:** Ubuntu Latest (Linux)
- **Java:** Version 17 (Temurin distribution)
- **Maven:** Cached for faster builds
- **Timeout:** 60 minutes (default)

### Tests Executed
- **Framework:** JUnit 5 with Mockito
- **Build Tool:** Maven
- **Command:** `./mvnw test -DfailIfNoTests=false`
- **Failure Behavior:** Stops pipeline

### Reports Generated
- **Surefire Reports:** HTML + XML
- **JUnit XML:** For GitHub annotations
- **Artifacts:** 30-day retention

### Notifications
- **GitHub Email:** On workflow failure
- **GitHub Checks:** Pass/Fail in PR/commit
- **Artifacts:** Available 30 days

---

## Troubleshooting CI/CD

### Tests Pass Locally but Fail in CI

**Possible Causes:**
1. Environment differences (Java version, locale)
2. Timing issues (async operations)
3. Mock setup differences
4. File path issues

**Solutions:**
```bash
# Match CI Java version
java -version

# Run tests with CI environment
export MAVEN_OPTS="-Xmx512m -XX:MaxPermSize=256m"
./mvnw test

# Increase test timeout
./mvnw test -DsocketTimeoutInSeconds=30
```

### Artifacts Not Uploading

**Check in GitHub Actions:**
1. Look for upload step in logs
2. Verify artifact path is correct
3. Ensure tests run (artifacts only on test completion)

**Verify locally:**
```bash
./mvnw test
ls -la **/target/surefire-reports/
```

### Test Reporter Not Showing Results

**Solutions:**
1. Check XML format is correct
2. Verify reporter action version
3. Ensure XML files are generated

```bash
./mvnw test surefire-report:report
ls -la **/target/surefire-reports/TEST-*.xml
```

---

## Integration with Pull Requests

### PR Workflow
1. **Create PR** on GitHub
2. **Trigger Workflow** automatically
3. **Show Status Check** in PR
4. **Display Test Results** in Checks tab
5. **Require Status Check** for merge (optional setting)

### Require Tests Before Merge
**In GitHub Repository Settings:**
1. Go to Settings → Branches
2. Select branch protection rule for `main`
3. Enable "Require status checks to pass"
4. Select "build" job as required

---

## Monitoring & Analytics

### GitHub Actions Insights
1. Go to Actions tab
2. Filter by workflow or date
3. View success/failure trends
4. Analyze execution times

### Test Metrics
```bash
# Generate test statistics
./mvnw test

# Count test methods
grep -r "@Test" src/test/java | wc -l

# Analyze test execution time
./mvnw test -q

# Count assertions
grep -r "assertThat\|assertEquals\|assertTrue" src/test/java | wc -l
```

---

## Maintenance Schedule

### Weekly
- Monitor test failures
- Review coverage trends
- Update dependencies if needed

### Monthly
- Review test effectiveness
- Update test documentation
- Add tests for new features

### Quarterly
- Audit test quality
- Optimize slow tests
- Refactor test code

---

## References

- [Maven Surefire Plugin](https://maven.apache.org/surefire/maven-surefire-plugin/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [JUnit 5 Guide](https://junit.org/junit5/docs/current/user-guide/)
- [Mockito Documentation](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html)

---

## Support

For issues or questions:
1. Check TEST_CASES_DOCUMENTATION.md for test details
2. Check FILE_TRACKING_CHANGES.md for file locations
3. Review GitHub Actions logs for CI/CD issues
4. Run tests locally with verbose output: `./mvnw test -X`

---

**Last Updated:** June 3, 2026  
**Status:** Ready for production  
**Maintained By:** DevOps/QA Team

