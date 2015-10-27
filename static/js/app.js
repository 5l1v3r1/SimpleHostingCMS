$(function () {//это выполнится после полной загрузки страницы
 
    $('.menu-toggler').each(function () {//это выполнится для каждого элемента с классом menu-toggler
        //в this будет текущий элемент коллекции $('.menu-toggler'). Оборачиваем в jquery
        var $element = $(this);
        //составляем селектор для поиска соответствующей вслпывашки
        var targetClass = $element.data('targetclass');
        var popupSelector = ".menu-toggler-target." + targetClass;
        //находим всплывашку
        var $popup = $(popupSelector);
 
        $element.mouseenter(function (e) {
            console.log("Mouse enter у пункта меню");
            $popup.stop().slideDown();
        });
 
        $element.mouseleave(function (e) {
            console.log("Mouse leave у пункта меню");
            //находим элемент, на который ушла мышь
            var $toElement = $(e.toElement || e.relatedTarget);
            console.log($toElement);
            console.log(!($toElement.parents('.menu-toggler-target').length || $toElement.hasClass('.menu-toggler-target')))
            //если нет родителей с классом menu-toggler-target и сам $toElement не menu-toggler-target
            if (!($toElement.parents('.menu-toggler-target').length || $toElement.hasClass('.menu-toggler-target'))) {
                $popup.stop().slideUp();
            }
        });
 
        $popup.mouseleave(function (e) {
            console.log("Mouse leave у всплывашки");
 
            var $toElement = $(e.toElement||e.relatedTarget);
            console.log($toElement);
            //если возвращаемся не на вызвавшую кнопку меню
            if ($toElement.data('targetclass') != targetClass) {
                $popup.stop().slideUp();
            }
        });
 
        console.log("привязали обработчики событий к пункту меню с целью " + targetClass);
    });
 
    console.log('привязали все обработчики событий')
});
