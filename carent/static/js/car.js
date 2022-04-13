document.addEventListener("DOMContentLoaded", () => {
  const sliderImages = document.querySelectorAll(".slider img");
  const tumbnails = document.querySelectorAll(".tumbnail");
  const max_id = sliderImages.length - 1;
  let currentActiveImage = sliderImages[0];
  let currentActiveTumbnail = tumbnails[0];

  function onNextClick(e) {
    const imageId = currentActiveImage.getAttribute("data-id");
    currentActiveImage.classList.remove("active");
    currentActiveTumbnail.classList.remove("active");
    currentActiveImage =
      imageId == max_id ? sliderImages[0] : sliderImages[parseInt(imageId) + 1];
    currentActiveTumbnail =
      imageId == max_id ? tumbnails[0] : tumbnails[parseInt(imageId) + 1];
    currentActiveImage.classList.add("active");
    currentActiveTumbnail.classList.add("active");
  }

  function onPrevClick(e) {
    const imageId = currentActiveImage.getAttribute("data-id");
    currentActiveImage.classList.remove("active");
    currentActiveTumbnail.classList.remove("active");
    currentActiveImage =
      imageId == 0 ? sliderImages[max_id] : sliderImages[parseInt(imageId) - 1];
    currentActiveTumbnail =
      imageId == 0 ? tumbnails[max_id] : tumbnails[parseInt(imageId) - 1];
    currentActiveImage.classList.add("active");
    currentActiveTumbnail.classList.add("active");
  }

  function onTumbnailClick(e) {
    const imageId = parseInt(currentActiveImage.getAttribute("data-id"));
    const tumbnailImageId = parseInt(e.target.getAttribute("data-id"));
    if (imageId == tumbnailImageId) {
      return;
    } else {
      currentActiveImage.classList.remove("active");
      currentActiveTumbnail.classList.remove("active");
      currentActiveImage = sliderImages[tumbnailImageId];
      currentActiveTumbnail = tumbnails[tumbnailImageId];
      currentActiveImage.classList.add("active");
      currentActiveTumbnail.classList.add("active");
    }
  }

  for (let i = 0; i < sliderImages.length; i++) {
    sliderImages[i].setAttribute("data-id", i);
    tumbnails[i].setAttribute("data-id", i);
    tumbnails[i].onclick = onTumbnailClick;
  }

  if (max_id != 0) {
    const next = document.querySelector(".slider .next");
    next.onclick = onNextClick;
    const prev = document.querySelector(".slider .prev");
    prev.onclick = onPrevClick;
  }

  const priceElement = document.querySelector(".detail .prices .price span");
  const price = parseInt(priceElement.textContent);
  const priceWithoutDiscoutElement = document.querySelector(
    ".detail .without-discount span"
  );
  const priceWithoutDiscount =
    priceWithoutDiscoutElement !== undefined
      ? parseInt(priceWithoutDiscoutElement.textContent)
      : null;

  const plusButton = document.querySelector(".detail .rent .plus");
  const minusButton = document.querySelector(".detail .rent .minus");
  const counterInput = document.querySelector(".detail .rent input");

  counterInput.addEventListener("change", (e) => {
    if (e.target.value == "") {
      e.target.value = 1;
    }
    let value = parseInt(e.target.value);
    if (value == 0) {
      e.target.value = 1;
    }
    if (e.target.value > 999) {
      e.target.value = 999;
    }
    priceElement.textContent = price * parseInt(e.target.value);
    if (priceWithoutDiscoutElement !== undefined)
      priceWithoutDiscoutElement.textContent =
        priceWithoutDiscount * parseInt(e.target.value);
  });

  plusButton.addEventListener("click", () => {
    if (parseInt(counterInput.value) == 999) return;
    counterInput.value = parseInt(counterInput.value) + 1;
    counterInput.dispatchEvent(new Event("change"));
  });
  minusButton.addEventListener("click", () => {
    if (parseInt(counterInput.value) == 0) return;
    counterInput.value = parseInt(counterInput.value) - 1;
    counterInput.dispatchEvent(new Event("change"));
  });

  const rentButton = document.querySelector(".detail .rent button");
  let days = 0;
  const overlay = document.querySelector(".overlay");
  const modal = document.querySelector(".modal");
  const closeModalButton = modal.querySelector(".close");
  const nameInput = modal.querySelector("input[name='name']");
  const phoneInput = modal.querySelector("input[name='phone']");
  const formButton = modal.querySelector("form button");
  const form = modal.querySelector("form");

  const inputs = [
    {
      instance: phoneInput,
      error: modal.querySelector(".error.phone"),
      valid: null,
      pattern: /^(\+375|80)(29|25|44|33)\d{7}$/,
      check: function () {
        this.valid = this.pattern.test(this.instance.value);
        if (this.valid) {
          this.error.classList.remove("visible");
          this.instance.classList.add("valid");
          this.instance.classList.remove("notvalid");
        } else {
          this.error.classList.add("visible");
          this.instance.classList.remove("valid");
          this.instance.classList.add("notvalid");
        }
        formIsValid();
      },
      clear: function () {
        this.instance.value = "";
        this.valid = null;
        this.error.classList.remove("visible");
        this.instance.classList.remove("valid");
        this.instance.classList.remove("notvalid");
      },
    },
    {
      instance: nameInput,
      error: modal.querySelector(".error.name"),
      valid: null,
      pattern: /^[А-Яа-яA-Za-z]{1,255}$/,
      check: function () {
        this.valid = this.pattern.test(this.instance.value);
        if (this.valid) {
          this.error.classList.remove("visible");
          this.instance.classList.add("valid");
          this.instance.classList.remove("notvalid");
        } else {
          this.error.classList.add("visible");
          this.instance.classList.remove("valid");
          this.instance.classList.add("notvalid");
        }
        formIsValid();
      },
      clear: function () {
        this.instance.value = "";
        this.valid = null;
        this.error.classList.remove("visible");
        this.instance.classList.remove("valid");
        this.instance.classList.remove("notvalid");
      },
    },
  ];
  let buttonLock = false;
  function formIsValid() {
    if (buttonLock) return;
    let valid = true;
    for (let i = 0; i < inputs.length; i++) {
      if (inputs[i].valid == false || inputs[i].valid == null) {
        valid = false;
        break;
      }
    }
    if (valid == true) {
      formButton.disabled = false;
      form.addEventListener("submit", onFormSubmit);
    } else {
      formButton.disabled = true;
      form.removeEventListener("submit", onFormSubmit);
    }
    return valid;
  }

  async function onFormSubmit(e) {
    e.preventDefault();
    if (!formIsValid()) {
      return;
    }
    buttonLock = true;
    formButton.disabled = true;
    form.removeEventListener("submit", onFormSubmit);
    const data = {
      name: nameInput.value,
      phone: phoneInput.value,
      car_id: parseInt(document.querySelector(".detail").getAttribute("data-car")),
      day: days
    };
    try {
      const response = await fetch(
        `${window.location.origin}/api/v1/orders/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json;charset=utf-8",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify(data),
        }
      );
      if (!response.ok) {
        throw new Error("Беда");
      }
      new Toast({
        title: false,
        text: "Бронь совершена",
        theme: "success",
        autohide: true,
        interval: 7000,
      });
      resetForm();
      closeModal();
    } catch (e) {
      console.log(e);
    } finally {
      buttonLock = false;
    }
  }

  function resetForm() {
    inputs.forEach((elem) => {
      elem.clear();
    });
  }

  inputs.forEach((elem) => {
    elem.instance.addEventListener("input", elem.check.bind(elem));
  });

  function closeModal(e) {
    overlay.classList.remove("active");
    modal.classList.remove("active");
  }

  function showModal(e) {
    overlay.classList.add("active");
    modal.classList.add("active");
  }

  closeModalButton.addEventListener("click", closeModal);
  overlay.addEventListener("click", closeModal);

  overlay.removeAttribute("style");
  modal.removeAttribute("style");
  rentButton.addEventListener("click", () => {
    days = parseInt(counterInput.value);
    modal.querySelector(".sum span").textContent = days * price;
    modal.querySelector(".days span").textContent = days;
    showModal();
  });
});

function getCookie(name) {
  let matches = document.cookie.match(
    new RegExp(
      "(?:^|; )" +
        name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, "\\$1") +
        "=([^;]*)"
    )
  );
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

const csrftoken = getCookie("csrftoken");
