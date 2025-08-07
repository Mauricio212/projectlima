# PROJECT LIMA OPERATIONAL DASHBOARD TESTING & CERTIFICATION PROCEDURE

## DOCUMENT CONTROL
**Document ID:** LIMA-OD-TEST-001  
**Version:** 1.0  
**Created:** August 1, 2025  
**Status:** ACTIVE  

## CRITICAL TESTING RULES
- ALL tests on ACTUAL systems only - NO simulations
- 100% verifiable dashboard data - 0% deviation tolerance  
- Real processes, connections, metrics ONLY

## PHASE 1: DASHBOARD HTTP RESPONSE TESTING

### TEST 1.1: Dashboard Accessibility
echo "=== DASHBOARD HTTP TEST ===" 
curl -s http://localhost:8080/ops-enhanced | head -20
echo "Expected: HTML response with Enhanced Operational Monitoring title"

### TEST 1.2: Response Time Testing  
echo "=== RESPONSE TIME TEST ==="
time curl -s http://localhost:8080/ops-enhanced > /dev/null
echo "Expected: Response under 2 seconds"
