/* Meet Me There site settings.
   Fill in a link and every button or footer link for it appears across the site.
   Leave a value as "" and that link stays hidden (the page shows a fallback where it needs one).
   See README.md "Going live" for the full checklist. */
window.MMT = {
  // EDIT: confirm the exact launch time. Written in UTC ("Z"); the "All aboard" line
  // switches to "Now open on Roblox" at this moment for every visitor.
  launchAt: "2026-12-01T00:00:00Z",

  links: {
    play: "https://www.roblox.com/games/82055512169089/Meet-Me-There",  // Roblox experience
    support: "",  // EDIT: support email address only, e.g. help@example.org (becomes a mailto: link)
    terms: "",    // EDIT: Terms of Service URL
    privacy: "",  // EDIT: Privacy Policy URL
    discord: "https://discord.gg/BKfU8xBUXA",  // Discord invite (also hard-coded in the footer social icons)
    group: ""     // EDIT: Roblox community (group) URL
  }
};
