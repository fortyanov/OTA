$(document).ready(function(){
    var Controller = Backbone.Router.extend({
        routes: {
            "": "start", // Пустой hash-тэг
            "!/": "start", // Начальная страница
            "!/server": "server", // Блок настроек сервера
            "!/pdg": "pdg",// Блок настроек генератора
            "!/user": "user" // Блок настроек пользователей
        },

        start: function () {
            $('#container').load('/hello');
            $("a").css("font-weight", "normal");
        },

        server: function () {
            $('#container').load('/staff/server');
            $("a").css("font-weight", "normal");
            $("a[href='#!/server']").css("font-weight", "bold")
        },

        pdg: function () {
            $('#container').load('/staff/pdg/set');
            $("a").css("font-weight", "normal");
            $("a[href='#!/pdg']").css("font-weight", "bold")
        },

        user: function () {
            $('#container').load('/staff/user/add');
            $("a").css("font-weight", "normal");
            $("a[href='#!/user']").css("font-weight", "bold")
        }
    });

    controller = new Controller(); // Создаём контроллер
    Backbone.history.start();  // Запускаем HTML5 History push
});