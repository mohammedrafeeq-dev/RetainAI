# Dataset

## Sales & Marketing Customer Dataset

Place the dataset file here with the name: **`Sales_Marketing_Customer_Dataset.csv`**

### Source

The dataset contains ~10,000 customer records with 30 features including:

| Feature Category | Examples |
|-----------------|----------|
| Demographics | `customer_id`, `gender`, `age`, `country`, `city` |
| Dates | `signup_date`, `last_purchase_date` |
| Acquisition | `acquisition_channel`, `device_type` |
| Behaviour | `total_spent`, `total_visits`, `avg_session_time` |
| Engagement | `email_open_rate`, `email_click_rate`, `coupon_code` |
| Satisfaction | `satisfaction_score`, `nps_score`, `support_tickets` |
| Financial | `payment_method`, `lifetime_value`, `marketing_spend_per_user` |
| **Target** | `churn` (0 = retained, 1 = churned) |

### Setup

1. Download or copy the CSV file into this `data/` directory
2. Ensure the filename matches: `Sales_Marketing_Customer_Dataset.csv`
3. The notebook will automatically load from this path
