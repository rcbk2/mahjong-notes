// Comments are GitHub Discussions, rendered by giscus.  Nothing is stored
// here and nothing tracks the reader until the thread loads.
//
// The category is Announcement-format on purpose: only the giscus app can
// open a thread, so one thread means one post rather than whatever anyone
// felt like starting.  Threads are matched to posts by pathname, so renaming
// a file orphans its comments.
const GISCUS = {
  repo: "rcbk2/mahjong-notes",
  repoId: "R_kgDOUQnZkg",
  category: "Comments",
  categoryId: "DIC_kwDOUQnZks4DFClN",
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
