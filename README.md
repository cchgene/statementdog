##If in local mode
use crontab or airflow

create crawler.sh
/usr/bin/python3 /Users/Desktop/statementdog/listed.py
/usr/bin/python3 /Users/Desktop/statementdog/industry_top3.py

> crontab -e
0 18 * * * /usr/bin/bash crawler.sh


##IF in AWS
suggest use lambda


第二題
1.本次執行結果是先存成file, 照理說應該因應DB塞進去
2.deploy 將來應該會打包成setup.py
3.雲端會使用lambda
4.將來會再加入測試，因為這次時間不足，沒有寫上去
5.如果資料來源只有一個網站，又要大量爬取，下次可能會改成邊寫檔案，這樣一來若是哪裡有缺也不用整個重跑
