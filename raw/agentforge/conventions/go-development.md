# Go Development

> Go development principles, patterns, and conventions for AgentForge framework.
> **Related:** [[Infrastructure]], [[Lessons-Learned]]

---

## Philosophy

Embrace Go's design, don't fight it:
- No classes — use interfaces implicitly
- Explicit error handling (no exceptions)
- Intentional verbosity for clarity
- Small, focused functions
- Idiomatic patterns matter for long-term maintainability

## Code Review Checklist (in order)

1. **Idiomatic Go** — follows conventions, not Java/Python style
2. **Goroutine safety** — clear lifecycle, context propagation, shared state protected
3. **Error handling** — explicit, wrapped with `fmt.Errorf("context: %w", err)`
4. **Tests** — unit tests for exported functions, table-driven for variations
5. **Formatting** — `gofmt` + `golangci-lint` (automated in CI)
6. **Edge cases** — off-by-one, nil pointer, empty slice
7. **Performance** — no unnecessary allocations, no goroutine leaks
8. **Maintainability** — clear names, no magic numbers, single-responsibility

## Concurrency Patterns

Every goroutine must have a shutdown path:
```go
// Wrong: no exit
go func() { for { doWork() } }()

// Right: context-cancellable
go func(ctx context.Context) {
    for {
        select {
        case <-ctx.Done(): return
        default: doWork()
        }
    }
}(ctx)
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Inefficient slice building | Preallocate with `make([]T, 0, len(items))` |
| Goroutine without shutdown | Always trace: can this goroutine stop? |
| Errors without context | `fmt.Errorf("loading config: %w", err)` |
| Race conditions | Profile first, design for the race |

## Performance Rules

1. Profile first (`go tool pprof`), never guess
2. Measure with benchmarks (`go test -bench`, `-benchmem`)
3. Preallocate slices/maps when size is known
4. `sync.Pool` for hot-path allocations
5. Struct field alignment — larger fields first to reduce padding

## Testing Conventions

Table-driven tests for multiple cases:
```go
tests := []struct {
    name string
    // inputs / expected
}{{name: "case 1", ...}}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) { /* ... */ })
}
```

## Required Tools

- `gofmt` — automated, non-negotiable
- `golangci-lint` — automated in CI
- `go test -race` — must pass
- `go tool pprof` — for any performance work

## AgentForge Go Framework

- **Language:** Go 1.24.2
- **Files:** 68 `.go` files, 29,672 LOC
- **Binary size:** 14 MB (stripped)
- **Module:** `github.com/agentforge/agentforge`
- **Cross-compile:** darwin/linux/windows, amd64/arm64
- **Core design:** CSP (goroutines + typed message bus), Capability Security (HMAC-SHA256), MeMex Memory (git-tracked markdown), Provider-Agnostic LLM, Skill Marketplace

**See:** [[AgentForge-Framework]] for full architecture reference
