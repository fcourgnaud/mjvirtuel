/* MJ virtuel : vérification des mises à jour (v1.0)
   Chaque page déclare sa version :  window.MJV_PAGE = { name: "jeu", version: "2.1" };
   version.json (à la racine du site) donne les dernières versions publiées.
   Un élément avec l'attribut data-maj devient un bouton « Mettre à jour ». */
(function(){
  const page = window.MJV_PAGE || { name: "?", version: "0" };

  function cmp(a, b){
    a = String(a).split(".").map(Number); b = String(b).split(".").map(Number);
    for (let i = 0; i < Math.max(a.length, b.length); i++){ const d = (a[i] || 0) - (b[i] || 0); if (d) return d; }
    return 0;
  }

  const style = document.createElement("style");
  style.textContent = `
    #mjv-maj{position:fixed;left:50%;top:10px;transform:translateX(-50%);z-index:100;max-width:calc(100% - 24px);
      background:#151512;color:#e8e4d4;border:1px solid #e8b04a;padding:10px 12px;font:13px "IBM Plex Mono",ui-monospace,monospace;
      display:flex;gap:10px;align-items:center;flex-wrap:wrap;box-shadow:0 6px 24px rgba(0,0,0,.6)}
    #mjv-maj button{font:inherit;background:#e8b04a;color:#111;border:0;padding:6px 10px;cursor:pointer}
    #mjv-maj button.sec{background:transparent;color:#8c8774;border:1px solid #2a2a24}`;
  document.head.appendChild(style);

  let timer = null;
  function banner(text, buttons, autoClose){
    let el = document.getElementById("mjv-maj");
    if (!el){ el = document.createElement("div"); el.id = "mjv-maj"; document.body.appendChild(el); }
    el.innerHTML = "";
    const span = document.createElement("span"); span.textContent = text; el.appendChild(span);
    (buttons || []).concat([["✕", () => el.remove(), "sec"]]).forEach(([label, fn, cls]) => {
      const b = document.createElement("button"); b.textContent = label; if (cls) b.className = cls; b.onclick = fn; el.appendChild(b);
    });
    clearTimeout(timer); if (autoClose) timer = setTimeout(() => el.remove(), autoClose);
  }

  function reloadTo(tag){
    const u = new URL(location.href);
    u.searchParams.set("v", tag);
    location.replace(u.toString());
  }

  async function latest(){
    const r = await fetch("version.json?t=" + Date.now(), { cache: "no-store" });
    if (!r.ok) throw new Error(r.status);
    return r.json();
  }

  window.MJV_latest = latest;
  window.MJV_cmp = cmp;
  window.MJV_checkUpdate = async function(manual){
    try{
      const v = await latest(); window.MJV_LATEST = v;
      const l = v[page.name];
      if (l && cmp(l, page.version) > 0){
        banner(`Nouvelle version v${l} disponible (tu as v${page.version}).` + (v.notes ? " " + v.notes : ""), [["Mettre à jour", () => reloadTo(l)]]);
        return "ancienne";
      }
      if (manual) banner(`✔ À jour : v${page.version} (${v.date || ""}).`, [["Recharger quand même", () => reloadTo(page.version + "-" + Date.now())]], 6000);
      return "a-jour";
    }catch(e){
      if (manual) banner("Impossible de vérifier les mises à jour (pas de réseau ?).", [], 4000);
      return "erreur";
    }
  };

  document.addEventListener("click", e => {
    const b = e.target.closest && e.target.closest("[data-maj]");
    if (b){ e.preventDefault(); window.MJV_checkUpdate(true); }
  });
  // vérification automatique au chargement et au retour sur l'onglet
  setTimeout(() => window.MJV_checkUpdate(false), 800);
  let last = Date.now();
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible" && Date.now() - last > 60000){ last = Date.now(); window.MJV_checkUpdate(false); }
  });
})();
