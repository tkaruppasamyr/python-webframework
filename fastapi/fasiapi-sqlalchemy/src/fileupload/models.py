from database import get_db_raw
import io
import csv


class EcommerceRepository:

    TABLE_NAME = "ecommerce_data"

    def __init__(self):
        self.db_context = get_db_raw()

    def bulk_insert(self, rows):

        print("Bulk insert started...", len(rows))

        if not rows:
            return 0

        buffer = io.StringIO()

        writer = csv.writer(buffer)
        writer.writerows(rows)

        buffer.seek(0)

        with get_db_raw() as cursor:
            cursor.copy_expert(
                """
                COPY ecommerce_data
                (
                    order_id,
                    placed_at,
                    customer_id,
                    customer_first,
                    customer_last,
                    customer_country,
                    items_count,
                    total_cents,
                    currency,
                    status
                )
                FROM STDIN
                WITH (FORMAT CSV, HEADER)
                """,
                buffer
            )
            cursor.execute("commit")
                

            