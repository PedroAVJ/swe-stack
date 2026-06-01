# Google Tasks API Limitations

Use this note when a request sounds simple in the Google Tasks UI but is awkward or unavailable through the public API.

## Confirmed Practical Limits

- Due dates are date-only. The API does not preserve a meaningful due time.
- The product supports repeating tasks, but the public REST schema does not expose a documented recurrence field or recurrence-management method. Treat recurring task creation and editing as unsupported.
- Completed tasks are readable, but a cleared completed task becomes hidden, so history queries often need both `showCompleted=true` and `showHidden=true`.
- Assigned tasks from Google Docs or Chat are special:
  - they can be listed,
  - they cannot be created from the public Tasks API,
  - they have extra move/nesting restrictions.
- No documented webhook or push-watch flow is available in the public API. Design sync as polling, usually with `updatedMin`.

## Structural Limits

- Up to 2,000 task lists per user.
- Up to 20,000 non-hidden tasks per list.
- Up to 100,000 tasks total.
- Up to 2,000 subtasks under one parent task.
- Default courtesy quota is 50,000 queries per day.

## Recommended Workarounds

- For recurring workflows, create a normal task and let a separate automation recreate it after completion.
- For due-time workflows, store the time in `notes` or in a parallel calendar/reminder system.
- For reporting, query tasks in batches and keep a lightweight cache keyed by task ID plus `updated`.
