// Click-to-play YouTube: nothing loads from YouTube until the visitor presses play (privacy-enhanced domain).
document.querySelectorAll("button.vid3[data-yt]").forEach(function (btn) {
  btn.addEventListener("click", function () {
    var id = btn.getAttribute("data-yt");
    if (!/^[\w-]{11}$/.test(id)) return;
    var f = document.createElement("iframe");
    f.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
    f.title = btn.querySelector(".vt").textContent;
    f.allow = "autoplay; encrypted-media; picture-in-picture";
    f.allowFullscreen = true;
    f.referrerPolicy = "strict-origin-when-cross-origin";
    var box = document.createElement("div");
    box.className = "vid3 on";
    box.appendChild(f);
    btn.replaceWith(box);
  }, { once: true });
});
