中文|[ENGLISH](https://github.com/iii-org/gpt-inside-openai/blob/master/README_EN.md)

# 簡介

提供企業便利的開源GPT訓練工具，可快速透過excel版型導入企業自有資料，使企業可快速將資料接上chat gpt模型。未來可結合本計畫研發的對話驗證技術，打造可信任的AI對話生成服務，更多的介紹請參考本工具之[介紹網站](http://www.openiii.org/)。

本工具由[中華民國數位發展部數位產業署(ADI)](https://moda.gov.tw/ADI/)支持開發
# 目錄

* 系統環境需求
* 安裝
* 訓練
* 推論

# 系統環境需求
系統硬體部分，可選擇本機端或是雲端的運算資源，詳情如下所示。
### 硬體


|         | 最低需求            | 建議需求            |
| :-------- | --------------------- | --------------------- |
| CPU     | 4 core             | 8 core             |
| Memory  | 8 G               | 16G                 |
| Storage | 256G                | 512G                |


# 訓練資料格式

以衛生福利部國民健康署提供的[孕婦衛教手冊](https://www.hpa.gov.tw/Pages/EBook.aspx?nodeid=1454)問答為例，格式如```data/raw_data.xlsx```所示。每一列資料為一則的問答，每個欄位之定義如下：


| 欄位名稱      | 欄位定義   | 欄位範例                                                  |
| :-------------- | ------------ | ----------------------------------------------------------- |
| Q      | 問題    | 在哪個孕期進行高層次超音波檢查？          |
| A      | 回應    | 建議於懷孕20~24週進行。                                                      |
| REF    | 參考資料 | 高層次超音波能清楚顯示胎兒影像，建議於懷孕20~24週進行。這是屬於自費檢查項目，孕婦可以考慮自身狀況，決定是否接受。高層次超音波依規定不可用來判定胎兒性別。若孕婦身體不適或胎兒有特殊狀況，可與醫師討論檢查的頻率及次數。發現胎兒畸形時，請諮詢相關專科醫師。 |

# 快速開始
首先，您需要確認您的OpenAI推論引擎，及編碼引擎是否可用，確認完成後在Ubuntu 20.04 TLS作業系統中，於命令列執行以下指令：
```
bash run_service.sh -i 127.0.0.1 -d ./data/raw_data.xlsx -b {your openai api base} -t azure -v {your openai api version} -k {your openai api key} -e {your openai api engine} -c {your openai api embedding engine}
```
其中：
- -i: 機器的IP位置，預設為本機端，若網頁介面需提供給其他外部機器使用，則需設置一個可對外的IP位置
- -d: 資料存儲路徑
- -b: openai的api網址
- -t: openai的類型，目前僅支援azure或是openai
- -v: openai的api版本
- -k: openai的api金鑰
- -e: openai的api引擎
- -c: openai的api編碼引擎
- -s: 跳過訓練/推論階段(-s skip-train/skip-inference)

該指令將會自動安裝環境並訓練模型，訓練完成後可在畫面上看到以下訊息
```
Please enter the URL link below into your browser to activate the dialog interface
    URL link: http://127.0.0.1/gpt/qa/
```
請將URL link複製並貼到瀏覽器的網址列上，即可開始進行問答

### 僅啟動網頁服務
在命令列執行以下指令：
```
bash run_service.sh -i 127.0.0.1 -d ./data/raw_data.xlsx -b {your openai api base} -t azure -v {your openai api version} -k {your openai api key} -e {your openai api engine} -c {your openai api embedding engine} -s skip-train
```
該指令將會跳過訓練階段，直接使用現有模型啟動網頁服務

### 關閉系統服務
在命令列執行以下指令：
```
bash stop_service.sh
```
