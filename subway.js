


document.addEventListener("DOMContentLoaded", function() {
  // Добавление класса show к тексту
  const flyInText = document.querySelector('.fly-in-text');
  setTimeout(() => {
    flyInText.classList.add('show');
  }, 100);

  // Добавление класса show к каждой картинке
  const flyInImages = document.querySelectorAll('.fly-in-image');
  flyInImages.forEach((image, index) => {
    setTimeout(() => {
      image.classList.add('show');
    }, 300 * (index + 1)); // Задержка для каждой картинки
  });
});


// Тексты для popup для каждой станции
const stationTexts = [
  "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod\
    tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,\
    quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo\
    consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse\
    cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non\
    proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
  "Описание станции 2"
  // Добавьте больше описаний для других станций здесь
];

function showPopup(index) {
  const popup = document.getElementById("popup");
  const popupText = document.getElementById("popup-text");
  const overlay = document.getElementById("overlay");

  // Устанавливаем текст для соответствующей станции
  popupText.textContent = stationTexts[index];
  
  // Отображаем overlay и popup с анимацией
  overlay.style.display = "block";
  setTimeout(() => {
    overlay.classList.add("show");
  }, 10); // Задержка для запуска анимации

  popup.style.display = "block";
  setTimeout(() => {
    popup.classList.add("show");
  }, 10);
}

function closePopup() {
  const popup = document.getElementById("popup");
  const overlay = document.getElementById("overlay");

  // Скрываем overlay и popup с анимацией
  popup.classList.remove("show");
  overlay.classList.remove("show");

  // Ждём завершения анимации перед полным скрытием
  setTimeout(() => {
    popup.style.display = "none";
    overlay.style.display = "none";
  }, 500); // Время совпадает с transition в CSS
}
