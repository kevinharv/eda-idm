# Event Driven Identity Management System
**Enable near real-time identity management solution.**

# New Architecture
1. RESTful microservices - DB for each
1. Job scheduler - schedules actions based on events
1. Job executor - calls each service

# TEMP - To-Do
1. Setup GitHub Actions to build all services
1. PostgreSQL DB - single host (dev), DB per service
1. Kafka event bus
1. User service (primary) for CRUD
1. Rules service? Jobs to perform logic?
1. DB service to read input DB tables
1. CRON service to manage scheduled tasks
1. Group management service for automatic CRUD + membership?
1. Course management service
1. AD service
1. Entra ID service
1. Management portal/service/gateway

- AD connector should likely be written in .NET/C# with Windows Server target.
- Dynamic attributes should be supported where possible

# About


# Deployment


# Contribution
