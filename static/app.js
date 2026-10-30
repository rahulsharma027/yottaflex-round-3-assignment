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

// Queue controls keep real server-rendered URLs as their no-JavaScript fallback.
let queueController = null;
let queueNavigation = 0;
let queueQuery = window.location.pathname + window.location.search;

async function navigateQueue(destination, recordHistory = true) {
  const target = new URL(destination, window.location.href);
  const queue = document.getElementById("case-queue");
  if (!queue || target.origin !== window.location.origin) return;
  const navigation = ++queueNavigation;
  if (queueController) queueController.abort();
  queueController = new AbortController();
  queue.setAttribute("aria-busy", "true");
  const announcement = document.getElementById("queue-announcement");
  announcement.textContent = "Updating cases…";
  try {
    const response = await fetch(target.pathname + target.search, {
      signal: queueController.signal,
      credentials: "same-origin",
      cache: "no-store",
      headers: { "X-Requested-With": "XMLHttpRequest" },
    });
    if (!response.ok) throw new Error("Queue unavailable");
    const page = new DOMParser().parseFromString(await response.text(), "text/html");
    const nextQueue = page.getElementById("case-queue");
    const nextSummary = page.querySelector("[data-case-summary]");
    if (!nextQueue || !nextSummary) throw new Error("Full navigation required");
    if (navigation !== queueNavigation) return;
    queue.replaceWith(nextQueue);
    document.querySelector("[data-case-summary]").replaceWith(nextSummary);
    queueQuery = target.pathname + target.search;
    if (recordHistory && target.href !== window.location.href) {
      window.history.pushState(null, "", target.pathname + target.search + target.hash);
    }
    announcement.textContent = `${nextQueue.dataset.resultCount} cases match this view.`;
    nextQueue.focus({ preventScroll: true });
    nextQueue.scrollIntoView({
      behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth",
      block: "start",
    });
  } catch (error) {
    if (error.name !== "AbortError" && navigation === queueNavigation) {
      // Includes expired sessions: let Django perform its normal navigation/redirect.
      window.location.assign(target.href);
    }
  } finally {
    if (navigation === queueNavigation) {
      document.getElementById("case-queue")?.removeAttribute("aria-busy");
      queueController = null;
    }
  }
}

document.addEventListener("click", (event) => {
  const link = event.target instanceof Element ? event.target.closest("a[data-queue-navigation]") : null;
  if (!link || event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
  if (!document.getElementById("case-queue") || new URL(link.href).origin !== window.location.origin) return;
  event.preventDefault();
  navigateQueue(link.href);
});

document.addEventListener("submit", (event) => {
  const form = event.target;
  if (!(form instanceof HTMLFormElement) || !form.matches("[data-queue-filter]")) return;
  event.preventDefault();
  const destination = new URL(form.action);
  destination.search = new URLSearchParams(new FormData(form)).toString();
  destination.hash = "case-queue";
  navigateQueue(destination);
});

window.addEventListener("popstate", () => {
  const query = window.location.pathname + window.location.search;
  if (document.getElementById("case-queue") && query !== queueQuery) navigateQueue(window.location.href, false);
});

const errors = document.querySelector(".errorlist");
if (errors) {
  const detail = errors.closest("details");
  if (detail) detail.open = true;
  errors.setAttribute("tabindex", "-1");
  errors.focus();
}
