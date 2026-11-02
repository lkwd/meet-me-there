# Meet Me There website

The website for Meet Me There, a yacht-life roleplay experience on Roblox by
Lockwood Publishing. It's a static site: plain HTML and CSS with a little
JavaScript. There's no build step and no framework.

Temporary home: **https://lkwd.github.io/meet-me-there/** (GitHub Pages, from
the `main` branch). It stays there until the final domain and host are ready.

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
Discord, Roblox group) live in `assets/js/config.js`. Each one stays **hidden**
on the site until you set it, so a visitor never sees a broken or placeholder
link. Where a gap would look odd, a fallback shows instead:

- With no Play link, the hero shows "Launching 9 November on Roblox".
- With no support email, "Still need help?" points to Roblox Support.

Set a value, commit, and every matching button and footer link on every page
appears.

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
4. **Events, activity statuses, Founding Crew benefits:** confirm the copy in
   `index.html` (search for `EDIT:`).
5. **Trailer captions:** the trailer has an audio track. If it includes speech
   or lyrics, add a WebVTT `<track kind="captions">` to the `<video>`.

## Moving to the final host

1. **Copy the folder.** Upload everything except `.git`, `.github` and
   `tools` to the host's web root. All paths are relative, so it works at a
   domain root or in a sub-folder.
2. **Remove noindex.** Delete the `<meta name="robots" content="noindex">` line
   from `index.html` and `faq/index.html`. It keeps search engines off the
   temporary copy. Leave it in `404.html`.
3. **Update social URLs.** Change `og:url` and `og:image` in `index.html` and
   `faq/index.html` to full URLs on the new domain. Share previews break
   without this.
4. **Configure the host:**
   - Serve `index.html` for folder URLs, so `/faq/` loads `faq/index.html`.
     Netlify, Cloudflare Pages and nginx do this by default.
     **S3 + CloudFront with a REST origin does not:** add a CloudFront Function
     that appends `index.html` to URLs ending in `/`.
   - Use `404.html` as the error page.
5. **Redirect the old address.** Point the GitHub Pages URL at the new
   domain, or replace this site with a redirect page, so shared links keep
   working.

## Tracking and consent

The site sets no cookies and runs no analytics. Analytics (GA4, GTM or
similar) must not be added until a consent setup is in place.

## Notes

- **Fonts:** Helvetica Neue / Helvetica, falling back to Arial. No web fonts
  are loaded.
- **Video:** WebM (VP9) and MP4 (H.264), about 12.5 MB each. The trailer only
  downloads when someone presses play. Without JavaScript, the native video
  controls are used.
- **Colour:** white text on the brand pink (#E8197D) is below WCAG AA contrast.
  Buttons and small pink text use `--magenta-ink` (#DA1576, 4.8:1), and the
  brand pink stays for decoration.
