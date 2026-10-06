document.addEventListener("DOMContentLoaded", async () => {

    try {

        const response = await fetch(window.EXPENSE_API);

        if (!response.ok) {
            throw new Error("Chart API request failed");
        }

        const data = await response.json();

        console.log("Chart data:", data);

        // =========================
        // EXPENSE BREAKDOWN
        // =========================

        const expenseCanvas =
            document.getElementById("expenseChart");

        if (expenseCanvas) {

            const labels = data.categories.map(
                item => item.label
            );

            const values = data.categories.map(
                item => item.value
            );

            new Chart(expenseCanvas, {

                type: "doughnut",

                data: {
                    labels: labels,

                    datasets: [{
                        data: values,
                        borderWidth: 0
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    plugins: {
                        legend: {
                            position: "bottom"
                        }
                    },

                    cutout: "68%"
                }

            });
        }


        // =========================
        // MONTHLY OVERVIEW
        // =========================

        const monthlyCanvas =
            document.getElementById("monthlyChart");

        if (monthlyCanvas) {

            const months = data.monthly.map(
                item => item.month
            );

            const income = data.monthly.map(
                item => item.income
            );

            const expenses = data.monthly.map(
                item => item.expense
            );

            new Chart(monthlyCanvas, {

                type: "bar",

                data: {

                    labels: months,

                    datasets: [

                        {
                            label: "Income",
                            data: income,
                            borderRadius: 7
                        },

                        {
                            label: "Expenses",
                            data: expenses,
                            borderRadius: 7
                        }

                    ]
                },

                options: {

                    responsive: true,
                    maintainAspectRatio: false,

                    plugins: {
                        legend: {
                            position: "bottom"
                        }
                    },

                    scales: {

                        y: {
                            beginAtZero: true
                        },

                        x: {
                            grid: {
                                display: false
                            }
                        }

                    }

                }

            });
        }

    } catch (error) {

        console.error(
            "Expense Tracker chart error:",
            error
        );

    }

});