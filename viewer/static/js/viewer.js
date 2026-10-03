"use strict";

document.addEventListener("click", (event) => {
    const button = event.target.closest(".copy-code-button");

    if (!button) {
        return;
    }

    const code = button.parentElement.querySelector("code");

    if (!code) {
        return;
    }

    navigator.clipboard.writeText(code.innerText).then(() => {
        button.classList.add("copied");
        button.textContent = "Copied!";

        setTimeout(() => {
            button.textContent = "Copy code";
            button.classList.remove("copied");
        }, 1500);
    }).catch(() => {
        button.textContent = "Copy failed";
    });
});
