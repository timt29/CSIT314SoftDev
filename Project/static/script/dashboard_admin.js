function logout() {
    window.location.href = "/logout";  // Redirect to the logout route
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

async function loadUserTable(searchQuery = "") {
    const response = await fetch(`/api/users?search=${encodeURIComponent(searchQuery)}`);
    const users = await response.json();

    let rows = "";

    users.forEach(user => {
        const formattedDoB = new Date(user.DoB).toLocaleDateString(); // Format the date
        rows += `
            <tr>
                <td><a href="#" onclick="viewUserDetails('${user.Email}')">${user.Email}</a></td>
                <td>${user.Name}</td>
                <td>${user.Role}</td>
                <td>${formattedDoB}</td>
                <td>${user.Status}</td>
                <td>
                    <button class="action-button" onclick="showUpdateForm('${user.Email}')">Update</button>
                    <button class="suspend-button" onclick="suspendUser('${user.Email}')">Suspend</button>
                </td>
            </tr>`;
    });

    const tableBody = document.querySelector("#user-table tbody");
    if (tableBody) {
        tableBody.innerHTML = rows;
    } else {
        document.getElementById('content').innerHTML = `
            <h3>Manage Users</h3>
            <input type="text" id="user-search" placeholder="Search by name or email" value="${searchQuery}" oninput="searchUsers()" />
            <table id="user-table">
                <thead>
                    <tr>
                        <th>Email</th>
                        <th>Name</th>
                        <th>Role</th>
                        <th>Date of Birth</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${rows}
                </tbody>
            </table>
        `;
    }
}

function searchUsers() {
    const searchQuery = document.getElementById("user-search").value;
    loadUserTable(searchQuery);
}

async function viewUserDetails(email) {
    const response = await fetch('/api/users');
    const users = await response.json();
    const user = users.find(u => u.Email === email);

    document.getElementById('update-user-form').innerHTML = '';

    const formattedDoB = new Date(user.DoB).toLocaleDateString();

    document.getElementById('user-detail').innerHTML = `
        <h3>User Details</h3>
        <p><strong>Email:</strong> ${user.Email}</p>
        <p><strong>Name:</strong> ${user.Name}</p>
        <p><strong>Role:</strong> ${user.Role}</p>
        <p><strong>Date of Birth:</strong> ${formattedDoB}</p>
        <p><strong>Status:</strong> ${user.Status}</p>
        <button onclick="closeUserDetail()">Close</button>
    `;
}

function closeUserDetail() {
    document.getElementById('user-detail').innerHTML = '';
}

async function suspendUser(email) {
    const response = await fetch(`/api/users/${email}/suspend`, { method: 'PATCH' });

    if (response.ok) {
        alert("User suspended successfully!");
        loadUserTable();
    } else {
        const error = await response.json();
        alert(`Failed to suspend user: ${error.message}`);
    }
}

async function showUpdateForm(email) {
    try {
        const response = await fetch('/api/users');
        const users = await response.json();
        const user = users.find(u => u.Email === email);

        if (!user) {
            alert("User not found!");
            return;
        }

        const rolesResponse = await fetch('/api/user_profiles');
        const profiles = await rolesResponse.json();

        const roleOptions = profiles.map(profile => `
            <option value="${profile.Role}" ${profile.Role === user.Role ? 'selected' : ''}>
                ${profile.Role}
            </option>
        `).join('');

        document.getElementById('modal-email').value = user.Email;
        document.getElementById('modal-new-email').value = user.Email;
        document.getElementById('modal-new-email').defaultValue = user.Email;
        document.getElementById('modal-name').value = user.Name;
        document.getElementById('modal-name').defaultValue = user.Name;
        document.getElementById('update-role').innerHTML = roleOptions;
        document.getElementById('update-role').defaultValue = user.Role;

        document.getElementById('updateUserModal').style.display = 'block';
    } catch (error) {
        console.error("Error in showUpdateForm:", error);
        alert("Failed to load user details or roles.");
    }
}

async function updateUser() {
    const currentEmail = document.getElementById('modal-email').value;
    const newEmail = document.getElementById('modal-new-email').value;
    const name = document.getElementById('modal-name').value;
    const role = document.getElementById('update-role').value;

    const payload = {};
    if (newEmail !== currentEmail) payload.new_email = newEmail;
    if (name !== document.getElementById('modal-name').defaultValue) payload.name = name;
    if (role !== document.getElementById('update-role').defaultValue) payload.role = role;

    if (Object.keys(payload).length === 0) {
        alert("No changes to update.");
        return;
    }

    const response = await fetch(`/api/users/${currentEmail}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        alert("User updated successfully!");
        closeModal('updateUserModal');
        loadUserTable();
    } else {
        const error = await response.json();
        alert(`Failed to update user: ${error.error}`);
    }
}

async function createUser() {
    const email = document.getElementById("create-email").value;
    const name = document.getElementById("create-name").value;
    const password = document.getElementById("create-password").value;
    const role = document.getElementById("create-role").value;
    const dob = document.getElementById("create-dob").value;

    const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, name, password, role, dob })
    });

    if (response.ok) {
        alert("User created successfully!");
        showTab('view');
    } else {
        const error = await response.json();
        alert(`Failed to create user: ${error.message}`);
    }
}

async function createUserProfile() {
    const role = document.getElementById("create-role-name").value;
    const description = document.getElementById("create-role-description").value;

    const response = await fetch('/api/user_profiles', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role, description })
    });

    if (response.ok) {
        alert("User profile created!");
        showTab('viewProfiles');
    } else {
        alert("Failed to create profile.");
    }
}

async function loadProfileTable(searchQuery = "") {
    const response = await fetch(`/api/profiles?search=${encodeURIComponent(searchQuery)}`);
    const profiles = await response.json();

    let rows = "";

    profiles.forEach(profile => {
        rows += `
            <tr>
                <td>${profile.Role}</td>
                <td>${profile.Description}</td>
                <td>
                    <button class="action-button" onclick="showUpdateProfileForm('${profile.Role}', '${profile.Description}')">Update</button>
                    <button class="suspend-button" onclick="deleteUserProfile('${profile.Role}')">Delete</button>
                </td>
            </tr>`;
    });

    const tableBody = document.querySelector("#profile-table tbody");
    if (tableBody) {
        tableBody.innerHTML = rows;
    } else {
        document.getElementById('content').innerHTML = `
            <h3>User Profiles</h3>
            <input type="text" id="profile-search" placeholder="Search by role or description" value="${searchQuery}" oninput="searchProfiles()" />
            <table id="profile-table">
                <thead>
                    <tr>
                        <th>Role</th>
                        <th>Description</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${rows}
                </tbody>
            </table>
        `;
    }
}

function searchProfiles() {
    const searchQuery = document.getElementById("profile-search").value;
    loadProfileTable(searchQuery);
}

function renderCreateProfileForm() {
    document.getElementById('content').innerHTML = `
        <h3>Create User Profile</h3>
        <form id="create-profile-form">
            <div class="form-group">
                <label>Role:</label>
                <input id="create-role-name" type="text" placeholder="Enter Role Name" required>
            </div>
            <div class="form-group">
                <label>Description:</label>
                <input id="create-role-description" type="text" placeholder="Enter Description" required>
            </div>
            <button type="button" onclick="createUserProfile()">Create Profile</button>
        </form>
    `;
}

async function renderCreateUserForm() {
    const response = await fetch('/api/user_profiles');
    const profiles = await response.json();

    const roleOptions = profiles.map(profile => `<option value="${profile.Role}">${profile.Role}</option>`).join('');

    document.getElementById('content').innerHTML = `
        <h3>Create New User</h3>
        <form id="create-form">
            <div class="form-group">
                <label>Email:</label>
                <input id="create-email" type="email" placeholder="Enter Email" required>
            </div>
            <div class="form-group">
                <label>Password:</label>
                <input id="create-password" type="password" placeholder="Enter Password" required>
            </div>
            <div class="form-group">
                <label>Name:</label>
                <input id="create-name" type="text" placeholder="Enter Name" required>
            </div>
            <div class="form-group">
                <label>Role:</label>
                <select id="create-role" required>
                    ${roleOptions}
                </select>
            </div>
            <div class="form-group">
                <label>Date of Birth:</label>
                <input id="create-dob" type="date" required>
            </div>
            <button type="button" onclick="createUser()">Create User</button>
        </form>
    `;
}

function showUpdateProfileForm(role, description) {
    document.getElementById('modal-role').value = role;
    document.getElementById('modal-description').value = description;
    document.getElementById('updateProfileModal').style.display = 'block';
}

function closeUpdateProfileForm() {
    document.getElementById('update-user-form').innerHTML = '';
}

async function updateUserProfile() {
    const role = document.getElementById('modal-role').value;
    const description = document.getElementById('modal-description').value;

    const response = await fetch(`/api/user_profiles/${role}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description })
    });

    if (response.ok) {
        alert("User profile updated successfully!");
        closeModal('updateProfileModal');
        loadProfileTable();
    } else {
        const error = await response.json();
        alert(`Failed to update user profile: ${error.error}`);
    }
}

async function deleteUserProfile(role) {
    if (!confirm(`Are you sure you want to delete the role "${role}"?`)) return;

    const response = await fetch(`/api/user_profiles/${role}`, { method: 'DELETE' });

    if (response.ok) {
        alert("User profile deleted successfully!");
        loadProfileTable();
    } else {
        const error = await response.json();
        alert(`Failed to delete user profile: ${error.message}`);
    }
}

async function showTab(tab) {
    document.getElementById('user-detail').innerHTML = '';
    document.getElementById('update-user-form').innerHTML = '';

    if (tab === "create") {
        await renderCreateUserForm();
    } else if (tab === "view") {
        loadUserTable();
    } else if (tab === "createProfile") {
        renderCreateProfileForm();
    } else if (tab === "viewProfiles") {
        loadProfileTable();
    }
}

window.onload = () => {
    showTab('view');
};