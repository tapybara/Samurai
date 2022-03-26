url = "http://192.168.11.11";

let ledon_btn = document.getElementById("ledon");
let ledoff_btn = document.getElementById("ledoff");

function httpHandler(param) {
  const send_data = new XMLHttpRequest();
  send_data.open("POST", url, true);
  send_data.setRequestHeader(
    "content-type",
    "application/x-www-form-urlencoded"
  );
  send_data.send("params=ON");
  //POST を送信し、送信が完了した際に呼び出されるハンドラーを追加
  send_data.onloadend = function () {
    console.log(send_data.status);
    if (send_data.status == 200) {
      // HTTPステータス 200 で終了した場合。
      //######【課題】ここに、成功したときに修正するCSSを記載してみましょう。
      $("#led").text(param);
      if (param == "ON") {
        $("#ledon").addClass("ledon");
        $("#ledoff").removeClass("ledoff");
      } else if (param == "OFF") {
        $("#ledoff").addClass("ledoff");
        $("#ledon").removeClass("ledon");
      }
      console.log("post request ok");
      db_tag = send_data.responseText;
      $(".db_table").html(db_tag);
    } else {
      // エラーで終了した場合。
      console.log("error");
    }
  };
}

ledon_btn.addEventListener("click", function () {
  httpHandler("ON");
});

ledoff_btn.addEventListener("click", function () {
  httpHandler("OFF");
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
