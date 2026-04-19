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

  var dlg = document.getElementById("dashDeleteDialog");
  var form = document.getElementById("dashDeleteForm");
  var msg = document.getElementById("dashDeleteMessage");
  if (!dlg || !form || !msg) return;

  function closeDialog() {
    if (dlg.open) dlg.close();
  }

  document.querySelectorAll("[data-dash-delete]").forEach(function (el) {
    el.addEventListener("click", function () {
      var url = el.getAttribute("data-delete-url");
      var text = el.getAttribute("data-delete-message");
      if (!url) return;
      form.setAttribute("action", url);
      msg.textContent = text || "This cannot be undone.";
      dlg.showModal();
      var cancelBtn = document.getElementById("dashDeleteCancel");
      if (cancelBtn) cancelBtn.focus();
    });
  });

  dlg.querySelectorAll("[data-dialog-close]").forEach(function (b) {
    b.addEventListener("click", closeDialog);
  });

  dlg.addEventListener("click", function (e) {
    if (e.target === dlg) closeDialog();
  });
})();
