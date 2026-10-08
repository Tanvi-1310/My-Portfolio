/**
 * Tanvi Patil - Personal Developer Portfolio (Phase 2)
 * Vanilla JavaScript: Theme Management, Mobile Drawer, Active Scroll Spy & Flask Contact API Integration
 */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initMobileNavigation();
    initScrollSpy();
    initContactForm();
    initBackToTop();
});

/* ==========================================================================
   1. THEME MANAGEMENT (Light / Dark Mode with Persistence & Contrast Safeguards)
   ========================================================================== */
function initThemeToggle() {
    const themeToggleBtn = document.getElementById('theme-toggle');
    if (!themeToggleBtn) return;

    // Retrieve initial theme
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    updateThemeButtonAria(themeToggleBtn, currentTheme);

    themeToggleBtn.addEventListener('click', () => {
        const activeTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = activeTheme === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        try {
            localStorage.setItem('tanvi-portfolio-theme', newTheme);
        } catch (e) {
            console.warn('localStorage access denied for theme preference.');
        }

        updateThemeButtonAria(themeToggleBtn, newTheme);
    });
}

function updateThemeButtonAria(button, theme) {
    const nextThemeLabel = theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
    button.setAttribute('aria-label', nextThemeLabel);
    button.setAttribute('title', nextThemeLabel);
}

/* ==========================================================================
   2. MOBILE NAVIGATION DRAWER & ACCESSIBLE TOGGLE
   ========================================================================== */
function initMobileNavigation() {
    const mobileToggle = document.getElementById('mobile-toggle');
    const siteNav = document.getElementById('site-nav');
    const navLinks = document.querySelectorAll('.nav-link');

    if (!mobileToggle || !siteNav) return;

    const toggleMenu = (open) => {
        const isOpen = open !== undefined ? open : !siteNav.classList.contains('is-open');
        siteNav.classList.toggle('is-open', isOpen);
        mobileToggle.setAttribute('aria-expanded', isOpen.toString());

        if (isOpen) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    };

    mobileToggle.addEventListener('click', () => {
        toggleMenu();
    });

    // Close when clicking any navigation link
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (siteNav.classList.contains('is-open')) {
                toggleMenu(false);
            }
        });
    });

    // Close on click outside header
    document.addEventListener('click', (event) => {
        if (siteNav.classList.contains('is-open') &&
            !siteNav.contains(event.target) &&
            !mobileToggle.contains(event.target)) {
            toggleMenu(false);
        }
    });

    // Close on Escape key press
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && siteNav.classList.contains('is-open')) {
            toggleMenu(false);
            mobileToggle.focus();
        }
    });
}

/* ==========================================================================
   3. ACTIVE SECTION SCROLL SPY & SMOOTH NAVIGATION
   ========================================================================== */
function initScrollSpy() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    if (!sections.length || !navLinks.length) return;

    const setActiveLink = (id) => {
        navLinks.forEach(link => {
            if (link.getAttribute('data-nav') === id) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    };

    // Use IntersectionObserver with tuned rootMargin
    const observerOptions = {
        root: null,
        rootMargin: '-25% 0px -65% 0px',
        threshold: 0
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                setActiveLink(entry.target.getAttribute('id'));
            }
        });
    }, observerOptions);

    sections.forEach(section => observer.observe(section));

    // Fallback on direct link clicks
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const targetId = link.getAttribute('data-nav');
            if (targetId) {
                setActiveLink(targetId);
            }
        });
    });
}

/* ==========================================================================
   4. CONTACT FORM VALIDATION & FLASK POST API INTEGRATION
   ========================================================================== */
