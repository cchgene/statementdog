## If in local
use crontab or airflow

> crontab -e
```
0 18 * * * /usr/bin/bash /Users/Desktop/statementdog/scripts/crawler.sh
```

## IF in cloud
suggest use lambda


第二題
1.本次執行結果是先存成file, 後續可以因應DB做動作

2.deploy 將來應該會打包成setup.py

3.雲端會使用lambda

4.將來會再加入測試，因為這次時間不足，沒有寫上去

