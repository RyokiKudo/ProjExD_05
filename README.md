
# アンチヒーロー

## 実行環境の必要条件
* python >= 3.10
* pygame >= 2.1

## ゲームの概要
主人公キャラクター魔王が城を攻めてきた勇者一行を迎え撃つゲーム。

## ゲームの実装
### 共通基本機能
* 背景画像と主要キャラの実装
* 背景画像と主人公キャラクターと戦士(雑魚)の描画

### 担当追加機能
* スコアとレベルアップ機能:スコアの表示とスコアに応じてレベルが上がり魔王が進化する機能(担当:喜佐見)
* 敵キャラの出現、魔王と敵キャラの移動プレイアブルとなる魔王のクラス、移動する敵キャラのクラス(担当：戸塚)
* 魔王のHP表示クラスの制作(担当：大野)
* ビーム機能：魔王がビームを出す機能。レベルに応じて進化する。(担当：小坂)
* エネミー(担当：工藤)：魔王に倒す戦士達を表示する機能、大きさをランダム

### ToDo
- [ ] まだ作られていないがHPを追加したらレベルが上がった時にHPを増やす機能(実装済み)
- [ ] 魔王の体力の追加（実装済み）

### メモ
* maouクラスにchange_imgを追加し、魔王を進化するときに用いる画像maou2.pngを追加してある。
* zakoとenemysのところは、コンフリクト関係でコメントで印を付けています。