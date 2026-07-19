fetch("/api/dashboard")

.then(response => response.json())

.then(data => {

    const labels = data.nationalities.map(
        item => item.name
    );

    const values = data.nationalities.map(
        item => item.count
    );

    new Chart(

        document.getElementById("nationalityPie"),

        {

            type: "pie",

            data: {

                labels: labels,

                datasets: [

                    {

                        data: values

                    }

                ]

            },

            options: {

                responsive: true,

                plugins: {

                    legend: {

                        position: "bottom"

                    }

                }

            }

        }

    );

    new Chart(

    document.getElementById("nationalityBar"),

    {

        type: "bar",

        data: {

            labels: labels,

            datasets: [

                {

                    label: "Persons",

                    data: values

                }

            ]

        },

        options: {

            responsive: true,

            indexAxis: "y",

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                x: {

                    beginAtZero: true

                }

            }

        }

    }

);

});