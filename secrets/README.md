# Secrets

Everything in this folder except this README is gitignored (`secrets/*.json`).
**Never commit these files.** They grant write access to your YouTube channel.

## `client_secrets.json`

Your Google Cloud OAuth 2.0 **Desktop app** client. Download it from the Google Cloud Console
and save it here unchanged. See the README's "YouTube setup" walkthrough for the full
click-path. The file looks like this:

```json
{
  "installed": {
    "client_id": "....apps.googleusercontent.com",
    "project_id": "your-project",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_secret": "....",
    "redirect_uris": ["http://localhost"]
  }
}
```

If the top-level key is `"web"` instead of `"installed"`, you created the wrong client type.
Delete it and create a **Desktop app** client.

## `token.json`

Written automatically by `python main.py auth` after you approve the consent screen. It holds
the access and refresh tokens. The pipeline creates it with `0o600` permissions on POSIX
systems and refreshes it silently when it expires.

Delete this file and re-run `python main.py auth` if you see `RefreshError` or
`invalid_grant`.

## The 7-day test-mode expiry

While your Google Cloud OAuth consent screen is in **Testing** status, refresh tokens expire
after **7 days**. You will need to re-run `python main.py auth` weekly until you either
publish the app or complete verification. Videos uploaded by an unverified app are also locked
to `private` regardless of the `privacy_status` you request.

## If a secret leaks

1. Google Cloud Console → APIs & Services → Credentials → delete the OAuth client.
2. Create a new Desktop client and replace `client_secrets.json`.
3. Delete `token.json` and re-run `python main.py auth`.
4. Revoke the old grant at <https://myaccount.google.com/permissions>.
