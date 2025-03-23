## Intro

Jemalloc HPA is hugepages aware implementation of pages allocator. HPA
leverages hugepages to reduce cost of TLB misses and thereby improve
application performance.

## Glossary

### Pageslab

Pageslab is hugepage aligned and sized memory range. You can think of it as a
set of pages packed together into a hugepage. Pageslab is not necessary backed
up by a hugepage.


### Active Page

Active page is a memory page that potentially stores application data.

### Dirty Page

Dirty page is a memory page that might have had application data on it in the
past, but has no application data now. It can be reused (became active again)
or returned back to the OS anytime.

### Purge

Purge is a process of returning dirty pages back to the OS.

### Hugification

Hugification is a request to the OS back pageslab by a hugepage.

## Constants

### `PAGE`

`PAGE` is the size of a jemalloc page. By default it is `4096` bytes on x86\_64.

### `HUGEPAGE`

`HUGEPAGE` is the size of the OS hugepage. By default it is `2097152` bytes (2
MiB) on x86\_64.

### `HUGEPAGES_PAGES`

Number of pages in a single hugepage: `HUGEPAGE / PAGE`. By default it is `512`
on x86\_64.

## Documentation

HPA is under active development and options are not described in documentation
yet. Below is a brief description of currently available options.

### hpa

HPA enabled/disabled.

Master switch to enable HPA. This option should be enabled to make other
options to work.

Boolean. Default value: `false`.

### hpa_slab_max_alloc

Maximum allocation size in bytes allowed to be served from HPA page allocator.

Allocations of greater size will be served from a more general (for now)
classic page allocator (PAC), which can handle allocation requests of any size.
Slab allocations will always be served out of HPA, even when the
`hpa_slab_max_alloc` option is set to a small value like `PAGE` due to
implementation quirks. This implementation quirks can be leveraged to serve out
of HPA only small allocations (small in jemalloc definition is allocation less
than 16 KiB).

Unsigned integer. Default value: `65536` bytes. Minimum value: `PAGE` bytes.
Maximum value: `HUGEPAGE` bytes.

### hpa_hugification_threshold

Minimum number of active bytes in a pageslab necessary for pageslab to be
placed into hugification queue.

Pageslab always produced in a non-huge state. Over time, when number of active
bytes became greater or equal than `hpa_hugification_threshold`, jemalloc puts
pageslab into hugification queue.

Unsigned integer. Default value: `0.95 * HUGEPAGE` bytes. Minimum value: `PAGE`
bytes. Maximum value: `HUGEPAGE` bytes.

### hpa_hugification_threshold_ratio

Minimum percent of active bytes in a pageslab necessary for pageslab to be 
placed into hugification queue.

This option has the same semantic as `hpa_hugification_threshold`, but in
percent notation.

Fixed-point fractional. Default value: `0.95`. Minimum value: `0`. Maximum
value: `1.0`.

### hpa_hugify_delay_ms

Time in milliseconds required for pageslab to spent in hugification queue,
before jemalloc requests OS to back pageslab by a hugepage.

Hugification queue is ordered by timestamp, when pageslab was placed into the
queue, with head of the queue being pageslab placed into the queue earliest and
tail of the queue being pageslab there latest. When pageslab stops meeting
hugification criteria: number of active bytes is less than
`hpa_hugification_threshold` it is **not** removed from hugification queue.
Only purge can remove pageslab from hugification queue.

Unsigned integer. Default value: `10000` milliseconds.

### hpa_hugify_sync

Switch to use synchronous hugification requests.

Use `madvise(..., MADV_COLLAPSE)` to request OS back up pageslab by a hugepage
alongside `madvise(..., MADV_HUGEPAGE)`. Increments
`stats.arenas.<i>.hpa_shard.nhugify_failures` counter on failure.

Usual asynchronous hugification introduces delay of unknown length, between
request to OS has been made to hugify a pageslab and OS actually backs up
pageslab by a hugepage. This option allows to eliminate this delay. Requires
Linux 6.1 or higher. 

Boolean. Default value: `false`.

### hpa_min_purge_interval_ms

Minimum time between two consecutive purge phases in milliseconds.

