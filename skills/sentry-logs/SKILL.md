---
name: sentry-logs
description: Use when the user asks for Sentry Logs, log observability, Sentry Logs/Explore, runtime log capture, or asks to distinguish Sentry logs from Sentry issues, events, traces, breadcrumbs, or captureMessage.
---

# Sentry Logs

## Rule

When the user says **Sentry Logs**, they mean the Sentry Logs product/surface: log records visible in Logs/Explore or queried from the logs dataset. Do not substitute Sentry Issues, Events, traces, breadcrumbs, or `captureMessage`.

## Do This

- Use the Sentry Logs surface or API logs dataset when checking logs. If using an API, prefer a logs-specific query/dataset such as `dataset=logs` where available.
- For JavaScript SDK logging, initialize Sentry with `enableLogs: true` and emit logs with `Sentry.logger.trace/debug/info/warn/error/fatal(...)`.
- Use structured log attributes for runtime facts: component, feature, device, version, status code, request id, printer status, and other key fields.
- Flush in short-lived/serverless contexts when needed so buffered logs are actually sent.
- Report exactly which Sentry surfaces you checked: Logs/Explore, issues/events, traces, releases, or another named surface.

## Do Not Do This

- Do not call `Sentry.captureMessage` and call that "Sentry Logs"; it creates an event/issue-like item, not a Logs record.
- Do not call `Sentry.captureException` and call that logs; it creates exception events/issues.
- Do not treat breadcrumbs as logs; breadcrumbs are context on events.
- Do not treat console output, Vercel function logs, or a custom public HTTP endpoint as Sentry Logs unless they are explicitly forwarded into Sentry Logs through the logging SDK/API.
- Do not create a public unauthenticated log-ingest endpoint as the default answer to "add Sentry Logs".

## Implementation Shape

For web/server JavaScript:

```js
import * as Sentry from '@sentry/node'

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  enableLogs: true,
})

Sentry.logger.info('Printer service bind result', {
  component: 'native-print-test',
  service_bind_requested: false,
  printer_status: 'unavailable',
})
```

For Android/native apps, prefer the official Sentry Android SDK logging support if available for the installed version. If native SDK logs are not available, say so plainly and use a secure forwarding design only if the user asks for it.

## Closeout Language

If only issues/events were checked, say: "I checked Sentry issues/events, not Sentry Logs."

If logs were checked, say: "I checked Sentry Logs/Explore" and include the query/filter/time window.
