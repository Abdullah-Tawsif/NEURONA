// Auto-dismiss flash messages
window.setTimeout(function () {
  const flashes = document.querySelectorAll('.flash-message');
  flashes.forEach(function (flash) {
    flash.style.transition = 'opacity 0.5s ease-out';
    flash.style.opacity = '0';
    setTimeout(function () {
      flash.remove();
    }, 500);
  });
}, 4000);

// Get form elements
var allowedDomains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'neurona.com'];
var username = document.getElementById('username');
var email = document.getElementById('email');
var password = document.getElementById('password');
var confirm = document.getElementById('confirm_password');
var roleInputs = document.querySelectorAll('input[name="role"]');
var submitBtn = document.getElementById('submitBtn');
var termsCheckbox = document.getElementById('terms');

var emailHint = document.getElementById('emailHint');
var passwordHint = document.getElementById('passwordHint');
var confirmHint = document.getElementById('confirmHint');
var usernameHint = document.getElementById('usernameHint');

var strengthBar = document.getElementById('strengthBar');
var reqLength = document.getElementById('reqLength');
var reqSpecial = document.getElementById('reqSpecial');

// Track if user has interacted with fields (for showing validation)
var usernameTouched = false;
var emailTouched = false;
var passwordTouched = false;
var confirmTouched = false;

// Toggle password visibility
function togglePassword(inputId, iconId) {
    const passwordInput = document.getElementById(inputId);
    const eyeIcon = document.getElementById(iconId);

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeIcon.classList.remove('fa-eye');
        eyeIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        eyeIcon.classList.remove('fa-eye-slash');
        eyeIcon.classList.add('fa-eye');
    }
}

// Validate username
function validateUsername() {
    var value = username.value.trim();
    if (!usernameTouched) return true;

    if (value.length === 0) {
        username.classList.add('is-invalid');
        username.classList.remove('is-valid');
        usernameHint.textContent = 'Username is required';
        usernameHint.className = 'hint invalid';
        return false;
    } else if (value.length < 3) {
        username.classList.add('is-invalid');
        username.classList.remove('is-valid');
        usernameHint.textContent = 'Username must be at least 3 characters';
        usernameHint.className = 'hint invalid';
        return false;
    } else {
        username.classList.remove('is-invalid');
        username.classList.add('is-valid');
        usernameHint.textContent = 'Username available';
        usernameHint.className = 'hint valid';
        return true;
    }
}

// Validate email
function validateEmail() {
    var value = email.value.trim();
    if (!emailTouched) return true;

    var domain = value.split('@')[1];

    if (value.length === 0) {
        email.classList.add('is-invalid');
        email.classList.remove('is-valid');
        emailHint.textContent = 'Email is required';
        emailHint.className = 'hint invalid';
        return false;
    } else if (domain && allowedDomains.includes(domain.toLowerCase())) {
        email.classList.add('is-valid');
        email.classList.remove('is-invalid');
        emailHint.textContent = 'Allowed email domain';
        emailHint.className = 'hint valid';
        return true;
    } else {
        email.classList.add('is-invalid');
        email.classList.remove('is-valid');
        emailHint.textContent = 'Use email from: ' + allowedDomains.join(', ');
        emailHint.className = 'hint invalid';
        return false;
    }
}

// Validate password and update strength
function validatePassword() {
    var value = password.value;
    updatePasswordStrength(value);

    if (!passwordTouched) return true;

    var hasLength = value.length >= 8;
    var hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(value);

    // Update requirement indicators
    if (hasLength) {
        reqLength.classList.add('valid');
    } else {
        reqLength.classList.remove('valid');
    }

    if (hasSpecial) {
        reqSpecial.classList.add('valid');
    } else {
        reqSpecial.classList.remove('valid');
    }

    if (value.length === 0) {
        password.classList.add('is-invalid');
        password.classList.remove('is-valid');
        passwordHint.textContent = 'Password is required';
        passwordHint.className = 'hint invalid';
        return false;
    } else if (hasLength && hasSpecial) {
        password.classList.add('is-valid');
        password.classList.remove('is-invalid');
        passwordHint.textContent = 'Strong password';
        passwordHint.className = 'hint valid';
        return true;
    } else {
        password.classList.add('is-invalid');
        password.classList.remove('is-valid');
        passwordHint.textContent = 'At least 8 characters and 1 special character';
        passwordHint.className = 'hint invalid';
        return false;
    }
}

