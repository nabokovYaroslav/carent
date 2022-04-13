document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll(".links ul li a");
  const options = {
    threshold: 0.3,
  };
  const observableElements = [];
  for (let i = 0; i < links.length; i++) {
    dataId = links[i].getAttribute("data-id");
    if (dataId == null) continue;
    observableElements.push(document.getElementById(dataId));
  }
  const callback = function (entries, observer) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const currentActiveLink = document.querySelector(
          `a[data-id='${entry.target.getAttribute("id")}']`
        );
        currentActiveLink.classList.add("active");
        history.replaceState(
          undefined,
          undefined,
          "#" + entry.target.getAttribute("id")
        );
      } else {
        const currentActiveLink = document.querySelector(
          `a[data-id='${entry.target.getAttribute("id")}']`
        );
        currentActiveLink.classList.remove("active");
      }
    });
  };
  const observer = new IntersectionObserver(callback, options);
  observableElements.forEach((element) => {
    observer.observe(element);
  });
  const form = document.querySelector(".offer form");
  const nameInput = form.querySelector("input[name='name']");
  const phoneInput = form.querySelector("input[name='phone']");
  const carInput = form.querySelector("select[name='car']");
  const formButton = form.querySelector("button");

  const inputs = [
    {
      instance: phoneInput,
      error: form.querySelector(".error.phone"),
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
      clear: function(){
        this.instance.value = ""
        this.valid = null
        this.error.classList.remove("visible");
        this.instance.classList.remove("valid");
        this.instance.classList.remove("notvalid");
      }
    },
    {
      instance: nameInput,
      error: form.querySelector(".error.name"),
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
      clear: function(){
        this.instance.value = ""
        this.valid = null
        this.error.classList.remove("visible");
        this.instance.classList.remove("valid");
        this.instance.classList.remove("notvalid");
      }
    },
    {
      instance: carInput,
      error: form.querySelector(".error.car"),
      valid: null,
      pattern: /^\d+$/,
      check: function () {
        this.valid = this.pattern.test(this.instance.value);
        if (this.valid) {
          this.error.classList.remove("visible");
          this.instance.classList.add("valid");
          this.instance.classList.remove("notvalid");
        } else{
          this.error.classList.add("visible");
          this.instance.classList.remove("valid");
          this.instance.classList.add("notvalid");
        }
        formIsValid();
      },
      clear: function(){
        this.instance.value = ""
        this.valid = null
        this.error.classList.remove("visible");
        this.instance.classList.remove("valid");
        this.instance.classList.remove("notvalid");
      }
    },
  ];
  let buttonLock = false;
  function formIsValid() {
    if(buttonLock) return
    let valid = true;
    for (let i = 0; i < inputs.length; i++) {
      if (inputs[i].valid == false || inputs[i].valid == null) {
        valid = false;
        break;
      }
    }

    if(valid == true){
      formButton.disabled = false
      form.addEventListener("submit", onFormSubmit)
    }else{
      formButton.disabled = true
      form.removeEventListener("submit", onFormSubmit)
    }
    return valid
  }

  async function onFormSubmit(e){
    e.preventDefault()
    if(!formIsValid()){
      return
    }
    buttonLock = true
    formButton.disabled = true
    form.removeEventListener("submit", onFormSubmit)
    const data = {
      name: nameInput.value,
      phone: phoneInput.value,
      car_id: parseInt(carInput.value)
    }
    try{
      const response = await fetch(`${window.location.origin}/api/v1/pre_order/`, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json;charset=utf-8',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
      })
      if(!response.ok){
        throw new Error("Беда")
      }
      new Toast({
        title: false,
        text: "Предварительная бронь совершена",
        theme: "success",
        autohide: true,
        interval: 7000,
      });
      resetForm()
    }
    catch (e){
      console.log(e)
    }
    finally{
      buttonLock = false
    }
  }

  function resetForm(){
    inputs.forEach(elem=>{
      elem.clear()
    })
  }

  inputs.forEach((elem) => {
    elem.instance.addEventListener("input", elem.check.bind(elem));
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