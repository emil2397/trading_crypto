# trading_crypto

## ngrok usage
```ngrok http --region=us --hostname=trad.ngrok.io 80```

## creds
https://docs.google.com/spreadsheets/d/1Qi0GCCCTr2NBMbw9poXRsdWbywQGGosXOiqoDDn_i0w/edit#gid=0
user = "trading.view.alerts777@gmail.com"
pwd = "syvxuc-vivxYq-2kuhfa"

## old instructions
```
user = "trading.view.alerts777@gmail.com"
pwd = "kaif666aA"
Это логин и пароль для авторизации в ngrok, trading view и google sheets

1. Устанавливаем Ngrok.exe https://dashboard.ngrok.com/get-started/setup
2. Запускаем Ngrok.exe, в командной строке вбиваем ngrok config add-authtoken 3XdC1NSkQug7veFTZDdKT_34NqWwWngcNsvk4qv6Azp
3. Далее вбиваем - ngrok http --region=us --hostname=trad.ngrok.io 80

for Google sheets:
4. Далее запускаем код и открыаем google sheets (или просто переходим по ссылке в коде)

for TradingView (needs to be revisited):
4. В командной строке появится строка Forwarding - берем из нее http адрес
5. Переход на сайт trading view, в alert - они обозначены иконкой в виде будльника и назвается "оповещения"
нажимаем на шестеренку - редактировать и добавляем адрес из ngrok в строку url Web hook
```
