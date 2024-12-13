# Database Migrations

This project uses Alembic for database migrations. Below are the common commands and processes for managing database migrations.

## Common Commands

### Create a New Migration

To generate a new migration based on model changes:

```bash
alembic revision --autogenerate -m "<migration_message>"
```

Replace `<migration_message>` with a descriptive message about your changes, for example:
- `"create_user_table"`
- `"add_email_column"`
- `"update_product_constraints"`

### Apply Migrations

To apply all pending migrations:

```bash
alembic upgrade head
```

## Additional Commands

### Check Current Migration Status

```bash
alembic current
```

### View Migration History

```bash
alembic history
```

### Downgrade Migrations

Rollback the last migration:
```bash
alembic downgrade -1
```

Rollback to a specific migration:
```bash
alembic downgrade <revision_id>
```

### Generate Empty Migration

Create an empty migration file for manual editing:
```bash
alembic revision -m "<migration_message>"
```

## Best Practices

1. **Always review** generated migrations before applying them
2. **Test migrations** in development before applying to production
3. **Backup database** before applying migrations in production
4. **Keep migrations small** and focused on specific changes
5. **Use descriptive messages** when creating migrations
6. **Never modify existing migrations** that have been applied to any environment

## Deployment

When deploying to production:
1. Always backup the database first
2. Run migrations as a separate step before deploying new application code
3. Verify migrations were successful before proceeding with deployment

## Common Issues

### Migration Not Detected

If changes aren't being detected:
1. Ensure models are properly imported in `env.py`
2. Verify changes are actually different from database state
3. Check if tables already exist in database

### Migration Conflicts

If you encounter migration conflicts:
1. Never modify existing migrations
2. Create a new migration to fix issues
3. Consider using branch labels if working with feature branches