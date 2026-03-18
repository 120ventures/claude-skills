# Meta Marketing API Setup — 120 Ventures

## Prerequisites
- Meta Business Manager account with admin access
- At least one Ad Account connected

## Setup Steps

### 1. Create a Meta App
1. Go to [developers.facebook.com](https://developers.facebook.com)
2. My Apps → Create App
3. Use case: **"Measure ad performance data with Marketing API"**
4. Complete the wizard (Business → Requirements → Overview)

### 2. Create a System User
1. Go to [business.facebook.com/settings](https://business.facebook.com/settings)
2. Users → System Users → Add
3. Name: "ClaudeAnalytics" (no spaces)
4. Role: **Admin**

### 3. Generate Access Token
1. Click on the System User → Generate New Token
2. Select your app
3. Permissions: **Full control → Manage app**
4. Token permissions: check **`ads_read`**
5. Generate Token → copy it

### 4. Configure Credentials
Save to `~/.claude/.env`:
```
META_ACCESS_TOKEN="your_token_here"
META_AD_ACCOUNT_ID="act_your_account_id"
```

### 5. Find Ad Account ID
- Business Manager → Accounts → Ad Accounts
- Or in Ads Manager URL: `act_XXXXXXXXX`

## Campaign Naming Convention (120V)
Campaigns are filtered by venture name. Follow this naming:
- Single campaign: `yymm_venture` (e.g., `2603_attuned`)
- Multiple campaigns: `yymm_venture_#nr details` (e.g., `2603_attuned_#2 retargeting`)
- Ad sets: `[Campaign Name]_Ad Set`

## API Endpoints Used
- `GET /v21.0/act_{id}/campaigns?fields=name,status,objective` — list campaigns
- `GET /v21.0/{campaign_id}/insights?level=ad&fields=...` — ad-level performance data

## Token Security
- Token is read-only (`ads_read`) — cannot modify ads or spend budget
- Stored locally in `~/.claude/.env`, never committed to git
- Can be revoked anytime in Business Manager → System Users
- Worst case if leaked: someone sees ad performance data (no write access)

## Troubleshooting
- **"Invalid OAuth access token"** → Token expired or revoked, regenerate in Business Manager
- **Empty campaign list** → Check Ad Account ID format (must include `act_` prefix)
- **Permission denied** → System User needs Admin role + `ads_read` permission
