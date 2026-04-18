(function () {
  var KEY = "studioDashSidebarCollapsed";
  var body = document.body;

  function apply(saved) {
    if (saved === "1") {
      body.classList.add("dash--collapsed");
    } else {
      body.classList.remove("dash--collapsed");
    }
  }

  apply(localStorage.getItem(KEY));

  var btn = document.getElementById("js-sidebar-toggle");
  if (btn) {
    btn.addEventListener("click", function () {
      body.classList.toggle("dash--collapsed");
      localStorage.setItem(KEY, body.classList.contains("dash--collapsed") ? "1" : "0");
      btn.setAttribute(
        "aria-expanded",
        body.classList.contains("dash--collapsed") ? "false" : "true"
      );
    });
    btn.setAttribute(
      "aria-expanded",
      body.classList.contains("dash--collapsed") ? "false" : "true"
    );
  }
})();