function initContactForm() {
    const contactForm = document.getElementById('contact-form');
    if (!contactForm) return;

    const nameInput = document.getElementById('contact-name');
    const emailInput = document.getElementById('contact-email');
    const messageInput = document.getElementById('contact-message');
    const submitBtn = document.getElementById('btn-submit-contact');
    const feedbackBanner = document.getElementById('form-feedback');
    const feedbackContent = document.getElementById('feedback-content');

    const nameError = document.getElementById('name-error');
    const emailError = document.getElementById('email-error');
    const messageError = document.getElementById('message-error');

    // Input error clearer
    [nameInput, emailInput, messageInput].forEach(input => {
        if (input) {
            input.addEventListener('input', () => {
                input.closest('.form-group').classList.remove('has-error');
                if (feedbackBanner) feedbackBanner.style.display = 'none';
            });
        }
    });

    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Client-side pre-validation
        let isValid = true;
        document.querySelectorAll('.form-group').forEach(group => group.classList.remove('has-error'));

        const nameVal = nameInput.value.trim();
        const emailVal = emailInput.value.trim();
        const messageVal = messageInput.value.trim();

        // Validate Name
        if (!nameVal || nameVal.length < 2) {
            nameInput.closest('.form-group').classList.add('has-error');
            if (nameError) nameError.textContent = 'Please enter your name (at least 2 characters).';
            isValid = false;
        }

        // Validate Email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailVal || !emailRegex.test(emailVal)) {
            emailInput.closest('.form-group').classList.add('has-error');
            if (emailError) emailError.textContent = 'Please enter a valid email address.';
            isValid = false;
        }

        // Validate Message
        if (!messageVal || messageVal.length < 10) {
            messageInput.closest('.form-group').classList.add('has-error');
            if (messageError) messageError.textContent = 'Please enter a message (at least 10 characters).';
            isValid = false;
        }

        if (!isValid) {
            feedbackBanner.style.display = 'none';
            return;
        }

        // Set Loading State on Button
        setButtonLoading(submitBtn, true);

        try {
            const response = await fetch('/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    name: nameVal,
                    email: emailVal,
                    message: messageVal
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Truthful Success Message
                feedbackBanner.className = 'form-feedback-banner is-success';
                feedbackBanner.style.display = 'block';
                feedbackContent.innerHTML = `<strong>Message Received!</strong><br>${escapeHtml(data.message)}`;
                contactForm.reset();
            } else {
                // Server Validation Errors
                feedbackBanner.className = 'form-feedback-banner is-error';
                feedbackBanner.style.display = 'block';

                if (data.errors) {
                    if (data.errors.name) {
                        nameInput.closest('.form-group').classList.add('has-error');
                        if (nameError) nameError.textContent = data.errors.name;
                    }
                    if (data.errors.email) {
                        emailInput.closest('.form-group').classList.add('has-error');
                        if (emailError) emailError.textContent = data.errors.email;
                    }
                    if (data.errors.message) {
                        messageInput.closest('.form-group').classList.add('has-error');
                        if (messageError) messageError.textContent = data.errors.message;
                    }
                }

                feedbackContent.textContent = data.message || 'There was an error with your submission. Please check your fields.';
            }
        } catch (err) {
            console.error('Contact form transmission error:', err);
            feedbackBanner.className = 'form-feedback-banner is-error';
            feedbackBanner.style.display = 'block';
            feedbackContent.textContent = 'Unable to connect to the server at this time. Please try again or reach out directly on GitHub.';
        } finally {
            setButtonLoading(submitBtn, false);
        }
    });
}

function setButtonLoading(btn, isLoading) {
    if (!btn) return;
    const btnText = btn.querySelector('.btn-text');
    const btnIcon = btn.querySelector('.btn-icon');
    const spinner = btn.querySelector('.btn-spinner');

    if (isLoading) {
        btn.disabled = true;
        if (btnText) btnText.textContent = 'Sending...';
        if (btnIcon) btnIcon.style.display = 'none';
        if (spinner) spinner.style.display = 'inline-block';
    } else {
        btn.disabled = false;
        if (btnText) btnText.textContent = 'Send Message';
        if (btnIcon) btnIcon.style.display = 'inline-block';
        if (spinner) spinner.style.display = 'none';
    }
}

function escapeHtml(string) {
    const div = document.createElement('div');
    div.textContent = string;
    return div.innerHTML;
}

/* ==========================================================================
   5. BACK TO TOP BUTTON
   ========================================================================== */
function initBackToTop() {
    const backToTopBtn = document.getElementById('back-to-top');
    if (!backToTopBtn) return;

    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}
