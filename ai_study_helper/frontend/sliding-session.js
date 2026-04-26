// Sliding Session Logic
(function() {
    // Only run if user is logged in (has an access token)
    if (!localStorage.getItem('access_token')) return;

    const IDLE_TIMEOUT_MS = 30 * 60 * 1000; // 30 minutes
    const WARNING_TIME_MS = 28 * 60 * 1000; // 28 minutes
    let warningElement = null;

    function updateActivity() {
        // Prevent unnecessary writes to localStorage on every mousemove
        const now = Date.now();
        const lastActivityStr = localStorage.getItem('last_activity');
        if (lastActivityStr && now - parseInt(lastActivityStr, 10) < 1000) {
            return; // Throttle to max 1 write per second
        }
        localStorage.setItem('last_activity', now.toString());
        hideWarning();
    }

    function checkIdleTime() {
        if (!localStorage.getItem('access_token')) return; // logged out

        const lastActivityStr = localStorage.getItem('last_activity');
        if (!lastActivityStr) {
            updateActivity();
            return;
        }

        const lastActivity = parseInt(lastActivityStr, 10);
        const idleTime = Date.now() - lastActivity;

        if (idleTime >= IDLE_TIMEOUT_MS) {
            // Logout
            localStorage.clear();
            window.location.href = 'login.html';
        } else if (idleTime >= WARNING_TIME_MS) {
            showWarning();
        }
    }

    function showWarning() {
        if (warningElement) return; // already showing

        warningElement = document.createElement('div');
        warningElement.className = 'fixed bottom-4 right-4 z-50 bg-yellow-500 text-white px-6 py-4 rounded-lg shadow-xl flex items-center gap-4 transform transition-all duration-300';
        warningElement.innerHTML = `
            <div>
                <p class="font-bold">Session Expiring Soon</p>
                <p class="text-sm">You'll be logged out in 2 minutes due to inactivity.</p>
            </div>
            <button id="stayLoggedInBtn" class="bg-white text-yellow-600 px-4 py-2 rounded-md font-bold hover:bg-yellow-50 transition-colors shadow-sm">
                Stay Logged In
            </button>
        `;
        document.body.appendChild(warningElement);

        document.getElementById('stayLoggedInBtn').addEventListener('click', (e) => {
            e.stopPropagation(); // don't trigger document click
            updateActivity();
        });
    }

    function hideWarning() {
        if (warningElement) {
            warningElement.remove();
            warningElement = null;
        }
    }

    // Initialize last activity
    if (!localStorage.getItem('last_activity')) {
        updateActivity();
    }

    // Track activity events (using passive to not block scrolling)
    const events = ['click', 'keypress', 'scroll', 'mousemove', 'touchstart'];
    events.forEach(event => {
        document.addEventListener(event, updateActivity, { passive: true });
    });

    // Check idle time every 60 seconds
    setInterval(checkIdleTime, 60 * 1000);
    
    // Initial check just in case they loaded the page after 30 mins of background idle
    checkIdleTime();
})();
