# AI Teacher v3 upgrade

## Security
- Signed, expiring HMAC session tokens; no user-id parsing or fallback user.
- Protected lesson/profile/notes/RAG/assessment/tutor endpoints.
- Lesson ownership checks prevent IDOR/BOLA.
- Secure randomized upload filenames, extension allowlist, 10 MB default limit, streamed writes.
- Strict CORS and production-safe DEBUG default.
- Client-supplied API keys removed from lesson creation.

## RAG
- Persistent JSON-backed index survives restart.
- Per-user document isolation.
- BM25-style lexical scoring.
- PDF/TXT/Markdown parser.

## Classroom
- Interactive checkpoints no longer interrupt playback as soon as a scene loads. The question modal opens after the scene media finishes.
- Video remains the primary playback surface.
- Frontend API helper automatically attaches the session token.

## Visual routing
- Search, trees, sorting, graphs, derivatives, integrals, algebra, atoms and periodic-table topics no longer all map to Binary Search or a quadratic graph.

## Important
Set `APP_SECRET_KEY` before deployment. Existing v2 tokens are intentionally invalid under v3; users must sign in again.
