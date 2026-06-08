PTA適正化推進委員会サイト 構造再設計版（試験用）

目的
- ページごとにヘッダー、フッター、ナビ、余白、色が変わる問題を解消する。
- 入口ページやカード型ハブを増やさず、本文で論理を読ませる構造に戻す。
- GitHub Pages にそのまま置ける静的HTMLとして構成する。

主な構成
- index.html：トップ。問題の核心と三つの立場別入口。
- parents.html：保護者向け。入会申込記録、会費、名簿、学校への確認。
- pta.html：PTA役員向け。自動加入停止、会費分離、名簿取得、規約改正。
- board.html：教育委員会・学校管理職向け。学校が是正できる範囲、公私分離。
- materials.html：資料台帳。行政資料、法令、通知、PPC資料、働き方改革資料の分類。
- responses.html：教育委員会回答集の掲載形式。
- contact.html：連絡窓口。
- 旧URL互換用の薄いリダイレクトHTMLを同梱。

共通化
- css/site.css：全ページ共通のデザイン、本文、表、フッター、レスポンシブを管理。
- js/common.js：全ページ共通のヘッダー、フッター、ナビ、検索、スマホメニューを生成。
- 各HTMLにはヘッダー・フッターを直接書かず、<div id="siteHeader"></div> と <div id="siteFooter"></div> だけを置く。

変更しない範囲
- 既存のPDF、Excel、画像、動画、教育委員会回答本文、全国資料本文は入れていない。
- 未確認URLや未確認資料名は断定していない。
- 現行リポジトリへ直接pushしていない。

ブラウザ確認
- ローカル静的ファイルとしてのHTML構造、内部リンク、共通CSS/JS参照を検査済み。
- 実ブラウザでの目視確認は、この環境では未実施。

アップロード方法
1. 新しいテスト用リポジトリを作る。
2. ZIP内の全ファイルをリポジトリ直下に置く。
3. GitHub Pages を main / root で有効化する。
4. index.html、parents.html、pta.html、board.html、materials.html、responses.html、contact.html を確認する。
