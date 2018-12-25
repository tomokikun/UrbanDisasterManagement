# UrbanDisasterManagement
This repository is for the script to calculate seismic intensity for an assignment of Urban Disaster Management.

# 課題
計測震度の算出および最大加速度、最大速度などとの対応の確認。

- 気象庁の計測震度を算出し、震度階を調べる
- 対象は、熊本地震の本震や前震で観測された地震動とする
気象庁、防災科学技術研究所などが公開している強震動記録
- 得られた震度階もしくは計測震度と最大加速度、最大速度などとどのような対応になっているかを確
認をする

# 各種リンク

[気象庁「計測震度の算出方法」](http://www.data.jma.go.jp/svd/eqev/data/kyoshin/kaisetsu/calc_sindo.htm)

[気象庁「主な地震の強震観測データ」](http://www.data.jma.go.jp/svd/eqev/data/kyoshin/jishin/index.html)

[防災科学技術研究所「強震観測網 K-NET, KiK-net」](http://www.kyoshin.bosai.go.jp/kyoshin/ )


# テスト
[気象庁の計測震度の算出方法のページ](http://www.data.jma.go.jp/svd/eqev/data/kyoshin/kaisetsu/calc_sindo.htm)に掲載されている例を用いて、
コードのテストを行った。
この例では、[2000年10月6日に発生した鳥取県西部地震の米子市（計測震度＝5.1）](http://www.data.jma.go.jp/svd/eqev/data/kyoshin/jishin/001006_tottori-seibu/dat/AA06EA01.csv)のデータを用いている。

- 手順 5 において、ａ＝127.85 gal
- 手順 6 において、I~5.1

以上の2点を満たすことをテストした。

    
# 使用データについて

テスト データとして、[2000年10月6日に発生した鳥取県西部地震の米子市（計測震度＝5.1）](http://www.data.jma.go.jp/svd/eqev/data/kyoshin/jishin/001006_tottori-seibu/dat/AA06EA01.csv)を使用。

実際の計測震度の計算用データとして、[2016年4月14日 熊本県熊本地方の地震](http://www.data.jma.go.jp/svd/eqev/data/kyoshin/jishin/1604142126_kumamoto/data/Q4149CF2.csv)を使用した。
以下、使用した計算用データの詳細。

|都道府県|観測点名|震度	|計測震度|最大加速度（gal=cm/s2）|震央距離（km)|３成分合成|南北|東西|上下|ファイル名|
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
|熊本県|宇城市松橋町|６弱|5.7|364.5|327.1|280.9|220.9|15.8|Q4149CF2.csv|
|熊本県|南阿蘇村中松|５強|5.0|357.3|246.2|297.8|133.0|19.8|Q416EED018.csv|
|熊本県|上天草市大矢野町|５弱|4.6|132.6|118.8|75.4|34.5|Q4169D2004.csv|	
