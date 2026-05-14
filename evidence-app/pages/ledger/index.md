---
title: Exceptions & Ledger Detail
---

# Exceptions &amp; Ledger Detail

Drill-through view of all ledger records with exception filtering.

```sql symbol_options
SELECT '' AS val UNION ALL SELECT DISTINCT SYMBOL AS val FROM short_sales.intraday_ledger WHERE SYMBOL IS NOT NULL ORDER BY 1
```

```sql book_opts
SELECT '' AS val UNION ALL SELECT DISTINCT BOOK::VARCHAR AS val FROM short_sales.intraday_ledger WHERE BOOK IS NOT NULL ORDER BY 1
```

```sql agg_unit_opts
SELECT '' AS val UNION ALL SELECT DISTINCT AGG_UNIT AS val FROM short_sales.intraday_ledger WHERE AGG_UNIT IS NOT NULL ORDER BY 1
```

```sql sourcesystem_opts
SELECT '' AS val UNION ALL SELECT DISTINCT SOURCESYSTEM AS val FROM short_sales.intraday_ledger WHERE SOURCESYSTEM IS NOT NULL ORDER BY 1
```

```sql exception_reason_opts
SELECT '' AS val UNION ALL SELECT DISTINCT EXCEPTION_REASON AS val FROM short_sales.intraday_ledger WHERE EXCEPTION_REASON IS NOT NULL AND EXCEPTION_REASON != '' ORDER BY 1
```

<Grid cols=3>
  <Dropdown data={symbol_options}          name=symbol           value=val title="Symbol"           defaultValue="" />
  <Dropdown data={book_opts}               name=book             value=val title="Book"             defaultValue="" />
  <Dropdown data={agg_unit_opts}           name=agg_unit         value=val title="AGG Unit"         defaultValue="" />
  <Dropdown data={sourcesystem_opts}       name=sourcesystem     value=val title="Source System"    defaultValue="" />
  <Dropdown data={exception_reason_opts}   name=exception_reason value=val title="Exception Reason" defaultValue="" />
</Grid>

```sql ledger_detail
SELECT
    SOURCESYSTEM,
    TYPE,
    TIMESTAMP,
    AGG_UNIT,
    SYMBOL,
    SIDE,
    QUANTITY,
    BOOK::VARCHAR   AS BOOK,
    SOD,
    MQUANT,
    CURR_POSITION,
    ORDER_ID,
    BUSINESS_DATE,
    IS_EXCEPTION,
    EXCEPTION_REASON,
    IS_EXCEPTION_FLAG
FROM short_sales.intraday_ledger
WHERE (SYMBOL         = '${inputs.symbol}'          OR '${inputs.symbol}'         = '')
  AND (BOOK::VARCHAR  = '${inputs.book}'            OR '${inputs.book}'           = '')
  AND (AGG_UNIT       = '${inputs.agg_unit}'        OR '${inputs.agg_unit}'       = '')
  AND (SOURCESYSTEM   = '${inputs.sourcesystem}'    OR '${inputs.sourcesystem}'   = '')
  AND (EXCEPTION_REASON = '${inputs.exception_reason}' OR '${inputs.exception_reason}' = '')
ORDER BY TIMESTAMP DESC
LIMIT 10000
```

<DataTable data={ledger_detail} rows=50 search=true />

---

## Historical Ledger (Oct 26–30, 2025)

```sql historical_ledger
SELECT SOURCESYSTEM, TYPE, TIMESTAMP, AGG_UNIT, SYMBOL, SIDE, QUANTITY, BOOK::VARCHAR AS BOOK, SOD, CURR_POSITION, BUSINESS_DATE, IS_EXCEPTION AS IS_EXCEPTION_FLAG FROM short_sales.ledger_oct26 WHERE SOURCESYSTEM IS NOT NULL
UNION ALL
SELECT SOURCESYSTEM, TYPE, TIMESTAMP, AGG_UNIT, SYMBOL, SIDE, QUANTITY, BOOK::VARCHAR AS BOOK, SOD, CURR_POSITION, BUSINESS_DATE, IS_EXCEPTION AS IS_EXCEPTION_FLAG FROM short_sales.ledger_oct27 WHERE SOURCESYSTEM IS NOT NULL
UNION ALL
SELECT SOURCESYSTEM, TYPE, TIMESTAMP, AGG_UNIT, SYMBOL, SIDE, QUANTITY, BOOK::VARCHAR AS BOOK, SOD, CURR_POSITION, BUSINESS_DATE, IS_EXCEPTION AS IS_EXCEPTION_FLAG FROM short_sales.ledger_oct28 WHERE SOURCESYSTEM IS NOT NULL
UNION ALL
SELECT SOURCESYSTEM, TYPE, TIMESTAMP, AGG_UNIT, SYMBOL, SIDE, QUANTITY, BOOK::VARCHAR AS BOOK, SOD, CURR_POSITION, BUSINESS_DATE, IS_EXCEPTION AS IS_EXCEPTION_FLAG FROM short_sales.ledger_oct29 WHERE SOURCESYSTEM IS NOT NULL
UNION ALL
SELECT SOURCESYSTEM, TYPE, TIMESTAMP, AGG_UNIT, SYMBOL, SIDE, QUANTITY, BOOK::VARCHAR AS BOOK, SOD, CURR_POSITION, BUSINESS_DATE, IS_EXCEPTION AS IS_EXCEPTION_FLAG FROM short_sales.ledger_oct30 WHERE SOURCESYSTEM IS NOT NULL
ORDER BY TIMESTAMP DESC
LIMIT 5000
```

<DataTable data={historical_ledger} rows=50 search=true />
