
document.addEventListener("DOMContentLoaded", () => {
    const lightbox = document.getElementById("gallery-lightbox");
    if (!lightbox) return;

    const track = lightbox.querySelector(".lightbox-track");
    const currentImage = lightbox.querySelector(".lightbox-current");
    const adjacentImage = lightbox.querySelector(".lightbox-adjacent");
    const closeButton = lightbox.querySelector(".lightbox-close");
    const prevButton = lightbox.querySelector(".lightbox-prev");
    const nextButton = lightbox.querySelector(".lightbox-next");
    const galleryButtons = [...document.querySelectorAll(".gallery-item")];

    if (!track || !currentImage || !adjacentImage || !galleryButtons.length) return;

    let currentIndex = 0;
    let previousFocus = null;
    let startX = 0;
    let startY = 0;
    let dragX = 0;
    let dragging = false;
    let animating = false;
    let swipeDirection = -1;
    let animationTimer = null;

    const indexOf = index =>
        (index + galleryButtons.length) % galleryButtons.length;

    function setImage(image, index) {
        const button = galleryButtons[indexOf(index)];
        image.src = button.dataset.fullImage;
        image.alt = button.querySelector("img").alt;
    }

    function resetPositions() {
        currentImage.style.transition = "none";
        adjacentImage.style.transition = "none";
        currentImage.style.transform = "translateX(0)";
        adjacentImage.style.transform = "translateX(100%)";
    }

    function showImage(index) {
        currentIndex = indexOf(index);
        setImage(currentImage, currentIndex);
        setImage(adjacentImage, currentIndex + 1);
        resetPositions();
    }

    function openLightbox(index) {
        previousFocus = galleryButtons[index];
        showImage(index);
        lightbox.hidden = false;
        document.body.style.overflow = "hidden";
        closeButton.focus();
    }

    function closeLightbox() {
        clearTimeout(animationTimer);

        animating = false;
        dragging = false;
        dragX = 0;

        lightbox.hidden = true;

        currentImage.src = "";
        adjacentImage.src = "";

        currentImage.style.transition = "none";
        adjacentImage.style.transition = "none";
        currentImage.style.transform = "translateX(0)";
        adjacentImage.style.transform = "translateX(100%)";

        document.body.style.overflow = "";

        if (previousFocus) {
            previousFocus.focus();
        }
    }

    function prepareAdjacent(direction) {
        swipeDirection = direction;
        setImage(adjacentImage, currentIndex + (direction === -1 ? 1 : -1));
        adjacentImage.style.transition = "none";
        adjacentImage.style.transform =
            `translateX(${-direction * track.clientWidth}px)`;
    }

    function animateTo(direction) {
        if (animating) return;

        animating = true;
        dragging = false;

        const width = track.clientWidth;
        const duration = "transform 250ms ease-out";

        currentImage.style.transition = duration;
        adjacentImage.style.transition = duration;

        if (direction === 0) {
            currentImage.style.transform = "translateX(0)";
            adjacentImage.style.transform =
                `translateX(${-swipeDirection * width}px)`;
        } else {
            currentImage.style.transform = `translateX(${direction * width}px)`;
            adjacentImage.style.transform = "translateX(0)";
        }

        clearTimeout(animationTimer);
        animationTimer = setTimeout(() => {
            if (lightbox.hidden) return;

            if (direction !== 0) {
                currentIndex = indexOf(currentIndex + (direction === -1 ? 1 : -1));
            }

            setImage(currentImage, currentIndex);
            setImage(adjacentImage, currentIndex + 1);
            resetPositions();

            animating = false;
            swipeDirection = -1;
        }, 270);
    }

    function startDrag(event) {
        if (animating || event.touches.length !== 1) return;

        startX = event.touches[0].clientX;
        startY = event.touches[0].clientY;
        dragX = 0;
        dragging = true;
        swipeDirection = 0;

        currentImage.style.transition = "none";
        adjacentImage.style.transition = "none";
    }

    function moveDrag(event) {
        if (!dragging || event.touches.length !== 1) return;

        const dx = event.touches[0].clientX - startX;
        const dy = event.touches[0].clientY - startY;

        if (Math.abs(dy) > Math.abs(dx) && Math.abs(dy) > 8) {
            dragging = false;
            resetPositions();
            return;
        }

        dragX = dx;
        const direction = dx < 0 ? -1 : 1;

        if (direction !== swipeDirection) {
            prepareAdjacent(direction);
        }

        const width = track.clientWidth;
        currentImage.style.transform = `translateX(${dx}px)`;
        adjacentImage.style.transform =
            `translateX(${dx - direction * width}px)`;
    }

    function endDrag() {
        if (!dragging) return;

        const threshold = Math.min(track.clientWidth * 0.2, 100);

        if (Math.abs(dragX) >= threshold) {
            animateTo(dragX < 0 ? -1 : 1);
        } else {
            animateTo(0);
        }
    }

    function changeBy(direction) {
        if (animating) return;

        // Влево: следующая фотография. Вправо: предыдущая.
        prepareAdjacent(direction);
        currentImage.style.transition = "none";
        currentImage.style.transform = "translateX(0)";

        requestAnimationFrame(() => {
            requestAnimationFrame(() => animateTo(direction));
        });
    }

    galleryButtons.forEach((button, index) => {
        button.addEventListener("click", () => openLightbox(index));
    });

    closeButton.addEventListener("pointerup", (event) => {
        event.preventDefault();
        event.stopPropagation();
        closeLightbox();
    });
    prevButton.addEventListener("click", () => changeBy(1));
    nextButton.addEventListener("click", () => changeBy(-1));
  // closeButton.addEventListener("click", () => {
  //     console.log("Нажат крестик");
  //     closeLightbox();
  // });

  // prevButton.addEventListener("click", () => {
  //     console.log("Нажата левая стрелка");
  //     changeBy(1);
  // });

  // nextButton.addEventListener("click", () => {
  //     console.log("Нажата правая стрелка");
  //     changeBy(-1);
  // });

    track.addEventListener("touchstart", startDrag, { passive: true });
    track.addEventListener("touchmove", moveDrag, { passive: true });
    track.addEventListener("touchend", endDrag, { passive: true });
    track.addEventListener("touchcancel", endDrag, { passive: true });

    lightbox.addEventListener("click", event => {
        if (event.target === lightbox) closeLightbox();
    });

    document.addEventListener("keydown", event => {
        if (lightbox.hidden) return;

        if (event.key === "Escape") closeLightbox();
        if (event.key === "ArrowLeft") changeBy(1);
        if (event.key === "ArrowRight") changeBy(-1);
    });
});
