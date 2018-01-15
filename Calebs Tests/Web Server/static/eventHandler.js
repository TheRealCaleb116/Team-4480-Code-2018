var webSocket;

webSocket = new WebSocket("ws://localhost:8888/EventHandler")

webSocket.onmessage = function(e){
    alert(e.data);
}