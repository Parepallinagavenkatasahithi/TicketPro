# TicketPro Security Specification

## Security Enforcement Rules
1. **Internal Notes Privacy**: Employees can NEVER post or view internal agent notes (`is_internal_note = True`). The API filters out internal notes from responses when the caller is an `EMPLOYEE`.
2. **Path Traversal Protection**: Uploaded filenames are sanitized and stored under random UUID identifiers (`storage/uploads/uuid.ext`). Original filenames are stored only as display metadata.
3. **MIME & Extension Whitelisting**: Executables (`.exe`, `.sh`, `.bat`) are strictly rejected. Allowed formats: `.png`, `.jpg`, `.pdf`, `.doc`, `.txt`, `.log`, `.zip`.
4. **RBAC Control**: All endpoints enforce permissions via `@require_permission(...)` backend dependencies.
5. **No Secrets Policy**: Environment variables use `.env.example` templates. No production secrets or credentials are hardcoded.
