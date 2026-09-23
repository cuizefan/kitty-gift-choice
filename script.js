const coverScreen = document.getElementById('cover-screen');
const giftScreen = document.getElementById('gift-screen');
const letterScreen = document.getElementById('letter-screen');
const yesBtn = document.querySelector('.choice-affirm');
const noBtn = document.querySelector('.choice-deny');
const giftItems = document.querySelectorAll('.gift-item');
const giftNameLabel = document.getElementById('selected-gift-name');
const letterBackBtn = document.querySelector('.letter-btn.back');
const letterConfirmBtn = document.querySelector('.letter-btn.confirm');
const screens = document.querySelectorAll('.screen');
const giftResult = document.getElementById('gift-result');

function showScreen(targetScreen) {
  screens.forEach((screen) => {
    const isActive = screen === targetScreen;
    screen.classList.toggle('active', isActive);
    screen.style.opacity = isActive ? '1' : '0';
    screen.style.visibility = isActive ? 'visible' : 'hidden';
    screen.style.transform = isActive ? 'translateY(0) scale(1)' : 'translateY(22px) scale(0.96)';
  });
}

async function fetchGiftResult() {
  if (!giftResult) return;

  try {
    const response = await fetch('/gift-result');
    const data = await response.json();
    giftResult.textContent = data.gift || '等待确认中...';
  } catch (error) {
    giftResult.textContent = '等待确认中...';
  }
}

if (yesBtn && noBtn) {
  noBtn.addEventListener('click', () => {
    yesBtn.classList.remove('is-bigger');
    void yesBtn.offsetWidth;
    yesBtn.classList.add('is-bigger');
    setTimeout(() => {
      yesBtn.classList.remove('is-bigger');
    }, 700);
  });

  yesBtn.addEventListener('click', () => {
    showScreen(giftScreen);
  });
}

giftItems.forEach((item) => {
  item.addEventListener('click', () => {
    giftItems.forEach((next) => next.classList.remove('active'));
    item.classList.add('active');

    const giftName = item.dataset.name || '礼物';
    if (giftNameLabel) {
      giftNameLabel.textContent = giftName;
    }

    showScreen(letterScreen);
  });
});

if (letterBackBtn) {
  letterBackBtn.addEventListener('click', () => {
    showScreen(giftScreen);
  });
}

if (letterConfirmBtn) {
  letterConfirmBtn.addEventListener('click', async () => {
    const selectedGift = giftNameLabel ? giftNameLabel.textContent : '礼物';
    localStorage.setItem('selectedGift', selectedGift);

    try {
      const response = await fetch('/save-gift', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ gift: selectedGift })
      });

      const data = await response.json();
      alert(`已收到：${data.gift || selectedGift}`);
    } catch (error) {
      alert(`已收到：${selectedGift}`);
    }
  });
}

if (giftResult) {
  fetchGiftResult();
  setInterval(fetchGiftResult, 2000);
}
