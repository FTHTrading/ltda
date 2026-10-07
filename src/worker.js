// livethedreamathletics.com — parent brand site. Static assets + www redirect + health.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === "www.livethedreamathletics.com") {
      url.hostname = "livethedreamathletics.com";
      return Response.redirect(url.toString(), 301);
    }
    if (url.pathname === "/api/health") {
      return new Response(JSON.stringify({ ok: true, site: "livethedreamathletics.com" }), { headers: { "Content-Type": "application/json", "Cache-Control": "no-store" } });
    }
    // short links to the family of sites
    if (url.pathname === "/powerpunch" || url.pathname === "/pp") return Response.redirect("https://powerpunchathletics.com/", 302);
    if (url.pathname === "/dispatch") return Response.redirect("https://powerpunchathletics.com/dispatch/", 302);
    if (url.pathname === "/nil33") return Response.redirect("https://nil33.com/", 302);
    return env.ASSETS.fetch(request);
  },
};
