document.addEventListener("DOMContentLoaded", () => {
    const likeCount = document.querySelector("#like-count")
    const likeBtn = document.querySelector("#like-btn")

    if (likeBtn) {
        const postID = likeBtn.getAttribute("data-post-id")
        likeBtn.addEventListener("click", () => {
            fetch(`/like-post/${postID}`, {
                method: 'GET',
                headers: {
                    'Content-type': 'application/json'
                }
            }).then(
                res => res.json()
            ).then(res => {
                console.log(res)
                likeCount.innerHTML = res['like_count']
                if (res['liked']) {
                    likePost()
                } else {
                    unLikePost()
                }
            })
        })
    }
})

function likePost() {
    const likeBtn = document.querySelector("#like-btn i")

    likeBtn.classList.add("fa-solid")
    likeBtn.classList.remove("fa-regular")
}

function unLikePost() {
    const likeBtn = document.querySelector("#like-btn i")

    likeBtn.classList.add("fa-regular")
    likeBtn.classList.remove("fa-solid")
}
