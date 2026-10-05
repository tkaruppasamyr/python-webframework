from pathlib import Path

from database import get_db_raw


SRC_DIR = Path(__file__).parent / "src"


def create_migration_table():
    query = """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            app_name TEXT NOT NULL,
            version INTEGER NOT NULL,
            filename TEXT NOT NULL,
            applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

            PRIMARY KEY (app_name, version)
        );
    """

    with get_db_raw() as db:
        db.execute(query)


def get_applied_migrations():
    query = """
        SELECT app_name, version
        FROM schema_migrations
        ORDER BY app_name, version;
    """

    with get_db_raw() as db:
        db.execute(query)

        return {
            (row[0], row[1])
            for row in db.fetchall()
        }


def get_migration_files():
    """
    Find all migrations directories:

        src/*/migrations/

    Example:

        src/ecommerce/migrations/
        src/users/migrations/
    """

    migrations = []

    for migration_dir in SRC_DIR.glob("*/migrations"):

        app_name = migration_dir.parent.name

        print(f"Application   : {app_name}")
        print(f"Migration dir : {migration_dir}")

        migration_files = sorted(
            migration_dir.glob("*.sql")
        )

        for migration_file in migration_files:

            version = int(
                migration_file.name.split("_")[0]
            )

            migrations.append(
                (
                    app_name,
                    version,
                    migration_file
                )
            )

    return migrations


def run_migrations():

    # 1. Create migration tracking table
    create_migration_table()

    # 2. Get already executed migrations
    applied = get_applied_migrations()

    # 3. Find all migration files
    migration_files = get_migration_files()

    # 4. Sort by application + version
    migration_files.sort(
        key=lambda item: (item[0], item[1])
    )

    # 5. Execute migrations
    for app_name, version, migration_file in migration_files:

        migration_key = (
            app_name,
            version
        )

        if migration_key in applied:

            print(
                f"Already applied: "
                f"{app_name} - {migration_file.name}"
            )

            continue

        print(
            f"Applying: "
            f"{app_name} - {migration_file.name}"
        )

        sql = migration_file.read_text(
            encoding="utf-8"
        )

        with get_db_raw() as db:

            # Execute migration
            db.execute(sql)

            # Record migration
            db.execute(
                """
                INSERT INTO schema_migrations (
                    app_name,
                    version,
                    filename
                )
                VALUES (%s, %s, %s)
                """,
                (
                    app_name,
                    version,
                    migration_file.name
                )
            )

        print(
            f"Applied: "
            f"{app_name} - {migration_file.name}"
        )


if __name__ == "__main__":
    run_migrations()