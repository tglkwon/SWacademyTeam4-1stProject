// https://khw11044.github.io/blog/blog-etc/2021-02-02-colab-01/

function ClickConnect() {
  console.log('코랩 연결 끊김 방지');
  document.querySelector('colab-toolbar-button#connect').click();
}
setInterval(ClickConnect, 60 * 1000);
