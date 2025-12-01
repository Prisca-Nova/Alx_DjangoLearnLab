
## Features Implemented

### 1. Custom User Model
- Extended AbstractUser
- Added `date_of_birth` and `profile_photo` fields
- Email-based authentication (no username)
- Custom user manager

### 2. Permissions System
Custom permissions defined for Book and Author models:
- `can_view_book` - Permission to view book details
- `can_create_book` - Permission to create new books
- `can_edit_book` - Permission to edit existing books
- `can_delete_book` - Permission to delete books
- `can_view_author` - Permission to view author details
- `can_create_author` - Permission to create new authors
- `can_edit_author` - Permission to edit existing authors
- `can_delete_author` - Permission to delete authors

### 3. User Groups
Three predefined groups with specific permissions:

#### Viewers Group
- Permissions: `can_view_book`, `can_view_author`
- Can only view content, no modifications

#### Editors Group
- Permissions: `can_view_book`, `can_create_book`, `can_edit_book`, 
               `can_view_author`, `can_create_author`, `can_edit_author`
- Can view, create, and edit content

#### Admins Group
- All permissions for books and authors
- Full access to all operations

### 4. Permission Enforcement
Permissions are enforced using Django's decorators:

```python
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_edit(request, pk):
    # View logic here