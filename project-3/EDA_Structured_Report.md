# Exploratory Data Analysis (EDA) Project Report
**Dataset**: IBM Telecom Customer Churn

## 1. Project Objective
To analyze the Telco Customer dataset to uncover patterns and trends regarding customer churn, developing analytical thinking and data exploration skills.

## 2. Statistical Summaries 

| Feature | Count | Mean | Std Dev | Min | 25% | 50% | 75% | Max |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tenure (Months)** | 7032 | 32.42 | 24.54 | 1.00 | 9.00 | 29.00 | 55.00 | 72.00 |
| **Monthly Charges ($)** | 7032 | 64.79 | 30.08 | 18.25 | 35.58 | 70.35 | 89.86 | 118.75 |
| **Total Charges ($)** | 7032 | 2283.30 | 2266.77 | 18.80 | 401.45 | 1397.47 | 3794.73 | 8684.80 |

**Distribution Insights:**
- The average customer has been with the company for ~32 months. 
- Monthly charges span a wide range, from a minimum of \$18.25 to \$118.75, indicating distinct tiers of service (e.g., basic phone vs. full fiber-optic + TV).
- The dataset is relatively clean, requiring only the removal of 11 rows where `TotalCharges` was improperly recorded as blank strings.

## 3. Visualizations & Patterns Discovered
*(These patterns are actively mapped visually in the accompanying Streamlit Dashboard)*

1. **Demographic Risk**: Senior Citizens hold a disproportionately higher churn rate compared to younger demographics. Customers without dependents or partners are significantly more likely to leave the service.
2. **Service Risk (Internet)**: Customers on Fiber Optic networks churn at an alarming rate compared to those on DSL. This warrants an immediate quality-of-service investigation into the Fiber infrastructure.
3. **Contract Risk**: Month-to-Month contracts account for the vast majority of churned users. Customers locked into 1-year or 2-year contracts rarely leave.

## 4. Correlations and Key Influencing Factors

To calculate direct linear influences, we cast `Churn` to a binary numeric format (`Yes`=1, `No`=0) and analyzed Pearson Correlation coefficients against numeric factors:

*   **Tenure vs. Churn (-0.35)**: There is a moderate *negative* correlation. The longer a customer stays, the less likely they are to churn. 
*   **Monthly Charges vs. Churn (+0.19)**: There is a *positive* correlation. As the monthly bill increases, the customer becomes a higher flight risk.
*   **Total Charges vs. Tenure (+0.82)**: A highly positive, expected correlation since Total Charge is a direct product of tenure months and monthly bill.

**Top Influencing Factors (Categorical):**
1. **Tech Support & Online Security**: Customers lacking these two add-on services are vastly more vulnerable to churning.
2. **Payment Method**: Users paying by "Electronic Check" are churning significantly faster than those on automatic credit card/bank transfers.

## 5. Final Insights & Recommendations (Structured Outcome)

Through rigorous data exploration and analytical mapping, we conclude the following actionable business insights:

1. **Shift Customers off Month-to-Month**: Offer targeted discounts (e.g., 10% off the monthly bill) for Month-to-Month users who agree to sign a 1-year contract. The correlation data proves that extending tenure reduces flight risk significantly.
2. **Bundle "Sticky" Features**: Tech Support and Online Security drop churn drastically. These should be bundled for free for the first 6 months to get users accustomed to the lock-in ecosystem.
3. **Investigate Fiber Optics**: The high churn rate in the premium Fiber network suggests either pricing is uncompetitive or the service is unreliable. Comparing competitors in the local market is advised. 
4. **Push Auto-Pay**: Electronic Check users are churning. Implementing a $5 incentive for customers who switch to automatic credit card payments will increase retention.
