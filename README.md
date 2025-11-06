# AWS Windows Auto-Patching & Hardening with Zero-Downtime ASG (Terraform + Python)

Automates **Windows OS patching**, **CIS hardening**, **golden AMI**, and **zero-downtime rollout** using **Terraform IaC** and **Python (Boto3)**.

> **Reduced 1-week manual patching to under 1 hour with 100% compliance and zero downtime.**

---

## Overview

This project automates **end-to-end Windows EC2 security lifecycle** in an Auto Scaling Group (ASG):

1. **Patch & Harden** a running instance via **AWS SSM + PowerShell**
2. Create **hardened golden AMI** (`NoReboot=True`)
3. Deploy **latest app from S3** via UserData
4. Provision **VPC, ASG, ALB, Launch Template** using **Terraform IaC**
5. Perform **rolling refresh** (90% healthy) to replace old instances
6. Register new instances with **Load Balancer**

---

## Key Features

| Feature | Benefit |
|-------|--------|
| **AWS SSM + PowerShell** | No RDP, fully automated patching & hardening |
| **CIS-Level Hardening** | Disable Guest, enforce passwords, firewall, disable services |
| **Zero Downtime** | `NoReboot=True` + ASG rolling refresh |
| **Terraform IaC** | Reproducible, secure infrastructure |
| **S3 + UserData** | Auto-deploy latest app on boot |
| **CloudWatch Monitoring** | Full traceability |

---

## Tech Stack

- **Python (Boto3)** – Automation logic
- **Terraform** – VPC, ASG, ALB, Launch Template
- **AWS SSM** – Run PowerShell on Windows EC2
- **ASG + ALB** – Scalable, resilient deployment
- **S3** – Store app installer

---

## Setup

git clone https://github.com/Mamtesh2001/aws-windows-auto-patching-hardening-zero-downtime-asg-terraform-python.git

cd aws-windows-auto-patching-hardening-zero-downtime-asg-terraform-python

# Update variables in terraform/variables.tf

terraform init && terraform apply -auto-approve

python auto_deploy.py
