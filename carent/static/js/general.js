document.addEventListener("DOMContentLoaded", () => {
    const nav = document.querySelector("nav");
    const links = nav.querySelector(".links")
    const a = links.querySelectorAll("a")
    const burger = nav.querySelector(".burger")
    const navOverlay = document.querySelector(".nav-overlay")
    document.addEventListener("scroll", () => {
      if (document.documentElement.scrollTop >= 100) {
        nav.classList.add("active");
      } else {
        nav.classList.remove("active");
      }
    });
    document.dispatchEvent(new Event("scroll"));

    for(let i = 0; i<a.length; i++){
      a[i].addEventListener("click", ()=>{
        links.classList.remove("active")
        navOverlay.classList.remove("active")
      })
    }

    navOverlay.removeAttribute("style")
    navOverlay.addEventListener("click", ()=>{
      links.classList.remove("active")
      navOverlay.classList.remove("active")
    })

    burger.addEventListener("click", (e)=>{
      e.preventDefault()
      links.classList.add("active")
      navOverlay.classList.add("active")
    })
  }) 
