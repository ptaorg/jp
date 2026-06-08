(function(){
  'use strict';

  const site = {
    name: 'PTA適正化推進委員会',
    tagline: '任意加入・公私分離・個人情報・会費徴収を、一次資料と法令で整理する。',
    nav: [
      { id: 'home', label: 'トップ', href: 'index.html', group: 'main' },
      { id: 'parents', label: '保護者', href: 'parents.html', group: 'guide' },
      { id: 'pta', label: 'PTA役員', href: 'pta.html', group: 'guide' },
      { id: 'board', label: '教委・学校', href: 'board.html', group: 'guide' },
      { id: 'materials', label: '資料', href: 'materials.html', group: 'data' },
      { id: 'national', label: '全国PTA資料', href: 'national.html', group: 'data' },
      { id: 'articles', label: '論考', href: 'articles.html', group: 'data' },
      { id: 'responses', label: '回答集', href: 'responses.html', group: 'data' },
      { id: 'support', label: '応援', href: 'support.html', group: 'support' },
      { id: 'contact', label: '連絡', href: 'contact.html', group: 'support' }
    ],
    searchIndex: [
      { title: 'トップ', href: 'index.html', text: 'PTAが学校手続に溶け込む問題 任意加入 公私分離 会費 個人情報 教職員関与' },
      { title: '保護者の方へ', href: 'parents.html', text: '入会申込記録 学校徴収金 非会員 開示請求 学校への質問' },
      { title: 'PTA役員の方へ', href: 'pta.html', text: '自動加入停止 会費徴収分離 名簿取得 規約改正 学校依存からの移行' },
      { title: '教育委員会・学校管理職へ', href: 'board.html', text: '学校とPTAの公私分離 個人情報保護法 職務専念義務 施設利用 是正指導' },
      { title: '資料', href: 'materials.html', text: '行政資料 法令 文科省通知 個人情報保護委員会 社会教育法 学校教育法 働き方改革' },
      { title: '全国PTA資料', href: 'national.html', text: '学校別 PTA資料 自治体通知 入会案内 入会申込記録 会費徴収 役員選出' },
      { title: '論考', href: 'articles.html', text: '任意加入 公私分離 個人情報 会費徴収 教職員関与 学校施設利用 論考' },
      { title: '教育委員会回答集', href: 'responses.html', text: '自治体回答 入会意思確認 学校会費徴収 個人情報提供 教職員関与' },
      { title: '応援・寄付', href: 'support.html', text: '公文書開示 教育委員会訪問 旅費 資料整理 Web公開 調査継続' },
      { title: '連絡', href: 'contact.html', text: '情報提供 相談 資料提供 取材 教育委員会回答共有' }
    ]
  };

  function loadFixedLayout(){
    if(document.querySelector('link[href="css/fixed-layout.css"]')) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'css/fixed-layout.css';
    document.head.appendChild(link);
  }

  function esc(value){
    return String(value).replace(/[&<>'"]/g, char => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
    }[char]));
  }

  function isCurrent(item, current){
    return item.id === current;
  }

  function linkList(items, current, className){
    return items.map(item => {
      const active = isCurrent(item, current);
      const cls = className + (active ? ' is-active' : '');
      const aria = active ? ' aria-current="page"' : '';
      return `<a class="${cls}" href="${item.href}"${aria}>${item.label}</a>`;
    }).join('');
  }

  function renderHeader(){
    const host = document.getElementById('siteHeader');
    if(!host) return;

    const current = document.body.dataset.page || 'home';
    const primary = site.nav.filter(item => ['main','guide','data'].includes(item.group));
    const support = site.nav.filter(item => item.group === 'support');
    const allMobile = site.nav;

    host.innerHTML = `
      <a class="skip-link" href="#main">本文へ移動</a>
      <header class="site-header" role="banner">
        <div class="site-topline" aria-hidden="true"></div>
        <div class="header-inner">
          <a class="brand" href="index.html" aria-label="PTA適正化推進委員会トップへ">
            <span class="brand-mark">PTA</span>
            <span class="brand-copy">
              <span class="brand-name">${site.name}</span>
              <span class="brand-tagline">${site.tagline}</span>
            </span>
          </a>

          <nav class="desktop-nav" aria-label="主要ナビゲーション">
            ${linkList(primary, current, 'nav-link')}
          </nav>

          <div class="header-actions">
            <div class="search-wrap">
              <input class="search-input" type="search" placeholder="検索" aria-label="サイト内検索" autocomplete="off">
              <div class="search-results" aria-live="polite"></div>
            </div>
            <div class="support-links" aria-label="支援と連絡">
              ${linkList(support, current, 'support-link')}
            </div>
            <button class="menu-button" type="button" aria-controls="mobileNav" aria-expanded="false" aria-label="メニューを開閉">
              <span></span><span></span><span></span>
            </button>
          </div>
        </div>
        <nav class="mobile-nav" id="mobileNav" aria-label="スマートフォン用ナビゲーション">
          <div class="mobile-nav-inner">${linkList(allMobile, current, 'mobile-link')}</div>
        </nav>
      </header>`;
  }

  function renderFooter(){
    const host = document.getElementById('siteFooter');
    if(!host) return;

    host.innerHTML = `
      <footer class="site-footer" role="contentinfo">
        <div class="footer-inner">
          <div class="footer-main">
            <div class="footer-about">
              <div class="footer-title">PTA適正化推進委員会</div>
              <p>PTAの任意加入、学校とPTAの公私分離、個人情報、会費徴収、教職員関与、学校施設利用について、一次資料と法令に基づき整理します。</p>
            </div>
            <nav class="footer-nav" aria-label="フッターナビゲーション">
              <div>
                <strong>立場別</strong>
                <a href="parents.html">保護者の方へ</a>
                <a href="pta.html">PTA役員の方へ</a>
                <a href="board.html">教育委員会・学校管理職へ</a>
              </div>
              <div>
                <strong>資料・論考</strong>
                <a href="materials.html">資料</a>
                <a href="national.html">全国PTA資料</a>
                <a href="articles.html">論考</a>
                <a href="responses.html">回答集</a>
              </div>
              <div>
                <strong>活動</strong>
                <a href="support.html">応援・寄付</a>
                <a href="contact.html">連絡・情報提供</a>
              </div>
            </nav>
          </div>
          <div class="footer-bottom">
            <span>© PTA適正化推進委員会</span>
            <span>試験版です。事実認定、資料URL、法令・通知の引用箇所は公開前に再確認してください。</span>
          </div>
        </div>
      </footer>`;
  }

  function bindMenu(){
    const btn = document.querySelector('.menu-button');
    const nav = document.querySelector('.mobile-nav');
    if(!btn || !nav) return;
    btn.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      btn.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', event => {
      if(event.target.closest('a')){
        nav.classList.remove('is-open');
        btn.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  function bindSearch(){
    const input = document.querySelector('.search-input');
    const box = document.querySelector('.search-results');
    if(!input || !box) return;

    function close(){
      box.classList.remove('is-open');
      box.innerHTML = '';
    }

    input.addEventListener('input', () => {
      const q = input.value.trim().toLowerCase();
      if(!q){ close(); return; }
      const words = q.split(/\s+/).filter(Boolean);
      const hits = site.searchIndex.filter(item => {
        const haystack = (item.title + ' ' + item.text).toLowerCase();
        return words.every(word => haystack.includes(word));
      }).slice(0, 8);

      box.innerHTML = hits.length
        ? hits.map(item => `<a class="search-result" href="${item.href}"><strong>${esc(item.title)}</strong><span>${esc(item.text)}</span></a>`).join('')
        : '<div class="search-empty">該当するページが見つかりません。</div>';
      box.classList.add('is-open');
    });

    input.addEventListener('keydown', event => {
      if(event.key === 'Escape') close();
    });

    document.addEventListener('click', event => {
      if(!event.target.closest('.search-wrap')) close();
    });
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
    if(nav){
      slides.forEach((_, index) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'slide-dot' + (index === 0 ? ' is-active' : '');
        button.setAttribute('aria-label', `${index + 1}枚目のスライド`);
        button.addEventListener('click', () => setSlide(index));
        nav.appendChild(button);
        dots.push(button);
      });
    }
    window.setInterval(() => setSlide((current + 1) % slides.length), 6500);
  }

  document.addEventListener('DOMContentLoaded', () => {
    loadFixedLayout();
    renderHeader();
    renderFooter();
    bindMenu();
    bindSearch();
    bindHero();
  });
})();
