---
title: Short Sales Dashboard
---

# Short Sales Dashboard

Exception monitoring for intraday trading ledger activity.

```sql kpis
SELECT
    COUNT(*)                                            AS records_in_ledger,
    SUM(IS_EXCEPTION_FLAG)                              AS total_exceptions,
    ROUND(SUM(IS_EXCEPTION_FLAG) * 1.0 / COUNT(*), 4) AS exception_pct
FROM short_sales.intraday_ledger
```

<Grid cols=3>
  <BigValue
    data={kpis}
    value="records_in_ledger"
    title="Records in Ledger"
    fmt="num0"
  />
  <BigValue
    data={kpis}
    value="total_exceptions"
    title="Total Exceptions"
    fmt="num0"
  />
  <BigValue
    data={kpis}
    value="exception_pct"
    title="Exception %"
    fmt="pct2"
  />
</Grid>

---

## Navigate

<Grid cols=2>
  <BigLink url="/short-sales/exceptions">Exceptions Dashboard</BigLink>
  <BigLink url="/short-sales/ledger">Exceptions &amp; Ledger Detail</BigLink>
</Grid>
