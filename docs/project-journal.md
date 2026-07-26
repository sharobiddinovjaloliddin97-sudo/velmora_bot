## 2026-07-25

### Completed
- Created a custom `User` model by extending Django's `AbstractUser`.
- Made the `email` field unique.
- Configured authentication to use `email` instead of `username` (`USERNAME_FIELD = "email"`).
- Set `REQUIRED_FIELDS = ["username"]` for superuser creation.
- Configured `AUTH_USER_MODEL = "users.User"` in Django settings.
- Generated and applied the initial migration for the custom user model.
- Created a Django superuser.
- Registered the custom `User` model in Django Admin using `UserAdmin`.
- Verified the custom user model is accessible from the Django Admin panel.



### Next Steps
- Implement a custom `UserManager`.
- Connect the manager to the `User` model.
- Add additional user fields (role, phone number, avatar, etc.) if required by the project.
- Begin implementing authentication APIs (registration, login, JWT).


### Completed
- Implemented a custom `UserManager`.
- Added `create_user()` to validate email, hash passwords, and save users safely.
- Added `create_superuser()` to create administrator accounts with the required permissions.
- Connected the custom manager to the `User` model using `objects = UserManager()`.
- Verified superuser creation works through the custom manager.


### Completed
- Created `RegisterSerializer` for user registration.
- Configured the password as a write-only field.
- Overrode the `create()` method to use the custom `UserManager`.
- Ensured passwords are hashed during registration by calling `User.objects.create_user()`.

### Completed
- Created `RegisterView` using DRF's `CreateAPIView`.
- Connected the registration endpoint to `RegisterSerializer`.
- Returned user information using `UserSerializer` after successful registration.
- Verified the complete registration flow from HTTP request to database persistence.

### Completed
- Created `apps/users/urls.py` for user-related endpoints.
- Registered the `RegisterView` at `/register/`.
- Included the users URL configuration in the project's root URL configuration.
- Verified the complete request routing from the project URL configuration to the registration view.

### Fixed
- Resolved a `ProgrammingError` caused by the `role` field existing in the Django model but not in the PostgreSQL database.
- Generated and applied the missing migration for the `role` field.
- Verified successful user registration through the API after synchronizing the database schema.

### Decision
- Selected JWT as the authentication mechanism for the REST API.
- Authentication will use access and refresh tokens via SimpleJWT.
- The API will remain stateless and suitable for React and Telegram clients.


### Completed
- Created `LoginSerializer` using DRF's `Serializer`.
- Implemented credential validation using Django's `authenticate()` function.
- Configured JWT generation using `RefreshToken.for_user()`.
- Returned the authenticated user along with access and refresh tokens.

### Completed
- Created `LoginView` using DRF's `GenericAPIView`.
- Connected `LoginView` to `LoginSerializer`.
- Returned authenticated user information together with JWT access and refresh tokens.
- Added the `/api/users/login/` endpoint.

### Completed
- Introduced a `UserService` to centralize user-related business logic.
- Moved registration logic from `RegisterSerializer` to the service layer.
- Wrapped user creation in a database transaction using `transaction.atomic`.
- Reduced the serializer's responsibility to validation and data conversion.

### Completed
- Moved login business logic into `UserService`.
- Refactored `LoginSerializer` to delegate authentication to the service layer.
- Centralized JWT generation inside the service layer.


### Completed
- Implemented the `/api/users/me/` endpoint.
- Protected the endpoint using `IsAuthenticated`.
- Used `JWTAuthentication` to resolve the current user from the access token.
- Returned the authenticated user's profile through `UserSerializer`.

### Completed
- Created `ChangePasswordSerializer`.
- Added `current_password` and `new_password` as write-only fields.
- Prepared the serializer for delegation to the service layer.

### Completed
- Implemented `UserService.change_password()`.
- Verified the current password using `check_password()`.
- Updated the password securely using `set_password()`.
- Saved only the `password` field using `update_fields`.

### Completed
- Connected `ChangePasswordSerializer` to `UserService`.
- Retrieved the authenticated user through `self.context["request"]`.
- Delegated password change logic to the service layer.

### Completed
- Enabled SimpleJWT token blacklist support.
- Added the `token_blacklist` application.
- Applied database migrations for outstanding and blacklisted refresh tokens.
- Configured refresh token blacklisting for logout support.


### Completed
- Created `LogoutSerializer`.
- Implemented `UserService.logout()`.
- Blacklisted refresh tokens using SimpleJWT.
- Returned a validation error for invalid or expired refresh tokens.


## Phase 2 - Catalog

### Completed

- Created `Category` model.
- Created `Product` model.
- Created `ProductImage` model.
- Registered all catalog models in Django Admin.
- Configured media settings for product image uploads.

### Notes

- Categories can be activated/deactivated using `is_active`.
- Products belong to categories using `ForeignKey`.
- A product can have multiple images through the `ProductImage` model.
- Product images are stored under `media/products/`.


## Catalog API

### Completed

- Created CategorySerializer.
- Created ProductSerializer.
- Created ProductImageSerializer.

### Completed

- Created CatalogService.
- Added methods for listing categories, products, and product details.


### Completed

- Added CategoryListView.
- Added ProductListView.
- Added ProductDetailView.

### Completed

- Configured Catalog API.
- Implemented Category, Product, and Product Detail endpoints.
- Verified DRF configuration.

### Completed

- Added search to Product API.
- Added filtering by category and material.
- Added ordering by price, name, and created date.

### Completed

- Added custom permission `IsAdminOrEmployee`.
- Restricted catalog management to admins and employees.

## Catalog Module

### Completed

- Created Category, Product, and ProductImage models.
- Configured media file uploads.
- Registered catalog models in Django Admin.
- Implemented nested serializers for product images.
- Added CatalogService for product retrieval.
- Implemented product and category API endpoints.
- Added filtering, searching, ordering, and pagination.
- Implemented product CRUD:
  - List Products
  - Product Detail
  - Create Product
  - Update Product
  - Delete Product
- Added custom permission (`IsAdminOrEmployee`) for catalog management.
- Restricted create, update, and delete operations to authenticated admins and employees.

### Status

✅ Catalog module completed.