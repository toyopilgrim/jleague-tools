## J League tool

This script generates J-league match days data in a nice json format. (J1 & J2 are currently supported. To see it further, look at `source.py`)

このスクリプトはJリーグの試合日程をまとまった以下の Json形式で生成します。(現在は J1, J2のみ対応。追加する場合は `source.py`)


```
[
    {
        "id": "nagasaki",
        "category": "j2",
        "matchDays": [
            {
                "location": "トラスタ",
                "date": "2021-02-27",
                "time": "14:03",
                "opponent": "金沢",
                "is_home": true
            },
            {
                "location": "デンカＳ",
                "date": "2021-03-06",
                "time": "13:33",
                "opponent": "新潟",
                "is_home": false
            },
        ]
    },
]
```

### Setup
Install dependencies. 

```
python3 pip install -m . 
```

Run script.
```
python3 j_calendar.py
```

