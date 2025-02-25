# AWS CloudWatch Automation 

## Overview
This project automates fetching **CloudWatch metrics for EC2 and S3** using Python and **boto3**. It allows users to:
- Select an EC2 instance and retrieve **CPU utilization**.
- Select an S3 bucket and fetch **storage size & object count**.
- Handle edge cases like missing metrics, stopped instances, and empty buckets.

This was built as part of a structured learning roadmap for AWS CloudWatch monitoring. We faced a few challenges along the way, and this README walks through the process, so you get **both the solution and the learning experience.**

---

## Setup & Prerequisites

### Install Required Packages
Ensure you have **boto3** installed:
```bash
pip install boto3
```

### Configure AWS Credentials
If not configured, set up AWS CLI with:
```bash
aws configure
```
You'll need **IAM permissions** to read CloudWatch metrics and S3 bucket info.

---

##  How We Built This (Step-by-Step)

### Step 1: Fetch EC2 Instances & Retrieve CPU Utilization
**Goal:** Fetch all EC2 instances and let the user pick one to monitor CPU utilization.

**Challenges Faced & Solutions:**
- Initially, the script failed due to **stopped instances having no metrics** in CloudWatch. We fixed this by checking the instance state before querying metrics.
- Encountered **non-ASCII character errors** in instance IDs. Fixed by ensuring proper string formatting.

**Final Implementation:**
- Fetch running instances and display them.
- Let the user pick an instance by number or manually enter an ID.
- Retrieve CPU utilization metrics and display them in a human-readable format.

### Step 2: Fetch S3 Bucket Storage Metrics
**Goal:** List available S3 buckets, allow user selection, and retrieve storage size and object count.

**Challenges Faced & Solutions:**
- CloudWatch doesn’t show **real-time data** for S3. We handled this by **checking existing CloudWatch metrics instead of fetching live data**.
- When testing with an empty bucket, it displayed "0 GB," which was misleading. We fixed this by displaying **bytes when under 1MB**.

**Final Implementation:**
- Fetch all available S3 buckets and display them.
- Let the user select a bucket.
- Retrieve and display **storage size & object count**.

### Step 3: GitHub Integration & Debugging Issues

**Challenges Faced:**
- `git push origin main` failed with *"src refspec main does not match any"*.
- The fix: Ensure a valid branch exists, commit files first, then push.

**Final Steps:**
```bash
git init
git add .
git commit -m "Initial commit - AWS CloudWatch Automation"
git branch -M main
git remote add origin git@github.com:Extraordinarytechy/AWS-Cloudwatch-Automation.git
git push -u origin main
```

---

## How to Run the Script

### Running EC2 Monitoring
```bash
python EC2-CPU.py
```
- Select an instance to fetch CPU utilization.
- If the instance is stopped, an appropriate message is displayed.

### Running S3 Monitoring
```bash
python S3-CW.py
```
- Select a bucket to fetch storage details.
- Shows size in **GB, MB, or bytes** depending on content.

---

# Next Steps
- Adding **CloudWatch alarms** for automatic alerts.
- Expanding support for more AWS services.

**Contributions & Feedback:** Feel free to **fork**, raise issues, or suggest improvements!

---

# Built as part of our AWS learning roadmap. Every challenge faced & fixed is documented here to help others on the same path! 

