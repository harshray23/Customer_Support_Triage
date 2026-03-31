---
title: Support Ticket Triage Environment
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---
# 🧠 Support Ticket Triage Environment (OpenEnv)

## 🚀 Overview

This project implements a **real-world customer support triage simulation environment** using the OpenEnv framework.

The environment models how modern companies (e.g., SaaS platforms) handle incoming customer support tickets by requiring an agent to:

- Classify the issue type  
- Assign an appropriate priority  
- Route the ticket to the correct team  
- Handle business-critical constraints (e.g., enterprise users, urgent issues)

---

## 🎯 Motivation

Customer support automation is a critical problem in real-world systems such as Zendesk, Freshdesk, and internal enterprise tools.

This environment is designed to evaluate **agent reasoning, prioritization, and decision-making**, rather than simple classification.

It introduces:
- Multi-step decision logic  
- Realistic trade-offs  
- Business-aware reward shaping  

---

## ⚙️ Environment Design

### 🧾 Observation Space

Each step provides:

- `ticket_id` — unique identifier  
- `message` — customer query (natural language)  
- `customer_tier` — `free`, `pro`, or `enterprise`  
- `step_count` — current timestep  

---

### 🎬 Action Space

The agent must output:

- `classify_as` → `billing`, `technical`, `account`, `other`  
- `priority` → `low`, `medium`, `high`, `urgent`  
- `assign_to` → `tier1`, `tier2`, `billing_team`, `security_team`  
- `respond` (optional)  

---

### 🧠 Tasks

The environment supports **3 difficulty levels**:

| Task | Description |
|------|------------|
| Easy | Classification only |
| Medium | Classification + Priority |
| Hard | Full triage (classification + priority + routing) |

---

## 🏆 Reward Design

The reward function is **multi-dimensional and realistic**, designed to reflect real-world decision quality.

### Components:

- ✅ Classification accuracy  
- ✅ Priority correctness  
- ✅ Routing correctness  
- ⚠️ Step penalty (efficiency)  
- 🚨 Urgent handling penalty  
- 💼 Enterprise customer importance  
- 🎯 Bonus for correct routing (hard task)

---

### 💡 Key Features

#### 🚨 Urgent Ticket Handling
Missing urgent priority results in a strong penalty: