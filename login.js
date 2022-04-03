url = "http://192.168.11.11";

submit_btn.addEventListener("click", function () {
  let submit_btn = document.getElementById("submit_btn");
  const id = $('[name="user_id"]').val(); //フォーム欄(ID)の入力値を読み出し
  const password = $('[name="user_password"]').val(); //フォーム欄(password)の入力値を読み出し
  let post_text = `user_id=${id}&user_password=${password}`; //POSTリクエストのボディー部生成

  const send_data = new XMLHttpRequest();
  send_data.open("POST", url, true);
  send_data.setRequestHeader(
    "content-type",
    "application/x-www-form-urlencoded"
  );
  send_data.send(post_text);

  //POST送信が完了した時の処理
  send_data.onloadend = function () {
    console.log(send_data.status, "login.js");
    // submit_btn.attr("disabled", true); //通信終了時まで多重送信を防止

    res_text = send_data.responseText;
    if (res_text == "login_success") {
      alert("ログインに成功しました。");
      window.location.href = "/top.html";
    } else {
      alert("ログインに失敗しました。");
      window.location.reload();
    }
  };
});
