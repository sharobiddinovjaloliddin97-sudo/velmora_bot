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