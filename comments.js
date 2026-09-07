// Comments are GitHub Discussions, rendered by giscus.  Nothing is stored
// here and nothing tracks the reader until the thread loads.
//
// SETUP -- fill these four in once, after the repository exists:
//   1. make the repository public and turn on Discussions
//   2. install the giscus app: https://github.com/apps/giscus
//   3. go to https://giscus.app, enter the repo, and copy what it gives you
const GISCUS = {
  repo: "",            // "yourname/mahjong-notes"
  repoId: "",          // from giscus.app
  category: "Comments",
  categoryId: "",      // from giscus.app
};

(function () {
  const host = document.getElementById("comments");
  if (!host) return;
  if (!GISCUS.repo || !GISCUS.repoId || !GISCUS.categoryId) {
    host.innerHTML = '<p class="lede" style="font-size:.85rem">'
      + "Comments are not configured yet — see comments.js.</p>";
    return;
  }
  const s = document.createElement("script");
  Object.assign(s, { src: "https://giscus.app/client.js", async: true,
                     crossOrigin: "anonymous" });
  const d = { repo: GISCUS.repo, "repo-id": GISCUS.repoId,
              category: GISCUS.category, "category-id": GISCUS.categoryId,
              mapping: "pathname", strict: "1", "reactions-enabled": "1",
              "emit-metadata": "0", "input-position": "top",
              theme: "preferred_color_scheme", lang: "en", loading: "lazy" };
  for (const [k, v] of Object.entries(d)) s.setAttribute("data-" + k, v);
  host.appendChild(s);
})();