// Update password strength bar
function updatePasswordStrength(value) {
    if (!strengthBar) return;

    var score = 0;
    if (value.length >= 8) score++;
    if (/[!@#$%^&*(),.?":{}|<>]/.test(value)) score++;
    if (/[A-Z]/.test(value)) score++;
    if (/[0-9]/.test(value)) score++;
    if (value.length >= 12) score++;

    strengthBar.className = 'strength-bar';

    if (score <= 1) {
        strengthBar.classList.add('weak');
    } else if (score <= 3) {
        strengthBar.classList.add('medium');
    } else {
        strengthBar.classList.add('strong');
    }
}

// Validate confirm password
function validateConfirm() {
    var value = confirm.value;
    if (!confirmTouched) return true;

    if (value.length === 0) {
        confirm.classList.add('is-invalid');
        confirm.classList.remove('is-valid');
        confirmHint.textContent = 'Please confirm your password';
        confirmHint.className = 'hint invalid';
        return false;
    } else if (value === password.value) {
        confirm.classList.add('is-valid');
        confirm.classList.remove('is-invalid');
        confirmHint.textContent = 'Passwords match';
        confirmHint.className = 'hint valid';
        return true;
    } else {
        confirm.classList.add('is-invalid');
        confirm.classList.remove('is-valid');
        confirmHint.textContent = 'Passwords do not match';
        confirmHint.className = 'hint invalid';
        return false;
    }
}

// Check if a role is selected
function isRoleSelected() {
    for (var i = 0; i < roleInputs.length; i++) {
        if (roleInputs[i].checked) {
            return true;
        }
    }
    return false;
}

// Validate entire form
function validateForm() {
    var allValid =
        username.value.trim() !== '' &&
        username.value.trim().length >= 3 &&
        (function() {
            var domain = email.value.split('@')[1];
            return domain && allowedDomains.includes(domain.toLowerCase());
        })() &&
        password.value.length >= 8 &&
        /[!@#$%^&*(),.?":{}|<>]/.test(password.value) &&
        confirm.value === password.value &&
        confirm.value.length > 0 &&
        isRoleSelected() &&
        termsCheckbox.checked;

    submitBtn.disabled = !allValid;
    return allValid;
}

// Mark field as touched on blur
username.addEventListener('blur', function() {
    usernameTouched = true;
    validateUsername();
    validateForm();
});

email.addEventListener('blur', function() {
    emailTouched = true;
    validateEmail();
    validateForm();
});

password.addEventListener('blur', function() {
    passwordTouched = true;
    validatePassword();
    validateForm();
});

confirm.addEventListener('blur', function() {
    confirmTouched = true;
    validateConfirm();
    validateForm();
});

// Real-time validation on input (only after touched)
username.addEventListener('input', function() {
    if (usernameTouched) validateUsername();
    validateForm();
});

email.addEventListener('input', function() {
    if (emailTouched) validateEmail();
    validateForm();
});

password.addEventListener('input', function() {
    updatePasswordStrength(password.value);
    if (passwordTouched) validatePassword();
    if (confirmTouched) validateConfirm();
    validateForm();
});

confirm.addEventListener('input', function() {
    if (confirmTouched) validateConfirm();
    validateForm();
});

// Role selection listeners
roleInputs.forEach(function(input) {
    input.addEventListener('change', validateForm);
});

// Terms checkbox listener
termsCheckbox.addEventListener('change', validateForm);

// Form submission - validate all fields before submitting
document.getElementById('signupForm').addEventListener('submit', function(e) {
    // Mark all fields as touched
    usernameTouched = true;
    emailTouched = true;
    passwordTouched = true;
    confirmTouched = true;

    // Validate all fields
    var isUsernameValid = validateUsername();
    var isEmailValid = validateEmail();
    var isPasswordValid = validatePassword();
    var isConfirmValid = validateConfirm();

    // Prevent submission if any field is invalid
    if (!isUsernameValid || !isEmailValid || !isPasswordValid || !isConfirmValid || !isRoleSelected() || !termsCheckbox.checked) {
        e.preventDefault();

        // Focus the first invalid field
        if (!isUsernameValid) {
            username.focus();
        } else if (!isEmailValid) {
            email.focus();
        } else if (!isPasswordValid) {
            password.focus();
        } else if (!isConfirmValid) {
            confirm.focus();
        }
    }
});

// Initial form state - button should be disabled
validateForm();
