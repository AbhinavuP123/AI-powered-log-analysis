async function fetchEntries() {
    try {
        const response = await fetch('../db.json');
        if (!response.ok) throw new Error('Could not fetch db.json');
        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.error('Error fetching data:', error);
        // Load mock data if file doesn't exist yet
        updateDashboard([
            {
                timestamp: new Date().toISOString(),
                status: "failed",
                summary: "Sample Entry: AI Analysis will appear here once you run the workflow.",
                root_cause: "No data found in db.json yet."
            }
        ]);
    }
}

function updateDashboard(entries) {
    const tableBody = document.getElementById('entries-body');
    const totalCount = document.getElementById('total-count');
    const successCount = document.getElementById('success-count');
    const failCount = document.getElementById('fail-count');

    // Sort by timestamp descending
    entries.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    tableBody.innerHTML = '';
    let success = 0;
    let fail = 0;

    entries.forEach(entry => {
        const row = document.createElement('tr');
        
        const date = new Date(entry.timestamp);
        const timeStr = date.toLocaleString();
        
        if (entry.status === 'passed') success++;
        else fail++;

        row.innerHTML = `
            <td class="time-cell">${timeStr}</td>
            <td><span class="status-badge ${entry.status}">${entry.status}</span></td>
            <td class="summary-cell">${entry.summary}</td>
            <td class="cause-cell">${entry.root_cause}</td>
        `;
        tableBody.appendChild(row);
    });

    totalCount.innerText = entries.length;
    successCount.innerText = success;
    failCount.innerText = fail;
}

document.getElementById('refresh-btn').addEventListener('click', fetchEntries);

// Initial fetch
fetchEntries();
// Auto-refresh every 30 seconds
setInterval(fetchEntries, 30000);
