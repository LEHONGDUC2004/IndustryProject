
document.addEventListener('DOMContentLoaded', function () {
  const deployForm = document.getElementById('deploy-form');

  const optionCreate = document.getElementById('option_create');
  const optionExisting = document.getElementById('option_existing');

  const sqlGroup = document.getElementById('sql_file_group');
  const hostGroup = document.getElementById('host_db_group');

  const fileSql = document.getElementById('file_sql');
  const passwd = document.getElementById('passwd');
  const confirmPasswd = document.getElementById('confirm_passwd');

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
      // trả về giá trị mặt định value
      document.getElementById('host_db').value = "";
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

    // Nếu muốn: alert khi thành công (có thể xoá nếu bạn submit thật)
    alert("Tải lên và triển khai thành công!");
  });
});

setInterval(function() {
    document.getElementById("jenkins-frame").contentWindow.location.reload();
  }, 1000);


