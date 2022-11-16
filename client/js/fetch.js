function fetchRoute(route, verb) {
  return new Promise((resolve, rejetct) => {
    fetch(`http://localhost:5000${route}`, {
      method: verb,
      headers: {
        'Content-Type': 'application/json',
      },
      'Access-Control-Allow-Origin': '*',
      mode: 'cors',
      cache: 'default',
    })
      .then((res) => {
        res
          .json()
          .then((res) => resolve(res))
          .catch((err) => rejetct(err))
      })
      .catch((err) => {
        element.innerHTML = err
      })
  })
}

const element = document.getElementById('hello-world')
fetchRoute('/', 'GET')
  .then((res) => {
    element.innerHTML = res.text
  })
  .catch((err) => {
    console.error(err)
  })
