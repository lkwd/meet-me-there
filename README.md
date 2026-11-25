# Meet Me There website

The website for Meet Me There, a yacht-life roleplay experience on Roblox by
Lockwood Publishing. It's a static site: plain HTML and CSS with a little
JavaScript. There's no build step and no framework.

Temporary home: **https://gate.apps.avkn.co/meet-me-there/** (the Okta gate,
served from a copy in lkwd/avakin-prototypes). It stays there until the final
domain and host are ready. GitHub Pages is off for this repo (2026-11-23).

To publish, copy `index.html`, `404.html`, `faq/` and `assets/` into
`avakin-prototypes/meet-me-there/`, update `repo_sha` and `published` in its
`prototype.json` (keep its `feedback.html`), and push `main`. The gate syncs
within 5 minutes; `https://gate.apps.avkn.co/healthz` shows the commit.

```
index.html             home page
faq/index.html         Help & FAQs (the single source for all FAQ answers)
404.html               not-found page (self-contained, works at any depth)
assets/js/config.js    every link that isn't final yet, plus the launch time
assets/js/main.js      fills links from config.js, launch line, trailer cover, FAQ deep links
assets/css/styles.css  all styles
assets/img/            images (WebP, plus hero.jpg for social sharing)
assets/video/          trailer (WebM + MP4) and poster
tools/check.py         link, anchor and placeholder check (runs in CI)
```

## Preview locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000/.

## Changing links

All the links that aren't final yet (Play, support email, Terms, Privacy,
Roblox group) live in `assets/js/config.js`, along with the Discord invite
(set 2026-11-23). Each one stays **hidden**
on the site until you set it, so a visitor never sees a broken or placeholder
link. Where a gap would look odd, a fallback shows instead:

- With no Play link, the hero shows "Launching 9 November on Roblox".
- With no support email, "Still need help?" points to Roblox Support.

Set a value, commit, and every matching button and footer link on every page
appears.

The footer social icons (Instagram, TikTok, Twitch, YouTube, Discord) are
plain links in the footer of `index.html` and `faq/index.html`. Change both
pages if one moves. If the Discord invite changes, update `config.js` too.

## Editing FAQs

All FAQ answers live in `faq/index.html`, between `FAQ CONTENT START` and
`FAQ CONTENT END`. The home page only links to them, so there's one copy to
keep up to date.

- Each question is a `<details>` with an `id`, and `faq/#refunds` opens that
  answer directly. Keep ids stable once they've been shared.
- The home page "Need a hand?" list links to five of them by id.
- To use a hosted help centre instead, replace the block between the two
  markers with its embed.

The current answers are a draft. The game-specific ones come from the landing page
copy. The Roblox ones (refunds, accounts, bans, parental controls)
describe Roblox's own tools and link to Roblox. Have them reviewed before
launch.

## Going live

Run `python3 tools/check.py --launch`. It lists everything below that's still
missing.

1. **Links:** fill in every value in `assets/js/config.js`.
2. **Launch time:** confirm `launchAt` in `config.js` (UTC). The "All aboard"
   line switches to "Now open on Roblox" at that moment.
3. **FAQs:** final copy replaces the draft block.
4. **Activity statuses, Founding Crew benefits:** confirm the copy in
   `index.html` (search for `EDIT:`).
5. **Trailer captions:** the trailer has an audio track. If it includes speech
   or lyrics, add a WebVTT `<track kind="captions">` to the `<video>`.

## Moving to the final host

1. **Copy the folder.** Upload everything except `.git`, `.github`,
   `tools` and `README.md` to the host's web root. All paths are relative, so it works at a
   domain root or in a sub-folder.
2. **Indexing.** `index.html` and `faq/index.html` carry
   `<meta name="robots" content="index, follow">` (since 2026-11-25). Keep it.
   `404.html` stays `noindex`.
3. **Update social URLs.** Change `og:url` and `og:image` in `index.html` and
   `faq/index.html` to full URLs on the new domain. They point at the gate for
   now, which is behind Okta, so share previews don't work until this is done.
4. **Configure the host:**
   - Serve `index.html` for folder URLs, so `/faq/` loads `faq/index.html`.
     Netlify, Cloudflare Pages and nginx do this by default.
     **S3 + CloudFront with a REST origin does not:** add a CloudFront Function
     that appends `index.html` to URLs ending in `/`.
   - Use `404.html` as the error page.
5. **Retire the gate copy.** Point people at the new domain and remove
   `meet-me-there/` from lkwd/avakin-prototypes, or leave it as an internal
   preview.

## Tracking and consent

The site sets no cookies and runs no analytics. Analytics (GA4, GTM or
similar) must not be added until a consent setup is in place.

## Notes

- **Fonts:** Helvetica Neue / Helvetica, falling back to Arial. No web fonts
  are loaded.
- **Images:** screenshots are 1280×720 WebP. The four "Your voyage" cards
  (`voyage-*.webp`) are designed 4:5 posters from Vanessa (about 1020×1283,
  2026-11-23) with the logo along the bottom, so they show uncropped at 4:5 on
  every screen. Replace them with images of the same shape.
- **Video:** the 22-second reveal trailer as WebM (VP9, about 8 MB) and MP4
  (H.264, about 9.5 MB). The trailer only
  downloads when someone presses play. Without JavaScript, the native video
  controls are used.
- **Colour:** white text on the brand pink (#E8197D) is below WCAG AA contrast.
  Buttons and small pink text use `--magenta-ink` (#DA1576, 4.8:1), and the
  brand pink stays for decoration.
