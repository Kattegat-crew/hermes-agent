---
name: gmail-mailbox-organization
description: "Label, archive and filter Gmail mailboxes safely, verified."
version: 1.0.0
author: Ragnar (NeuralCrew Labs)
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [Email, Gmail, Labels, Filters, Inbox, Integrations]
    related_skills: [google-workspace, email-inbox-triage, email-report-ingestion]
---

# Gmail Mailbox Organization

Structural cleanup of a Gmail mailbox: classify historical mail into a sender-based label tree, archive machine noise out of INBOX, and create native filters so FUTURE mail lands labeled without ever appearing in INBOX. This is not triage (priorities/replies — that is `email-inbox-triage`); it is one-time ordering plus permanent inbound routing.

Accounts are accessed with per-owner OAuth credentials in `/opt/data/secrets/{owner}-gmail.json`. Quirk: the `scopes` field may be a STRING — wrap it in a list before building `google.oauth2.credentials.Credentials`.

## When to Use

- "Organiza/limpia el correo de X" — full mailbox ordering by sender → label.
- Inbox flooding with automated mail that should arrive pre-labeled.
- Extending an existing label tree to cover new senders.

## Procedure

1. **Inventory**: pull senders + counts via `messages.list` paginated (`maxResults=500`), normalize addresses, aggregate by sender. Save a JSON inventory file.
2. **Propose map**: sender (or domain-level fallback) → label tree, e.g. `Sistema/GitHub`, `Sistema/Dominio-Web`, `Cobros/Facturas`, `Marketing/Herramientas`. Present tree + counts for approval before mutating.
3. **Backup first**: dump the map AND all message ids per label to a JSON backup before any mutation.
4. **Classify historical**: `batchModify` with `addLabelIds` + `removeLabelIds:["INBOX"]` (label + archive). Hard rule: ONLY label and archive — never delete, never mark read/spam.
5. **Verify two ways**: paginated `messages.list` per label AND `labels.get` `messagesTotal`; both must agree. Gmail auto-creates missing labels.
6. **Future mail = native filters**: the filters API needs scope `gmail.settings.basic`, which existing tokens usually lack. Expand scope via a fresh consent URL; validate Google accepts it (HTTP 200, no `invalid_scope` error) BEFORE asking the user to click. Then `POST /gmail/v1/users/me/settings/filters` with `addLabelIds` + `removeLabelIds:["INBOX"]` per rule.
7. **Fallback** if the user won't re-consent: schedule the classifier on a cron (works, not instant — new mail sits in INBOX until the next tick).

## Pitfalls

- **Incremental runs**: label counts are cumulative. Comparing "messages labeled this run" against the label's total produces false REVISAR verdicts — track run-new vs total separately.
- **Trash counts**: `labels.get` totals include messages in TRASH — a label can show messages you never filed (e.g. an alert that was already trashed).
- **New senders between inventory and run**: match by domain rule, not only exact address, or mail gets missed on the second pass.
- A scope the token lacks is a user click away, never guessable — no workaround exists for `settings/filters` without `gmail.settings.basic`.

## Verification

- [ ] Label membership confirmed by two independent queries that agree.
- [ ] No message deleted or marked-read anywhere in the run.
- [ ] Backup file exists with map + message ids.
- [ ] Future-mail path decided: filters created, or cron fallback explicitly accepted by the user.
