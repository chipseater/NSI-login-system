function fetchToElement(element, route, verb) {
  fetch(`http://localhost:8000${route}`, {
    method: verb,
    headers: {
      "Content-Type": "application/json",
    },
    "Access-Control-Allow-Origin": "*",
    cache: "default",
  })
    .then((res) => {
        res.json().then(res => {
            element.innerHTML = res.text
            console.log(res)
        })
    })
    .catch((err) => {
      element.innerHTML = err;
    });
}

const element = document.getElementById("hello-world");
fetchToElement(element, "/", "GET");
