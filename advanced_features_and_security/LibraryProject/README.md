# Permissions and Groups Management

## Overview
This Django application implements a comprehensive permissions and groups system to control access to various parts of the application. The system uses custom permissions and predefined user groups.

## Custom Permissions

### Book Model Permissions
- `can_view_book`: Permission to view book details
- `can_create_book`: Permission to create new books
- `can_edit_book`: Permission to edit existing books
- `can_delete_book`: Permission to delete books

### Author Model Permissions
- `can_view_author`: Permission to view author details
- `can_create_author`: Permission to create new authors
- `can_edit_author`: Permission to edit existing authors
- `can_delete_author`: Permission to delete authors

### User Model Permissions
- `can_view_dashboard`: Permission to view the dashboard
- `can_manage_users`: Permission to manage users

## User Groups

### 1. Viewers Group
- **Permissions**: 
  - `can_view_book`
  - `can_view_author`
- **Description**: Users in this group can only view book and author details but cannot make any changes.

### 2. Editors Group
- **Permissions**:
  - `can_view_book`
  - `can_create_book`
  - `can_edit_book`
  - `can_view_author`
  - `can_create_author`
  - `can_edit_author`
- **Description**: Users in this group can view, create, and edit books and authors, but cannot delete them.

### 3. Admins Group
- **Permissions**: All permissions for books and authors
- **Description**: Users in this group have full access to all operations.

## Implementation Details

### 1. Model Configuration
Custom permissions are defined in the `Meta` class of each model:
```python
class Meta:
    permissions = [
        ("can_view_book", "Can view book details"),
        ("can_create_book", "Can create new book"),
        ("can_edit_book", "Can edit existing book"),
        ("can_delete_book", "Can delete book"),
    ]