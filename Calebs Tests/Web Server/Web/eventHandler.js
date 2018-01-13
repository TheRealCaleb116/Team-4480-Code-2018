var webSocket;

webSocket = new WebSocket("ws://localhost:8888/eventHandler")

webSocket.onmessage = function(e){
    alert(e.data);
}