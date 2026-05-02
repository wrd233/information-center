# WeChat RSS

This subproject runs `we-mp-rss` for WeChat public account RSS feeds.

## Start

```bash
docker compose up -d
```

The service listens on:

```text
http://127.0.0.1:8003
```

## Data

Runtime data is stored in the local `./data` directory and mounted into the
container at `/app/data`.

Important files include:

- `data/db.db`
- `data/wx.lic`

The `data/` directory is ignored by Git because it contains runtime state and
license files.

## Stop

```bash
docker compose down
```

## Update Image

```bash
docker compose pull
docker compose up -d
```

## API Access

The API base URL is:

```text
http://127.0.0.1:8003/api/v1/wx
```

Login with the web account to get a JWT token:

```bash
curl -X POST http://127.0.0.1:8003/api/v1/wx/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "username=admin&password=admin%40123"
```

For scripts, use Access Key authentication:

```bash
curl -H "Authorization: AK-SK ${WE_RSS_ACCESS_KEY}:${WE_RSS_SECRET_KEY}" \
  http://127.0.0.1:8003/api/v1/wx/articles
```

Keep `WE_RSS_ACCESS_KEY` and `WE_RSS_SECRET_KEY` in a local `.env` file or in
your shell environment. The Secret Key is only shown once when the Access Key is
created, so create a new key if it has been lost.

Copy `.env.example` to `.env` and fill in the local credentials:

```bash
cp .env.example .env
```

List subscribed WeChat public accounts:

```bash
source .env
curl -H "Authorization: AK-SK ${WE_RSS_ACCESS_KEY}:${WE_RSS_SECRET_KEY}" \
  "${WE_RSS_BASE_URL}/mps?limit=10&offset=0"
```

Search and add public accounts through `/mps/search/{keyword}` and `POST /mps`.
If the WeChat session has expired, generate a fresh login QR code through:

```bash
curl -H "Authorization: Bearer ${WE_RSS_JWT_TOKEN}" \
  "${WE_RSS_BASE_URL}/auth/qr/code"
```

## Rate-Limit Hygiene

Adding or updating WeChat public accounts calls WeChat-side endpoints. Keep these
operations conservative:

- Check the local `/mps` list first and skip existing accounts.
- Add accounts only when the search result has an exact nickname match.
- Use small batches with randomized pauses between search and add requests.
- Stop the batch when login expires, search fails, or responses look unusual.
- Avoid repeated manual refreshes for the same account; let queued sync tasks run.
- Keep RSS reads local when possible instead of forcing fresh updates.
