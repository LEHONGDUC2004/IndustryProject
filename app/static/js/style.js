document.addEventListener('DOMContentLoaded', function () {
  const deployForm = document.getElementById('deploy-form');

  const optionCreate = document.getElementById('option_create');
  const optionExisting = document.getElementById('option_existing');

  const sqlGroup = document.getElementById('sql_file_group');
  const hostGroup = document.getElementById('host_db_group');

  const fileSql = document.getElementById('file_sql');
  const passwd = document.getElementById('passwd');
  const confirmPasswd = document.getElementById('confirm_passwd');
  const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));

  // Ẩn/hiện trường theo lựa chọn CSDL
  function toggleFields() {
    if (optionCreate.checked) {
      sqlGroup.style.display = 'block';
      hostGroup.style.display = 'none';
      fileSql.setAttribute('required', 'required');
    } else {
      sqlGroup.style.display = 'none';
      hostGroup.style.display = 'block';
      fileSql.removeAttribute('required');
    }
  }

  optionCreate.addEventListener('change', toggleFields);
  optionExisting.addEventListener('change', toggleFields);
  toggleFields(); // chạy khi load

  // Xử lý submit form
  deployForm.addEventListener('submit', function (e) {
    // Nếu là kết nối CSDL có sẵn thì kiểm tra mật khẩu
    if (optionExisting.checked) {
      const pass1 = passwd.value.trim();
      const pass2 = confirmPasswd.value.trim();
      document.getElementById('host_db').value = ""; // reset

      if (pass1.length < 6) {
        e.preventDefault();
        alert("Mật khẩu phải có ít nhất 6 ký tự.");
        return false;
      }

      if (pass1 !== pass2) {
        e.preventDefault();
        alert("Mật khẩu và nhập lại mật khẩu không khớp.");
        return false;
      }
    }

    // Hiện modal loading
    loadingModal.show();
  });
});
window.onload = function () {
  setInterval(function () {
    const frame = document.getElementById("jenkins-frame");
    frame.src = frame.src;
  }, 10000);
};
