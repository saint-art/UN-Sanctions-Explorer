document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector(".search-form");

    if (!form) return;

    form.addEventListener("submit", () => {

        const text = document.getElementById("searchText");

        if (text) {

            text.innerHTML = "⏳ Searching...";

        }

    });

});