url = "http://192.168.11.11";

let ledon_btn = document.getElementById("ledon");
let ledoff_btn = document.getElementById("ledoff");
let user_id = document.getElementById("user_id");
let password = document.getElementById("user_password");
const login_form = document.getElementById("login");
const LED_ON = "ON";
const LED_OFF = "OFF";

const httpHandler = (post_content) => {
  const send_data = new XMLHttpRequest();
  send_data.open("POST", url, true);
  send_data.setRequestHeader(
    "content-type",
    "application/x-www-form-urlencoded"
  );
  send_data.send(post_content);
  send_data.onloadend = function () { //
    if (send_data.status == 200) {
      console.log(send_data.status);
      console.log("post request ok");
    } else {
      // エラーで終了した場合。
      console.log("error");
    }
  };
};

  $("#led").text(ledstatus);
  if (ledstatus == LED_ON) {
    $("#ledon").addClass("ledon");
    $("#ledoff").removeClass("ledoff");
  } else if (ledstatus == LED_OFF) {
    $("#ledoff").addClass("ledoff");
    $("#ledon").removeClass("ledon");
  }
  db_tag = send_data.responseText;
  $(".db_table").html(db_tag);
};

ledon_btn.addEventListener("click", function () {
  httpHandler("params=ON");
  ledDisplayControl(LED_ON);
});

ledoff_btn.addEventListener("click", function () {
  httpHandler("params=OFF");
  ledDisplayControl(LED_OFF);
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
