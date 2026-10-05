CREATE TABLE IF NOT EXISTS ecommerce_data (
        id BIGSERIAL PRIMARY KEY,
        order_id INTEGER,
        placed_at TIMESTAMPTZ NOT NULL,
        customer_id TEXT NOT NULL,
        customer_first TEXT NOT NULL,
        customer_last TEXT NOT NULL,
        customer_country TEXT NOT NULL,
        items_count INTEGER NOT NULL,
        total_cents INTEGER NOT NULL,
        currency TEXT NOT NULL,
        status TEXT NOT NULL
    );

CREATE INDEX IF NOT EXISTS idx_ecommerce_id ON ecommerce_data(id);