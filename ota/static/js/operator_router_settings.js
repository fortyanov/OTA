$(document).ready(function(){
    var Controller = Backbone.Router.extend({
        routes: {
            "": "start", // Пустой hash-тэг
            "!/": "start", // Начальная страница
            "!/files": "files",
            "!/broadcast": "broadcast"
        },

        start: function () {
            $('#container').load('/hello');
            $("a").css("font-weight", "normal");
        },

        files: function () {
            $('#container').load('/operator/files/set');
            $("a").css("font-weight", "normal");
            $("a[href='#!/files']").css("font-weight", "bold")
        },

        broadcast: function () {
            $('#container').load('/operator/broadcast/first');
            $("a").css("font-weight", "normal");
            $("a[href='#!/broadcast']").css("font-weight", "bold")
        }
    });

    controller = new Controller(); // Создаём контроллер
    Backbone.history.start();  // Запускаем HTML5 History push
});