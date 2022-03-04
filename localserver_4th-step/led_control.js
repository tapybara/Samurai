url = "http://192.168.1.11:8080";

let ledon_btn = document.getElementById("ledon");
let ledoff_btn = document.getElementById("ledoff");

ledon_btn.addEventListener("click", function () {
  const send_data = new XMLHttpRequest();
  send_data.open("POST", url);
  send_data.setRequestHeader(
    "content-type",
    "application/x-www-form-urlencoded"
  );
  send_data.send("params=ON");
  console.log("SUCCESS LED ON");
});

//上記イベントのjQueryバージョン
/* $.post(url, { value: "ON" }, () => {
      console.log("SUCCESS LED ON");
      $(this).css({ "background-color": "lawngree", color: "white" });
}); */

ledoff_btn.addEventListener("click", function () {
  const send_data = new XMLHttpRequest();
  send_data.open("POST", url);
  send_data.setRequestHeader(
    "content-type",
    "application/x-www-form-urlencoded"
  );
  send_data.send("params=OFF");
  console.log("SUCCESS LED OFF");
});

//上記イベントのjQueryバージョン
/* $.post(url, { value: "OFF" }, () => {
      console.log("SUCCESS LED OFF");
      $(this).css({ "background-color": "red", color: "white" });
}); */
