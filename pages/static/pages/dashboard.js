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
  if (dlg && form && msg) {
    function closeDelete() {
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
      b.addEventListener("click", closeDelete);
    });

    dlg.addEventListener("click", function (e) {
      if (e.target === dlg) closeDelete();
    });
  }

  var editDlg = document.getElementById("dashCategoryEditDialog");
  var editForm = document.getElementById("dashCategoryEditForm");
  var editName = document.getElementById("dashCategoryEditName");
  if (editDlg && editForm && editName) {
    function closeEdit() {
      if (editDlg.open) editDlg.close();
    }

    document.querySelectorAll("[data-dash-category-edit]").forEach(function (el) {
      el.addEventListener("click", function () {
        var url = el.getAttribute("data-edit-url");
        var name = el.getAttribute("data-category-name");
        if (!url) return;
        editForm.setAttribute("action", url);
        editName.value = name || "";
        editDlg.showModal();
        editName.focus();
        editName.select();
      });
    });

    editDlg.querySelectorAll("[data-dialog-close]").forEach(function (b) {
      b.addEventListener("click", closeEdit);
    });

    editDlg.addEventListener("click", function (e) {
      if (e.target === editDlg) closeEdit();
    });
  }
})();
