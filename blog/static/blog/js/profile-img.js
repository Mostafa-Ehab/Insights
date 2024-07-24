document.addEventListener("DOMContentLoaded", () => {
    // Handle Change Profile image
    let img = document.querySelector("#id_profile_image")

    img.addEventListener("change", (event) => {
        document.querySelector(".img-form").submit()
    })
})