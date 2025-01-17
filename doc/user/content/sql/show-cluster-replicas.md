---
title: "SHOW CLUSTER REPLICAS"
description: "`SHOW CLUSTER REPLICAS` lists the replicas for each cluster configured in Materialize."
menu:
  main:
    parent: 'commands'

---

{{< show-command-note >}}

`SHOW CLUSTER REPLICAS` lists the [replicas](/overview/key-concepts/#cluster-replicas) for each cluster configured in Materialize. A cluster named `default` with a single replica named `r1` will exist in every environment; this cluster can be dropped at any time.

## Syntax

{{< diagram "show-cluster-replicas.svg" >}}

## Examples

```sql
SHOW CLUSTER REPLICAS;
```

```nofmt
    cluster    | replica |  size  |
---------------+---------|--------|
 auction_house | bigger  | xlarge |
 default       | r1      | xsmall |
```

```sql
SHOW CLUSTER REPLICAS WHERE cluster='default';
```

```nofmt
    cluster    | replica |  size  |
---------------+---------|--------|
 default       | r1      | xsmall |
```


## Related pages

- [`CREATE CLUSTER REPLICA`](../create-cluster-replica)
- [`DROP CLUSTER REPLICA`](../drop-cluster-replica)
