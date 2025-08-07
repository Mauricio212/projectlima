# 📡 Warehouse API Specification

> FastAPI running on EC2 `52.200.101.103:8001`

---

## 🔐 Authentication

All routes require a valid API key in the `Authorization` header:

```http
Authorization: Bearer YOUR_API_KEY
