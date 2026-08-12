/* Galerie — apparition au défilement + agrandissement au clic.
   Sans dépendance externe. Se dégrade proprement : si JavaScript est absent,
   les images restent visibles et cliquables (elles ouvrent leur source). */
(function () {
  "use strict";

  var animationsReduites = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var items = Array.prototype.slice.call(document.querySelectorAll(".galerie__item[data-src]"));

  /* 1. Apparition en fondu, décalée d'un item à l'autre. */
  if (animationsReduites || !("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("est-visible"); });
  } else {
    var observateur = new IntersectionObserver(function (entrees, obs) {
      entrees.forEach(function (entree) {
        if (entree.isIntersecting) {
          entree.target.classList.add("est-visible");
          obs.unobserve(entree.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    items.forEach(function (el) { observateur.observe(el); });
  }

  /* 2. Agrandissement (lightbox). */
  var boite = document.getElementById("lightbox");
  if (!boite) return;

  var img = boite.querySelector("img");
  var legende = boite.querySelector("figcaption");
  var boutonFermer = boite.querySelector(".lightbox__fermer");
  var declencheur = null;

  function ouvrir(figure) {
    var src = figure.getAttribute("data-src");
    if (!src) return;
    declencheur = figure;
    img.setAttribute("src", src);
    img.setAttribute("alt", figure.getAttribute("data-legende") || "");

    var texte = figure.getAttribute("data-legende") || "";
    var credit = figure.getAttribute("data-credit") || "";
    legende.textContent = "";
    if (texte) {
      var t = document.createElement("span");
      t.className = "lightbox__legende";
      t.textContent = texte;
      legende.appendChild(t);
    }
    if (credit) {
      var c = document.createElement("span");
      c.className = "lightbox__credit";
      c.textContent = credit;
      legende.appendChild(c);
    }

    boite.hidden = false;
    // Forcer un reflow avant d'ajouter la classe pour que la transition parte.
    void boite.offsetWidth;
    boite.classList.add("est-ouvert");
    document.body.style.overflow = "hidden";
    boutonFermer.focus();
  }

  function fermer() {
    boite.classList.remove("est-ouvert");
    document.body.style.overflow = "";
    var fin = function () {
      boite.hidden = true;
      img.setAttribute("src", "");
      boite.removeEventListener("transitionend", fin);
    };
    if (animationsReduites) fin();
    else boite.addEventListener("transitionend", fin);
    if (declencheur) { declencheur.focus(); declencheur = null; }
  }

  items.forEach(function (figure) {
    figure.addEventListener("click", function () { ouvrir(figure); });
    figure.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        ouvrir(figure);
      }
    });
  });

  boutonFermer.addEventListener("click", fermer);
  boite.addEventListener("click", function (e) {
    if (e.target === boite) fermer();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !boite.hidden) fermer();
  });
})();
