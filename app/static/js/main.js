// Toast Notification Utility
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.innerText = message;
    toast.style.backgroundColor = type === 'success' ? '#26a69a' : '#d32f2f';
    toast.style.display = 'block';
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

// Authentication Logic
const authBtn = document.getElementById('nav-auth-btn');

function updateAuthUI() {
    const user = JSON.parse(localStorage.getItem('user'));
    const dashLink = document.getElementById('dashboard-link');
    const portLink = document.getElementById('portfolio-nav-link');

    if (user) {
        authBtn.innerText = 'Logout';
        authBtn.onclick = logout;
        if (dashLink) {
            dashLink.style.display = 'block';
            const dashUrl = user.role === 'student' ? '/student/dashboard' : '/admin/dashboard';
            dashLink.querySelector('a').href = dashUrl;
        }
        if (portLink) {
            portLink.style.display = user.role === 'student' ? 'block' : 'none';
        }
    } else {
        authBtn.innerText = 'Login';
        authBtn.onclick = () => window.location.href = '/login';
        if (dashLink) dashLink.style.display = 'none';
        if (portLink) portLink.style.display = 'block'; // Show by default when not logged in (redirects to login anyway)
    }
}

async function login(e) {
    if (e) e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    const res = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    // Auth UI state is handled inside the login function via data.redirect

    const data = await res.json();
    if (res.ok) {
        localStorage.setItem('user', JSON.stringify({ email, role: data.role }));
        showToast(data.message || 'Login successful!');
        if (data.redirect) {
            setTimeout(() => window.location.href = data.redirect, 1000);
        } else {
            const redirectUrl = data.role === 'student' ? '/student/dashboard' : '/admin/dashboard';
            setTimeout(() => window.location.href = redirectUrl, 1000);
        }
    } else {
        showToast(data.error, 'error');
    }
}

async function changePassword(e) {
    if (e) e.preventDefault();
    const new_password = document.getElementById('new-password').value;
    const confirm_password = document.getElementById('confirm-password').value;

    if (new_password !== confirm_password) {
        showToast('Passwords do not match', 'error');
        return;
    }

    const res = await fetch('/change-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_password })
    });

    const data = await res.json();
    if (res.ok) {
        showToast('Password changed successfully!');
        const user = JSON.parse(localStorage.getItem('user'));
        const redirectUrl = user && user.role === 'admin' ? '/admin/dashboard' : '/student/dashboard';
        setTimeout(() => window.location.href = redirectUrl, 1000);
    } else {
        showToast(data.error, 'error');
    }
}

async function signup(e) {
    if (e) e.preventDefault();
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const role = document.getElementById('signup-role').value;

    const res = await fetch('/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, role })
    });

    const data = await res.json();
    if (res.ok) {
        showToast('Signup successful! Please login.');
        setTimeout(() => window.location.reload(), 1500);
    } else {
        showToast(data.error, 'error');
    }
}

async function signup(e) {
    e.preventDefault();
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;

    const res = await fetch('/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, role: 'admin' })
    });

    const data = await res.json();
    if (res.ok) {
        showToast(data.message, 'success');
        setTimeout(() => window.location.reload(), 2000);
    } else {
        showToast(data.error, 'error');
    }
}

async function logout() {
    const res = await fetch('/logout', { method: 'POST' });
    if (res.ok) {
        localStorage.removeItem('user');
        showToast('Logged out');
        setTimeout(() => window.location.href = '/', 1000);
    }
}

// Job Logic
let currentJobs = [];

async function loadJobs() {
    const res = await fetch('/jobs');
    const data = await res.json();
    currentJobs = data.jobs;
    const jobList = document.getElementById('job-list');
    const user = JSON.parse(localStorage.getItem('user'));
    const isStudent = user && user.role === 'student';

    if (data.jobs.length === 0) {
        jobList.innerHTML = '<p>No jobs posted yet.</p>';
        return;
    }

    jobList.innerHTML = data.jobs.map(job => `
        <div class="job-card" style="cursor: pointer;" onclick="viewJobDetails(${job.id})">
            <div style="flex-grow: 1;">
                <div class="meta">
                    <span class="badge">Job ID: #${job.id}</span>
                    <span>${new Date(job.deadline).toLocaleDateString()}</span>
                </div>
                <h3>${job.title}</h3>
                <p style="color: var(--secondary-teal); font-weight: 700; margin-bottom: 10px;">${job.company}</p>
                <p style="color: #666; font-size: 14px; margin-bottom: 15px;">${job.description.substring(0, 100)}...</p>
                <p style="font-size: 13px; font-weight: 600;">Min CGPA Requirement: <span style="color: var(--primary-blue);">${job.min_cgpa}</span></p>
            </div>
            ${isStudent ? `
                <button class="btn btn-primary" onclick="event.stopPropagation(); applyJob(${job.id})" style="margin-top: 20px; width: 100%;">Apply Now</button>
            ` : `
                <button class="btn btn-secondary" style="margin-top: 20px; width: 100%; pointer-events: none; opacity: 0.7;">View Details</button>
            `}
        </div>
    `).join('');
}

