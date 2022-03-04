url = "http://192.168.1.11:8080";

let ledon_btn = document.getElementById("ledon");
let ledoff_btn = document.getElementById("ledoff");

function httpHandler() {}

ledon_btn.addEventListener("click", function () {
  const send_data = new XMLHttpRequest();
  send_data.open("POST", url, true);
  send_data.setRequestHeader(
    "content-type",
    "application/x-www-form-urlencoded"
  );
  //POST を送信し、送信が完了した際に呼び出されるハンドラーを追加
  send_data.onloadend = function () {
    console.log(send_data.status);
    if (send_data.status == 200) {
      // HTTPステータス 200 で終了した場合。
      //######【課題】ここに、成功したときに修正するCSSを記載してみましょう。
      $("h1").css("color", "#ccc");
      console.log("post request ok");
    } else {
      // エラーで終了した場合。
      console.log("error");
    }
  };
  send_data.send("params=ON");
});

ledoff_btn.addEventListener("click", function () {
  const send_data = new XMLHttpRequest();
  send_data.open("POST", url);
  send_data.setRequestHeader(
    "content-type",
    "application/x-www-form-urlencoded"
  );
  //POST を送信し、送信が完了した際に呼び出されるハンドラーを追加
  send_data.onloadend = function () {
    console.log(send_data.status);
    if (send_data.status == 200) {
      // HTTPステータス 200 で終了した場合。
      //######【課題】ここに、成功したときに修正するCSSを記載してみましょう。
      $("h1").css("color", "#fff");
      console.log("post request ok");
    } else {
      // エラーで終了した場合。
      console.log("error");
    }
  };
  send_data.send("params=OFF");
});

//上記イベントのjQueryバージョン
/*$.post(url, { value: "ON" }, () => {
  console.log("SUCCESS LED ON");
  $(this).css({ "background-color": "lawngree", color: "white" });
});*/

//上記イベントのjQueryバージョン
/*$.post(url, { value: "OFF" }, () => {
  console.log("SUCCESS LED OFF");
  $(this).css({ "background-color": "red", color: "white" });
});*/
