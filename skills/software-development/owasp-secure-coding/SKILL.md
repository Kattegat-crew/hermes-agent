---
name: owasp-secure-coding
description: OWASP Top 10 prevention, secure coding guidelines, input validation, CSRF, XSS, and authorization checks.
license: MIT
compatibility: opencode
---

# OWASP Secure Coding Guidelines

Defensive coding standards to eliminate security vulnerabilities.

## Core Protections
1. **Injection Prevention**: Always use parameterized queries or ORMs; never concatenate user input into SQL or shell commands.
2. **Broken Object Level Authorization (BOLA)**: Always verify that the authenticated user owns the requested resource ID in every handler.
3. **XSS & Content Security Policy (CSP)**: Sanitize HTML outputs and enforce strict CSP headers (`default-src 'self'`).
4. **Sensitive Data Exposure**: Hash passwords with Argon2id or bcrypt; mask PII in logs; store secrets only in environment variables.
