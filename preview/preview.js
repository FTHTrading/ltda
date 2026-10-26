// Local redesign preview. Captions are scene and place only; names attach once Kevan maps them and the person says yes.
// Content comes from our own data files (people.json, records.src.json, hashes.json), not from visitors.
(function () {
  var M = "/preview/media/";
  var page = document.body.getAttribute("data-page");
  var pad = function (n) { return String(n).padStart(2, "0"); };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (ch) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]; }); };
  var safeUrl = function (u) { try { var x = new URL(u, location.href); return /^https?:$/.test(x.protocol) ? x.href : null; } catch (e) { return null; } };

  // Film strip: archive page only (the home page stays words-first).
  var FRAMES = [
    { f: "b03", place: "Little League", when: "the scrapbook", alt: "Scrapbook page: a young batter and his Little League team" },
    { f: "b14", place: "College", when: "team day", alt: "A college team gathered on the field" },
    { f: "b21", place: "Pride", when: "on the field", alt: "Player in a Pride jersey with a young fan" },
    { f: "k16", place: "Spring training", when: "March 2016", alt: "Two men talking at the dugout rail at spring training" },
    { f: "b07", place: "Pro ball", when: "mountain ballpark", alt: "Two players in uniform at a ballpark below mountains" },
    { f: "rod-carew-hillside", place: "Panama", when: "Rod Carew Stadium", alt: "Rod Carew Stadium from the hillside" },
    { f: "k01", place: "Night practice", when: "team talk", alt: "Coach talking to kneeling players on a lit field" }
  ];
  var SHEET = [
    { f: "b04", cap: "Scrapbook · team" }, { f: "b13", cap: "College days" }, { f: "b14", cap: "College · team day" },
    { f: "b07", cap: "Pro ball" }, { f: "b17", cap: "Teammates" }, { f: "b18", cap: "Minor league blues" },
    { f: "b20", cap: "Pride" }, { f: "b21", cap: "Pride · a young fan" }, { f: "b19", cap: "Old friends" },
    { f: "b06", cap: "Ballpark lineup" }, { f: "b23", cap: "Gear day" }, { f: "b24", cap: "The poster wall" },
    { f: "b16", cap: "Locker room" }, { f: "b05", cap: "Hotel lobby" }, { f: "b08", cap: "Night out" },
    { f: "b25", cap: "The crew" }, { f: "b09", cap: "The office" },
    { f: "coach-cage", cap: "The cage", anchored: true }, { f: "dugout", cap: "Dugout", anchored: true },
    { f: "rod-carew-hillside", cap: "Panama · Rod Carew" }, { f: "panama-rod-carew-rail", cap: "Panama · 2018" },
    { f: "k12", cap: "Summer ball · on film" }, { f: "k16", cap: "Spring training · 2016" }, { f: "k17", cap: "Spring training · 2016" },
    { f: "k02", cap: "Clinic" }, { f: "k03", cap: "Clinic · the group" }, { f: "k01", cap: "Night practice" },
    { f: "k06", cap: "Atlanta ballpark" }, { f: "k05", cap: "Tropicana Field" }, { f: "k04", cap: "Warning track" },
    { f: "k07", cap: "Under the lights" }, { f: "k15", cap: "Shoe day" }, { f: "k13", cap: "Octagon · baseball" },
    { f: "k11", cap: "The arena wall" }, { f: "k10", cap: "Signing day" }, { f: "k18", cap: "Studio" },
    { f: "k09", cap: "Night out" }, { f: "k08", cap: "Teammates" }, { f: "k14", cap: "The track" }
  ];

  var frames = document.getElementById("frames"), caption = document.getElementById("caption");
  if (frames) FRAMES.forEach(function (fr, i) {
    var el = document.createElement("div");
    el.className = "frame"; el.tabIndex = 0; el.setAttribute("role", "listitem");
    el.innerHTML = '<div class="pic"><img src="' + M + fr.f + '.duo.jpg" alt="' + fr.alt + '"><img class="orig" src="' + M + fr.f + '.orig.jpg" alt=""></div><div class="no">FRAME ' + pad(i + 1) + "</div>";
    function on() {
      Array.prototype.forEach.call(frames.children, function (c) { c.classList.remove("on"); });
      el.classList.add("on");
      caption.innerHTML = fr.place + " · " + fr.when + " · frame " + pad(i + 1);
    }
    el.addEventListener("mouseenter", on); el.addEventListener("focus", on); el.addEventListener("click", on);
    frames.appendChild(el);
    if (i === 3) on();
  });

  var sheet = document.getElementById("sheet");
  if (sheet) SHEET.forEach(function (c) {
    var d = document.createElement("figure");
    d.className = "cell"; d.style.margin = "0"; d.tabIndex = 0;
    d.innerHTML = '<div class="pic"><img src="' + M + c.f + '.duo.jpg" alt="' + c.cap + '" loading="lazy"><img class="orig" src="' + M + c.f + '.orig.jpg" alt="" loading="lazy"></div>' +
      (c.anchored ? '<a class="chip ok" href="https://livethedreamathletics.com/proof/">Checked</a>' : "") +
      '<figcaption class="cap"><span>' + c.cap + "</span></figcaption>";
    sheet.appendChild(d);
  });

  var records = document.getElementById("records");
  if (records) Promise.all([
    fetch("/data/collection/records.src.json").then(function (r) { return r.json(); }),
    fetch(M + "hashes.json").then(function (r) { return r.json(); })
  ]).then(function (res) {
    var H = res[1];
    res[0].records.forEach(function (c) {
      var h = H[c.photo] || {};
      var el = document.createElement("article");
      el.className = "rec"; el.tabIndex = 0;
      el.innerHTML = '<div class="pic"><img src="' + M + esc(c.photo) + '.duo.jpg" alt="' + esc(c.title) + '" loading="lazy"><img class="orig" src="' + M + esc(c.photo) + '.orig.jpg" alt="" loading="lazy"><span class="no">' + esc(c.id) + "</span></div>" +
        '<div class="body"><h3>' + esc(c.title) + "</h3><p>" + esc(c.story) + "</p>" +
        "<dl><dt>When</dt><dd>" + esc(c.era) + "</dd><dt>Original</dt><dd>where it's kept: to record</dd><dt>Fingerprint</dt><dd>" + (h.sha256 ? h.sha256.slice(0, 16) + "…" + h.sha256.slice(-8) : "—") + "</dd></dl>" +
        '<div class="chips"><span class="chip ok">Fingerprinted</span><span class="chip wait">Being finished</span></div></div>';
      records.appendChild(el);
    });
  });

  var people = document.getElementById("people");
  if (people) fetch("/data/people.json").then(function (r) { return r.json(); }).then(function (data) {
    var limit = Number(people.getAttribute("data-limit")) || data.people.length;
    data.people.slice(0, limit).forEach(function (p) {
      var srcs = (p.fact_sources || []).map(safeUrl).filter(Boolean).map(function (u, i) { return '<a class="chip src" href="' + esc(u) + '" target="_blank" rel="noopener">source ' + (i + 1) + "</a>"; }).join("");
      var el = document.createElement("article");
      el.className = "person" + (p.in_memory ? " memory" : "");
      el.innerHTML = '<div class="mono role">' + (p.in_memory ? "In memory · " : "") + esc(p.group) + "</div>" +
        "<h3>" + esc(p.name) + "</h3><p>" + esc(p.relationship) + "</p>" + (p.public_facts ? '<p class="facts">' + esc(p.public_facts) + "</p>" : "") +
        '<div class="src">' + srcs + '<span class="chip wait">' + (p.publish ? "Published" : "Awaiting yes") + "</span></div>";
      people.appendChild(el);
    });
  });
})();
