-- Historical ledger — October 26, 2025
-- UNION with a stub row ensures a non-empty Parquet cache when no data is present;
-- the stub row is excluded in page queries via WHERE SOURCESYSTEM IS NOT NULL.
SELECT
    SOURCESYSTEM,
    TYPE,
    TIMESTAMP::VARCHAR         AS TIMESTAMP,
    AGGREGATION_UNIT           AS AGG_UNIT,
    SYMBOL,
    SIDE,
    QUANTITY::BIGINT           AS QUANTITY,
    BOOK::VARCHAR              AS BOOK,
    SOD::BIGINT                AS SOD,
    CURR_POSITION::BIGINT      AS CURR_POSITION,
    UNIQUEID,
    BUSINESS_DATE,
    PREV_TIMESTAMP::VARCHAR    AS PREV_TIMESTAMP,
    NEXT_TIMESTAMP::VARCHAR    AS NEXT_TIMESTAMP,
    IS_EXCEPTION::BIGINT       AS IS_EXCEPTION
FROM read_parquet('${data_dir}ledger_2025_10_26.parquet')

UNION ALL

SELECT NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM read_parquet('${data_dir}ledger_2025_10_26.parquet') LIMIT 1)
