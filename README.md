начинать установку отсюда:
# pip install -r requirements.txt
установка ta-lib:
# $ cd ta-lib/
# $ ./configure --prefix=/usr
# $ make
# $ sudo make install
# $ pip install TA-Lib

<!-- ОПИСАНИЕ СТРАТЕГИИ:
(Для простоты возьму пример только для одного символа, хотя бот асинхронный и может торговать несколькьюми монетами одновременно). 
После первого сигнала открывается первая позиция и следом прописываются правила для второй позиции, а именно, если первая позиция, например, была в лонг то вторая будет в шорт (если до нее дойдет очередь). 
Дальше запускается вебсокет и каждые две секунды происходит проверка сигнала и цены (напомню что в этот момент открыта только первая позиция). Если срабатывает тригер цены - позиция закрывается и бот сбрасывает настройки и возвращается на следующий круг торговой итерации. Также, если сработал сигнал кроссовер и этот сигнал противоположной направленности и удовлетворяется условие минимально допустимого зазора - то позиция также успешно закрывается. В противном случае --   мы открываем второю позицию - хеджируемся (имеется в виду момент поступления сигнала). Дальше, в режиме хеджирования происходит мониторинг сигнала. При новом сигнале робот подбирает соответствие для той позиции, которую он закроет и если спред удовлетворительный, то позиция - первая или вторая - закрываются. На этот момент остается висеть вторая или первая позиция - разницы нет и уже под нее ищется сигнал на закрытытие. Если такой сигнал поступил и снова таки спред удовлетворительный - закрываемся - переходим на следующий цикл, есл нет - хеджируемся и так далее. Параллельно этому каждые 10 секунд происходит проверка на закрытость-открытость позиций. Если все позиции закрыты - бот сбрасывает данные и переходит на следующий цикл. Если какая либо позиция закрылась (алгоритмом или руками), то эта поправка вносится в список торговых пар.>


<!-- # pip install python-dotenv
# Установка talib:
# https://github.com/TA-Lib/ta-lib-python -----инструкция
# Linux:
# Download ta-lib-0.4.0-src.tar.gz and:

# $ tar -xzf ta-lib-0.4.0-src.tar.gz 
# % (ecxtraction. it could be manualy)
# % unzip {имя зип файла}.zip -->