This tool runs on both machines and reads/updates and delete records from the places.sqlite moz_bookmarks table.

Run on two machines before starting Firefox

# Run

# run on PC1 with example config
Where 192.168.1.200 is PC2's local ip

```
host=127.0.0.1
port=5000
bookmarks_file=~/.mozilla/firefox/rq1pmem1.default-release/places.sqlite
compare_host=192.168.1.200
compare_port=5000
```

# run on PC2 with example config
Where 192.168.1.220 is PC1's local ip
```
host=127.0.0.1
port=5000
bookmarks_file=~/.mozilla/firefox/rq1pmem1.default-release/places.sqlite
compare_host=192.168.1.220
compare_port=5000
```

It runs periodically until stopped