document.addEventListener("DOMContentLoaded", function () {
  var article = document.querySelector(".md-content__inner");
  if (!article) return;

  var text = article.innerText || "";
  var cjk = (text.match(/[\u4e00-\u9fff\u3400-\u4dbf]/g) || []).length;
  var latin = text.replace(/[\u4e00-\u9fff\u3400-\u4dbf]/g, "")
    .split(/\s+/)
    .filter(Boolean).length;

  var minutes = Math.ceil(cjk / 400 + latin / 200);
  if (minutes < 1) return;

  var isZh = document.documentElement.lang === "zh" ||
    location.pathname.indexOf("/zh/") !== -1;

  var label = isZh
    ? "⏱️ 阅读时间: ~" + minutes + " 分钟"
    : "⏱️ Reading time: ~" + minutes + " min";

  var h1 = article.querySelector("h1");
  if (!h1) return;

  var el = document.createElement("div");
  el.className = "reading-time";
  el.textContent = label;
  h1.parentNode.insertBefore(el, h1.nextSibling);
});
