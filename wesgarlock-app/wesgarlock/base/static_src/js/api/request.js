/* global context csrftoken */

const pageEndpoint = context.page_api_url
const imageEndpoint = context.image_api_url
const documentEndpoint = context.image_api_url

const parameters = {
  type: null,
  limit: null,
  offset: null,
  fields: []
}

function buildUrl (endpoint, parameters) {
  let url = endpoint + '?'
  let i = 0
  for (const [key, value] of Object.entries(parameters)) {
    if (value != null) {
      if (!(Array.isArray(value))) {
        if (i > 0) {
          url = url + '&'
        }
        url = url + key + '=' + value
      } else if (value.length !== 0) {
        if (i > 0) {
          url = url + '&'
        }
        url = url + key + '='
        let j = 0
        for (const subValue of value) {
          console.log(subValue)
          if (j > 0) {
            url = url + ','
          }
          url = url + value
          j++
        }
      }
    }
    i++
  }
  return url
}

const request = obj => {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()
    xhr.open(obj.method || 'GET', obj.url)
    if (obj.headers) {
      Object.keys(obj.headers).forEach(key => {
        xhr.setRequestHeader(key, obj.headers[key])
      })
    }
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(xhr.response)
      } else {
        reject(xhr.statusText)
      }
    }
    xhr.onerror = () => reject(xhr.statusText)
    const body = new FormData()
    if (obj.method !== 'GET') {
      obj.body.csrfmiddlewaretoken = csrftoken
    };
    for (const [key, value] of Object.entries(obj.body)) {
      body.append(key, value)
    };
    xhr.send(body)
  })
}

export { parameters, pageEndpoint, imageEndpoint, documentEndpoint, buildUrl, request }
