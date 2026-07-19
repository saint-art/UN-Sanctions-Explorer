document.addEventListener("DOMContentLoaded", () => {

    console.log("docs.js loaded");

    const buttons = document.querySelectorAll(".api-test-btn");

    const copyButtons = document.querySelectorAll(".copy-btn");

    copyButtons.forEach(button => {

        button.addEventListener("click", async () => {

            const endpoint = window.location.origin + button.dataset.endpoint;

            await navigator.clipboard.writeText(endpoint);

            const original = button.textContent;

            button.textContent = "Copied!";

            setTimeout(() => {

                button.textContent = original;

            }, 1500);

        });

    });

    console.log("Buttons:", buttons.length);

    buttons.forEach(button => {

        button.addEventListener("click", async () => {

            const endpoint = button.dataset.endpoint;

            const output = button.parentElement.querySelector(".api-output");

            output.classList.add("show");

            output.textContent = "Loading...";

            try {

                const response = await fetch(endpoint);

                const data = await response.json();

                output.textContent = JSON.stringify(
                    data,
                    null,
                    4
                );

            } catch (err) {

                output.textContent = err.toString();

            }

        });

    });

});