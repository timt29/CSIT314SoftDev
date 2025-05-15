function logout() {
    window.location.href = "/logout";  // Redirect to the logout route
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

async function loadUserTable(searchQuery = "") {
    const response = await fetch(`/users?search=${encodeURIComponent(searchQuery)}`);
    const users = await response.json();

    let rows = "";

    users.forEach(user => {
        const formattedDoB = new Date(user.DoB).toLocaleDateString();
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

    // Show "No users found" if empty
    if (users.length === 0) {
        rows = `<tr><td colspan="6">No users found.</td></tr>`;
    }

    const tableBody = document.querySelector("#user-table tbody");
    if (tableBody) {
        tableBody.innerHTML = rows;
    }
}

// Search profiles by role or description
function searchProfiles() {
    const searchQuery = document.getElementById("profile-search").value;
    loadProfileTable(searchQuery);
}

// Load and render the user profiles table, with Update and Delete buttons
async function loadProfileTable(searchQuery = "") {
    const response = await fetch(`/api/user_profiles${searchQuery ? '?search=' + encodeURIComponent(searchQuery) : ''}`);
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

// Delete a user profile by role
async function deleteUserProfile(role) {
    if (!confirm(`Are you sure you want to delete the role "${role}"?`)) return;

    const response = await fetch(`/api/user_profiles/${encodeURIComponent(role)}`, {
        method: 'DELETE'
    });

    if (response.ok) {
        alert("User profile deleted successfully!");
        loadProfileTable();
    } else {
        const error = await response.json();
        alert(`Failed to delete user profile: ${error.message || error.error}`);
    }
}

function searchUsers() {
    const searchQuery = document.getElementById("user-search").value;
    loadUserTable(searchQuery);
}

async function viewUserDetails(email) {
    try {
        const response = await fetch('/api/users');
        const users = await response.json();
        const user = users.find(u => u.Email === email);

        if (!user) {
            alert("User not found!");
            return;
        }

        const formattedDoB = new Date(user.DoB).toLocaleDateString();

        // Populate the modal with user details
        document.getElementById('view-user-details').innerHTML = `
            <p><strong>Email:</strong> ${user.Email}</p>
            <p><strong>Name:</strong> ${user.Name}</p>
            <p><strong>Role:</strong> ${user.Role}</p>
            <p><strong>Date of Birth:</strong> ${formattedDoB}</p>
            <p><strong>Status:</strong> ${user.Status}</p>
        `;

        // Show the modal
        document.getElementById('viewUserModal').style.display = 'block';
    } catch (error) {
        console.error("Error in viewUserDetails:", error);
        alert("Failed to load user details.");
    }
}

function closeUserDetail() {
    document.getElementById('view-user-details').innerHTML = '';
}

async function createUser(event) {
    event.preventDefault();

    const name = document.getElementById("create-name").value;
    const email = document.getElementById("create-email").value;
    const password = document.getElementById("create-password").value;
    const role = document.getElementById("create-role").value;
    const dob = document.getElementById("create-dob").value;
    const status = "Active"; // Default status 

    const payload = { name, email, password, role, dob, status };
    console.log("Payload being sent:", payload); // Log the payload

    try {
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (response.ok) {
            alert("User created successfully!");
            document.getElementById("create-user-form").reset(); // Reset the form
            showTab('view'); // Switch to the View Users tab
        } else {
            const error = await response.json();
            alert(`Failed to create user: ${error.message}`);
        }
    } catch (error) {
        console.error("Error in createUser:", error);
        alert("Failed to create user.");
    }
}

async function showUpdateForm(email) {
    // Fetch all users and find the one to update
    const response = await fetch('/api/users');
    const users = await response.json();
    const user = users.find(u => u.Email === email);

    if (!user) {
        alert("User not found.");
        return;
    }

    // Set modal fields
    document.getElementById('modal-email').value = user.Email;
    document.getElementById('modal-new-email').value = user.Email;
    document.getElementById('modal-name').value = user.Name;

    // Fetch available roles from the backend
    const profilesResponse = await fetch('/api/user_profiles');
    const profiles = await profilesResponse.json();

    // Populate the roles dropdown
    const roleSelect = document.getElementById('update-role');
    roleSelect.innerHTML = '';
    profiles.forEach(profile => {
        const option = document.createElement('option');
        option.value = profile.Role;
        option.text = profile.Role;
        if (profile.Role === user.Role) option.selected = true;
        roleSelect.appendChild(option);
    });

    // Set default values for comparison in updateUser()
    document.getElementById('modal-name').defaultValue = user.Name;
    roleSelect.defaultValue = user.Role;

    // Show the modal
    document.getElementById('updateUserModal').style.display = 'block';
}

async function updateUser() {
    const currentEmail = document.getElementById('modal-email').value;
    const newEmail = document.getElementById('modal-new-email').value;
    const name = document.getElementById('modal-name').value;
    const role = document.getElementById('update-role').value;

    // Build payload only with changed fields
    const payload = {};
    if (newEmail && newEmail !== currentEmail) payload.new_email = newEmail;
    if (name && name !== document.getElementById('modal-name').defaultValue) payload.name = name;
    if (role && role !== document.getElementById('update-role').defaultValue) payload.role = role;

    if (Object.keys(payload).length === 0) {
        alert("No changes to update.");
        return;
    }

    try {
        const response = await fetch(`/api/users/${encodeURIComponent(currentEmail)}`, {
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
            alert(`Failed to update user: ${error.error || error.message}`);
        }
    } catch (error) {
        alert("Failed to update user.");
        console.error(error);
    }
}

function showUpdateProfileForm(role, description) {
    document.getElementById('modal-role').value = role;
    document.getElementById('modal-description').value = description;
    document.getElementById('updateProfileModal').style.display = 'block';
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
        alert(`Failed to update user profile: ${error.error || error.message}`);
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
        const error = await response.json();
        alert(`Failed to create profile: ${error.message || error.error}`);
    }
}

function renderCreateProfileForm() {
    document.getElementById('content').innerHTML = `
        <h3>Create User Profile</h3>
        <form id="create-profile-form">
            <div class="form-group">
                <label for="create-role-name">Role:</label>
                <input id="create-role-name" type="text" placeholder="Enter Role Name" required>
            </div>
            <div class="form-group">
                <label for="create-role-description">Description:</label>
                <input id="create-role-description" type="text" placeholder="Enter Description" required>
            </div>
            <button type="button" onclick="createUserProfile()">Create Profile</button>
        </form>
    `;
}

async function showTab(tab) {
    
      const response = await fetch('/api/user_profiles');
    const profiles = await response.json();

    let roleOptions = '';
    profiles.forEach(profile => {
        roleOptions += `<option value="${profile.Role}">${profile.Role}</option>`;
    });

    if (tab === "view") {
        document.getElementById('content').innerHTML = `
            <h3>Manage Users</h3>
            <input type="text" id="user-search" placeholder="Search by name or email" oninput="searchUsers()" />
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
                <tbody></tbody>
            </table>
        `;
        loadUserTable();
    } else if (tab === "create") {
        document.getElementById('content').innerHTML = `
            <h3>Create User</h3>
            <form id="create-user-form" onsubmit="createUser(event)">
                <label for="create-name">Name:</label>
                <input type="text" id="create-name" required />

                <label for="create-email">Email:</label>
                <input type="email" id="create-email" required />

                <label for="create-password">Password:</label>
                <input type="password" id="create-password" required />

                <label for="create-role">Role:</label>
                <select id="create-role" required>
                    ${roleOptions}
                </select>

                <label for="create-dob">Date of Birth:</label>
                <input type="date" id="create-dob" required />

                <button type="submit">Create User</button>
            </form>
        `;
    } else if (tab === "viewProfiles") {
        document.getElementById('content').innerHTML = `
            <h3>View User Profiles</h3>
            <input type="text" id="profile-search" placeholder="Search by role or description" oninput="searchProfiles()" />
            <table id="profile-table">
                <thead>
                    <tr>
                        <th>Role</th>
                        <th>Description</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        `;
        loadProfileTable();
    } else if (tab === "createProfile") {
        renderCreateProfileForm();
    }
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


window.onload = () => {
    showTab('view');
};