// DOM Elements
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
const navbar = document.querySelector('.navbar');
const contactForm = document.getElementById('contactForm');
const alertContainer = document.createElement('div');
alertContainer.className = 'alert-container';
document.body.appendChild(alertContainer);

// Mobile Navigation Toggle
if (navToggle) {
    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        navToggle.classList.toggle('active');
    });
}

// Close mobile menu when clicking on a nav link
const navItems = document.querySelectorAll('.nav-links a');
navItems.forEach(link => {
    link.addEventListener('click', () => {
        if (navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            navToggle.classList.remove('active');
        }
    });
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80, // Account for fixed header
                behavior: 'smooth'
            });
        }
    });
});

// Set active navigation link based on current section
const sections = document.querySelectorAll('section[id]');
window.addEventListener('scroll', () => {
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        const sectionHeight = section.offsetHeight;
        
        if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
            current = section.getAttribute('id');
        }
    });
    
    navItems.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// Contact Form Validation and Submission
if (contactForm) {
    // Form elements
    const formElements = {
        name: contactForm.querySelector('#name'),
        email: contactForm.querySelector('#email'),
        phone: contactForm.querySelector('#phone'),
        subject: contactForm.querySelector('#subject'),
        message: contactForm.querySelector('#message'),
        privacy: contactForm.querySelector('#privacy'),
        submitBtn: contactForm.querySelector('#submitBtn')
    };

    // Error messages
    const errorMessages = {
        required: 'This field is required',
        email: 'Please enter a valid email address',
        minLength: (min) => `Please enter at least ${min} characters`,
        maxLength: (max) => `Maximum ${max} characters allowed`,
        pattern: 'Please match the requested format',
        privacy: 'You must accept the privacy policy'
    };

    // Validation functions
    const validators = {
        name: (value) => {
            if (!value.trim()) return errorMessages.required;
            if (value.length < 2) return errorMessages.minLength(2);
            if (value.length > 100) return errorMessages.maxLength(100);
            return '';
        },
        email: (value) => {
            if (!value.trim()) return errorMessages.required;
            if (!isValidEmail(value)) return errorMessages.email;
            return '';
        },
        phone: (value) => {
            if (!value.trim()) return ''; // Optional field
            const phoneRegex = /^[0-9\-\+\(\)\s]*$/;
            if (!phoneRegex.test(value)) return errorMessages.pattern;
            return '';
        },
        message: (value) => {
            if (!value.trim()) return errorMessages.required;
            if (value.length < 10) return errorMessages.minLength(10);
            if (value.length > 1000) return errorMessages.maxLength(1000);
            return '';
        },
        privacy: (checked) => {
            if (!checked) return errorMessages.privacy;
            return '';
        }
    };

    // Show error message for a field
    function showError(field, message) {
        if (!field) return;
        
        const errorElement = document.getElementById(`${field.id}-error`);
        if (errorElement) {
            errorElement.textContent = message || '';
            errorElement.style.display = message ? 'block' : 'none';
            field.classList.toggle('error', !!message);
            field.setAttribute('aria-invalid', !!message);
        }
    }

    // Validate a single field
    function validateField(field) {
        if (!field) return true;
        
        const fieldName = field.name || field.id;
        if (!fieldName || !(fieldName in validators)) return true;
        
        const value = field.type === 'checkbox' ? field.checked : field.value;
        const error = validators[fieldName](value);
        
        showError(field, error);
        return !error;
    }

    // Validate entire form
    function validateForm() {
        let isValid = true;
        
        Object.values(formElements).forEach(field => {
            if (field && field !== formElements.submitBtn) {
                if (!validateField(field)) {
                    isValid = false;
                }
            }
        });
        
        return isValid;
    }

    // Handle form submission
    async function handleSubmit(e) {
        e.preventDefault();
        
        // Reset previous errors
        contactForm.querySelectorAll('.error-message').forEach(el => {
            el.textContent = '';
            el.style.display = 'none';
        });
        
        // Validate form
        if (!validateForm()) {
            showAlert('Please correct the errors in the form', 'error');
            // Focus on first error
            const firstError = contactForm.querySelector('.error');
            if (firstError) firstError.focus();
            return;
        }
        
        // Prepare form data
        const formData = new FormData(contactForm);
        const submitBtn = formElements.submitBtn;
        const btnText = submitBtn?.querySelector('.btn-text');
        const spinner = submitBtn?.querySelector('.spinner');
        
        // Show loading state
        if (submitBtn) submitBtn.disabled = true;
        if (btnText) btnText.textContent = 'Sending...';
        if (spinner) spinner.style.display = 'inline-block';
        
        try {
            // Simulate API call (replace with actual fetch)
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            // Show success message
            showAlert('Thank you for your message! We will get back to you soon.', 'success');
            
            // Reset form
            contactForm.reset();
            
        } catch (error) {
            console.error('Form submission error:', error);
            showAlert('There was an error sending your message. Please try again later.', 'error');
        } finally {
            // Reset button state
            if (submitBtn) submitBtn.disabled = false;
            if (btnText) btnText.textContent = 'Send Message';
            if (spinner) spinner.style.display = 'none';
        }
    }

    // Event listeners for real-time validation
    Object.values(formElements).forEach(field => {
        if (!field || field === formElements.submitBtn) return;
        
        // Input/change events for real-time validation
        const eventType = field.type === 'checkbox' ? 'change' : 'input';
        field.addEventListener(eventType, () => validateField(field));
        
        // Blur for final validation
        field.addEventListener('blur', () => validateField(field));
    });
    
    // Form reset handler
    contactForm.addEventListener('reset', () => {
        // Clear all error messages
        contactForm.querySelectorAll('.error-message').forEach(el => {
            el.textContent = '';
            el.style.display = 'none';
        });
        
        // Remove error classes
        contactForm.querySelectorAll('.error').forEach(el => {
            el.classList.remove('error');
            el.removeAttribute('aria-invalid');
        });
    });
    
    // Form submission
    contactForm.addEventListener('submit', handleSubmit);
}

