# Adapter Interface Specification

This document defines required behavior for adapters implementing `adapters.interface.ConnectorAdapter`.

## Required Methods

### `fetch_full(tenant_id, cursor=None) -> list[dict]`
Purpose:
- Return source objects for full sync bootstrap or reconciliation.

Requirements:
- Must be idempotent for repeated calls over the same source state.
- Must include enough metadata for downstream normalization and ACL mapping.
- Should support pagination internally if source requires it.

### `fetch_incremental(tenant_id, cursor) -> list[dict]`
Purpose:
- Return changed source objects since the given cursor/checkpoint.

Requirements:
- Cursor semantics must match source system change feed/token model.
- Must include updates and permission changes.
- Must surface deletions/removals via adapter tombstone path.

### `normalize(raw_object, sync_run_id) -> dict`
Purpose:
- Transform source-native object into normalized document contract.

Requirements:
- Output must satisfy base normalized document schema from `conn-contracts`.
- Must include stable `doc_id`, `source`, `object_type`, ACL principals, and `updated_at`.
- Must avoid lossy ACL transformations at this stage.

### `emit_tombstone(object_id, sync_run_id) -> dict`
Purpose:
- Build a normalized tombstone payload for deleted/inaccessible objects.

Requirements:
- Must set `is_deleted=true`.
- Must preserve stable identity fields (`doc_id`, `source`, `sync_run_id`).

### `checkpoint_commit(tenant_id, cursor) -> dict`
Purpose:
- Build checkpoint payload to persist successful sync progress.

Requirements:
- Cursor must represent a safe resume point.
- Should only be committed after successful processing of associated batch/window.

## Error Handling
- Raise explicit, typed exceptions for auth failures, rate limits, and data-contract failures.
- Do not swallow source API errors silently.
- Include source object IDs in error context where possible.

## Security Requirements
- Never log raw tokens or secrets.
- Treat ACL principals as sensitive metadata in logs.
- Enforce least-privilege source scopes.

## Test Expectations (Per Adapter)
- Valid normalize output passes schema checks.
- Invalid source object produces deterministic validation error.
- Tombstones generated for deletion/removal scenarios.
- Incremental cursor behavior covered by fixture tests.