function viewJobDetails(jobId) {
    const job = currentJobs.find(j => j.id === jobId);
    if (!job) return;

    const user = JSON.parse(localStorage.getItem('user'));
    const isStudent = user && user.role === 'student';

    const content = `
        <div class="meta" style="margin-bottom: 20px;">
            <span class="badge">Job ID: #${job.id}</span>
            <span>Deadline: ${new Date(job.deadline).toLocaleDateString()}</span>
        </div>
        <h2 style="color: var(--text-dark); margin-bottom: 5px;">${job.title}</h2>
        <h4 style="color: var(--secondary-teal); margin-bottom: 30px;">${job.company}</h4>
        
        <div style="margin-bottom: 30px;">
            <h5 style="text-transform: uppercase; font-size: 12px; letter-spacing: 1px; color: #999; margin-bottom: 10px;">Job Description</h5>
            <p style="line-height: 1.6; color: #444; white-space: pre-wrap;">${job.description}</p>
        </div>

        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
            <p style="margin: 0; font-weight: 600;">Minimum eligibility: <span style="color: var(--primary-blue); font-size: 18px;">${job.min_cgpa} CGPA</span></p>
        </div>

        ${isStudent ? `
            <button class="btn btn-primary" onclick="applyJob(${job.id})" style="width: 100%;">Apply for this Position</button>
        ` : ''}
    `;

    document.getElementById('job-details-content').innerHTML = content;
    document.getElementById('job-details-modal').style.display = 'flex';
}

async function postJob(e) {
    e.preventDefault();
    const title = document.getElementById('job-title').value;
    const company = document.getElementById('job-company').value;
    const description = document.getElementById('job-desc').value;
    const min_cgpa = document.getElementById('job-cgpa').value;
    const deadline = document.getElementById('job-deadline').value;

    const res = await fetch('/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, company, description, min_cgpa, deadline })
    });

    const data = await res.json();
    if (res.ok) {
        showToast('Job posted!');
        loadJobs();
        document.getElementById('add-job-form').reset();
    } else {
        showToast(data.error, 'error');
    }
}

async function applyJob(jobId) {
    const res = await fetch(`/apply/${jobId}`, { method: 'POST' });
    const data = await res.json();
    if (res.ok) {
        showToast('Application submitted!');
    } else {
        showToast(data.error, 'error');
    }
}

// Portfolio Logic
async function loadPortfolio() {
    const res = await fetch('/portfolio');
    if (res.ok) {
        const data = await res.json();
        document.getElementById('p-name').value = data.full_name || '';
        document.getElementById('p-dept').value = data.department || '';
        document.getElementById('p-cgpa').value = data.cgpa || '';
        document.getElementById('p-year').value = data.passing_year || '';
        document.getElementById('p-skills').value = data.skills || '';
        document.getElementById('p-resume').value = data.resume_link || '';
    }
}

async function updatePortfolio(e) {
    e.preventDefault();
    const payload = {
        full_name: document.getElementById('p-name').value,
        department: document.getElementById('p-dept').value,
        cgpa: parseFloat(document.getElementById('p-cgpa').value),
        passing_year: document.getElementById('p-year').value,
        skills: document.getElementById('p-skills').value,
        resume_link: document.getElementById('p-resume').value
    };

    const res = await fetch('/portfolio', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    if (res.ok) {
        showToast('Portfolio updated!');
    } else {
        const data = await res.json();
        showToast(data.error || 'Error updating portfolio', 'error');
    }
}

// Initializations
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();

    const loginForm = document.getElementById('login-form');
    if (loginForm) loginForm.onsubmit = login;

    const signupForm = document.getElementById('signup-form');
    if (signupForm) signupForm.onsubmit = signup;

    const addJobForm = document.getElementById('add-job-form');
    if (addJobForm) addJobForm.onsubmit = postJob;

    const portfolioForm = document.getElementById('portfolio-form');
    if (portfolioForm) portfolioForm.onsubmit = updatePortfolio;

    const changePasswordForm = document.getElementById('change-password-form');
    if (changePasswordForm) changePasswordForm.onsubmit = changePassword;

    // Login/Signup Toggles
    const showSignup = document.getElementById('show-signup');
    const showLogin = document.getElementById('show-login');
    if (showSignup && showLogin) {
        showSignup.onclick = (e) => {
            e.preventDefault();
            document.getElementById('login-form-content').style.display = 'none';
            document.getElementById('signup-form-content').style.display = 'block';
        };
        showLogin.onclick = (e) => {
            e.preventDefault();
            document.getElementById('login-form-content').style.display = 'block';
            document.getElementById('signup-form-content').style.display = 'none';
        };
    }
});
