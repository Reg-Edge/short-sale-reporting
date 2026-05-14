---
title: Exceptions Dashboard
---

# Exceptions Dashboard

```sql sourcesystem_options
SELECT '' AS val UNION ALL SELECT DISTINCT SOURCESYSTEM AS val FROM short_sales.intraday_ledger WHERE SOURCESYSTEM IS NOT NULL ORDER BY 1
```

```sql exception_reason_options
SELECT '' AS val UNION ALL SELECT DISTINCT EXCEPTION_REASON AS val FROM short_sales.intraday_ledger WHERE EXCEPTION_REASON IS NOT NULL AND EXCEPTION_REASON != '' ORDER BY 1
```

```sql book_options
SELECT '' AS val UNION ALL SELECT DISTINCT BOOK::VARCHAR AS val FROM short_sales.intraday_ledger WHERE BOOK IS NOT NULL ORDER BY 1
```

```sql agg_unit_options
SELECT '' AS val UNION ALL SELECT DISTINCT AGG_UNIT AS val FROM short_sales.intraday_ledger WHERE AGG_UNIT IS NOT NULL ORDER BY 1
```

<Grid cols=4>
  <Dropdown
    data={sourcesystem_options}
    name=sourcesystem
    value=val
    title="Source System"
    defaultValue=""
  />
  <Dropdown
    data={exception_reason_options}
    name=exception_reason
    value=val
    title="Exception Reason"
    defaultValue=""
  />
  <Dropdown
    data={book_options}
    name=book
    value=val
    title="Book"
    defaultValue=""
  />
  <Dropdown
    data={agg_unit_options}
    name=agg_unit
    value=val
    title="AGG Unit"
    defaultValue=""
  />
</Grid>

```sql exceptions_by_symbol
SELECT
    SYMBOL,
    SUM(IS_EXCEPTION_FLAG) AS total_exceptions
FROM short_sales.intraday_ledger
WHERE IS_EXCEPTION_FLAG = 1
  AND (SOURCESYSTEM  = '${inputs.sourcesystem}'  OR '${inputs.sourcesystem}'  = '')
  AND (EXCEPTION_REASON = '${inputs.exception_reason}' OR '${inputs.exception_reason}' = '')
  AND (BOOK::VARCHAR = '${inputs.book}'  OR '${inputs.book}'  = '')
  AND (AGG_UNIT      = '${inputs.agg_unit}'      OR '${inputs.agg_unit}'      = '')
GROUP BY SYMBOL
ORDER BY total_exceptions DESC
```

```sql exceptions_by_agg_unit
SELECT
    AGG_UNIT,
    SUM(IS_EXCEPTION_FLAG) AS total_exceptions
FROM short_sales.intraday_ledger
WHERE IS_EXCEPTION_FLAG = 1
  AND (SOURCESYSTEM  = '${inputs.sourcesystem}'  OR '${inputs.sourcesystem}'  = '')
  AND (EXCEPTION_REASON = '${inputs.exception_reason}' OR '${inputs.exception_reason}' = '')
  AND (BOOK::VARCHAR = '${inputs.book}'  OR '${inputs.book}'  = '')
  AND (AGG_UNIT      = '${inputs.agg_unit}'      OR '${inputs.agg_unit}'      = '')
GROUP BY AGG_UNIT
ORDER BY total_exceptions DESC
```

## Exceptions by Symbol

<DataTable data={exceptions_by_symbol} rows=20>
  <Column id=SYMBOL />
  <Column id=total_exceptions title="Total Exceptions" contentType=colorscale />
</DataTable>

## Exceptions by Aggregation Unit

<BarChart
  data={exceptions_by_agg_unit}
  x=AGG_UNIT
  y=total_exceptions
  title="Total Exceptions by AGG Unit"
  xAxisTitle="Aggregation Unit"
  yAxisTitle="Exception Count"
/>
