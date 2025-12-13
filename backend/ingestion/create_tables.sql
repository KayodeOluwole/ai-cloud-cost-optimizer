CREATE TABLE IF NOT EXISTS azure_costs (
    resource_id TEXT,
    cost_amount REAL,
    currency TEXT,
    usage_date TEXT,
    meterCategory TEXT
);
