
  window.setTimeout(function() {
    const flashes = document.querySelectorAll('.flash-message');
    flashes.forEach(flash => {
      flash.style.transition = 'opacity 0.5s ease-out';
      flash.style.opacity = '0';
      setTimeout(() => flash.remove(), 500);
    });
  }, 4000);


    const allowedDomains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "neurona.com"];
    const username = document.getElementById("username");
    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const confirm = document.getElementById("confirm_password");
    const role = document.getElementById("role");
    const submitBtn = document.getElementById("submitBtn");

    const emailHint = document.getElementById("emailHint");
    const passwordHint = document.getElementById("passwordHint");
    const confirmHint = document.getElementById("confirmHint");

    function validateEmail() {
        const domain = email.value.split('@')[1];
        if (domain && allowedDomains.includes(domain.toLowerCase())) {
            email.classList.add('is-valid');
            email.classList.remove('is-invalid');
            emailHint.textContent = "✅ Allowed email domain";
            emailHint.className = "hint valid";
            return true;
        } else {
            email.classList.add('is-invalid');
            email.classList.remove('is-valid');
            emailHint.textContent = "❌ Use email from: " + allowedDomains.join(", ");
            emailHint.className = "hint invalid";
            return false;
        }
    }

    function validatePassword() {
        const value = password.value;
        const isValid = value.length >= 8 && /[!@#$%^&*(),.?":{}|<>]/.test(value);
        if (isValid) {
            password.classList.add('is-valid');
            password.classList.remove('is-invalid');
            passwordHint.textContent = "✅ Strong password";
            passwordHint.className = "hint valid";
            return true;
        } else {
            password.classList.add('is-invalid');
            password.classList.remove('is-valid');
            passwordHint.textContent = "❌ At least 8 characters and 1 special character";
            passwordHint.className = "hint invalid";
            return false;
        }
    }

    function validateConfirm() {
        if (confirm.value === password.value && confirm.value.length > 0) {
            confirm.classList.add('is-valid');
            confirm.classList.remove('is-invalid');
            confirmHint.textContent = "✅ Passwords match";
            confirmHint.className = "hint valid";
            return true;
        } else {
            confirm.classList.add('is-invalid');
            confirm.classList.remove('is-valid');
            confirmHint.textContent = "❌ Passwords do not match";
            confirmHint.className = "hint invalid";
            return false;
        }
    }

    function validateForm() {
        const allValid =
            username.value.trim() !== "" &&
            validateEmail() &&
            validatePassword() &&
            validateConfirm() &&
            role.value !== "";

        submitBtn.disabled = !allValid;
    }

    username.addEventListener("input", validateForm);
    email.addEventListener("input", () => { validateEmail(); validateForm(); });
    password.addEventListener("input", () => { validatePassword(); validateConfirm(); validateForm(); });
    confirm.addEventListener("input", () => { validateConfirm(); validateForm(); });
    role.addEventListener("change", validateForm);

src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"