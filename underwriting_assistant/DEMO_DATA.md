# Underwriting Assistant - Demo Test Data

Use this test data to evaluate the underwriting system. Copy and paste into the web form.

---

## Test 1: HIGH RISK — Delivery Driver with Frequent Claims

**Risk Level Expected:** 🔴 HIGH → Manual Review / Not Recommended

### Applicant Data:
```
Name: Rajesh Kumar
Age: 38
Occupation: Delivery Driver
Vehicle: Two-wheeler (used for commercial delivery)
Annual Mileage: 45,000 km
Coverage Requested: ₹5,00,000
Location: High traffic zone, Mumbai
```

### Claims History:
```
1. March 2023 - Accident claim - ₹85,000 (third party injury)
2. August 2023 - Theft claim - ₹1,20,000 (vehicle stolen at night)
3. January 2024 - Accident claim - ₹55,000 (collision damage)
```

### External Report:
```
Inspection Report: Vehicle shows multiple unrepaired dents and scratches.
Evidence of continuous daily commercial usage. Parking in unsecured open area.
Locality has repeated theft incidents reported. No valid commercial license
found for delivery operations.
```

---

## Test 2: MEDIUM RISK — Sales Executive with One Major Claim

**Risk Level Expected:** 🟡 MEDIUM → Acceptance with Conditions

### Applicant Data:
```
Name: Priya Sharma
Age: 32
Occupation: Sales Executive
Vehicle: Car (personal use declared, frequent city travel)
Annual Mileage: 22,000 km
Coverage Requested: ₹3,00,000
Location: Urban congested area, Bangalore
```

### Claims History:
```
1. November 2023 - Accident claim - ₹2,20,000 (major collision, total repair)
```

### External Report:
```
Medical and vehicle inspection completed. Vehicle repaired and roadworthy.
No prior fraud indicators. Credit score: 635. Applicant cooperative during
inspection. No conflicting information found.
```

---

## Test 3: LOW RISK — Government Employee, Clean Record

**Risk Level Expected:** 🟢 LOW → Standard Acceptance

### Applicant Data:
```
Name: Amit Verma
Age: 45
Occupation: Government Employee
Vehicle: Car (personal use only)
Annual Mileage: 8,000 km
Coverage Requested: ₹2,00,000
Location: Residential area, Pune
```

### Claims History:
```
No claims in the last 5 years. Clean driving record.
```

### External Report:
```
Vehicle in excellent condition. Secure garage parking available.
Credit score: 720. All identity documents verified. No discrepancies found.
```

---

## How to Use:

1. **Open the web UI:** http://127.0.0.1:5000
2. **Choose a test scenario** (start with Test 1 for most interesting results)
3. **Copy & paste the data** into the three text areas:
   - Paste "Applicant Data" section into the first textarea
   - Paste "Claims History" section into the second textarea
   - Paste "External Report" section into the third textarea
4. **Click Submit**
5. **Review the results** - Risk Level, Recommendation, Triggered Rules, etc.

---

## Expected Behaviors:

| Test | Triggers | Expected |
|------|----------|----------|
| **Test 1** | High-risk occupation + Multiple claims + Theft + Poor inspection + High mileage | HIGH risk score (75+), Manual review recommended |
| **Test 2** | Medium-risk occupation + 1 major claim + Borderline credit | MEDIUM risk score (31-70), Conditions may apply |
| **Test 3** | Low-risk occupation + No claims + Good credit + Excellent condition | LOW risk score (0-30), Standard acceptance |

---

## Optional: Advanced Testing

### Test 4: Edge Case — Missing Information
Copy one test, but set External Report to `N/A` or `Missing` to see how system handles incomplete data.

### Test 5: Fraud Signal
Add "prior fraud investigation" or "identity verification failure" to any test to see automatic flagging.

---

**Created:** March 17, 2026  
**Project:** Underwriting Assistant with Smart Rulebook Filtering  
**Version:** 1.0
