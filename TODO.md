# To-Do List

## Tasks

### 1. Replace the `exported` field with the last export timestamp in the export table
- **Description**: Instead of using the `exported` field to track the export status, we will store the timestamp of the last export. This allows us to track the exact date and time of the last export, and eliminates the need to update every record during each export.
- **Steps**:
  - Create a `lastExportTimestamp` field in the export table.
  - Update this field during each export instead of the `exported` field.
  - Ensure that all records are exported correctly based on the new approach.

### 2. Remove the Global Secondary Index (GSI) from DynamoDB
- **Description**: Since using the index on the `exported` field becomes inefficient, we need to remove it. Instead, we will query based on the `lastExportTimestamp` field for filtering.
- **Steps**:
  - Delete the GSI associated with the `exported` field.
  - Adjust queries to filter based on the `lastExportTimestamp` field.
  - Ensure that all queries function correctly after the index removal.

### 3. Update IAM roles for access to the table without the index
- **Description**: After removing the index, we need to update the IAM roles that were using it for access to DynamoDB. The roles should be adjusted to work with the new method of access without using the index.
- **Steps**:
  - Review current IAM roles and policies.
  - Update policies to ensure access is based on filtering by the `lastExportTimestamp` field.

## Rationale: Why `update_item` does not work with `batch_writer`

The `batch_writer` only supports `put_item` and `delete_item`, not `update_item`. This is because `batch_writer` is optimized for bulk insertions and deletions for performance, but doesn't handle complex update operations. Hence, using `update_item` separately is necessary but can be slow and costly for large datasets.