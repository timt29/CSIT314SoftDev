function logout() {
    window.location.href = "/logout";
}

// Helper to render report data as a table
function renderTable(data) {
    if (!data.length) return "<p>No data available.</p>";
    let headers = Object.keys(data[0]);
    let html = "<table border='1' style='width:100%;border-collapse:collapse;'><thead><tr>";
    headers.forEach(h => html += `<th>${h}</th>`);
    html += "</tr></thead><tbody>";
    data.forEach(row => {
        html += "<tr>";
        headers.forEach(h => html += `<td>${row[h]}</td>`);
        html += "</tr>";
    });
    html += "</tbody></table>";
    return html;
}

function loadReport(endpoint, title) {
    const resultDiv = document.getElementById('report-result');
    resultDiv.innerHTML = `<h2>${title}</h2><p>Loading...</p>`;
    fetch(endpoint)
        .then(res => res.json())
        .then(data => {
            resultDiv.innerHTML = `<h2>${title}</h2>` + renderTable(data);
        })
        .catch(() => {
            resultDiv.innerHTML = `<h2>${title}</h2><p>Error loading report.</p>`;
        });
}

document.addEventListener('DOMContentLoaded', () => {
    const btnDaily = document.getElementById('btn-daily');
    if (btnDaily) {
        btnDaily.addEventListener('click', () => {
            loadReport('/api/report/cleaner_popularity', 'Cleaner Popularity Report');
        });
    }
    const btnMonthly = document.getElementById('btn-monthly');
    if (btnMonthly) {
        btnMonthly.addEventListener('click', () => {
            loadReport('/api/report/homeowner_engagement', 'Homeowner Engagement Report');
        });
    }
});

