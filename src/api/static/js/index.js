function redirectTo(url) {
    window.location.href = url;
}

function handleRegisterSuccess() {
    setTimeout(() => {
        redirectTo('/auth/login');
    }, 3000);
}

function handleLogoutSuccess() {
    setTimeout(() => {
        redirectTo('/');
    }, 3000);
}

function confirmAction(message) {
    return confirm(message);
}

function handleDelete(event) {
    if (!confirmAction("Sind Sie sicher, dass Sie den Eintrag löschen möchten?")) {
        event.preventDefault();
    }
}

function handleCreate(event) {
    if (!confirmAction("Sind Sie sicher, dass Sie den Eintrag anlegen möchten?")) {
        event.preventDefault();
    }
}

function handleSave(event) {
    if (!confirmAction("Möchten Sie die Änderung wirklich speichern?")) {
        event.preventDefault();
    }
}

const ctx = document.getElementById('goalChart').getContext('2d');
const goalChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Ziele',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
            fill: false,
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
            }
        }
    }
});

function populateChart(goalHistory) {
    goalHistory.forEach(entry => {
        goalChart.data.labels.push(entry.modified_date);
        goalChart.data.datasets[0].data.push(entry.rating);
    });
    goalChart.update();
}

fetch('/goal/api/goal_history')
    .then(response => response.json())
    .then(data => {
        populateChart(data.goal_history);
    })
    .catch(error => console.error('Error fetching goal history:', error));