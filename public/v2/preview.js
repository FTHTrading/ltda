// Live the Dream Athletics v2: phone menu and film-strip captions. All content is rendered at build time
// by tools/build_v2.py; this script only reads data-cap attributes it wrote.
(function () {
  var menu = document.getElementById("menu"), nav = document.getElementById("nav");
  if (menu && nav) menu.addEventListener("click", function () {
    nav.classList.toggle("open");
    menu.setAttribute("aria-expanded", nav.classList.contains("open"));
  });

  var frames = document.getElementById("frames"), caption = document.getElementById("caption");
  if (!frames || !caption) return;
  var list = Array.prototype.slice.call(frames.querySelectorAll(".frame"));
  function on(el) {
    list.forEach(function (c) { c.classList.remove("on"); });
    el.classList.add("on");
    caption.textContent = el.getAttribute("data-cap") || "";
  }
  list.forEach(function (el) {
    el.addEventListener("mouseenter", function () { on(el); });
    el.addEventListener("focus", function () { on(el); });
    el.addEventListener("click", function () { on(el); });
  });
  var start = frames.querySelector(".frame.on") || list[0];
  if (start) on(start);
})();
