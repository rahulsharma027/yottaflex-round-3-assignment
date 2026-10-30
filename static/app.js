// Progressive enhancement only; all navigation and forms work without JavaScript.
const sidebar = document.querySelector(".sidebar");
const menu = document.querySelector(".nav-toggle");
if (sidebar && menu) {
  sidebar.classList.add("enhanced");
  menu.addEventListener("click", () => {
    const expanded = menu.getAttribute("aria-expanded") !== "true";
    menu.setAttribute("aria-expanded", String(expanded));
    sidebar.classList.toggle("menu-open", expanded);
    menu.textContent = expanded ? "Close menu" : "Menu";
  });
}
document.querySelectorAll('form[method="post"]').forEach((form) => {
  form.addEventListener("submit", () => {
    if (!form.checkValidity()) return;
    const button = form.querySelector('button[type="submit"]');
    if (button) {
      button.disabled = true;
      button.dataset.originalText = button.textContent;
      button.textContent = form.dataset.pendingText || "Saving…";
      button.setAttribute("aria-busy", "true");
    }
  });
});
window.addEventListener("pageshow", () => {
  document.querySelectorAll("button[data-original-text]").forEach((button) => {
    button.disabled = false;
    button.textContent = button.dataset.originalText;
    button.removeAttribute("aria-busy");
  });
});
// Username shortcuts still require the matching password and Django authentication.
const usernameInput = document.getElementById("id_username");
const passwordInput = document.getElementById("id_password");
const accountStatus = document.getElementById("demo-account-status");
if (usernameInput && passwordInput && accountStatus) {
  document.querySelectorAll("[data-demo-username]").forEach((button) => {
    button.hidden = false;
    button.addEventListener("click", () => {
      const username = button.dataset.demoUsername;
      if (usernameInput.value !== username) passwordInput.value = "";
      usernameInput.value = username;
      usernameInput.dispatchEvent(new Event("input", { bubbles: true }));
      accountStatus.textContent = `Username filled: ${username}. Enter this account’s generated password to sign in.`;
      passwordInput.focus();
    });
  });
}

const errors = document.querySelector(".errorlist");
if (errors) {
  const detail = errors.closest("details");
  if (detail) detail.open = true;
  errors.setAttribute("tabindex", "-1");
  errors.focus();
}
