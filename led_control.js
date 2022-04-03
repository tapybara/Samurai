let ledon_btn = document.getElementById("ledon");
let ledoff_btn = document.getElementById("ledoff");
const LED_ON = "ON";
const LED_OFF = "OFF";

url = "http://192.168.11.11";

const ledCssChange = (ledstatus) => {
  /* ボタンを押した時に適用CSSを変更メソッド */
  $("#led").text(ledstatus);
  if (ledstatus == LED_ON) {
    $("#ledon").addClass("ledon");
    $("#ledoff").removeClass("ledoff");
  } else if (ledstatus == LED_OFF) {
    $("#ledoff").addClass("ledoff");
    $("#ledon").removeClass("ledon");
  }
};

const httpHandler = (post_content) => {
  /* POST送信の処理メソッド（DBリスト更新・LEDボタンCSS変更）*/
  const led_status = post_content.split("=")[1];
  const send_data = new XMLHttpRequest();
  send_data.open("POST", url, true);
  send_data.setRequestHeader(
    "content-type",
    "application/x-www-form-urlencoded"
  );
  send_data.send(post_content);

  send_data.onloadend = function () {
    /* POST送信完了後の処理 */
    console.log(send_data.status, "ldebtn_control.js");
    if (send_data.status == 200) {
      ledCssChange(led_status); //CSS変更
      res_tag = send_data.responseText; //サーバーレスポンス情報の取得
      $(".db_table").html(res_tag); //DBリスト更新
    } else {
      alert(`LEDを${led_status}に出来ませんでした。`);
    }
  };
};

ledon_btn.addEventListener("click", function () {
  //ONボタン押下時のPOSTリクエストと成功時の処理
  httpHandler("params=ON");
});

ledoff_btn.addEventListener("click", function () {
  //OFFボタン押下時のPOSTリクエストと成功時の処理
  httpHandler("params=OFF");
});
