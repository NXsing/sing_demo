from sing import r,d,t,a,e,x,abay,img

# x("<script>alert('h');</script>") - можно вставлять тег script, тем самым вызывая функции на javascript и добавляя дополнительнвй функционал(напр. счетчики)

d("M4",True)

r("start")
x("Приветствую, вы находитесь в начале пути")
x("Далее","next") # next обеспечивает переход в следующую(в коде) комнату
e()

r("первый дом")
t("Вы идете по улице города<br>")
t("<i>На ней ничего необычного</i>")
#~ a("Посмотреть вокруг","mes <script>alert(2)</script>;goto вокруг") # можно даже скрипты задавать
a("Посмотреть вокруг","goto вокруг")
e()

r("вокруг")
t("Вы смотрите на дома")
t(", вы в первый раз здесь<br>","ifnot посетил")
t(", вы уже были здесь<br>","ifset посетил")
t("<i>Обычные дома</i>")
a("Посмотреть на окна","set посетил;next") # какие-либо условия посещения комнаты устанавливаются на выходе из неё(все элементы комнаты обрабатываются последовательно)
a("[открыто] Посмотреть видео на смартфоне","goto smart","ifset посетил")
e()

r()
t("Вы видите окна зданий")
x("<br><i>Обычные окна</i>")
x("Посмотреть на дорогу","goto road") #x("текст","команда") соответствует a("текст","команда")
x("[открыто] Посмотреть на плакат","goto постер","ifset дорога") #x("текст","команда") соответствует a("текст","команда") 
e()

r("road")
x("Обычная дорога, ничего необычного","ifnot дорога")
x("Обычная дорога, ...","ifset дорога")
x("<br>...")
x("обратно","set дорога;return")
e()

r("постер")
x("Плакат с картинкой<br>")
#http://www.playcast.ru/uploads/2015/12/16/16352910.gif
#http://99px.ru/sstorage/1/2017/04/image_11104171100568538743.gif

x("<div style=\"margin-top: 0.15cm;\" class=\"text-center\"> <img class=\"img-fluid\" style=\"margin: 0 auto;\" width='450px' src='HTML/image.jpg'></div>")
x("обратно","goto вокруг")
e()


r("smart")
#~ x("Комната с видео<br>")
x("""<iframe width="605" style="border-radius: 15px;" height="340" src="https://www.youtube.com/embed/bQb8ckTAV0k?autoplay=1&loop=1&mute=1&showinfo=0&controls=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>""")
#xaYip20we00

#https://www.youtube.com/watch?v=lwH3FgbXqMM&feature=youtu.be
#https://youtu.be/5j6_GC3ASOs?list=PLj6XzcqwRpN7XNnbz2R-SMQ5JmFs3qYmr
#https://youtu.be/bQb8ckTAV0k
#https://www.youtube.com/watch?v=uUrWFGln8Uc
#https://youtu.be/4AA4qYGunr4
a("Конец","goto end")
e()

r("end")
t("Для текста можно применять любые стили css.<br>Можно использовать любые теги html.<br>(включая встроенные видео, картинки)<br>")
x("Используя sing(simple interactive novel generator) можно делать интерактивные истории. ")
x("Эти истории могут включать видео, картинками и даже погодные информеры")
x("<br> И любые шрифты и их сочетание")
x("...","goto start2")
t("""<h1 style="text-align:center">THE END</h1>""")
x("""<center><a href="https://clck.yandex.ru/redir/dtype=stred/pid=7/cid=1228/*https://yandex.ru/pogoda/10393" target="_blank"><img src="https://info.weather.yandex.net/10393/1_white.ru.png?domain=ru" border="0" alt="Яндекс.Погода"/><img width="1" height="1" src="https://clck.yandex.ru/click/dtype=stred/pid=7/cid=1227/*https://img.yandex.ru/i/pix.gif" alt="" border="0"/></a></center>""")
e()


r("start2")
x("Вы снова находитесь в начале пути")
x("<br><i>Другое начало - другая судьба</i>")
x("Далее","next")
e()

r()
t("Вы находитесь в первом доме<br>")
t("<i>В нем ничего необычного, кроме перехода в следующую комнату</i>")
a("Пройти в комнату","goto комната2")
e()

r("комната2")
t("Вы находитесь в комнате")
t(", вы в первый раз здесь<br>","ifnot посетил2")
t(", вы уже были здесь<br>","ifset посетил2")
a("[открыто] Посмотреть видео на смартфоне ","set посетил2;next")
e()

r("smart2")
#https://youtu.be/gukgjwIw600
x("""<iframe width="605" style="border-radius: 15px;" height="340" src="https://www.youtube.com/embed/QWw832K5fME?autoplay=1&loop=1&mute=1&modestbranding=1&showinfo=0&controls=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>""")
a("Конец","goto end")
e()
