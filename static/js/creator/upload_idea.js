/* ================================================
   UPLOAD IDEA - Multi-Step Wizard JavaScript
   ================================================ */

var currentStep = 1;
var totalSteps = 4;
var tags = [];
var selectedCategories = [];
var selectedStatuses = [];
var selectedTargetMarkets = [];
var selectedIP = [];
var productImages = [];
var ipDocuments = [];
var autoSaveInterval = null;

// ================================================
// STEP NAVIGATION
// ================================================

function showStep(step) {
  document.querySelectorAll('.wizard-step').forEach(function(s) {
    s.classList.remove('active');
  });
  var stepEl = document.querySelector('.wizard-step[data-step="' + step + '"]');
  if (!stepEl) return;
  stepEl.classList.add('active');

  document.querySelectorAll('.progress-step').forEach(function(ps, idx) {
    ps.classList.remove('active', 'completed');
    if (idx + 1 === step) {
      ps.classList.add('active');
    } else if (idx + 1 < step) {
      ps.classList.add('completed');
    }
  });

  var progressPercent = (step / totalSteps) * 100;
  var progressFill = document.getElementById('progressFill');
  if (progressFill) progressFill.style.width = progressPercent + '%';

  if (step === 4) {
    populateReview();
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function nextStep(fromStep) {
  if (validateStep(fromStep)) {
    currentStep = fromStep + 1;
    showStep(currentStep);
  } else {
    var stepEl = document.querySelector('.wizard-step[data-step="' + fromStep + '"]');
    if (stepEl) {
      var firstError = stepEl.querySelector('.is-invalid, .invalid-feedback.show');
      if (firstError) {
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  }
}

function prevStep(fromStep) {
  currentStep = fromStep - 1;
  showStep(currentStep);
}

// ================================================
// VALIDATION
// ================================================

function showFieldError(fieldId, message) {
  var field = document.getElementById(fieldId);
  if (!field) return;

  field.classList.add('is-invalid');

  var feedback = field.parentElement.querySelector('.invalid-feedback');
  if (!feedback) {
    feedback = field.closest('.form-group').querySelector('.invalid-feedback');
  }
  if (feedback) {
    feedback.classList.add('show');
    if (message) feedback.textContent = message;
  }
}

function showGroupError(containerId, message) {
  var container = document.getElementById(containerId);
  if (!container) return;

  var group = container.closest('.form-group');
  if (!group) return;

  var feedback = group.querySelector('.invalid-feedback');
  if (feedback) {
    feedback.classList.add('show');
    if (message) feedback.textContent = message;
  }
}

function clearStepErrors(step) {
  var stepEl = document.querySelector('.wizard-step[data-step="' + step + '"]');
  if (!stepEl) return;

  stepEl.querySelectorAll('.invalid-feedback').forEach(function(el) {
    el.classList.remove('show');
  });
  stepEl.querySelectorAll('.is-invalid').forEach(function(el) {
    el.classList.remove('is-invalid');
  });
}

function validateStep(step) {
  var isValid = true;
  clearStepErrors(step);

  if (step === 1) {
    var title = document.getElementById('title').value.trim();
    if (!title || title.split(/\s+/).length > 8) {
      showFieldError('title', 'Title must be 8 words or less');
      isValid = false;
    }

    if (selectedCategories.length === 0) {
      showGroupError('categoryContainer', 'Please select at least one category');
      isValid = false;
    }

    if (selectedCategories.indexOf('Other') !== -1) {
      var otherCat = document.getElementById('other_category').value.trim();
      if (!otherCat || otherCat.split(/\s+/).length > 2) {
        showFieldError('other_category', 'Other category must be 2 words or less');
        isValid = false;
      }
    }

    if (selectedStatuses.length === 0) {
      showGroupError('statusContainer', 'Please select at least one status');
      isValid = false;
    }

    if (tags.length === 0) {
      showGroupError('tagsDisplay', 'Please add at least one tag');
      isValid = false;
    }

    if (selectedTargetMarkets.length === 0) {
      showGroupError('targetMarketContainer', 'Please select at least one target market');
      isValid = false;
    }

    var summary = document.getElementById('summary').value.trim();
    if (!summary) {
      showFieldError('summary', 'Summary is required');
      isValid = false;
    }

    var problem = document.getElementById('problem_statement').value.trim();
    if (!problem) {
      showFieldError('problem_statement', 'Problem statement is required');
      isValid = false;
    }

    var solution = document.getElementById('proposed_solution').value.trim();
    if (!solution) {
      showFieldError('proposed_solution', 'Proposed solution is required');
      isValid = false;
    }
  }

  if (step === 2) {
    var fullName = document.getElementById('full_name').value.trim();
    if (!fullName) {
      showFieldError('full_name', 'Full name is required');
      isValid = false;
    }

    var email = document.getElementById('email').value.trim();
    if (!email || !isValidEmail(email)) {
      showFieldError('email', 'Please enter a valid email');
      isValid = false;
    }

    var phone = document.getElementById('contact_number').value.trim();
    if (!phone || !isValidPhone(phone)) {
      showFieldError('contact_number', 'Please enter a valid phone number');
      isValid = false;
    }

    var founders = collectFounders();
    if (founders.length === 0) {
      showGroupError('foundersContainer', 'Please add at least one founder with valid LinkedIn URLs');
      isValid = false;
    } else {
      for (var i = 0; i < founders.length; i++) {
        if (!founders[i].name || !founders[i].role || !isValidLinkedIn(founders[i].linkedin)) {
          showGroupError('foundersContainer', 'Each founder needs a name, role, and valid LinkedIn URL');
          isValid = false;
          break;
        }
      }
    }

    var website = document.getElementById('company_website').value.trim();
    if (website && !isValidURL(website)) {
      showFieldError('company_website', 'Please enter a valid URL');
      isValid = false;
    }

    var teamSize = document.getElementById('team_size').value;
    if (!teamSize || parseInt(teamSize) < 1) {
      showFieldError('team_size', 'Team size must be at least 1');
      isValid = false;
    }

    var address = document.getElementById('address').value.trim();
    if (!address) {
      showFieldError('address', 'Address is required');
      isValid = false;
    }

    var country = document.getElementById('country').value;
    if (!country) {
      showFieldError('country', 'Please select a country');
      isValid = false;
    }
  }

  if (step === 3) {
    var fundingGoal = parseFloat(document.getElementById('funding_goal').value);
    if (isNaN(fundingGoal) || fundingGoal < 50) {
      showFieldError('funding_goal', 'Funding goal must be at least 50');
      isValid = false;
    }

    var productStageVal = document.getElementById('productStageInput').value;
    var selectedStageCard = document.querySelector('.stage-card.selected');
    if (!productStageVal && !selectedStageCard) {
      showGroupError('productStageContainer', 'Please select a product stage');
      isValid = false;
    }

    var equity = parseFloat(document.getElementById('equity_offered').value);
    if (isNaN(equity) || equity < 0 || equity > 100) {
      showFieldError('equity_offered', 'Equity must be between 0 and 100');
      isValid = false;
    }

    var fundingUsage = document.getElementById('funding_usage').value.trim();
    if (!fundingUsage) {
      showFieldError('funding_usage', 'Funding usage is required');
      isValid = false;
    }

    var timelineVal = document.getElementById('timelineInput').value;
    var selectedTimeline = document.querySelector('.timeline-option.selected');
    if (!timelineVal && !selectedTimeline) {
      showGroupError('timelineContainer', 'Please select a timeline');
      isValid = false;
    }

    var revenueVal = document.getElementById('revenueInput').value;
    var selectedRevenue = document.querySelector('.revenue-option.selected');
    if (!revenueVal && !selectedRevenue) {
      showGroupError('revenueContainer', 'Please select a revenue status');
      isValid = false;
    }

    var businessPlan = document.getElementById('business_plan').files.length;
    if (businessPlan === 0) {
      showGroupError('businessPlanArea', 'Business plan is required');
      isValid = false;
    }

    if (productImages.length === 0) {
      showGroupError('productImagesArea', 'At least one product image is required');
      isValid = false;
    }
  }

  return isValid;
}

// ================================================
// VALIDATION HELPERS
// ================================================

function isValidEmail(email) {
  return /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);
}

function isValidLinkedIn(url) {
  return /^(https?:\/\/)?(www\.)?linkedin\.com\/in\/[a-zA-Z0-9\-_%]+\/?$/.test(url);
}

function isValidURL(url) {
  return /^(https?:\/\/)?(www\.)?[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(\/.*)?$/.test(url);
}

function isValidPhone(phone) {
  return /^\+?\d{6,15}$/.test(phone.replace(/[\s\-]/g, ''));
}

// ================================================
// CHIPS (Categories, Statuses, Target Markets)
// ================================================

function toggleChip(el, type) {
  var value = el.getAttribute('data-value');
  var selected;

  if (type === 'category') selected = selectedCategories;
  else if (type === 'current_status') selected = selectedStatuses;
  else if (type === 'target_market') selected = selectedTargetMarkets;

  var idx = selected.indexOf(value);
  if (idx === -1) {
    selected.push(value);
    el.classList.add('selected');
  } else {
    selected.splice(idx, 1);
    el.classList.remove('selected');
  }

  if (type === 'category') {
    document.getElementById('categoryInput').value = selected.join(',');
    var otherGroup = document.getElementById('otherCategoryGroup');
    if (selected.indexOf('Other') !== -1) {
      otherGroup.style.display = 'block';
    } else {
      otherGroup.style.display = 'none';
      document.getElementById('other_category').value = '';
    }
  } else if (type === 'current_status') {
    document.getElementById('currentStatusInput').value = selected.join(',');
  } else if (type === 'target_market') {
    document.getElementById('targetMarketInput').value = selected.join(',');
  }
}

// ================================================
// TAGS
// ================================================

function addTag() {
  var input = document.getElementById('tagInput');
  var value = input.value.trim();
  if (value && tags.indexOf(value) === -1) {
    tags.push(value);
    renderTags();
    input.value = '';
  }
}

function removeTag(index) {
  tags.splice(index, 1);
  renderTags();
}

function renderTags() {
  var container = document.getElementById('tagsDisplay');
  container.innerHTML = '';
  tags.forEach(function(tag, idx) {
    var chip = document.createElement('div');
    chip.className = 'tag-chip';
    chip.innerHTML = tag + ' <span class="remove-tag" onclick="removeTag(' + idx + ')"><i class="fas fa-times"></i></span>';
    container.appendChild(chip);
  });
  document.getElementById('tagsInput').value = tags.join(',');
}

// ================================================
// FOUNDERS
// ================================================

function addFounder() {
  var container = document.getElementById('foundersContainer');
  var row = document.createElement('div');
  row.className = 'founder-row';
  row.innerHTML = `
    <div class="founder-fields">
      <input type="text" class="form-control founder-name" placeholder="Founder Name *">
      <input type="text" class="form-control founder-role" placeholder="Role *">
      <input type="url" class="form-control founder-linkedin" placeholder="LinkedIn URL *">
      <button type="button" class="btn-remove-founder" onclick="removeFounder(this)">
        <i class="fas fa-times"></i>
      </button>
    </div>
  `;
  container.appendChild(row);
}

function removeFounder(btn) {
  var container = document.getElementById('foundersContainer');
  if (container.children.length > 1) {
    btn.closest('.founder-row').remove();
  }
}

function collectFounders() {
  var founders = [];
  document.querySelectorAll('.founder-row').forEach(function(row) {
    var name = row.querySelector('.founder-name').value.trim();
    var role = row.querySelector('.founder-role').value.trim();
    var linkedin = row.querySelector('.founder-linkedin').value.trim();
    if (name || role || linkedin) {
      founders.push({ name: name, role: role, linkedin: linkedin });
    }
  });
  return founders;
}

// ================================================
// STAGE CARDS
// ================================================

function selectStage(el) {
  document.querySelectorAll('.stage-card').forEach(function(c) {
    c.classList.remove('selected');
  });
  el.classList.add('selected');
  document.getElementById('productStageInput').value = el.getAttribute('data-value');
}

// ================================================
// TIMELINE
// ================================================

function selectTimeline(el) {
  document.querySelectorAll('.timeline-option').forEach(function(o) {
    o.classList.remove('selected');
    o.querySelector('i').className = 'far fa-circle';
  });
  el.classList.add('selected');
  el.querySelector('i').className = 'fas fa-circle-check';
  document.getElementById('timelineInput').value = el.getAttribute('data-value');
}

// ================================================
// REVENUE STATUS
// ================================================

function selectRevenue(el) {
  document.querySelectorAll('.revenue-option').forEach(function(o) {
    o.classList.remove('selected');
    o.querySelector('i').className = 'far fa-circle';
  });
  el.classList.add('selected');
  el.querySelector('i').className = 'fas fa-circle-check';
  document.getElementById('revenueInput').value = el.getAttribute('data-value');

  var value = el.getAttribute('data-value');
  var monthlyGroup = document.getElementById('monthlyRevenueGroup');
  if (value === 'Generating Revenue' || value === 'Profitable') {
    monthlyGroup.style.display = 'block';
  } else {
    monthlyGroup.style.display = 'none';
    document.getElementById('monthly_revenue').value = '';
  }
}

// ================================================
// EXISTING INVESTORS
// ================================================

function selectInvestorOption(el) {
  document.querySelectorAll('.investor-option').forEach(function(o) {
    o.classList.remove('active');
    o.querySelector('i').className = 'far fa-circle';
  });
  el.classList.add('active');
  el.querySelector('i').className = 'fas fa-circle-check';

  var value = el.getAttribute('data-value');
  var container = document.getElementById('investorsContainer');
  var addBtn = document.getElementById('addInvestorBtn');

  if (value === 'yes') {
    container.style.display = 'block';
    addBtn.style.display = 'inline-flex';
  } else {
    container.style.display = 'none';
    addBtn.style.display = 'none';
    document.querySelectorAll('.investor-row').forEach(function(r, idx) {
      if (idx > 0) r.remove();
    });
    var nameInput = document.querySelector('.investor-name');
    var amountInput = document.querySelector('.investor-amount');
    if (nameInput) nameInput.value = '';
    if (amountInput) amountInput.value = '';
  }
}

function addInvestor() {
  var container = document.getElementById('investorsContainer');
  var row = document.createElement('div');
  row.className = 'investor-row';
  row.innerHTML = `
    <div class="investor-fields">
      <input type="text" class="form-control investor-name" placeholder="Investor Name *">
      <input type="number" class="form-control investor-amount" placeholder="Amount Invested *" min="0" step="any">
      <button type="button" class="btn-remove-investor" onclick="removeInvestor(this)">
        <i class="fas fa-times"></i>
      </button>
    </div>
  `;
  container.appendChild(row);
}

function removeInvestor(btn) {
  var container = document.getElementById('investorsContainer');
  if (container.children.length > 1) {
    btn.closest('.investor-row').remove();
  }
}

function collectInvestors() {
  var investors = [];
  var activeOption = document.querySelector('.investor-option.active');
  if (activeOption && activeOption.getAttribute('data-value') === 'yes') {
    document.querySelectorAll('.investor-row').forEach(function(row) {
      var name = row.querySelector('.investor-name').value.trim();
      var amount = row.querySelector('.investor-amount').value;
      if (name || amount) {
        investors.push({ name: name, amount: parseFloat(amount) || 0 });
      }
    });
  }
  return investors;
}

// ================================================
// INTELLECTUAL PROPERTY
// ================================================

function toggleIP(checkbox) {
  var value = checkbox.value;
  if (checkbox.checked) {
    if (value !== 'None') {
      if (selectedIP.indexOf('None') !== -1) {
        selectedIP.splice(selectedIP.indexOf('None'), 1);
        var noneCheckbox = document.querySelector('.ip-checkbox input[value="None"]');
        if (noneCheckbox) noneCheckbox.checked = false;
      }
      selectedIP.push(value);
    } else {
      selectedIP = ['None'];
      document.querySelectorAll('.ip-checkbox input').forEach(function(inp) {
        if (inp.value !== 'None') inp.checked = false;
      });
    }
  } else {
    var idx = selectedIP.indexOf(value);
    if (idx !== -1) selectedIP.splice(idx, 1);
  }

  document.getElementById('ipInput').value = selectedIP.join(',');

  var hasIP = selectedIP.length > 0 && selectedIP.indexOf('None') === -1;
  document.getElementById('ipUploadGroup').style.display = hasIP ? 'block' : 'none';
}

function toggleIPNone(checkbox) {
  toggleIP(checkbox);
}

// ================================================
// FILE UPLOADS
// ================================================

document.addEventListener('DOMContentLoaded', function() {
  // Business Plan
  document.getElementById('business_plan').addEventListener('change', function(e) {
    var file = e.target.files[0];
    if (file) {
      document.getElementById('businessPlanName').textContent = file.name;
    }
  });

  // Product Images
  document.getElementById('product_images').addEventListener('change', function(e) {
    var files = Array.from(e.target.files);
    files.forEach(function(file) {
      if (file.size > 5 * 1024 * 1024) {
        alert(file.name + ' exceeds 5MB limit');
        return;
      }
      var reader = new FileReader();
      reader.onload = function(ev) {
        var idx = productImages.indexOf(file);
        if (idx === -1) return;
        var preview = document.createElement('div');
        preview.className = 'image-preview-item';
        preview.innerHTML = `
          <img src="${ev.target.result}" alt="Preview">
          <button type="button" class="remove-image" onclick="removeImage(${idx})">
            <i class="fas fa-times"></i>
          </button>
        `;
        document.getElementById('imagePreviews').appendChild(preview);
      };
      reader.readAsDataURL(file);
      productImages.push(file);
    });
    renderImagePreviews();
  });

  // IP Documents
  document.getElementById('ip_documents').addEventListener('change', function(e) {
    var files = Array.from(e.target.files);
    files.forEach(function(file) {
      ipDocuments.push(file);
      var item = document.createElement('div');
      item.className = 'ip-doc-item';
      item.innerHTML = `<i class="fas fa-file"></i> ${file.name}`;
      document.getElementById('ipDocList').appendChild(item);
    });
  });

  // Demo Video
  document.getElementById('demo_video').addEventListener('change', function(e) {
    var file = e.target.files[0];
    if (file) {
      document.getElementById('demoVideoName').textContent = file.name;
    }
  });

  // Character counters
  ['summary', 'problem_statement', 'proposed_solution', 'funding_usage'].forEach(function(id) {
    var el = document.getElementById(id);
    if (el) {
      var counterId = id === 'problem_statement' ? 'problemCount' :
                      id === 'proposed_solution' ? 'solutionCount' :
                      id === 'funding_usage' ? 'fundingUsageCount' : id + 'Count';
      el.addEventListener('input', function() {
        var counter = document.getElementById(counterId);
        if (counter) counter.textContent = this.value.length;
      });
      var counter = document.getElementById(counterId);
      if (counter) counter.textContent = el.value.length;
    }
  });

  // Tag input - add on Enter
  document.getElementById('tagInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      addTag();
    }
  });

  // Form submit
  document.getElementById('uploadIdeaForm').addEventListener('submit', function(e) {
    if (!document.getElementById('termsAgree').checked) {
      e.preventDefault();
      alert('Please agree to the Terms & Policies before submitting');
      return;
    }

    // Collect founders and investors before submit
    document.getElementById('foundersInput').value = JSON.stringify(collectFounders());
    document.getElementById('existingInvestorsInput').value = JSON.stringify(collectInvestors());

    // Prepend country code to phone number
    var countryCode = document.getElementById('phoneCountryCode').value;
    var phoneInput = document.getElementById('contact_number');
    var phoneVal = phoneInput.value.trim();
    if (phoneVal && !phoneVal.startsWith('+')) {
      phoneInput.value = countryCode + phoneVal;
    }

    var submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.querySelector('.btn-text').style.display = 'none';
    submitBtn.querySelector('.btn-spinner').style.display = 'inline-flex';
  });

  // Start auto-save
  startAutoSave();
});

function renderImagePreviews() {
  // Previews are rendered on file change
}

function removeImage(index) {
  productImages.splice(index, 1);
  var previews = document.getElementById('imagePreviews');
  previews.innerHTML = '';
  productImages.forEach(function(file, idx) {
    var reader = new FileReader();
    reader.onload = function(ev) {
      var preview = document.createElement('div');
      preview.className = 'image-preview-item';
      preview.innerHTML = `
        <img src="${ev.target.result}" alt="Preview">
        <button type="button" class="remove-image" onclick="removeImage(${idx})">
          <i class="fas fa-times"></i>
        </button>
      `;
      previews.appendChild(preview);
    };
    reader.readAsDataURL(file);
  });
}

// ================================================
// REVIEW PAGE
// ================================================

function populateReview() {
  var container = document.getElementById('reviewContainer');
  if (!container) return;
  var founders = collectFounders();
  var investors = collectInvestors();

  var foundersHtml = founders.map(function(f) {
    return escapeHtml(f.name) + ' (' + escapeHtml(f.role) + ') - ' + escapeHtml(f.linkedin);
  }).join('<br>');

  var investorsHtml = investors.length > 0
    ? investors.map(function(i) { return escapeHtml(i.name) + ': ' + i.amount; }).join('<br>')
    : 'None';

  var ipHtml = selectedIP.length > 0 ? selectedIP.map(escapeHtml).join(', ') : 'None';

  container.innerHTML = `
    <div class="review-section">
      <h3><i class="fas fa-info-circle"></i> Basic Information</h3>
      <div class="review-item"><div class="review-label">Title:</div><div class="review-value">${escapeHtml(document.getElementById('title').value)}</div></div>
      <div class="review-item"><div class="review-label">Category:</div><div class="review-value">${selectedCategories.map(escapeHtml).join(', ')}</div></div>
      ${selectedCategories.indexOf('Other') !== -1 ? `<div class="review-item"><div class="review-label">Other Category:</div><div class="review-value">${escapeHtml(document.getElementById('other_category').value)}</div></div>` : ''}
      <div class="review-item"><div class="review-label">Current Status:</div><div class="review-value">${selectedStatuses.map(escapeHtml).join(', ')}</div></div>
      <div class="review-item"><div class="review-label">Tags:</div><div class="review-value">${tags.map(escapeHtml).join(', ')}</div></div>
      <div class="review-item"><div class="review-label">Target Market:</div><div class="review-value">${selectedTargetMarkets.map(escapeHtml).join(', ')}</div></div>
      <div class="review-item"><div class="review-label">Summary:</div><div class="review-value">${escapeHtml(document.getElementById('summary').value)}</div></div>
      <div class="review-item"><div class="review-label">Problem Statement:</div><div class="review-value">${escapeHtml(document.getElementById('problem_statement').value)}</div></div>
      <div class="review-item"><div class="review-label">Proposed Solution:</div><div class="review-value">${escapeHtml(document.getElementById('proposed_solution').value)}</div></div>
    </div>

    <div class="review-section">
      <h3><i class="fas fa-address-card"></i> Contact Information</h3>
      <div class="review-item"><div class="review-label">Full Name:</div><div class="review-value">${escapeHtml(document.getElementById('full_name').value)}</div></div>
      <div class="review-item"><div class="review-label">Email:</div><div class="review-value">${escapeHtml(document.getElementById('email').value)}</div></div>
      <div class="review-item"><div class="review-label">Contact Number:</div><div class="review-value">${escapeHtml(document.getElementById('phoneCountryCode').value)} ${escapeHtml(document.getElementById('contact_number').value)}</div></div>
      <div class="review-item"><div class="review-label">Founders:</div><div class="review-value">${foundersHtml}</div></div>
      <div class="review-item"><div class="review-label">Company Website:</div><div class="review-value">${escapeHtml(document.getElementById('company_website').value) || 'N/A'}</div></div>
      <div class="review-item"><div class="review-label">Team Size:</div><div class="review-value">${escapeHtml(document.getElementById('team_size').value)}</div></div>
      <div class="review-item"><div class="review-label">Address:</div><div class="review-value">${escapeHtml(document.getElementById('address').value)}</div></div>
      <div class="review-item"><div class="review-label">Country:</div><div class="review-value">${escapeHtml(document.getElementById('country').value)}</div></div>
    </div>

    <div class="review-section">
      <h3><i class="fas fa-money-bill-wave"></i> Funding & Attachments</h3>
      <div class="review-item"><div class="review-label">Funding Goal:</div><div class="review-value">${escapeHtml(document.getElementById('funding_goal').value)} ${escapeHtml(document.getElementById('currency').value)}</div></div>
      <div class="review-item"><div class="review-label">Product Stage:</div><div class="review-value">${escapeHtml(document.getElementById('productStageInput').value)}</div></div>
      <div class="review-item"><div class="review-label">Equity Offered:</div><div class="review-value">${escapeHtml(document.getElementById('equity_offered').value)}%</div></div>
      <div class="review-item"><div class="review-label">Funding Usage:</div><div class="review-value">${escapeHtml(document.getElementById('funding_usage').value)}</div></div>
      <div class="review-item"><div class="review-label">Expected Timeline:</div><div class="review-value">${escapeHtml(document.getElementById('timelineInput').value)}</div></div>
      <div class="review-item"><div class="review-label">Revenue Status:</div><div class="review-value">${escapeHtml(document.getElementById('revenueInput').value)}</div></div>
      ${document.getElementById('monthly_revenue').value ? `<div class="review-item"><div class="review-label">Monthly Revenue:</div><div class="review-value">${escapeHtml(document.getElementById('monthly_revenue').value)}</div></div>` : ''}
      <div class="review-item"><div class="review-label">Existing Investors:</div><div class="review-value">${investorsHtml}</div></div>
      <div class="review-item"><div class="review-label">Intellectual Property:</div><div class="review-value">${ipHtml}</div></div>
      <div class="review-item"><div class="review-label">Business Plan:</div><div class="review-value">${document.getElementById('business_plan').files[0] ? escapeHtml(document.getElementById('business_plan').files[0].name) : 'N/A'}</div></div>
      <div class="review-item"><div class="review-label">Product Images:</div><div class="review-value">${productImages.length} image(s)</div></div>
      <div class="review-item"><div class="review-label">Product Demo URL:</div><div class="review-value">${escapeHtml(document.getElementById('product_demo_url').value) || 'N/A'}</div></div>
    </div>
  `;
}

function escapeHtml(text) {
  if (!text) return '';
  var div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// ================================================
// TERMS & SUBMIT
// ================================================

function updateSubmitButton() {
  var checkbox = document.getElementById('termsAgree');
  var btn = document.getElementById('submitBtn');
  btn.disabled = !checkbox.checked;
}

// ================================================
// DRAFT SAVE (AUTO & MANUAL)
// ================================================

function saveDraft() {
  document.getElementById('isDraftInput').value = 'true';
  document.getElementById('foundersInput').value = JSON.stringify(collectFounders());
  document.getElementById('existingInvestorsInput').value = JSON.stringify(collectInvestors());

  var formData = new FormData(document.getElementById('uploadIdeaForm'));

  fetch('/upload_idea', {
    method: 'POST',
    body: formData
  })
  .then(function(res) { return res.json(); })
  .then(function(data) {
    if (data.success) {
      showAutoSaveIndicator();
      if (data.draft_id) {
        document.getElementById('draftIdInput').value = data.draft_id;
      }
    } else {
      console.error('Failed to save draft:', data.error || 'Unknown error');
    }
  })
  .catch(function(err) {
    console.error('Draft save error:', err);
  });

  document.getElementById('isDraftInput').value = 'false';
}

function startAutoSave() {
  if (autoSaveInterval) clearInterval(autoSaveInterval);
  autoSaveInterval = setInterval(function() {
    saveDraft();
  }, 45000);
}

function showAutoSaveIndicator() {
  var indicator = document.getElementById('autoSaveIndicator');
  if (!indicator) return;
  indicator.style.display = 'flex';
  setTimeout(function() {
    indicator.style.display = 'none';
  }, 3000);
}
