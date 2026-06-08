(function(){
  const site = {
    name: 'PTA適正化推進委員会',
    sub: '任意加入・公私分離・個人情報・会費徴収',
    nav: [
      {id:'home', label:'トップ', href:'index.html'},
      {id:'parents', label:'保護者', href:'parents.html'},
      {id:'pta', label:'PTA役員', href:'pta.html'},
      {id:'board', label:'教委・学校', href:'board.html'},
      {id:'materials', label:'資料', href:'materials.html'},
      {id:'responses', label:'回答集', href:'responses.html'},
      {id:'contact', label:'連絡', href:'contact.html'}
    ],
    index: [
      {title:'トップ', href:'index.html', text:'PTAが学校手続に溶け込む問題、任意加入、公私分離、会費、個人情報、教職員関与'},
      {title:'保護者の方へ', href:'parents.html', text:'入会申込記録、学校徴収金、非会員の扱い、開示請求、学校への質問'},
      {title:'PTA役員の方へ', href:'pta.html', text:'自動加入の停止、会費徴収の分離、名簿取得、規約改正、学校依存からの移行'},
      {title:'教育委員会・学校管理職へ', href:'board.html', text:'学校とPTAの公私分離、個人情報保護法、職務専念義務、施設利用、是正指導'},
      {title:'資料', href:'materials.html', text:'行政資料、文科省通知、個人情報保護委員会、社会教育法、学校教育法、働き方改革'},
      {title:'教育委員会回答集', href:'responses.html', text:'自治体回答、任意加入、入会意思確認、学校による会費徴収、個人情報提供'},
      {title:'連絡', href:'contact.html', text:'情報提供、相談、資料提供、取材、教育委員会回答共有'}
    ]
  };
  function esc(s){return String(s).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));}
  function renderHeader(){
    const current = document.body.dataset.page || '';
    const nav = site.nav.map(item=>`<a class="nav-link${item.id===current?' is-active':''}" href="${item.href}">${item.label}</a>`).join('');
    const mobile = site.nav.map(item=>`<a href="${item.href}"${item.id===current?' aria-current="page"':''}>${item.label}</a>`).join('');
    const html = `
      <a class="skip-link" href="#main">本文へ移動</a>
      <header class="site-header">
        <div class="header-bar" aria-hidden="true"></div>
        <div class="header-inner">
          <a class="brand" href="index.html" aria-label="PTA適正化推進委員会トップへ">
            <span class="brand-mark">PTA</span>
            <span><span>${site.name}</span><span class="brand-sub">${site.sub}</span></span>
          </a>
          <nav class="desktop-nav" aria-label="主要ナビゲーション">${nav}</nav>
          <div class="header-tools">
            <div class="search-wrap">
              <input class="search-input" type="search" placeholder="サイト内検索" aria-label="サイト内検索">
              <div class="search-results" aria-live="polite"></div>
            </div>
            <button class="menu-button" type="button" aria-controls="mobileNav" aria-expanded="false" aria-label="メニューを開閉"><span></span><span></span><span></span></button>
          </div>
        </div>
        <nav class="mobile-nav" id="mobileNav" aria-label="スマートフォン用ナビゲーション"><div class="mobile-nav-inner">${mobile}</div></nav>
      </header>`;
    document.getElementById('siteHeader').innerHTML = html;
  }
  function renderFooter(){
    const html = `
      <footer class="site-footer">
        <div class="footer-inner">
          <div class="footer-grid">
            <div>
              <div class="footer-title">PTA適正化推進委員会</div>
              <p>PTAの任意加入、学校とPTAの公私分離、個人情報、会費徴収、教職員関与、学校施設利用について、一次資料と法令に基づき整理します。</p>
            </div>
            <div>
              <div class="footer-title">主要ページ</div>
              <nav class="footer-nav" aria-label="フッターナビゲーション">
                <a href="parents.html">保護者の方へ</a>
                <a href="pta.html">PTA役員の方へ</a>
                <a href="board.html">教育委員会・学校管理職へ</a>
                <a href="materials.html">資料</a>
                <a href="responses.html">回答集</a>
              </nav>
            </div>
            <div>
              <div class="footer-title">連絡</div>
              <p><a href="mailto:info@ptaorg.com">info@ptaorg.com</a></p>
              <p><a href="contact.html">情報提供・取材・相談の窓口</a></p>
            </div>
          </div>
          <div class="footer-small">© PTA適正化推進委員会. 本試験版は構造整理用の静的HTMLです。事実認定・資料URLは公開前に再確認してください。</div>
        </div>
      </footer>`;
    document.getElementById('siteFooter').innerHTML = html;
  }
  function bindMenu(){
    const btn = document.querySelector('.menu-button');
    const nav = document.querySelector('.mobile-nav');
    if(!btn || !nav) return;
    btn.addEventListener('click',()=>{
      const open = nav.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  function bindSearch(){
    const input = document.querySelector('.search-input');
    const box = document.querySelector('.search-results');
    if(!input || !box) return;
    function close(){box.classList.remove('is-open');box.innerHTML='';}
    input.addEventListener('input',()=>{
      const q = input.value.trim().toLowerCase();
      if(!q){close();return;}
      const words = q.split(/\s+/).filter(Boolean);
      const hits = site.index.filter(item=>words.every(w=>(item.title+' '+item.text).toLowerCase().includes(w))).slice(0,6);
      box.innerHTML = hits.length ? hits.map(item=>`<a class="search-result" href="${item.href}"><strong>${esc(item.title)}</strong><span>${esc(item.text)}</span></a>`).join('') : '<div class="search-empty">該当するページが見つかりません。</div>';
      box.classList.add('is-open');
    });
    document.addEventListener('click',e=>{if(!e.target.closest('.search-wrap')) close();});
    input.addEventListener('keydown',e=>{if(e.key==='Escape') close();});
  }
  document.addEventListener('DOMContentLoaded',()=>{renderHeader();renderFooter();bindMenu();bindSearch();});
})();
