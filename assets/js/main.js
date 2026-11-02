/* Meet Me There: links from config.js, launch line, trailer cover, FAQ deep links */
var MMT = window.MMT || { links: {} };

// Links: show each [data-link] once its value is set in config.js; otherwise show its [data-fallback].
(function(){
  var links = MMT.links || {};
  function has(k){ return typeof links[k] === "string" && links[k].trim() !== ""; }
  // An element can list several keys ("discord group"): it shows when any is set, and a link inside takes the first one set.
  document.querySelectorAll("[data-link]").forEach(function(el){
    var k = el.getAttribute("data-link").split(/\s+/).filter(has)[0];
    if (!k) return;
    var a = el.matches("a") ? el : el.querySelector("a");
    var v = links[k].trim();
    if (a) a.href = k === "support" ? "mailto:" + v : v;
    el.hidden = false;
  });
  // A fallback lists one or more keys and shows only while all of them are empty.
  document.querySelectorAll("[data-fallback]").forEach(function(el){
    var keys = el.getAttribute("data-fallback").split(/\s+/);
    if (keys.some(has)) el.hidden = true;
  });
})();

// Year, then the launch line: switches at one fixed moment for every time zone.
(function(){
  var y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
  var at = Date.parse(MMT.launchAt || "");
  if (isNaN(at) || Date.now() < at) return;
  document.querySelectorAll("[data-after-launch]").forEach(function(el){
    el.textContent = el.getAttribute("data-after-launch");
  });
})();

// Trailer: the cover ships hidden so native controls work without JS; show it, then hide it on play.
(function(){
  var v = document.getElementById("trailerVideo"), c = document.getElementById("trailerCover");
  if (!v || !c) return;
  c.hidden = false;
  c.addEventListener("click", function(){ c.hidden = true; v.play().catch(function(){}); v.focus(); });
  v.addEventListener("play", function(){ c.hidden = true; });
})();

// FAQ: open the question named in the URL (faq/#refunds), and keep the URL in step when one is opened.
(function(){
  var list = document.querySelectorAll(".faq details[id]");
  if (!list.length) return;
  function openFromHash(){
    var id = decodeURIComponent(location.hash.slice(1));
    var d = id && document.getElementById(id);
    if (d && d.tagName === "DETAILS") { d.open = true; d.scrollIntoView({ block: "start" }); d.querySelector("summary").focus({ preventScroll: true }); }
  }
  list.forEach(function(d){
    d.addEventListener("toggle", function(){
      if (d.open && history.replaceState) history.replaceState(null, "", "#" + d.id);
    });
  });
  window.addEventListener("hashchange", openFromHash);
  openFromHash();
})();
