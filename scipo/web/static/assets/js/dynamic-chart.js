(async () => {
    // Function to fetch data from the API during initial load
    async function fetchData() {
        try {
            const response = await fetch('/api/resources');
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching data about resources:', error);
        }
    }

    // Function to initialize and render the doughnut chart
    async function initializeChart(canvasId, label, used, quota) {
        // Chart configuration
        const options = {
            responsive: false,
            maintainAspectRatio: false,
            cutout: '70%', // Adjust the size of the doughnut hole
            plugins: {
                legend: {
                    display: true,
                    position: 'right',
                },
            },
        };

        // Create and render the doughnut chart
        const ctx = document.getElementById(canvasId).getContext('2d');
        const resourceChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: [`Used ${label}`, `Unused ${label}`],
                datasets: [{
                    data: [used.value, quota.value - used.value],
                    backgroundColor: ["#007bff", "#f2f4f6"],
                    borderColor: ["#007bff", "#f2f4f6"],
                    borderWidth: 1
                }]
            },
            options: options
        });
    }

    const initialData = await fetchData();
    initializeChart('resourceChartCpu', "CPU", initialData.resources_used.cpu,    initialData.resources_quota.cpu);
    initializeChart('resourceChartRam', "RAM", initialData.resources_used.memory, initialData.resources_quota.memory);
})();
