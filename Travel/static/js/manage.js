        $(function () {
            $(".menu-item").click(function () {
                $(".menu-item").removeClass("menu-item-active");
                $(this).addClass("menu-item-active");
                var itmeObj = $(".menu-item").find("img");
                itmeObj.each(function () {
                    var items = $(this).attr("src");
                    items = items.replace("_grey.png", ".png");
                    items = items.replace(".png", "_grey.png")
                    $(this).attr("src", items);
                });
                var attrObj = $(this).find("img").attr("src");
                ;
                attrObj = attrObj.replace("_grey.png", ".png");
                $(this).find("img").attr("src", attrObj);
            });
        });

        function changeFrameHeight() {
            var ifm = document.getElementById("fourIfm");
            ifm.height = document.documentElement.clientHeight;

            var one = document.getElementById("one");
            one.height = document.documentElement.clientHeight;

            var two = document.getElementById("two");
            two.height = document.documentElement.clientHeight;

        }

        window.onresize = function () {
            changeFrameHeight();
        }