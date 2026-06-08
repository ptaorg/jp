(function(){
  'use strict';

  const pages = [
    ['トップ','index.html'],
    ['保護者','parents.html'],
    ['PTA役員','pta.html'],
    ['教委・学校','board.html'],
    ['資料','materials.html'],
    ['全国PTA資料','national.html'],
    ['論考','articles.html'],
    ['回答集','responses.html'],
    ['応援','support.html'],
    ['連絡','contact.html']
  ];

  const searchIndex = [
    { title:'トップ', href:'index.html', text:'PTA 任意加入 公私分離 個人情報 会費徴収 教職員関与' },
    { title:'保護者の方へ', href:'parents.html', text:'入会申込記録 学校徴収金 非会員 開示請求' },
    { title:'PTA役員の方へ', href:'pta.html', text:'自動加入 名簿 会費 規約 学校依存' },
    { title:'教育委員会・学校管理職へ', href:'board.html', text:'学校 PTA 分離 個人情報 職務専念 施設利用' },
    { title:'資料', href:'materials.html', text:'行政資料 法令 通知 個人情報 社会教育法 学校教育法' },
    { title:'全国PTA資料', href:'national.html', text:'学校別 自治体別 入会案内 会費徴収 役員選出' },
    { title:'論考', href:'articles.html', text:'任意加入 公私分離 個人情報 会費徴収 教職員関与' },
    { title:'教育委員会回答集', href:'responses.html', text:'自治体回答 入会意思確認 会費徴収 名簿提供' },
    { title:'応援・寄付', href:'support.html', text:'公文書開示 教育委員会訪問 旅費 資料整理' }
  ];

  function loadFixedLayout(){
    if(document.querySelector('link[href="css/fixed-layout.css"]')) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'css/fixed-layout.css';
    document.head.appendChild(link);
  }

  function esc(value){
    return String(value).replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
  }

  function activeFor(href){
    const path = location.pathname.split('/').pop() || 'index.html';
    return path === href ? ' is-active' : '';
  }

  function mobileLinks(){
    return pages.map(([label,href]) => `<a class="mobile-link${activeFor(href)}" href="${href}">${label}</a>`).join('');
  }

  function renderHeader(){
    const host = document.getElementById('siteHeader');
    if(!host) return;
    host.innerHTML = `
      <a class="skip-link" href="#main">本文へ移動</a>
      <header class="site-header main-header" role="banner">
        <div class="nav-container">
          <a class="logo" href="index.html" aria-label="PTA適正化推進委員会トップへ">
            <img alt="PTA適正化推進委員会ロゴ" src="https://ptaorg.com/assets/popc-logo.png">
            <span>PTA適正化推進委員会</span>
          </a>
          <div class="header-search">
            <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.35-4.35"></path></svg>
            <input aria-label="サイト内検索" class="search-input" placeholder="キーワードで検索…" type="text">
            <div class="search-results-dropdown" aria-live="polite"></div>
          </div>
          <nav aria-label="主要ナビゲーション" class="desktop-nav main-desktop-nav">
            <a class="nav-link${activeFor('index.html')}" href="index.html">トップ</a>
            <div class="nav-item has-dropdown">
              <a class="nav-link" href="parents.html">立場別入口</a>
              <div class="mega-menu">
                <div class="mega-col"><h4>立場別ガイド</h4><ul><li><a href="parents.html">保護者の方へ</a></li><li><a href="pta.html">PTA役員の方へ</a></li><li><a href="board.html">学校・教育委員会の方へ</a></li></ul></div>
              </div>
            </div>
            <div class="nav-item has-dropdown">
              <a class="nav-link" href="materials.html">資料</a>
              <div class="mega-menu mega-menu-wide">
                <div class="mega-col"><h4>証拠資料</h4><ul><li><a href="responses.html">教育委員会の回答</a></li><li><a href="national.html">全国PTA資料</a></li><li><a href="materials.html">行政資料・法令</a></li></ul></div>
                <div class="mega-col"><h4>論点別</h4><ul><li><a href="parents.html">入会手続</a></li><li><a href="materials.html">個人情報</a></li><li><a href="board.html">教職員関与・施設利用</a></li></ul></div>
              </div>
            </div>
            <div class="nav-item has-dropdown">
              <a class="nav-link" href="articles.html">研究論考</a>
              <div class="mega-menu">
                <div class="mega-col"><h4>研究・論考</h4><ul><li><a href="articles.html">論考・調査報告</a></li><li><a href="materials.html">法制度資料</a></li><li><a href="responses.html">回答分析</a></li></ul></div>
              </div>
            </div>
            <a class="nav-link${activeFor('support.html')} support-nav-link" href="support.html">応援</a>
            <a class="btn-gold" href="contact.html">情報提供</a>
          </nav>
          <button class="hamburger" type="button" aria-controls="mobileNav" aria-expanded="false" aria-label="メニューを開閉"><span></span><span></span><span></span></button>
        </div>
        <nav class="mobile-nav" id="mobileNav" aria-label="スマートフォン用ナビゲーション"><div class="mobile-nav-inner">${mobileLinks()}</div></nav>
      </header>`;
  }

  function renderFooter(){
    const host = document.getElementById('siteFooter');
    if(!host) return;
    host.innerHTML = `
      <footer class="footer site-footer" role="contentinfo">
        <div class="footer-inner">
          <div class="footer-grid">
            <div>
              <h3>PTA適正化推進委員会</h3>
              <div class="footer-contact">
                <p>〒235-0021<br>神奈川県横浜市磯子区岡村8-17-5-301</p>
                <p><strong>070-9012-7772</strong></p>
                <p><a href="mailto:info@ptaorg.com">info@ptaorg.com</a></p>
              </div>
              <a class="yokomusubi-img-link" href="https://yokomusubi.city.yokohama.lg.jp/organizations/detail/f69c7ad2-cf21-4dfa-87bb-9c891874eb6b/" rel="noopener noreferrer" target="_blank">
                <img alt="よこむすび" src="https://ptaorg.com/assets/yokomusubi.png">
              </a>
              <p class="yokomusubi-tagline-out">磯子区「よこむすび」掲載団体</p>
              <p class="yokomusubi-meta-out">登録番号：磯子12406　分類番号：12-4（市民活動・社会教育推進）</p>
            </div>
            <div>
              <h4>公式発信</h4>
              <p class="footer-sns-sub">最新資料・論考・動画はこちら</p>
              <div class="footer-sns-cards">
                <a class="fsns-card fsns-x" href="https://x.com/jjjqqqxxx0852" rel="noopener" target="_blank"><span class="fsns-icon">X</span><span><span class="fsns-name">X</span><span class="fsns-desc">速報・資料更新</span></span></a>
                <a class="fsns-card fsns-yt" href="https://www.youtube.com/@PTA%E9%81%A9%E6%AD%A3%E5%8C%96%E6%8E%A8%E9%80%B2%E5%A7%94%E5%93%A1%E4%BC%9A" rel="noopener" target="_blank"><span class="fsns-icon">▶</span><span><span class="fsns-name">YouTube</span><span class="fsns-desc">動画で解説</span></span></a>
                <a class="fsns-card fsns-note" href="https://note.com/hiroshisatoh" rel="noopener" target="_blank"><span class="fsns-icon">n</span><span><span class="fsns-name">note</span><span class="fsns-desc">論考・研究ノート</span></span></a>
              </div>
            </div>
            <div>
              <h4>立場別</h4>
              <ul><li><a href="parents.html">保護者</a></li><li><a href="pta.html">PTA役員</a></li><li><a href="board.html">教育委員会・学校</a></li><li><a href="board.html">教育委員会向け指針</a></li></ul>
            </div>
            <div>
              <h4>論点</h4>
              <ul><li><a href="parents.html">入会手続</a></li><li><a href="materials.html">個人情報</a></li><li><a href="parents.html">会費徴収</a></li><li><a href="board.html">教職員関与</a></li><li><a href="board.html">施設利用</a></li></ul>
            </div>
            <div>
              <h4>資料・支援</h4>
              <ul><li><a href="support.html">応援・寄付</a></li><li><a href="responses.html">教育委員会の回答</a></li><li><a href="national.html">全国PTA資料</a></li><li><a href="articles.html">論考・調査報告</a></li><li><a href="materials.html">資料</a></li></ul>
            </div>
          </div>
          <div class="footer-support"><div><strong>調査・資料公開の継続を応援してください</strong><p>いただいたご支援は、公文書開示、資料整理、Web公開、自治体・学校への働きかけに活用します。</p></div><a href="support.html">応援ページへ</a></div>
          <p class="copyright">© PTA適正化推進委員会</p>
        </div>
      </footer>`;
  }

  function bindMenu(){
    const btn = document.querySelector('.hamburger');
    const nav = document.querySelector('.mobile-nav');
    if(!btn || !nav) return;
    btn.addEventListener('click', () => { const open = nav.classList.toggle('is-open'); btn.classList.toggle('is-open', open); btn.setAttribute('aria-expanded', open ? 'true' : 'false'); });
    nav.addEventListener('click', event => { if(event.target.closest('a')){ nav.classList.remove('is-open'); btn.classList.remove('is-open'); btn.setAttribute('aria-expanded','false'); } });
  }

  function bindSearch(){
    const input = document.querySelector('.search-input');
    const box = document.querySelector('.search-results-dropdown') || document.querySelector('.search-results');
    if(!input || !box) return;
    function close(){ box.classList.remove('is-open'); box.innerHTML = ''; }
    input.addEventListener('input', () => {
      const q = input.value.trim().toLowerCase();
      if(!q){ close(); return; }
      const words = q.split(/\s+/).filter(Boolean);
      const hits = searchIndex.filter(item => words.every(word => (item.title + ' ' + item.text).toLowerCase().includes(word))).slice(0, 8);
      box.innerHTML = hits.length ? hits.map(item => `<a class="search-result" href="${item.href}"><strong>${esc(item.title)}</strong><span>${esc(item.text)}</span></a>`).join('') : '<div class="search-empty">該当するページが見つかりません。</div>';
      box.classList.add('is-open');
    });
    document.addEventListener('click', event => { if(!event.target.closest('.header-search')) close(); });
  }

  function bindHero(){
    const slides = document.querySelectorAll('#heroSlideshow .slide');
    const nav = document.getElementById('slideNav');
    if(!slides.length) return;
    const dots = [];
    let current = 0;
    function setSlide(next){
      slides[current].classList.remove('is-active');
      if(dots[current]) dots[current].classList.remove('is-active');
      current = next;
      slides[current].classList.add('is-active');
      if(dots[current]) dots[current].classList.add('is-active');
    }
    if(nav && !nav.children.length){
      slides.forEach((_, index) => { const button = document.createElement('button'); button.type = 'button'; button.className = 'slide-dot' + (index === 0 ? ' is-active' : ''); button.setAttribute('aria-label', `${index + 1}枚目のスライド`); button.addEventListener('click', () => setSlide(index)); nav.appendChild(button); dots.push(button); });
    }
    window.setInterval(() => setSlide((current + 1) % slides.length), 6500);
  }

  document.addEventListener('DOMContentLoaded', () => { loadFixedLayout(); renderHeader(); renderFooter(); bindMenu(); bindSearch(); bindHero(); });
})();
