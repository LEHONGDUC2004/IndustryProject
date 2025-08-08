
document.addEventListener('DOMContentLoaded', function () {
  const optionCreate = document.getElementById('option_create');
  const optionExisting = document.getElementById('option_existing');
  const sqlGroup = document.getElementById('sql_file_group');
  const hostGroup = document.getElementById('host_db_group');
  const fileSql = document.getElementById('file_sql');
  const passwd = document.getElementById('passwd');
  const confirmPasswd = document.getElementById('confirm_passwd');

  const loadingModal = document.getElementById('loadingModal');
  const deployModal = document.getElementById('deployModal');
  const deployForm = document.getElementById('deploy-form');
  const newDeployBtn = document.getElementById('deploy-btn-login');
  const modalEl = document.getElementById('loginRequiredModal1');
  // Toggle radio group
  function toggleFields() {
    if (optionCreate && optionCreate.checked) {
      sqlGroup.style.display = 'block';
      hostGroup.style.display = 'none';
      fileSql.setAttribute('required', 'required');
    } else {
      sqlGroup.style.display = 'none';
      hostGroup.style.display = 'block';
      fileSql.removeAttribute('required');
    }
  }
  if (optionCreate && optionExisting) {
    optionCreate.addEventListener('change', toggleFields);
    optionExisting.addEventListener('change', toggleFields);
    toggleFields();
  }


  if (newDeployBtn && modalEl) {
    const loginModal = new bootstrap.Modal(modalEl);

    newDeployBtn.addEventListener('click', function (e) {
      e.preventDefault();
      loginModal.show();
    });
  }


  if (deployForm) {
   const loadingModal1 = new bootstrap.Modal(loadingModal, {
             backdrop: 'static',
             keyboard: false
  });
    deployForm.addEventListener('submit', function (e) {
      loadingModal1.show();
    });
  }
});

window.onload = function () {
  setInterval(function () {
    const frame = document.getElementById("jenkins-frame");
    if (frame) frame.src = frame.src;
  }, 10000);
};

function changeTypePassword() {
  let password = document.getElementById('passwd');
  let eyeIcon = document.querySelector('.fa-regular');

  if (password.type === 'text') {
    password.type = 'password';
    eyeIcon.classList.remove('fa-eye-slash');
    eyeIcon.classList.add('fa-eye');
  } else {
    password.type = 'text';
    eyeIcon.classList.remove('fa-eye');
    eyeIcon.classList.add('fa-eye-slash');
  }
}

