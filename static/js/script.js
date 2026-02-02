let slideIndex = 0;
const slides = [
  '/static/images/slider1.png',
  '/static/images/slider2.png',
  '/static/images/slider3.jpg',
  '/static/images/slider4.jfif',
  '/static/images/slider5.jfif'
];

  


function showSlides() {
  document.getElementById("slideImg").src = slides[slideIndex];
  slideIndex = (slideIndex + 1) % slides.length;
  setTimeout(showSlides, 3000);
}
showSlides();

function togglePassword() {
  const pw = document.querySelector('input[name="password"]');
  pw.type = pw.type === "password" ? "text" : "password";
}
