  function capitalizeWords(str) {
    return str
      .toLowerCase()
      .trim()
      .split(/\s+/)
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  document.getElementById('full_name').addEventListener('blur', function () {
  this.value = capitalizeWords(this.value);
});


  document.getElementById('verifyForm').addEventListener('submit', function (e) {
    let isValid = true;

    // Full Name
    const fullNameInput = document.getElementById('full_name');
    const nameValue = fullNameInput.value.trim();
    const wordCount = nameValue.split(/\s+/).length;
    const nameFeedback = document.getElementById('name-feedback');
    if (wordCount !== 2) {
      fullNameInput.classList.add('is-invalid');
      fullNameInput.classList.remove('is-valid');
      nameFeedback.classList.remove('d-none');
      isValid = false;
    } else {
      fullNameInput.classList.remove('is-invalid');
      fullNameInput.classList.add('is-valid');
      nameFeedback.classList.add('d-none');
    }

    // Phone Number
    const phoneInput = document.getElementById('phone');
    const phonePattern = /^(\+8801|01)[3-9]\d{8}$/;
    const phoneFeedback = document.getElementById('phone-feedback');
    if (!phonePattern.test(phoneInput.value.trim())) {
      phoneInput.classList.add('is-invalid');
      phoneInput.classList.remove('is-valid');
      phoneFeedback.classList.remove('d-none');
      isValid = false;
    } else {
      phoneInput.classList.remove('is-invalid');
      phoneInput.classList.add('is-valid');
      phoneFeedback.classList.add('d-none');
    }

    // Government ID
    const govInput = document.getElementById('gov_id');
    const govPattern = /^\d{17}$/;
    const govFeedback = document.getElementById('gov-feedback');
    if (!govPattern.test(govInput.value.trim())) {
      govInput.classList.add('is-invalid');
      govInput.classList.remove('is-valid');
      govFeedback.classList.remove('d-none');
      isValid = false;
    } else {
      govInput.classList.remove('is-invalid');
      govInput.classList.add('is-valid');
      govFeedback.classList.add('d-none');
    }

    // LinkedIn URL
    const linkedinInput = document.getElementById('linkedin_id');
    const linkedinPattern = /^(https?:\/\/)?(www\.)?linkedin\.com\/in\/[a-zA-Z0-9-_%]+\/?$/;
    const linkedinFeedback = document.getElementById('linkedin-feedback');
    if (!linkedinPattern.test(linkedinInput.value.trim())) {
      linkedinInput.classList.add('is-invalid');
      linkedinInput.classList.remove('is-valid');
      linkedinFeedback.classList.remove('d-none');
      isValid = false;
    } else {
      linkedinInput.classList.remove('is-invalid');
      linkedinInput.classList.add('is-valid');
      linkedinFeedback.classList.add('d-none');
    }

    // Address
    const addressInput = document.getElementById('present_address');
    const addressFeedback = document.getElementById('address-feedback');
    if (addressInput.value.trim() === "") {
      addressInput.classList.add('is-invalid');
      addressInput.classList.remove('is-valid');
      addressFeedback.classList.remove('d-none');
      isValid = false;
    } else {
      addressInput.classList.remove('is-invalid');
      addressInput.classList.add('is-valid');
      addressFeedback.classList.add('d-none');
    }

    // Prevent form submission if any field is invalid
    if (!isValid) e.preventDefault();
  });

  // Auto-dismiss alert after 2 seconds
  setTimeout(function () {
    const alert = document.querySelector(".alert");
    if (alert) {
      alert.classList.remove("show");
      alert.classList.add("fade");
    }
  }, 2000);