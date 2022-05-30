 function checkform1() {
     if (document.form1.username.value == "") {
         alert("用户名为空！")
         return false;
     }

     if (document.form1.password.value == "") {
         alert("密码为空！");
         return false;
     }
     if (document.form1.code.value == "") {
         alert("验证码为空！");
         return false;
     }
     if (document.form1.code.value !=document.querySelector('canvas')) {
         alert("验证码错误！");
         return false;
     }

     return true;
 }

  function checkform2() {
      if (document.form2.username1.value == "") {
          alert("用户名为空！")
          return false;
      }

      if (document.form2.password1.value == "") {
          alert("密码为空！");
          return false;
      }
      if (document.form2.password2.value == "") {
          alert("确认密码为空！");
          return false;
      }
      if (document.form2.password1.value !=document.form1.password2.value) {
          alert("两次密码不一致！");
          return false;
      }
      if (document.form2.tel.value == "") {
          alert("电话号码为空！");
          return false;
      }


      return true;
  }