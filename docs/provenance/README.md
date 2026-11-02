# Provenance

Independent proof of when the site's content and launch existed.

| File | What it is |
|---|---|
| `2026-11-02-manifest.txt` | Git commit ids, trees and archive hashes of the first commit (24 Oct 2026), the public launch (29 Oct 2026, 19:17 UTC) and the state on 2 Nov 2026 |
| `2026-11-02-manifest.tsq` | The timestamp request (SHA-256 of the manifest) |
| `2026-11-02-manifest.freetsa.tsr` | RFC 3161 timestamp token from FreeTSA (freetsa.org), 2 Nov 2026 21:31:11 UTC |
| `2026-11-02-manifest.digicert.tsr` | RFC 3161 timestamp token from DigiCert (timestamp.digicert.com), 2 Nov 2026 21:31:18 UTC |
| `freetsa-cacert.pem`, `freetsa-tsa.crt` | FreeTSA certificates needed to verify its token |

A token proves the manifest existed **no later than** the time it states. The launch date itself is
also recorded by third parties: GitHub (push and pull request times), the Internet Archive
(web.archive.org), Google Search Console and Bing Webmaster Tools (site verified 29 Oct 2026).

## Verify

```sh
# 1. the manifest matches the request
openssl ts -query -data 2026-11-02-manifest.txt -sha256 -cert -no_nonce | cmp - 2026-11-02-manifest.tsq || true
openssl ts -reply -in 2026-11-02-manifest.freetsa.tsr -text   # shows the time and the hash

# 2. the tokens are valid
openssl ts -verify -in 2026-11-02-manifest.freetsa.tsr -data 2026-11-02-manifest.txt \
  -CAfile freetsa-cacert.pem -untrusted freetsa-tsa.crt
openssl ts -verify -in 2026-11-02-manifest.digicert.tsr -data 2026-11-02-manifest.txt \
  -CAfile /etc/ssl/certs/ca-certificates.crt

# 3. the repository matches the manifest (run in a clone)
git rev-parse e2a690353d4b80621d726031cbc0df154c4adcf2^{tree}
git archive --format=tar e2a690353d4b80621d726031cbc0df154c4adcf2 | sha256sum
```

Do not edit the manifest: any change, even whitespace, breaks the verification.