// Email validation helper
function isValidEmail(email) {
    if (!email) return false;
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email.trim());
}

// Show alert message
function showAlert(message, type = 'info') {
    // Remove any existing alerts to prevent stacking
    const existingAlerts = document.querySelectorAll('.alert.show');
    existingAlerts.forEach(alert => {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 300);
    });
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.setAttribute('role', 'alert');
    
    // Add appropriate icon based on alert type
    let icon = 'ℹ️';
    if (type === 'success') icon = '✓';
    if (type === 'error') icon = '✗';
    if (type === 'warning') icon = '⚠️';
    
    alert.innerHTML = `
        <div class="alert-content">
            <span class="alert-icon">${icon}</span>
            <span class="alert-message">${message}</span>
            <button class="close-alert" aria-label="Close alert">&times;</button>
        </div>
    `;
    
    // Add to container
    alertContainer.appendChild(alert);
    
    // Trigger reflow to enable CSS transition
    void alert.offsetWidth;
    
    // Show the alert with animation
    alert.classList.add('show');
    
    // Auto-remove after delay
    const removeAlert = () => {
        if (alert) {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 300);
        }
    };
    
    // Close button
    const closeBtn = alert.querySelector('.close-alert');
    closeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        removeAlert();
    });
    
    // Auto-remove after delay (longer for success messages)
    const delay = type === 'success' ? 8000 : 5000;
    const timeoutId = setTimeout(removeAlert, delay);
    
    // Pause auto-remove on hover
    alert.addEventListener('mouseenter', () => {
        clearTimeout(timeoutId);
    });
    
    alert.addEventListener('mouseleave', () => {
        setTimeout(removeAlert, 2000);
    });
    
    // Make alert focusable and handle keyboard
    alert.setAttribute('tabindex', '-1');
    alert.focus();
    
    return alert;
}

// Product filtering
const categoryBtns = document.querySelectorAll('.category-btn');
const productCategories = document.querySelectorAll('.product-category');

if (categoryBtns.length > 0) {
    // Set first category as active by default
    if (categoryBtns[0] && productCategories[0]) {
        categoryBtns[0].classList.add('active');
        productCategories[0].classList.add('active');
    }
    
    // Add click event to category buttons
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const category = btn.getAttribute('data-category');
            
            // Update active button
            categoryBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Show selected category
            productCategories.forEach(cat => {
                if (cat.id === category) {
                    cat.classList.add('active');
                } else {
                    cat.classList.remove('active');
                }
            });
        });
    });
}

// Modal functionality
const modalTriggers = document.querySelectorAll('[data-modal]');
const modals = document.querySelectorAll('.modal');
const closeModalBtns = document.querySelectorAll('.close-modal');

// Open modal
modalTriggers.forEach(trigger => {
    trigger.addEventListener('click', (e) => {
        e.preventDefault();
        const modalId = trigger.getAttribute('data-modal');
        const modal = document.getElementById(modalId);
        
        if (modal) {
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        }
    });
});

// Close modal
function closeModal(modal) {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

closeModalBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const modal = btn.closest('.modal');
        closeModal(modal);
    });
});

// Close modal when clicking outside content
window.addEventListener('click', (e) => {
    modals.forEach(modal => {
        if (e.target === modal) {
            closeModal(modal);
        }
    });
});

// Close modal with Escape key
window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        modals.forEach(modal => {
            if (modal.style.display === 'block') {
                closeModal(modal);
            }
        });
    }
});

// Animation on scroll
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right');
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
        
        if (elementTop < windowHeight - 100) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
};

// Initialize animations
window.addEventListener('load', () => {
    // Add initial animation classes
    document.querySelectorAll('.animate-on-load').forEach((el, index) => {
        el.style.transitionDelay = `${index * 0.1}s`;
        el.classList.add('fade-in');
    });
    
    // Trigger initial animation check
    animateOnScroll();
});

// Check for animations on scroll
window.addEventListener('scroll', animateOnScroll);

// Back to top button
const backToTopBtn = document.createElement('button');
backToTopBtn.className = 'back-to-top';
backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
document.body.appendChild(backToTopBtn);

// Show/hide back to top button
window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        backToTopBtn.classList.add('show');
    } else {
        backToTopBtn.classList.remove('show');
    }
});

// Scroll to top on click
backToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Add some basic styling to the back to top button
const style = document.createElement('style');
style.textContent = `
    .back-to-top {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: var(--primary-color);
        color: white;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        opacity: 0;
        visibility: hidden;
        transform: translateY(20px);
        transition: all 0.3s ease;
        z-index: 999;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .back-to-top.show {
        opacity: 1;
        visibility: visible;
        transform: translateY(0);
    }
    
    .back-to-top:hover {
        background-color: var(--primary-dark);
        transform: translateY(-3px);
    }
`;
document.head.appendChild(style);
