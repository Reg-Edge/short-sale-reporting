-- Intraday ledger with derived exception flag
SELECT
    SOURCESYSTEM,
    TYPE,
    TIMESTAMP::VARCHAR AS TIMESTAMP,
    AGGREGATION_UNIT                                              AS AGG_UNIT,
    SYMBOL,
    SIDE,
    QUANTITY::BIGINT                                              AS QUANTITY,
    BOOK::VARCHAR                                                 AS BOOK,
    SOD::BIGINT                                                   AS SOD,
    MQUANT::BIGINT                                                AS MQUANT,
    CURR_POSITION::BIGINT                                         AS CURR_POSITION,
    ORDER_ID::VARCHAR                                             AS ORDER_ID,
    BUSINESS_DATE::VARCHAR                                        AS BUSINESS_DATE,
    IS_EXCEPTION::VARCHAR                                         AS IS_EXCEPTION,
    COALESCE(EXCEPTION_REASON::VARCHAR, '')                       AS EXCEPTION_REASON,
    IS_EXCEPTION_FLAG::BIGINT                                     AS IS_EXCEPTION_FLAG
FROM read_parquet('${data_dir}intraday_ledger.parquet')
