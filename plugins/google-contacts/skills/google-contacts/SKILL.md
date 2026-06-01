---
name: google-contacts
description: Resolve saved Google Contacts, phone numbers, organizations, and WhatsApp identities through the authenticated Google Workspace CLI.
---

# Google Contacts (CLI)

Use this plugin when a person, phone number, company, or WhatsApp identity is unclear.

Use the installed `gws` CLI for Google People and Contacts operations. This plugin is the product shell and operating manual around `gws people ...`; use WhatsApp for chat/message data and Google Contacts for identity enrichment.

## Start

```bash
command -v gws
gws auth status
gws people people get --params '{"resourceName":"people/me","personFields":"names,emailAddresses"}'
```

## Common Queries

Search saved contacts:

```bash
gws people people searchContacts --params '{"query":"Luis Vargas","readMask":"names,emailAddresses,phoneNumbers,organizations"}'
```

List connections with a bounded page size:

```bash
gws people people connections list --params '{"resourceName":"people/me","personFields":"names,emailAddresses,phoneNumbers,organizations","pageSize":100}'
```

Read a specific contact by resource name:

```bash
gws people people get --params '{"resourceName":"people/CONTACT_ID","personFields":"names,emailAddresses,phoneNumbers,organizations,metadata"}'
```

Use `--page-all --page-limit N` for bounded broad reads.

## Phone Matching

Do not trust one raw phone form. Try normalized variants when matching WhatsApp numbers against contacts:

- `+52XXXXXXXXXX`
- `52XXXXXXXXXX`
- `521XXXXXXXXXX`
- national 10-digit form

Mexican WhatsApp mobile numbers often appear as `521XXXXXXXXXX`, while Google Contacts often stores the same number as `+52XXXXXXXXXX`.

## Writes

Default to read-only contact resolution. Ask before creating, updating, deleting, or photo-editing contacts.

```bash
gws people people createContact --json '{"names":[{"givenName":"Name","familyName":"Last"}],"emailAddresses":[{"value":"person@example.com"}]}' --dry-run
gws people people updateContact --params '{"resourceName":"people/CONTACT_ID","updatePersonFields":"names,emailAddresses,phoneNumbers"}' --json '{}' --dry-run
```

## Raw API Help

Use schema discovery before unfamiliar fields or methods:

```bash
gws schema people.people.searchContacts --resolve-refs
gws schema people.people.connections.list --resolve-refs
gws schema people.people.get --resolve-refs
```

## Output Rules

Show contact-facing fields only:

- Google Contacts name
- saved phone number
- email address when relevant
- organization and title when present
- WhatsApp display name or phone number
- match bucket
- short reason

Do not show raw Google resource IDs, WhatsApp JIDs, or LIDs unless debugging internals.
