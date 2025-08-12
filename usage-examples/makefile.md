# Makefile

```
.NOTPARALLEL: api-spec
app-test:
	@set -e
	@pnpm run test || (speaky "APP tests failed!"; exit 1)
	@speaky "All tests passed."
```