Each `hpa_min_purge_interval_ms` jemalloc will check if purging criteria are
met and if they are, it will purge as much pageslabs as needed until purging
criteria are no longer met. Minimal unit of purging is pageslab, meaning all
dirty pages will be returned back to the OS from chosen pageslab, even if less
pages required to be purged to reach purging target. If there are few
consecutive dirty pages, one syscall will be issued to purge them together in
one go.

Unsigned integer. Default value: 5000 milliseconds.

### hpa_peak_demand_window_ms

Length of peak demand sliding window in milliseconds.

Time component of purging criteria. Jemalloc will track the maximum number of
active pages used within `hpa_peak_demand_window_ms` milliseconds sliding
window. Jemalloc will purge dirty pages above that peak usage.

It is easier to explain in an example. Suppose `ncurrent` is the number of
active pages currently in use and `npeak` is the peak (maximum) number of
active pages within the last 10 seconds. Then jemalloc is allowed to keep
`npeak - ncurrent` dirty pages and will purge the rest of them if there are
any.

Option `hpa_peak_demand_window_ms` works in combination with `hpa_dirty_mult`.

Unsigned integer. Default value: 0 milliseconds (disabled by default).

### hpa_dirty_mult

Maximum of dirty to active pages ratio jemalloc is allowed to keep.

Ratio based component of purging criteria.

Jemalloc is trying to estimate the maximum amount of active memory application
might likely need in the near future. It does so by projecting future active
memory demand (based on peak active memory usage observed in the past within a
sliding window) and adds slack on top of it (an overhead it is reasonable to
have in exchange on higher hugepages coverage). When peak demand tracking is
off, projection of future active memory is current active memory usage.

Estimation is essentially the same as `npeak * (1 + hpa_dirty_mult)`. In case,
when `hpa_peak_demand_window_ms` is set to `0`, then `npeak` equals to
`ncurrent` and expression became `ncurrent * hpa_dirty_mult`. When
`hpa_dirty_mult` is `0`, then the expression becomes just `npeak`.

Option `hpa_dirty_mult` works in combination with `hpa_peak_demand_window_ms`.

Fixed-point fractional or `-1`. Default value is `0.25` (not a great default).
When set to `-1` disables purging completely.

### hpa_sec_nshards

Number of small extent cache (SEC) shards.

SEC is a cache layer above the HPA page allocator. Requests are distributed
across small extent cache shards `[0, nshards - 1)`. If a request can not be
served out of SEC, it will be forwarded to the HPA page allocator.

I can not say I saw cases when the SEC helped much. Probably, more work is
required to make SEC useful.

Unsigned integer. Default value: 4 shards. When set to `0` disables small
extent cache (SEC).

### hpa_sec_max_alloc

Maximum size of allocation in bytes, that can be served out of SEC.

Jemalloc will refuse to cache any objects if their size is greater than
`hpa_sec_max_alloc` and forward such objects to the HPA page allocator.

Unsigned integer. Default value: 32768 bytes. Minimum value: `PAGE` bytes.
Maximum value: `32768` bytes.

### hpa_sec_max_bytes

Maximum number of bytes small extent cache shard allowed to cache.

When shard cached bytes size exceeds `hpa_sec_max_bytes`, jemalloc will flush
bins until the number of cached bytes falls below `hpa_sec_bytes_after_flush`.

Unsigned integer. Default value: `262144` bytes. Minimum value: `PAGE`.

### hpa_sec_bytes_after_flush

Maximum number of bytes SEC is allowed to have after flush caused by exceeding
`hpa_sec_max_bytes`.

This option should be less than `hpa_sec_max_bytes` for SEC to be useful.

Unsigned integer. Default value: `131072` bytes. Minimum value: `PAGE`.

### hpa_sec_batch_fill_extra

Number of extra objects to fill on SEC miss.

When allocation request can not be satisfied out of SEC, because there are no
available ones cached, jemalloc brings `hpa_sec_batch_fill_extra` additional
objects to SEC out of HPA page allocator.

Unsigned integer. Default value: `0`. Maximum value: `HUGEPAGES_PAGES`.

### experimental_hpa_max_purge_nhp

Maximum number of pageslabs to purge on each purging phase.

Experimental option that likely will be removed soon. Limits number of pageslab
to purge on each purging phase.

Signed integer. Default value: `-1` (disabled by default).

## Acknowledgements

Thanks to Kevin Svetlitski, whose note introduced me to the HPA world.
