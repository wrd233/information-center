# Run Lifecycle

Run states: `running`, `success`, `failed`, `cancelled`.

Run event flow: `run_created`, `run_started`, source events, item events, semantic events, `run_completed` or failure/cancel event.

Dry-run writes run rows and events but no items. Real-write writes items, `item_run_links`, source results, audit rows, and lightweight information objects.
