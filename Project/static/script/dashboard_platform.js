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
            loadReport('/api/report/cleaner_popularity', 'Daily Report');
        });
    }
    const btnWeekly = document.getElementById('btn-weekly');
    if (btnWeekly) {
        btnWeekly.addEventListener('click', () => {
            loadReport('/api/report/cleaner_service_usage', 'Weekly Report');
        });
    }
    const btnMonthly = document.getElementById('btn-monthly');
    if (btnMonthly) {
        btnMonthly.addEventListener('click', () => {
            loadReport('/api/report/homeowner_engagement', 'Monthly Report');
        });
    }
    const btnCreate = document.getElementById('create-service-category');
    if (btnCreate) {
        btnCreate.addEventListener('click', () => showCategoryTab('create'));
    }
    const btnView = document.getElementById('view-service-category');
    if (btnView) {
        btnView.addEventListener('click', () => showCategoryTab('view'));
    }
});

// test code for service category management
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Load and render the service categories table
async function loadCategoryTable(searchQuery = "") {
    const response = await fetch(`/api/service_categories${searchQuery ? '?search=' + encodeURIComponent(searchQuery) : ''}`);
    const categories = await response.json();

    let rows = "";
    categories.forEach(category => {
        rows += `
            <tr>
                <td>${category.CategoryName}</td>
                <td>
                    <button class="action-button" onclick="showUpdateCategoryForm('${category.CategoryName}')">Update</button>
                    <button class="suspend-button" onclick="deleteServiceCategory('${category.CategoryName}')">Delete</button>
                </td>
            </tr>`;
    });

    if (categories.length === 0) {
        rows = `<tr><td colspan="2">No service categories found.</td></tr>`;
    }

    const tableBody = document.querySelector("#category-table tbody");
    if (tableBody) {
        tableBody.innerHTML = rows;
    }
}

function searchcategory() {
    const searchQuery = document.getElementById("category-search").value;
    loadCategoryTable(searchQuery);
}

// Show the form to create a new service category
function renderCreateCategoryForm() {
    document.getElementById('content').innerHTML = `
        <h3>Create Service Category</h3>
        <form id="create-category-form">
            <div class="form-group">
                <label for="create-category-name">Category Name:</label>
                <input id="create-category-name" type="text" placeholder="Enter Category Name" required>
            </div>
            <button type="button" onclick="createServiceCategory()">Create Category</button>
        </form>
    `;
}

// Create a new service category
async function createServiceCategory() {
    const categoryName = document.getElementById("create-category-name").value;

    const response = await fetch('/api/service_categories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ CategoryName: categoryName })
    });

    if (response.ok) {
        alert("Service category created!");
        showCategoryTab('view');
    } else {
        const error = await response.json();
        alert(`Failed to create category: ${error.message || error.error}`);
    }
}

// Show the update form for a category
function showUpdateCategoryForm(categoryName) {
    document.getElementById('modal-category-name').value = categoryName;
    document.getElementById('updateCategoryModal').style.display = 'block';
}

// Update a service category
async function updateServiceCategory() {
    const oldName = document.getElementById('modal-category-name').value;
    const newName = document.getElementById('modal-new-category-name').value;

    if (!newName) {
        alert("Please enter a new category name.");
        return;
    }

    const response = await fetch(`/api/service_categories/${encodeURIComponent(oldName)}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ CategoryName: newName })
    });

    if (response.ok) {
        alert("Service category updated successfully!");
        closeModal('updateCategoryModal');
        loadCategoryTable();
    } else {
        const error = await response.json();
        alert(`Failed to update category: ${error.error || error.message}`);
    }
}

// Delete a service category
async function deleteServiceCategory(categoryName) {
    if (!confirm(`Are you sure you want to delete the category "${categoryName}"?`)) return;

    const response = await fetch(`/api/service_categories/${encodeURIComponent(categoryName)}`, {
        method: 'DELETE'
    });

    if (response.ok) {
        alert("Service category deleted successfully!");
        loadCategoryTable();
    } else {
        const error = await response.json();
        alert(`Failed to delete category: ${error.message || error.error}`);
    }
}

// Tab navigation
async function showCategoryTab(tab) {
    if (tab === "view") {
        document.getElementById('content').innerHTML = `
            <h3>Manage Service Categories</h3>
            <input type="text" id="category-search" placeholder="Search by category name" oninput="searchCategories()" />
            <table id="category-table">
                <thead>
                    <tr>
                        <th>Category Name</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        `;
        loadCategoryTable();
    } else if (tab === "create") {
        renderCreateCategoryForm();
    }
}

// Modal close helper for update
function closeCategoryDetail() {
    document.getElementById('modal-category-name').value = '';
    document.getElementById('modal-new-category-name').value = '';
}

// On page load, show the view tab
window.onload = () => {
    showCategoryTab('view');
};


